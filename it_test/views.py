from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Question, Field

# 메인 소개 페이지
def main_page(request):
    return render(request, 'it_test/main_test.html')

# 질문 JSON 반환
def get_questions(request):
    questions = Question.objects.all().order_by('id')
    data = [
        {
            "id": q.id,
            "text": q.text,
        } for q in questions
    ]
    return JsonResponse({"questions": data})

# 질문 페이지 (템플릿은 빈 상태, JS로 JSON fetch)
def test_page(request):
    return render(request, 'it_test/test.html')

# =========================
# 테스트 제출
# =========================
@csrf_exempt  # CSRF 토큰 없이도 제출 가능, 필요하면 제거하고 JS에서 토큰 포함
def submit_test(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST 요청만 가능합니다."}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON 형식으로 보내주세요."}, status=400)

    fields = Field.objects.all()
    scores = {field.name: 0 for field in fields}

    for key, answer in data.items():
        # CSRF 토큰이 섞여 들어오면 건너뛰기
        if key == "csrfmiddlewaretoken":
            continue
        try:
            question_id = int(key.lstrip('q'))
            question = Question.objects.get(id=question_id)

            # 문자열 처리 수정
            if isinstance(answer,str) and answer.strip().lower() in ["예", "yes", "y"]:
                for field in question.fields.all():
                    scores[field.name] += 1

            # if answer.lower() in ["예", "yes", "y"]:
            #     for field in question.fields.all():
            #         scores[field.name] += 1

        except (ValueError, Question.DoesNotExist):
            return JsonResponse({"error": f"질문 ID {key} 처리 실패"}, status=400)

    max_score = max(scores.values(), default=0)
    best_fields = [f for f, s in scores.items() if s == max_score]

    # 세션에 저장
    request.session['best_fields'] = best_fields
    request.session['scores'] = scores

    return JsonResponse({"redirect_url": "/quiz/result/"})

# =========================
# 결과 페이지
# =========================
def result_page(request):
    best_fields = request.session.get('best_fields', [])
    scores = request.session.get('scores', {})

    # 세션 데이터 없으면 메인 페이지로
    if not best_fields or not scores:
        return redirect('it_test:main_page')

    return render(request, 'it_test/result.html', {
        'best_fields': best_fields,
        'scores': scores
    })
