from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Post, Comment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
# 카테고리 딕셔너리
CATEGORY_DISPLAY = dict(Post.CATEGORY_CHOICES)

# -------------------- 게시글 목록 --------------------
def post_list(request, category=None):
    if category:   # 카테고리별 게시글 필터링
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


# -------------------- 팔로우 글 --------------------
@login_required
def followed_posts(request):
    posts = Post.objects.filter(likes=request.user).order_by('-id')
    return render(request, 'board/post_list.html', {'posts': posts, 'category': '팔로우한 글'})


# -------------------- 인기글 --------------------
def popular_posts(request):
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
    posts = Post.objects.filter(comments__user=request.user).distinct().order_by('-id')
    return render(request, 'board/post_list.html', {'posts': posts, 'category': '내가 댓글 단 글'})


# -------------------- 내가 스크랩한 글 --------------------
@login_required
def my_scraps(request):
    posts = Post.objects.filter(scraps=request.user).order_by('-id')
    return render(request, 'board/post_list.html', {'posts': posts, 'category': '내 스크랩'})


# -------------------- 게시글 상세 --------------------
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    parent_comments = post.comments.filter(parent__isnull=True).order_by('-created_at')
    return render(request, 'board/post_detail.html', {'post': post, 'comments': parent_comments})


# -------------------- 게시글 작성 --------------------
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
            user=request.user,
            title=title,
            content=content,
            category=category,
            is_anonymous=is_anonymous,
            file=file,  # 파일 업로드
            image=image  # 이미지 업로드
        )

        # 리다이렉트: 특정 카테고리가 없다면 전체 게시판으로 리다이렉트
        if category:
            return redirect('board:post_list_category', category=category)
        else:
            return redirect('board:post_list')  # 카테고리 없이 리다이렉트

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
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.user:
        return redirect('board:post_detail', pk=pk)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.is_anonymous = bool(request.POST.get('is_anonymous'))

        # 파일 교체 가능하게 처리
        if request.FILES.get('file'):
            post.file = request.FILES.get('file')
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')

        post.save()
        return redirect('board:post_detail', pk=pk)

    return render(request, 'board/post_update.html', {'post': post})


# -------------------- 게시글 삭제 --------------------
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.user:
        post.delete()
    return redirect('board:post_list')


# -------------------- 게시글 좋아요 토글 --------------------
@login_required
def post_like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
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


# -------------------- 댓글/대댓글 작성 --------------------
@login_required
def comment_create(request, post_pk, parent_pk=None):
    post = get_object_or_404(Post, pk=post_pk)
    parent = get_object_or_404(Comment, pk=parent_pk) if parent_pk else None

    if request.method == 'POST':
        content = request.POST.get('content')
        is_anonymous = bool(request.POST.get('is_anonymous'))

        Comment.objects.create(
            post=post,
            user=request.user,
            content=content,
            parent=parent,
            is_anonymous=is_anonymous
        )
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

# 게시글 목록 API 뷰 (JSON)
class PostList(APIView):
    def get(self, request, category=None):
        if category:
            posts = Post.objects.filter(category=category).order_by('-id')
        else:
            posts = Post.objects.all().order_by('-id')

        # 직렬화하여 JSON 형태로 반환
        serializer = PostSerializer(posts, many=True)
        return Response({'board_list': serializer.data}, status=status.HTTP_200_OK)