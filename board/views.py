from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Post, Comment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer, CommentSerializer

# 카테고리 딕셔너리
CATEGORY_DISPLAY = dict(Post.CATEGORY_CHOICES)

# -------------------- 게시글 목록 --------------------
def post_list(request, category=None):
    if category:  # 카테고리별 게시글 필터링
        posts = Post.objects.filter(category=category).order_by('-id')
        category_display = CATEGORY_DISPLAY.get(category, category)
        template_name = f'board/{category}.html'  # 카테고리별 템플릿
    else:
        posts = Post.objects.all().order_by('-id')
        category_display = '전체 게시판'
        template_name = 'board/index.html'

    context = {
        'posts': posts,
        'category': category_display,
    }
    return render(request, template_name, context)

# -------------------- 인기글 --------------------
def popular_posts(request):
    # 인기글: 좋아요 수가 많은 순으로 정렬
    posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count', '-id')
    return render(request, 'board/popular.html', {'posts': posts, 'category': '현재 인기글'})

# -------------------- 내가 쓴 글 --------------------
@login_required
def my_posts(request):
    posts = Post.objects.filter(user=request.user).order_by('-id')
    return render(request, 'board/post_list.html', {'posts': posts, 'category': '내가 쓴 글'})

# -------------------- 내가 댓글 단 글 --------------------
@login_required
def my_comments(request):
    # 사용자가 댓글을 단 게시물들을 가져옴 
    comments = Comment.objects.filter(user=request.user).order_by('-created_at')  # 댓글을 기준으로 정렬
    return render(request, 'board/comment_list.html', {'comments': comments, 'category': '내가 댓글 단 글'})


# -------------------- 내가 스크랩한 글 --------------------
@login_required
def my_scraps(request):
    # 현재 사용자가 스크랩한 글들을 필터링하여 가져오기
    scraps = Post.objects.filter(scraps=request.user).order_by('-id')
    return render(request, 'board/scrap_list.html', {'scraps': scraps, 'category': '내 스크랩'})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    parent_comments = post.comments.filter(parent__isnull=True).order_by('-created_at')

    category = post.category  # 게시글의 카테고리

    context = {
        'post': post,
        'comments': parent_comments,
        'page_title': post.title,  # 제목을 게시글의 제목으로 설정
        'category': category,  # 카테고리 정보 추가
    }
    return render(request, 'board/board_detail.html', context)

@login_required
def post_create(request, category=None):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_anonymous = bool(request.POST.get('is_anonymous'))

        # 파일/이미지 업로드
        file = request.FILES.get('file')
        image = request.FILES.get('image')

        # URL에서 category 전달 안되면 form에서 가져오기
        if not category:
            category = request.POST.get('category')

        # 게시글 생성
        post = Post.objects.create(
            user=None if is_anonymous else request.user,  # 익명일 경우 user는 None으로 설정
            title=title,
            content=content,
            category=category,
            is_anonymous=is_anonymous,
            file=file,  # 파일 업로드
            image=image  # 이미지 업로드
        )

        # 리다이렉트: 특정 카테고리가 없다면 전체 게시판으로 리다이렉트
        return redirect('board:post_list_category' if category else 'board:post_list', category=category)

    return render(
        request,
        'board/postform.html',
        {
            'category': category,
            'categories': CATEGORY_DISPLAY
        }
    )



# -------------------- 게시글 수정 --------------------
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 로그인한 사용자만 수정할 수 있도록 처리
    if request.user != post.user:
        return redirect('board:post_detail', pk=pk)

    if request.method == 'POST':
        # 제목과 내용이 빈 값인지 체크
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title or not content:
            # 제목과 내용이 빈 값일 경우, 에러 메시지 출력
            return render(request, 'board/post_edit_page.html', {
                'post': post,
                'error': '제목과 내용을 모두 입력해 주세요.'
            })

        # 폼 데이터 처리
        post.title = title
        post.content = content
        post.is_anonymous = bool(request.POST.get('is_anonymous'))

        # 파일 처리 (새로운 파일을 올리면 기존 파일 교체)
        if request.FILES.get('file'):
            post.file = request.FILES.get('file')
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')

        # 게시글 수정 후 저장
        post.save()

        return redirect('board:post_detail', pk=pk)

    # GET 요청일 때, 수정 페이지 렌더링
    return render(request, 'board/post_edit_page.html', {'post': post})

# -------------------- 게시글 삭제 --------------------
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 게시글을 삭제하는 사용자 확인
    if request.user == post.user:
        category = post.category  # 게시글의 카테고리
        post.delete()
        
        # 삭제 후 해당 카테고리 게시판으로 리다이렉트
        return redirect('board:post_list_category', category=category)

    # 게시글을 삭제할 권한이 없으면 상세 페이지로 리다이렉트
    return redirect('board:post_detail', pk=pk)

# -------------------- 게시글 스크랩 토글 --------------------
@login_required
def post_scrap_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.scraps.all():
        post.scraps.remove(request.user)
    else:
        post.scraps.add(request.user)
    return redirect('board:post_detail', pk=pk)

