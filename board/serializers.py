from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # 댓글 작성자
    like_count = serializers.IntegerField()  # 댓글 좋아요 수
    content = serializers.CharField()  # 댓글 내용
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")  # 댓글 작성 시간

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'like_count', 'date', 'parent', 'is_anonymous']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # 게시글에 대한 댓글들
    like_count = serializers.IntegerField()  # 게시글 좋아요 수
    comment_count = serializers.IntegerField()  # 댓글 수
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")  # 게시글 작성 시간
    user = serializers.StringRelatedField()  # 게시글 작성자

    class Meta:
        model = Post
        fields = ['id', 'category', 'title', 'content', 'like_count', 'comment_count', 'date', 'user', 'anonymous', 'comments']
