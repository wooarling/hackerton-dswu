import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from streamlit import status

from .forms import *
from .models import *
from .serializers import *


# Create your views here.
def board_list(request):
    boards = Board.objects.all().order_by('-pk')
    board_list = []
    for board in boards:
        board_list.append({
            'id': board.id,
            'title': board.title,
            'content': board.content,
            'user': board.user_id,
            'date': board.date.isoformat(),
            'category': board.category,
            'comment_count': board.comments.count(),  # 댓글 개수 추가
        })

    return JsonResponse({'board_list': board_list})

    # board = Board.objects.all().order_by('-pk')
    # board_list=[]
    # for b in board:
    #     board_list.append({
    #         "id": b.id,
    #         "title": b.title,
    #         "content": b.content,
    #         "user": b.user_id,
    #         "date": b.date,
    #         "category": b.category,
    #         "comment_count": comments.count(),
    #     })
    # serializer=BoardSerializer(board,many=True)
    # board = Board.objects.all().values('id', 'title', 'content', 'user', 'date', 'category')
    # comment = board.comments.all()
    # return JsonResponse(serializer.data,status=status.HTTP_200_OK)
    # return JsonResponse({
    #     'board_list': board_list,
        # 'comment_count': comment_count.count()
    # })


@csrf_exempt
def board_upload(request):
    if request.method == "POST":
        data = json.loads(request.body)
        board_upload = Board.objects.create(
            title=data['title'],
            content=data['content'],
            user=request.user,
            category=data.get('category'),
            date=timezone.now()
        )
        return JsonResponse({
            "id": board_upload.id,
            "title": board_upload.title,
            "content": board_upload.content,
            "user": board_upload.user_id,
            "date": board_upload.date,
            "category": board_upload.category
        })
    return JsonResponse({"error": "Post 요청만 가능"}, status=405)


def board_detail(request, pk):
    try:
        board = Board.objects.get(id=pk)
        comment = board.comments.all()
        comment_list = []
        for c in comment:
            comment_list.append({
                "id": c.id,
                # "title": board.title,
                "content": c.content_comment,
                "user": c.user_comment_id,
                "date": c.date_comment.isoformat(),
                "category": c.category,
            })
        return JsonResponse({
            "id": board.id,
            "title": board.title,
            "content": board.content,
            "user": board.user_id,
            "date": board.date.isoformat(),
            "category": board.category,
            "comment": comment_list,
            "comment_count": comment.count(),
        })
    except Board.DoesNotExist:
        return JsonResponse({"error": "게시글 없음"}, status=404)


@csrf_exempt
def board_edit(request, pk):
    if request.method == 'PUT':
        try:
            board = get_object_or_404(Board, id=pk)
            data = json.loads(request.body)
            board.title = data['title']
            board.content = data['content']
            board.user = request.user
            board.date = timezone.now()
            board.save()
            return JsonResponse({
                "id": board.id,
                "title": board.title,
                "content": board.content,
                "user": board.user_id,
                "date": board.date.isoformat(),
                "category": board.category
            })
        except Board.DoesNotExist:
            return JsonResponse({"error": "게시글을 찾을 수 없음"}, status=404)
    return JsonResponse({"error": "PUT 요청만 가능"})


@csrf_exempt
def board_delete(request, pk):
    if request.method == 'DELETE':
        try:
            board = get_object_or_404(Board, id=pk)
            board.delete()
            return JsonResponse({
                "id": board.id,
                "title": board.title,
                "content": board.content,
                "user": board.user_id,
                "date": board.date,
                "category": board.category
            })
        except Board.DoesNotExist:
            return JsonResponse({"error": "게시글을 찾을 수 없음"}, status=404)
    return JsonResponse({"error": "DELETE 요청만 가능"}, status=405)


