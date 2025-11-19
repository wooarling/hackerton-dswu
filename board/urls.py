from django.urls import path
from .views import (
    post_list, post_detail, post_update, post_delete, 
    post_like_toggle, post_create, comment_create, comment_like_toggle,
    followed_posts, popular_posts,  # 추가
    my_posts, my_comments, my_scraps, post_scrap_toggle  # 스크랩 관련 추가
)

app_name = 'board'

urlpatterns = [
    path('', post_list, name='post_list'),  # 전체 게시판
    path('category/<str:category>/', post_list, name='post_list_category'),  # 카테고리별 게시판
    path('create/', post_create, name='post_create'),  # 새 글 작성 URL
    path('<int:pk>/', post_detail, name='post_detail'),
    path('<int:pk>/update/', post_update, name='post_update'),
    path('<int:pk>/delete/', post_delete, name='post_delete'),
    path('<int:pk>/like-toggle/', post_like_toggle, name='post_like_toggle'),
    path('<int:pk>/scrap-toggle/', post_scrap_toggle, name='post_scrap_toggle'),  # 스크랩 토글

    # 댓글 / 대댓글 URL 통합
    path('<int:post_pk>/comment/create/', comment_create, name='comment_create'),
    path('<int:post_pk>/comment/create/<int:parent_pk>/', comment_create, name='comment_create'),
    path('comment/<int:pk>/like-toggle/', comment_like_toggle, name='comment_like_toggle'),

    # 팔로우 글 / 인기글
    path('followed/', followed_posts, name='followed_posts'),
    path('popular/', popular_posts, name='popular_posts'),

    # 내가 쓴 글 / 내가 댓글 단 글 / 내가 스크랩한 글
    path('my-posts/', my_posts, name='my_posts'),
    path('my-comments/', my_comments, name='my_comments'),
    path('my-scraps/', my_scraps, name='my_scraps'),  
]
