from django.urls import path
from .views import register, user_login,logout_api

urlpatterns = [
    path('register/', register),
    path('login/', user_login),
    path("logout/", logout_api),
]