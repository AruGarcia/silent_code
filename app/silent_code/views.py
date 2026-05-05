from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, ListView, UpdateView

from app.silent_code.forms import TaskForm
from app.silent_code.models import Task


class UserTaskQuerysetMixin(LoginRequiredMixin):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskListView(UserTaskQuerysetMixin, ListView):
    context_object_name = "tasks"
    template_name = "silent_code/home.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.GET.get("status", "all")

        if status_filter == "pending":
            return queryset.filter(is_completed=False)
        if status_filter == "completed":
            return queryset.filter(is_completed=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = kwargs.get("form", TaskForm())
        context["status_filter"] = self.request.GET.get("status", "all")
        all_tasks = Task.objects.filter(user=self.request.user)
        context["task_counts"] = {
            "all": all_tasks.count(),
            "pending": all_tasks.filter(is_completed=False).count(),
            "completed": all_tasks.filter(is_completed=True).count(),
        }
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return HttpResponseRedirect(reverse("hello-world"))

        self.object_list = self.get_queryset()
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class TaskUpdateView(UserTaskQuerysetMixin, UpdateView):
    form_class = TaskForm
    template_name = "silent_code/task_form.html"
    success_url = reverse_lazy("hello-world")


class TaskDeleteView(UserTaskQuerysetMixin, DeleteView):
    template_name = "silent_code/task_confirm_delete.html"
    success_url = reverse_lazy("hello-world")


class TaskToggleCompleteView(UserTaskQuerysetMixin, UpdateView):
    fields = []
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(self.get_queryset(), pk=kwargs["pk"])
        task.is_completed = not task.is_completed
        task.save(update_fields=["is_completed", "updated_at"])
        return HttpResponseRedirect(reverse("hello-world"))
