from django.urls import path
from .views import submit_test,create_test,add_questions_bulk,get_tests,get_test

urlpatterns = [
    path('submit/', submit_test),
    path("create/", create_test),
    path("add_question/", add_questions_bulk),
    path("list/", get_tests),
    path("<int:test_id>/", get_test),

]