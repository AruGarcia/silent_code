import pytest
from django.apps import apps
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.urls import resolve, reverse

from app.silent_code.models import Task
from app.silent_code.views import TaskListView

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
    assert "Create task" in response.content.decode()


def test_root_url_resolves_to_hello_world():
    match = resolve(reverse("hello-world"))

    assert match.func.view_class == TaskListView


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


@pytest.mark.django_db
def test_authenticated_user_can_create_task_from_home(client):
    user = User.objects.create_user(email="user@example.com", password="StrongPassword123")
    client.force_login(user)

    response = client.post(
        reverse("hello-world"),
        {"title": "Write tests", "description": "Cover task CRUD"},
    )

    assert response.status_code == 302
    task = Task.objects.get()
    assert model_to_dict(task, fields=["title", "description"]) == {
        "title": "Write tests",
        "description": "Cover task CRUD",
    }
    assert task.user == user


@pytest.mark.django_db
def test_home_page_lists_only_authenticated_users_tasks(client):
    user = User.objects.create_user(email="user@example.com", password="StrongPassword123")
    other_user = User.objects.create_user(email="other@example.com", password="StrongPassword123")
    Task.objects.create(user=user, title="Visible task")
    Task.objects.create(user=other_user, title="Hidden task")
    client.force_login(user)

    response = client.get(reverse("hello-world"))

    content = response.content.decode()
    assert "Visible task" in content
    assert "Hidden task" not in content


@pytest.mark.django_db
def test_home_page_can_filter_pending_tasks(client):
    user = User.objects.create_user(email="user@example.com", password="StrongPassword123")
    Task.objects.create(user=user, title="Pending task", is_completed=False)
    Task.objects.create(user=user, title="Completed task", is_completed=True)
    client.force_login(user)

    response = client.get(reverse("hello-world"), {"status": "pending"})

    content = response.content.decode()
    assert "Pending task" in content
    assert "Completed task" not in content


@pytest.mark.django_db
def test_home_page_can_filter_completed_tasks(client):
    user = User.objects.create_user(email="user@example.com", password="StrongPassword123")
    Task.objects.create(user=user, title="Pending task", is_completed=False)
    Task.objects.create(user=user, title="Completed task", is_completed=True)
    client.force_login(user)

    response = client.get(reverse("hello-world"), {"status": "completed"})

    content = response.content.decode()
    assert "Completed task" in content
    assert "Pending task" not in content


@pytest.mark.django_db
def test_home_page_defaults_to_all_tasks(client):
    user = User.objects.create_user(email="user@example.com", password="StrongPassword123")
    Task.objects.create(user=user, title="Pending task", is_completed=False)
    Task.objects.create(user=user, title="Completed task", is_completed=True)
    client.force_login(user)

    response = client.get(reverse("hello-world"))

    content = response.content.decode()
    assert "Pending task" in content
    assert "Completed task" in content


@pytest.mark.django_db
def test_user_can_update_own_task(client):
    user = User.objects.create_user(email="user@example.com", password="StrongPassword123")
    task = Task.objects.create(user=user, title="Old title", description="Old description")
    client.force_login(user)

    response = client.post(
        reverse("task-update", args=[task.pk]),
        {"title": "New title", "description": "New description"},
    )

    assert response.status_code == 302
    task.refresh_from_db()
    assert task.title == "New title"
    assert task.description == "New description"


@pytest.mark.django_db
def test_user_cannot_update_other_users_task(client):
    user = User.objects.create_user(email="user@example.com", password="StrongPassword123")
    other_user = User.objects.create_user(email="other@example.com", password="StrongPassword123")
    task = Task.objects.create(user=other_user, title="Protected task")
    client.force_login(user)

    response = client.get(reverse("task-update", args=[task.pk]))

    assert response.status_code == 404


@pytest.mark.django_db
def test_user_can_toggle_task_completion(client):
    user = User.objects.create_user(email="user@example.com", password="StrongPassword123")
    task = Task.objects.create(user=user, title="Toggle me", is_completed=False)
    client.force_login(user)

    response = client.post(reverse("task-toggle", args=[task.pk]))

    assert response.status_code == 302
    task.refresh_from_db()
    assert task.is_completed is True


@pytest.mark.django_db
def test_user_can_delete_own_task(client):
    user = User.objects.create_user(email="user@example.com", password="StrongPassword123")
    task = Task.objects.create(user=user, title="Delete me")
    client.force_login(user)

    response = client.post(reverse("task-delete", args=[task.pk]))

    assert response.status_code == 302
    assert Task.objects.filter(pk=task.pk).exists() is False
