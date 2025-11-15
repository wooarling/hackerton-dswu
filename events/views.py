from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Event
import json
from datetime import datetime

# 전체 이벤트 조회
def events_list(request):
    events = Event.objects.all()
    data = [
        {
            'id': e.id,
            'title': e.title,
            'description': e.description,
            'start_time': e.start_time.isoformat(),  # 수정
            'end_time': e.end_time.isoformat(),      # 수정
            'category': e.category,
        }
        for e in events
    ]
    return JsonResponse(data, safe=False)

# 특정 이벤트 조회
def event_detail(request, pk):
    e = get_object_or_404(Event, pk=pk)
    data = {
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'start_time': e.start_time.isoformat(),  # 수정
        'end_time': e.end_time.isoformat(),      # 수정
        'category': e.category,
    }
    return JsonResponse(data)

# 이벤트 생성
@csrf_exempt
def event_create(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        e = Event.objects.create(
            title=payload['title'],
            description=payload.get('description', ''),
            start_time=datetime.fromisoformat(payload['start_time']),  # 수정
            end_time=datetime.fromisoformat(payload['end_time']),      # 수정
            category=payload['category']
        )
        return JsonResponse({'id': e.id}, status=201)  # 테스트와 일치하도록 201

# 이벤트 수정
@csrf_exempt
def event_update(request, pk):
    e = get_object_or_404(Event, pk=pk)
    if request.method == 'PUT':
        payload = json.loads(request.body)
        e.title = payload.get('title', e.title)
        e.description = payload.get('description', e.description)
        e.start_time = datetime.fromisoformat(payload.get('start_time', e.start_time.isoformat()))  # 수정
        e.end_time = datetime.fromisoformat(payload.get('end_time', e.end_time.isoformat()))        # 수정
        e.category = payload.get('category', e.category)
        e.save()
        return JsonResponse({'status': 'ok'})

@csrf_exempt
def event_delete(request, pk):
    e = get_object_or_404(Event, pk=pk)
    if request.method == 'DELETE':
        e.delete()
        return JsonResponse({}, status=204)  # 204 No Content 반환
