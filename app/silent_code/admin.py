from django.contrib import admin

from app.silent_code.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "is_completed", "created_at")
    list_filter = ("is_completed", "created_at")
    search_fields = ("title", "description", "user__email")
