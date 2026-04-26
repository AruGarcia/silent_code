from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.accounts.forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("hello-world")
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
