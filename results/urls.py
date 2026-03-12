from django.urls import path
from .views import get_results,get_test_results,my_results

urlpatterns = [
    path("results/", get_results),
    path("test/<int:test_id>/", get_test_results),
    path("results/my/", my_results),
]