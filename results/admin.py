from django.contrib import admin
from .models import Result


class ResultAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "test",
        "score",
        "total",
        "created_at"
    )

    list_filter = (
        "student",
        "test"
    )

    search_fields = (
        "student__username",
        "test__title"
    )


admin.site.register(Result, ResultAdmin)