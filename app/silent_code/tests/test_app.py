import pytest
from django.apps import apps
from django.contrib.auth import get_user_model
from django.urls import resolve, reverse

from app.silent_code.models import Task
from app.silent_code.views import hello_world

User = get_user_model()


@pytest.mark.django_db
def test_home_page_redirects_anonymous_user_to_login(client):
    response = client.get(reverse("hello-world"))

    assert response.status_code == 302
    assert response.headers["Location"].startswith(reverse("accounts:login"))


@pytest.mark.django_db
def test_home_page_returns_authenticated_content(client):
    user = User.objects.create_user(email="user@example.com", password="StrongPassword123")
    client.force_login(user)
    response = client.get(reverse("hello-world"))

    assert response.status_code == 200
    assert "user@example.com" in response.content.decode()


def test_root_url_resolves_to_hello_world():
    match = resolve(reverse("hello-world"))

    assert match.func == hello_world


def test_app_config_is_registered_with_expected_name_and_label():
    app_config = apps.get_app_config("silent_code")

    assert app_config.name == "app.silent_code"
    assert app_config.label == "silent_code"


@pytest.mark.django_db
def test_task_belongs_to_a_single_user():
    user = User.objects.create_user(email="owner@example.com", password="StrongPassword123")
    task = Task.objects.create(user=user, title="First task")

    assert task.user == user
    assert user.tasks.get() == task


@pytest.mark.django_db
def test_user_cannot_see_another_users_tasks_through_own_queryset():
    owner = User.objects.create_user(email="owner@example.com", password="StrongPassword123")
    other_user = User.objects.create_user(email="other@example.com", password="StrongPassword123")
    owner_task = Task.objects.create(user=owner, title="Owner task")
    Task.objects.create(user=other_user, title="Other task")

    assert list(owner.tasks.all()) == [owner_task]
