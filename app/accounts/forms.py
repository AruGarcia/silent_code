from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from app.accounts.models import User


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "first_name", "last_name")


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
