from django.urls import path
from .views import (
    post_list, post_detail, post_update, post_delete, 
    post_like_toggle, post_create, comment_create, comment_like_toggle
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
    # 댓글 / 대댓글 URL 통합
    path('<int:post_pk>/comment/create/', comment_create, name='comment_create'),
    path('<int:post_pk>/comment/create/<int:parent_pk>/', comment_create, name='comment_create'),
    path('comment/<int:pk>/like-toggle/', comment_like_toggle, name='comment_like_toggle'),
]



