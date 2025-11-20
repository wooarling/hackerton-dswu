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

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
        
    )  # 작성자
    title = models.CharField(max_length=200)  # 게시글 제목
    content = models.TextField()  # 게시글 내용
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)  # 카테고리
    is_anonymous = models.BooleanField(default=False)  # 익명 여부
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일
    updated_at = models.DateTimeField(auto_now=True)  # 수정일

    # 🔥 추가된 파일 업로드 필드들
    file = models.FileField(
        upload_to="uploads/files/",
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to="uploads/images/",
        null=True,
        blank=True
    )

    # 좋아요 기능
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_posts',
        blank=True
    )

    # 스크랩 기능
    scraps = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='scrapped_posts',
        blank=True
    )

    def like_count(self):
        """게시글의 좋아요 수를 반환"""
        return self.likes.count()

    def scrap_count(self):
        """게시글의 스크랩 수를 반환"""
        return self.scraps.count()

    @property
    def comment_count(self):
        """게시글의 댓글 수를 반환"""
        return self.comments.count()

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"


class Comment(models.Model):
    post = models.ForeignKey(
        'Post', 
        on_delete=models.CASCADE, 
        related_name='comments'
    )  # 게시글과 연결
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )  # 댓글 작성자
    content = models.TextField()  # 댓글 내용
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )  # 대댓글
    is_anonymous = models.BooleanField(default=False)  # 익명 여부

    # 댓글 좋아요
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_comments',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 생성일
    updated_at = models.DateTimeField(auto_now=True)  # 댓글 수정일

    def like_count(self):
        """댓글의 좋아요 수를 반환"""
        return self.likes.count()

    def __str__(self):
        username = "익명" if self.is_anonymous else self.user.username
        return f"{username}: {self.content[:20]}"
