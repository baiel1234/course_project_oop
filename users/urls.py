from django.urls import path
from .views import register, user_login
from tests.views import home

urlpatterns = [
    path('register/', register),
    path('login/', user_login),
]