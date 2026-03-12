from django.http import JsonResponse
from .models import Result


def get_results(request):

    results = Result.objects.all()

    data = []

    for result in results:

        data.append({
            "student": result.student.username,
            "test": result.test.title,
            "score": result.score,
            "total": result.total,
            "date": result.created_at
        })

    return JsonResponse(data, safe=False)

def get_test_results(request, test_id):

    results = Result.objects.filter(test_id=test_id)

    data = []

    for result in results:

        data.append({
            "student": result.student.username,
            "score": result.score,
            "total": result.total,
            "date": result.created_at
        })

    return JsonResponse(data, safe=False)

def my_results(request):

    results = Result.objects.filter(student=request.user)

    data = []

    for result in results:

        data.append({
            "test": result.test.title,
            "score": result.score,
            "total": result.total,
            "date": result.created_at
        })

    return JsonResponse(data, safe=False)