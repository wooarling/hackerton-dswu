from django.db import models
from django.conf import settings

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', '프론트엔드'),
        ('backend', '백엔드'),
        ('ai', '인공지능'),
        ('iot', '사물인터넷'),
        ('game', '게임'),
        ('bigdata', '빅데이터'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 작성자
    title = models.CharField(max_length=200)  # 게시글 제목
    content = models.TextField()  # 게시글 내용
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)  # 카테고리
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일
    updated_at = models.DateTimeField(auto_now=True)  # 수정일
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)  # 좋아요 기능

    def like_count(self):
        """게시글의 좋아요 수를 반환"""
        return self.likes.count()

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"

    # 댓글 수 반환 (게시글에 달린 댓글의 수)
    @property
    def comment_count(self):
        """게시글의 댓글 수를 반환"""
        return self.comments.count()


# **댓글 모델 추가**
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')  # 게시글과 연결
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 댓글 작성자
    content = models.TextField()  # 댓글 내용
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')  # 대댓글
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)  # 댓글 좋아요
    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 생성일
    updated_at = models.DateTimeField(auto_now=True)  # 댓글 수정일

    def like_count(self):
        """댓글의 좋아요 수를 반환"""
        return self.likes.count()

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"