def page_view(request):
    qs = Board.objects.all().order_by('-date')
    # qs = Board.objects.all().order_by('like')?
    paginator = Paginator(qs, 10)  # (데이터, 페이지당 보여줄 데이터 개수) #p
    page_number = int(request.GET.get('page', 1))  # now page
    page_obj = paginator.page(page_number)

    start_page = int(((page_number) - 1) // 10 * 10 + 1)
    end_page = start_page + 9
    if end_page > paginator.num_pages:
        end_page = paginator.num_pages
    page_range = list(range(start_page, end_page + 1))

    boards = []
    for board in page_obj:
        boards.append({
            'id': board.id,
            'title': board.title,
            "content": board.content,
            "user": board.user_id,
            "date": board.date.isoformat(),
            "category": board.category
        })

    return JsonResponse({
        # "page": paginator,
        'boards': boards,
        "page_number": page_number,
        "total_page": paginator.num_pages,
        "has_previous": page_obj.has_previous(),
        "has_next": page_obj.has_next(),
        "start_page": start_page,
        "end_page": end_page,
        "page_range": page_range
    })


def like(request, pk):
    if request.user.is_authenticated:
        board = get_object_or_404(Board, pk=pk)
        # board = Board.objects.get(pk=pk)
        if board.like.filter(pk=request.user.id).exists():
            # 좋아요 취소 (remove)
            board.like.remove(request.user)
            status = 'unlike'
        else:
            # 좋아요 추가 (add)
            board.like.add(request.user)
            status = 'like'
        return JsonResponse({
            "id": board.id,
            "status": status,
            "like_count": board.like_count,
        })
    return JsonResponse({"error": "login required"}, status=401)


def comment_list(request, pk):
    if request.method == 'GET':
        try:
            comment = Comments.objects.filter(board_comment_id=pk).order_by("id")
            comment_list = []
            for c in comment:
                comment_list.append({
                    "id": c.id,
                    # "title": board.title,
                    "content": c.content_comment,
                    "user": c.user_comment_id,
                    "date": c.date_comment.isoformat(),
                    "category": c.category,
                })
            return JsonResponse({'comment': comment_list},status=200)
        except Comments.DoesNotExist:
            return JsonResponse({"error": "댓글 없음"}, status=404)


@csrf_exempt
def comment_upload(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        comments = Comments()
        comments.board_comment_id = pk
        comments.user_comment_id = data.get('user_id', 1)
        comments.content_comment = data.get('content', '')
        comments.date_comment = timezone.now()
        comments.category = data.get('category', '프론트엔드')
        comments.save()

        return JsonResponse({
            "message": "댓글 작성됨",
            "comments_id": comments.id,
            "content": comments.content_comment,
            "user": comments.user_comment.username,
            "date": comments.date_comment.isoformat(),
            "category": comments.category,
        })
    return JsonResponse({"error":"POST만 가능"},status=405)


# @csrf_exempt
# def comment_upload(request, pk):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         comments = Comments.objects.create(
#             board_comment_id=pk,
#             # user_comment=request.user,    #front
#             user_comment_id=data.get('user_id', 1),
#             content_comment=data['content'],
#             date_comment=timezone.now(),
#         )
#         return JsonResponse({
#             "message":"댓글 작성됨",
#             "id": comments.id,
#             # # "title": board.title,
#             # "content": comments.content_comment,
#             # "user": comments.user_comment.username,
#             # "data": comments.date_comment.isoformat(),
#             # "category": comments.category,
#         })


@csrf_exempt
def comment_edit(request, pk,comment_pk):
    if request.method == 'PUT':
        try:
            comment = get_object_or_404(Comments, id=comment_pk,board_comment_id=pk)
            data = json.loads(request.body.decode("utf-8")) if request.body else {}
            edited_comment = data.get('content')
            comment.content_comment=edited_comment
            # comment.comment_user = request.user
            comment.date_comment = timezone.now()
            comment.save()
            return JsonResponse({
                "id": comment.id,
                "board_id":comment.board_comment_id,
                # "title": board.title,
                "content": comment.content_comment,
                "user": comment.user_comment.username,
                "data": comment.date_comment.isoformat(),
                "category": comment.category,
            })
        except Comments.DoesNotExist:
            return JsonResponse({"error": "게시글을 찾을 수 없음"}, status=404)
    return JsonResponse({"error": "PUT 요청만 가능"})


@csrf_exempt
def comment_delete(request, pk,comment_pk):
    if request.method == 'DELETE':
        try:
            comment = get_object_or_404(Comments, id=comment_pk,board_comment_id=pk)
            comment.delete()
            return JsonResponse({
                "id": comment.id,
                "board_id":comment.board_comment_id,
                # "title": board.title,
                "content": comment.content_comment,
                "user": comment.user_comment.username,
                "data": comment.date_comment.isoformat(),
                "category": comment.category,
            })
        except Comments.DoesNotExist:
            return JsonResponse({"error": "게시글을 찾을 수 없음"}, status=404)
    return JsonResponse({"error": "DELETE 요청만 가능"}, status=405)
