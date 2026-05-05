from django import forms

from app.silent_code.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("title", "description")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
