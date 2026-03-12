from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .models import Profile

@csrf_exempt
def register(request):

    data = json.loads(request.body)

    username = data["username"]
    password = data["password"]
    role = data["role"]

    user = User.objects.create_user(
        username=username,
        password=password
    )

    Profile.objects.create(
        user=user,
        role=role
    )

    return JsonResponse({"status": "user created"})

@csrf_exempt
def user_login(request):

    data = json.loads(request.body)

    username = data["username"]
    password = data["password"]

    user = authenticate(username=username, password=password)

    if user:

        login(request, user)

        return JsonResponse({"status": "logged in"})

    return JsonResponse({"error": "invalid credentials"})