@login_required
def comment_create(request, post_pk, parent_pk=None):
    post = get_object_or_404(Post, pk=post_pk)
    parent = get_object_or_404(Comment, pk=parent_pk) if parent_pk else None

    if request.method == 'POST':
        content = request.POST.get('content')
        is_anonymous = request.POST.get('is_anonymous') == 'on'  # 'on' 값으로 체크

        # 익명 댓글일 때 user는 None으로 설정
        user = request.user if not is_anonymous else None

        # 댓글 또는 대댓글 생성
        comment = Comment.objects.create(
            post=post,
            user=user,  # 익명 댓글일 때는 None, 아니면 로그인한 user
            content=content,
            parent=parent,
            is_anonymous=is_anonymous
        )
        return redirect('board:post_detail', pk=post.pk)

    return redirect('board:post_detail', pk=post.pk)



# -------------------- 댓글 좋아요 토글 --------------------
@login_required
def comment_like_toggle(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('board:post_detail', pk=comment.post.pk)

# -------------------- 게시글 좋아요 토글 --------------------
@login_required
def post_like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('board:post_detail', pk=pk)


# -------------------- 게시글 목록 API --------------------
class PostList(APIView):
    def get(self, request, category=None):
        if category:
            posts = Post.objects.filter(category=category).order_by('-id')
        else:
            posts = Post.objects.all().order_by('-id')

        # 직렬화하여 JSON 형태로 반환
        serializer = PostSerializer(posts, many=True)
        return Response({'board_list': serializer.data}, status=status.HTTP_200_OK)

# -------------------- 게시글 수정 API --------------------
class PostEdit(APIView):
    def patch(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user != post.user:
            return Response({'error': 'You are not authorized to edit this post'}, status=status.HTTP_403_FORBIDDEN)

        post.title = request.data.get('title', post.title)
        post.content = request.data.get('content', post.content)
        post.is_anonymous = bool(request.data.get('is_anonymous'))

        # 파일 교체 가능하게 처리
        if 'file' in request.FILES:
            post.file = request.FILES.get('file')
        if 'image' in request.FILES:
            post.image = request.FILES.get('image')

        post.save()
        post_serializer = PostSerializer(post)
        return Response(post_serializer.data, status=status.HTTP_200_OK)

# -------------------- 게시글 삭제 API --------------------
class PostDelete(APIView):
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if request.user == post.user:
            category = post.category  # 게시글의 카테고리
            post.delete()

            # 삭제 후 해당 카테고리 게시판으로 리다이렉트
            return Response({'category': category}, status=status.HTTP_200_OK)
        return Response({'error': 'You are not authorized to delete this post'}, status=status.HTTP_403_FORBIDDEN)

# -------------------- 게시글 좋아요 토글 API --------------------
class PostLikeToggle(APIView):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        
        post_serializer = PostSerializer(post)
        return Response(post_serializer.data, status=status.HTTP_200_OK)

# -------------------- 댓글/대댓글 작성 API --------------------
# 댓글 작성 시 익명 여부와 관계없이 작성자(user) 설정
class CommentCreate(APIView):
    def post(self, request, post_pk, parent_pk=None):
        post = get_object_or_404(Post, pk=post_pk)
        parent = get_object_or_404(Comment, pk=parent_pk) if parent_pk else None

        content = request.data.get('content')
        is_anonymous = bool(request.data.get('is_anonymous'))

        # 익명 댓글인 경우 user는 null로 설정, 아니면 작성자의 user로 설정
        user = request.user if not is_anonymous else None

        comment = Comment.objects.create(
            post=post, 
            content=content,
            parent=parent,
            is_anonymous=is_anonymous,
            user=user  # 익명 여부에 따라 user 설정
        )

        comment_serializer = CommentSerializer(comment)
        return Response(comment_serializer.data, status=status.HTTP_201_CREATED)


# -------------------- 댓글 좋아요 토글 API --------------------
class CommentLikeToggle(APIView):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)

        comment_serializer = CommentSerializer(comment)
        return Response(comment_serializer.data, status=status.HTTP_200_OK)
    
@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # 해당 댓글의 작성자가 아닌 경우 접근 불가
    # 수정 권한을 익명 여부와 관계없이 작성자에게만 부여
    if request.user != comment.user:
        return redirect('board:post_detail', pk=comment.post.pk)

    if request.method == 'POST':
        # 댓글 수정
        comment.content = request.POST.get('content')
        comment.is_anonymous = bool(request.POST.get('is_anonymous'))  # 수정 시 익명 여부 처리

        # 수정한 댓글 저장
        comment.save()
        return redirect('board:post_detail', pk=comment.post.pk)

    return render(request, 'board/comment_edit_page.html', {'comment': comment})



# -------------------- 댓글 삭제 --------------------
@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # 댓글 작성자만 삭제 가능
    if request.user == comment.user:
        comment.delete()

    # 삭제 후 원래의 게시글 상세 페이지로 리다이렉트
    return redirect('board:post_detail', pk=comment.post.pk)
