from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Test

def login_required(view_func):

    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({"error": "login required"}, status=401)

        return view_func(request, *args, **kwargs)

    return wrapper

def teacher_owner_required(view_func):

    def wrapper(request, test_id, *args, **kwargs):

        test = get_object_or_404(Test, id=test_id)

        if not request.user.is_authenticated:
            return JsonResponse({"error": "login required"}, status=401)

        if test.teacher != request.user:
            return JsonResponse({"error": "not your test"}, status=403)

        return view_func(request, test_id, *args, **kwargs)

    return wrapper

def teacher_required(view_func):

    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({"error": "login required"}, status=401)

        if request.user.profile.role != "teacher":
            return JsonResponse({"error": "teacher access only"}, status=403)

        return view_func(request, *args, **kwargs)

    return wrapper