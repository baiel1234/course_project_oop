from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Test,Question
from results.models import Result
import json
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.shortcuts import render
from .decorators import teacher_required, teacher_owner_required , login_required


@csrf_exempt
@teacher_required
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
@teacher_owner_required
def add_questions_bulk(request):

    if request.method == "POST":

        data = json.loads(request.body)

        test_id = data["test_id"]
        answers = data["answers"]

        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return JsonResponse({"error": "Test not found"}, status=404)

        # проверяем количество ответов
        if len(answers) != test.question_count:
            return JsonResponse(
                {
                    "error": "answers count must equal question_count",
                    "question_count": test.question_count,
                    "answers_received": len(answers)
                },
                status=400
            )

        # удаляем старые вопросы (если есть)
        Question.objects.filter(test=test).delete()

        # создаём новые
        for index, answer in enumerate(answers, start=1):

            Question.objects.create(
                test=test,
                number=index,
                correct_answer=answer
            )

        return JsonResponse({
            "message": "questions added",
            "questions_created": len(answers)
        })

@csrf_exempt
@login_required
def get_test(request, test_id):

    test = get_object_or_404(Test, id=test_id)

    questions = Question.objects.filter(test=test).order_by("number")

    questions_data = []

    for q in questions:
        questions_data.append({
            "number": q.number,
            "correct_answer": q.correct_answer
        })

    data = {
        "id": test.id,
        "title": test.title,
        "description": test.description,
        "pdf_file": test.pdf_file.url,
        "question_count": test.question_count,
        "questions": questions_data
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

@csrf_exempt
def search_tests(request):

    query = request.GET.get("q", "")

    tests = Test.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(teacher__username__icontains=query)
    )

    data = []

    for test in tests:
        data.append({
            "id": test.id,
            "title": test.title,
            "description": test.description,
            "teacher": test.teacher.username,
            "question_count": test.question_count,
            "pdf_file": test.pdf_file.url
        })

    return JsonResponse(data, safe=False)



# ----------------------------------------------- HTML ------------------------------------------------------------------
@csrf_exempt
def home(request):

    query = request.GET.get("q")

    if query:
        tests = Test.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        tests = Test.objects.all()

    role = None

    if request.user.is_authenticated:
        role = request.user.profile.role

    return render(request, "home.html", {
        "tests": tests,
        "role": role
    })

def student_tests(request):
    """Страница списка тестов для студента"""
    tests = Test.objects.all()
    return render(request, "student/tests.html", {"tests": tests})

def test_page(request, test_id):
    """Страница прохождения конкретного теста"""
    test = get_object_or_404(Test, id=test_id)
    questions = Question.objects.filter(test=test).order_by("number")
    return render(request, "student/test_page.html", {"test": test, "questions": questions})

def student_results(request):
    """Страница просмотра своих результатов"""
    results = request.user.result_set.all()  # Assuming Result has ForeignKey to user
    return render(request, "student/results.html", {"results": results})

def teacher_dashboard(request):
    """Главная панель учителя"""
    tests = Test.objects.filter(teacher=request.user)
    return render(request, "teacher/dashboard.html", {"tests": tests})

def create_test_page(request):
    """Страница создания теста"""
    return render(request, "teacher/create_test.html")

def edit_test_page(request, test_id):
    """Страница редактирования теста"""
    test = get_object_or_404(Test, id=test_id)
    return render(request, "teacher/edit_test.html", {"test": test})

def test_results(request, test_id):
    """Просмотр результатов студентов по конкретному тесту"""
    test = get_object_or_404(Test, id=test_id)
    results = Result.objects.filter(test=test)
    return render(request, "teacher/test_results.html", {"results": results, "test": test})