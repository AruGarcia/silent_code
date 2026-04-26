from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def hello_world(request):
    return render(request, "silent_code/home.html")
