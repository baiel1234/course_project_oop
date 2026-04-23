from django.urls import path
from .views import submit_test,create_test,add_questions_bulk,get_tests,get_test,edit_test,update_answers,delete_test,search_tests,home

urlpatterns = [
    path('submit/', submit_test, name='submit_test_api'),
    path("create/", create_test),
    path("add_question/", add_questions_bulk,name='add_questions'),
    path("list/", get_tests),
    path("<int:test_id>/", get_test),
    path("edit/<int:test_id>/", edit_test),
    path("update_answers/<int:test_id>/", update_answers),
    path("delete/<int:test_id>/", delete_test),
    path("search/", search_tests),
    path('', home,name='home'),
]