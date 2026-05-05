from django.urls import path

from app.silent_code.views import (
    TaskDeleteView,
    TaskListView,
    TaskToggleCompleteView,
    TaskUpdateView,
)

urlpatterns = [
    path("", TaskListView.as_view(), name="hello-world"),
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/toggle/", TaskToggleCompleteView.as_view(), name="task-toggle"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
]
