from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, ListView, UpdateView

from app.silent_code import facade
from app.silent_code.forms import TaskForm
from app.silent_code.models import Task


class UserTaskQuerysetMixin(LoginRequiredMixin):
    model = Task

    def get_queryset(self):
        return facade.tasks_for_user(self.request.user)

    def get_task(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])


class TaskListView(UserTaskQuerysetMixin, ListView):
    context_object_name = "tasks"
    template_name = "silent_code/home.html"

    def get_status_filter(self):
        return self.request.GET.get("status", facade.DEFAULT_STATUS_FILTER)

    def get_queryset(self):
        return facade.list_tasks_for_user(self.request.user, self.get_status_filter())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = kwargs.get("form", TaskForm())
        context["status_filter"] = self.get_status_filter()
        context["task_counts"] = facade.task_counts_for_user(self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            facade.create_task(user=request.user, **form.cleaned_data)
            return HttpResponseRedirect(reverse("hello-world"))

        self.object_list = self.get_queryset()
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class TaskUpdateView(UserTaskQuerysetMixin, UpdateView):
    form_class = TaskForm
    template_name = "silent_code/task_form.html"
    success_url = reverse_lazy("hello-world")

    def form_valid(self, form):
        facade.update_task(task=self.object, **form.cleaned_data)
        return HttpResponseRedirect(self.get_success_url())


class TaskDeleteView(UserTaskQuerysetMixin, DeleteView):
    template_name = "silent_code/task_confirm_delete.html"
    success_url = reverse_lazy("hello-world")

    def form_valid(self, form):
        facade.delete_task(task=self.object)
        return HttpResponseRedirect(self.get_success_url())


class TaskToggleCompleteView(UserTaskQuerysetMixin, UpdateView):
    fields = []
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        task = self.get_task()
        facade.toggle_task_completion(task=task)
        return HttpResponseRedirect(reverse("hello-world"))
