from django.urls import path

from app.silent_code.views import hello_world

urlpatterns = [
    path("", hello_world, name="hello-world"),
]
