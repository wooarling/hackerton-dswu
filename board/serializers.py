from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Post
        fields = ['id', 'category', 'title', 'content', 'like_count', 'comment_count', 'date', 'user', 'anonymous']
