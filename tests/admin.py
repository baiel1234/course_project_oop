from django.contrib import admin
from .models import Test, Question

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class TestAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "teacher",
        "question_count"
    )

    search_fields = (
        "title",
        "description",
        "teacher__username"
    )

    list_filter = (
        "teacher",
    )

    inlines = [QuestionInline]


admin.site.register(Test, TestAdmin)