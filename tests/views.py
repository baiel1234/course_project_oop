from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Test,Question
from results.models import Result
import json
from django.shortcuts import get_object_or_404

@csrf_exempt
def create_test(request):

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        question_count = request.POST.get("question_count")
        pdf_file = request.FILES.get("pdf_file")

        test = Test.objects.create(
            title=title,
            description=description,
            question_count=question_count,
            pdf_file=pdf_file,
            teacher=request.user
        )

        return JsonResponse({"message": "test created", "id": test.id})

@csrf_exempt
def get_tests(request):

    tests = Test.objects.all()

    data = []

    for test in tests:

        data.append({
            "id": test.id,
            "title": test.title,
            "description": test.description,
            "pdf_file": test.pdf_file.url,
            "question_count": test.question_count
        })

    return JsonResponse(data, safe=False)

@csrf_exempt
def submit_test(request):

    if request.method == "POST":

        data = json.loads(request.body)

        test_id = data["test_id"]
        student_answers = data["answers"]

        test = Test.objects.get(id=test_id)

        questions = Question.objects.filter(test=test).order_by("number")

        score = 0

        if len(student_answers) != questions.count():
            return JsonResponse({
                "error": "answers count must equal questions count"
            }, status=400)

        for i, question in enumerate(questions):

            if i < len(student_answers):

                if question.correct_answer == student_answers[i]:

                    score += 1

        result = Result.objects.create(
            student=request.user,
            test=test,
            score=score,
            total=len(questions)
        )

        return JsonResponse({
            "score": score,
            "total": len(questions)
        })

@csrf_exempt
def add_questions_bulk(request):

    if request.method == "POST":

        data = json.loads(request.body)

        test_id = data["test_id"]
        answers = data["answers"]

        test = Test.objects.get(id=test_id)

        for index, answer in enumerate(answers, start=1):

            Question.objects.create(
                test=test,
                number=index,
                correct_answer=answer
            )

        return JsonResponse({"message": "questions added"})

@csrf_exempt
def get_test(request, test_id):

    test = get_object_or_404(Test, id=test_id)

    data = {
        "id": test.id,
        "title": test.title,
        "description": test.description,
        "pdf_file": test.pdf_file.url,
        "question_count": test.question_count
    }

    return JsonResponse(data)

@csrf_exempt
def edit_test(request, test_id):

    test = Test.objects.get(id=test_id)

    if request.method == "POST":

        test.title = request.POST.get("title", test.title)
        test.description = request.POST.get("description", test.description)
        test.question_count = request.POST.get("question_count", test.question_count)

        if "pdf_file" in request.FILES:
            test.pdf_file = request.FILES["pdf_file"]

        test.save()

        return JsonResponse({"message": "updated"})

@csrf_exempt
def update_answers(request, test_id):

    if request.method == "PUT":

        data = json.loads(request.body)
        answers = data["answers"]

        test = Test.objects.get(id=test_id)

        questions = Question.objects.filter(test=test).order_by("number")

        if len(answers) != questions.count():
            return JsonResponse(
                {"error": "answers count must equal questions count"},
                status=400
            )

        for i, question in enumerate(questions):
            question.correct_answer = answers[i]
            question.save()

        return JsonResponse({"message": "answers updated"})

@csrf_exempt
def delete_test(request, test_id):

    if request.method == "DELETE":

        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return JsonResponse({"error": "Test not found"}, status=404)

        test.delete()

        return JsonResponse({
            "message": "Test deleted"
        })

#добавь админку в которой можно будет удалять пользователей / создавать ,изменять и удалять тесты и вопросы