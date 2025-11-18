from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment

def post_list(request, category=None):
    """
    카테고리별 게시글 목록을 출력하는 뷰
    - category가 없으면 전체 게시글을, 있으면 해당 카테고리의 게시글만 출력
    """
    if category:
        posts = Post.objects.filter(category=category).order_by('-id')
    else:
        posts = Post.objects.all().order_by('-id')
    
    return render(request, 'board/post_list.html', {'posts': posts, 'category': category})

def post_detail(request, pk):
    """
    게시글 상세 보기 및 댓글 기능을 포함하는 뷰
    - 부모 댓글만 필터링해서 템플릿으로 전달
    """
    post = get_object_or_404(Post, pk=pk)
    parent_comments = post.comments.filter(parent__isnull=True).order_by('-created_at')  # 부모 댓글만 필터링
    return render(request, 'board/post_detail.html', {
        'post': post,
        'comments': parent_comments,  # 필터링된 댓글 전달
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

        post = Post.objects.create(
            user=request.user,
            title=title,
            content=content,
            category=category
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
def comment_create(request, post_pk, parent_pk=None):
    """
    댓글/대댓글 작성 뷰
    """
    post = get_object_or_404(Post, pk=post_pk)
    parent = None
    if parent_pk:
        parent = get_object_or_404(Comment, pk=parent_pk)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(
            post=post,
            user=request.user,
            content=content,
            parent=parent
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
