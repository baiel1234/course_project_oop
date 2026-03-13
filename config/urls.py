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
from users.views import login_view, register_view
from tests.views import (home,
                        student_tests,
                        test_page,
                        student_results,
                        teacher_dashboard,
                        create_test_page,
                        edit_test_page,
                        delete_test,
                        test_results)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('tests/', include('tests.urls')),
    path("results/", include("results.urls")),
    path('', home),

    path('login/', login_view),
    path('register/', register_view),

    # student
    path('tests/', student_tests),
    path('test/<int:test_id>/', test_page),
    path('my_results/', student_results),

    # teacher
    path('teacher/', teacher_dashboard),
    path('teacher/create_test/', create_test_page),
    path('teacher/edit/<int:test_id>/', edit_test_page),
    path('teacher/delete/<int:test_id>/', delete_test),
    path('teacher/results/<int:test_id>/', test_results),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
