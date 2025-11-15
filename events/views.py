from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Event
import json
from datetime import datetime

def parse_json(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None


# 전체 이벤트 조회
def events_list(request):
    events = Event.objects.all()
    data = [
        {
            'id': e.id,
            'title': e.title,
            'description': e.description,
            'start_time': e.start_time.isoformat(),
            'end_time': e.end_time.isoformat(),
            'category': e.category,
        }
        for e in events
    ]
    return JsonResponse(data, safe=False)


# 특정 이벤트 조회
def event_detail(request, pk):
    try:
        e = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return JsonResponse({"error": "Event not found"}, status=404)

    data = {
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'start_time': e.start_time.isoformat(),
        'end_time': e.end_time.isoformat(),
        'category': e.category,
    }
    return JsonResponse(data)


# 이벤트 생성
@csrf_exempt
def event_create(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    payload = parse_json(request)
    if payload is None:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        start_time = datetime.fromisoformat(payload['start_time'])
        end_time = datetime.fromisoformat(payload['end_time'])
    except (KeyError, ValueError):
        return JsonResponse({"error": "Invalid datetime format"}, status=400)

    try:
        e = Event.objects.create(
            title=payload['title'],
            description=payload.get('description', ''),
            start_time=start_time,
            end_time=end_time,
            category=payload['category']
        )
    except KeyError:
        return JsonResponse({"error": "Missing required fields"}, status=400)

    return JsonResponse({'id': e.id}, status=201)


# 이벤트 수정
@csrf_exempt
def event_update(request, pk):
    if request.method != 'PUT':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    # 객체 조회
    try:
        e = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return JsonResponse({"error": "Event not found"}, status=404)

    # JSON 파싱
    payload = parse_json(request)
    if payload is None:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # datetime 처리
    try:
        if 'start_time' in payload:
            e.start_time = datetime.fromisoformat(payload['start_time'])
        if 'end_time' in payload:
            e.end_time = datetime.fromisoformat(payload['end_time'])
    except ValueError:
        return JsonResponse({"error": "Invalid datetime format"}, status=400)

    # 다른 필드
    e.title = payload.get('title', e.title)
    e.description = payload.get('description', e.description)
    e.category = payload.get('category', e.category)
    e.save()

    return JsonResponse({'status': 'ok'})


# 이벤트 삭제
@csrf_exempt
def event_delete(request, pk):
    if request.method != 'DELETE':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        e = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return JsonResponse({"error": "Event not found"}, status=404)

    e.delete()
    return JsonResponse({}, status=204)
