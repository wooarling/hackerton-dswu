from django.urls import path
from .views import (
    post_list, post_detail, post_edit, post_delete,
    post_like_toggle, post_create, comment_create, comment_like_toggle,
    popular_posts,
    my_posts, my_comments, my_scraps, post_scrap_toggle, comment_edit, comment_delete,
    PostList  # 추가된 API 뷰
)

app_name = 'board'

urlpatterns = [
    # -------------------- 게시글 목록 --------------------
    path('', post_list, name='post_list'),  # HTML 게시글 목록
    path('category/<str:category>/', post_list, name='post_list_category'),  # 카테고리별 HTML 게시글 목록

    # -------------------- 게시글 목록 (API) --------------------
    path('api/board/', PostList.as_view(), name='api_board_list'),  # API로 모든 게시글 목록
    path('api/board/<str:category>/', PostList.as_view(), name='api_board_category_list'),  # 카테고리별 API 게시글 목록

    # -------------------- 게시글 작성 --------------------
    path('create/', post_create, name='post_create'),
    path('create/<str:category>/', post_create, name='post_create_category'),

    # -------------------- 게시글 상세 / 수정 / 삭제 --------------------
    path('<int:pk>/', post_detail, name='post_detail'),
    path('<int:pk>/edit/', post_edit, name='post_edit'),  # 게시글 수정
    path('<int:pk>/delete/', post_delete, name='post_delete'),  # 게시글 삭제

    # -------------------- 게시글 좋아요 / 스크랩 --------------------
    path('<int:pk>/like-toggle/', post_like_toggle, name='post_like_toggle'),
    path('<int:pk>/scrap-toggle/', post_scrap_toggle, name='post_scrap_toggle'),

    # -------------------- 댓글 / 대댓글 --------------------
    path('<int:post_pk>/comment/create/', comment_create, name='comment_create'),
    path('<int:post_pk>/comment/create/reply/<int:parent_pk>/', comment_create, name='comment_create_reply'),
    path('comment/<int:pk>/like-toggle/', comment_like_toggle, name='comment_like_toggle'),

    # -------------------- 특수 게시글 --------------------
    path('popular/', popular_posts, name='popular_posts'),

    # -------------------- 내 글 / 댓글 단 글 / 스크랩 --------------------
    path('my-posts/', my_posts, name='my_posts'),
    path('my-comments/', my_comments, name='my_comments'),
    path('my-scraps/', my_scraps, name='my_scraps'),

    # -------------------- 댓글 수정 --------------------
    path('comment/edit/<int:pk>/', comment_edit, name='comment_edit'),  # views.comment_edit로 수정
    path('comment/delete/<int:pk>/', comment_delete, name='comment_delete'),  # 댓글 삭제 URL
]
