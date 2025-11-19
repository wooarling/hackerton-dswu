from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Post, Comment



CATEGORY_DISPLAY = dict(Post.CATEGORY_CHOICES)

def post_list(request, category=None):
    if category:
        posts = Post.objects.filter(category=category).order_by('-id')
        category_display = CATEGORY_DISPLAY.get(category, category)
    else:
        posts = Post.objects.all().order_by('-id')
        category_display = '전체 게시판'

    return render(request, 'board/post_list.html', {
        'posts': posts,
        'category': category_display
    })


@login_required
def followed_posts(request):
    """
    로그인한 사용자가 좋아요 누른 글(팔로우한 글) 목록
    """
    posts = Post.objects.filter(likes=request.user).order_by('-id')
    return render(request, 'board/post_list.html', {'posts': posts, 'category': '팔로우한 글'})

def popular_posts(request):
    """
    좋아요 많은 순으로 게시글 목록 (현재 인기글)
    """
    posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count', '-id')
    return render(request, 'board/post_list.html', {'posts': posts, 'category': '현재 인기글'})

@login_required
def my_posts(request):
    """
    로그인한 사용자가 작성한 글 목록
    """
    posts = Post.objects.filter(user=request.user).order_by('-id')
    return render(request, 'board/post_list.html', {
        'posts': posts,
        'category': '내가 쓴 글'
    })

@login_required
def my_comments(request):
    """
    로그인한 사용자가 댓글 단 글 목록
    """
    posts = Post.objects.filter(comments__user=request.user).distinct().order_by('-id')
    return render(request, 'board/post_list.html', {
        'posts': posts,
        'category': '내가 댓글 단 글'
    })

@login_required
def my_scraps(request):
    """
    로그인한 사용자가 스크랩한 글 목록
    """
    posts = Post.objects.filter(scraps=request.user).order_by('-id')
    return render(request, 'board/post_list.html', {
        'posts': posts,
        'category': '내 스크랩'
    })

def post_detail(request, pk):
    """
    게시글 상세 보기 및 댓글 기능을 포함하는 뷰
    - 부모 댓글만 필터링해서 템플릿으로 전달
    """
    post = get_object_or_404(Post, pk=pk)
    parent_comments = post.comments.filter(parent__isnull=True).order_by('-created_at')
    return render(request, 'board/post_detail.html', {
        'post': post,
        'comments': parent_comments,
    })

@login_required
def post_create(request):
    """
    새 게시글 작성 뷰
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        is_anonymous = bool(request.POST.get('is_anonymous'))  # 체크박스 처리

        post = Post.objects.create(
            user=request.user,
            title=title,
            content=content,
            category=category,
            is_anonymous=is_anonymous
        )
        return redirect('board:post_detail', pk=post.pk)
    
    return render(request, 'board/post_create.html')

@login_required
def post_update(request, pk):
    """
    게시글 수정 뷰
    """
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.user:
        return redirect('board:post_detail', pk=pk)
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.is_anonymous = bool(request.POST.get('is_anonymous'))  # 익명 여부 수정 가능
        post.save()
        return redirect('board:post_detail', pk=pk)
    
    return render(request, 'board/post_update.html', {'post': post})

@login_required
def post_delete(request, pk):
    """
    게시글 삭제 뷰
    """
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.user:
        post.delete()
    return redirect('board:post_list')

@login_required
def post_like_toggle(request, pk):
    """
    게시글 좋아요 토글 뷰
    """
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('board:post_detail', pk=pk)

@login_required
def post_scrap_toggle(request, pk):
    """
    게시글 스크랩 토글 뷰
    """
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.scraps.all():
        post.scraps.remove(request.user)
    else:
        post.scraps.add(request.user)
    return redirect('board:post_detail', pk=pk)

@login_required
def comment_create(request, post_pk, parent_pk=None):
    """
    댓글/대댓글 작성 뷰
    """
    post = get_object_or_404(Post, pk=post_pk)
    parent = get_object_or_404(Comment, pk=parent_pk) if parent_pk else None
    
    if request.method == 'POST':
        content = request.POST.get('content')
        is_anonymous = bool(request.POST.get('is_anonymous'))  # 체크박스 처리

        Comment.objects.create(
            post=post,
            user=request.user,
            content=content,
            parent=parent,
            is_anonymous=is_anonymous
        )
        return redirect('board:post_detail', pk=post.pk)

@login_required
def comment_like_toggle(request, pk):
    """
    댓글 좋아요 토글 뷰
    """
    comment = get_object_or_404(Comment, pk=pk)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('board:post_detail', pk=comment.post.pk)
