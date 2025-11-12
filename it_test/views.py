from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Question

# JSON 반환: 모든 질문 가져오기
def get_questions(request):
    questions = [
        {"id": q.id, "question": q.text}
        for q in Question.objects.all()
    ]
    return JsonResponse({"questions": questions})

# AJAX 요청 시 CSRF 예외 처리
@csrf_exempt
def submit_test(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST 요청만 가능합니다."}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON 형식으로 데이터를 보내주세요."}, status=400)

    questions = Question.objects.all()

    fields = ["백엔드", "프론트엔드", "사이버보안", "게임개발", "사물인터넷", "빅데이터", "인공지능"]
    scores = {field: 0 for field in fields}

    print("=== 새 테스트 제출 ===")
    for q in questions:
        answer = data.get(f"q{q.id}")
        print(f"질문 {q.id}: {q.text}, 답변: {answer}")

        if answer == "예":
            q_fields = [f.strip() for f in q.fields.split(",")]
            for field in q_fields:
                if field in scores:
                    scores[field] += 1
                    print(f"  → {field} 점수 +1 (현재 점수: {scores[field]})")
    print("----------------------")
    max_score = max(scores.values())
    best_fields = [field for field, score in scores.items() if score == max_score]

    print(f"최종 점수: {scores}")
    print(f"추천 분야: {best_fields}")
    print("=== 제출 종료 ===\n")

    return JsonResponse({
        "best_fields": best_fields,
        "scores": scores
    })
