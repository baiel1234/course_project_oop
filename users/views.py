from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import Profile
from django.shortcuts import render, redirect


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

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Проверяем пользователя
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # логиним пользователя
            return redirect("home")  # перенаправляем на home.html
        else:
            messages.error(request, "Неверный логин или пароль")

    return render(request, "login.html")

@csrf_exempt
def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user = User.objects.create_user(
            username=username,
            password=password
        )

        Profile.objects.create(
            user=user,
            role=role
        )

        return redirect("login")   # ← переход на страницу логина

    return render(request, "register.html")

@csrf_exempt
def logout_api(request):

    if not request.user.is_authenticated:
        return JsonResponse({"error": "user not logged in"}, status=401)

    logout(request)

    return JsonResponse({"status": "logged out"})