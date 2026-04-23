"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from users.views import login_view, register_view, logout_view
from tests.views import (home,
                        student_tests,
                        test_page_view,
                        student_results,
                        teacher_dashboard,
                        create_test_view,
                        edit_test_page,
                        delete_test,
                        test_results,
                        add_questions_view,
                        view_pdf,
                        submit_test_view)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('tests/', include('tests.urls')),
    path("results/", include("results.urls")),

    #front
    path('', home),

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # student
    path('tests/', student_tests),
    path('test/<int:test_id>/',test_page_view, name='test_page'),
    path('my_results/', student_results, name='my_results'),
    path('pdf/<int:test_id>/', view_pdf, name='view_pdf'),
    path('submit-test/<int:test_id>/', submit_test_view, name='submit_test'),

    # teacher
    path('teacher/', teacher_dashboard, name='teacher_dashboard'),
    path('teacher/create_test/', create_test_view, name='create_test'),
    path('teacher/edit/<int:test_id>/', edit_test_page),
    path('teacher/delete/<int:test_id>/', delete_test),
    path('teacher/results/<int:test_id>/', test_results),
    path('teacher/add-questions/<int:test_id>/', add_questions_view, name='add_questions_page')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
