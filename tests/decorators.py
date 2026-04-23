from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Test
from functools import wraps

def login_required(view_func):

    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({"error": "login required"}, status=401)

        return view_func(request, *args, **kwargs)

    return wrapper

def teacher_owner_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({"error": "not logged in"}, status=401)

        if not hasattr(request.user, "profile") or request.user.profile.role != "teacher":
            return JsonResponse({"error": "only teacher allowed"}, status=403)

        return view_func(request, *args, **kwargs)

    return wrapper

def teacher_required(view_func):

    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({"error": "login required"}, status=401)

        if request.user.profile.role != "teacher":
            return JsonResponse({"error": "teacher access only"}, status=403)

        return view_func(request, *args, **kwargs)

    return wrapper