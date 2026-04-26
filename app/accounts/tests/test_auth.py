import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
def test_signup_creates_user_and_logs_them_in(client):
    response = client.post(
        reverse("accounts:signup"),
        {
            "email": "user@example.com",
            "first_name": "Aru",
            "last_name": "Garcia",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"] == reverse("hello-world")
    assert User.objects.filter(email="user@example.com").exists()
    assert response.wsgi_request.user.is_authenticated is True


@pytest.mark.django_db
def test_login_accepts_email_as_identifier(client):
    password = "StrongPassword123"
    user = User.objects.create_user(email="user@example.com", password=password)

    response = client.post(
        reverse("accounts:login"),
        {"username": user.email, "password": password},
    )

    assert response.status_code == 302
    assert response.headers["Location"] == reverse("hello-world")


@pytest.mark.django_db
def test_logout_ends_authenticated_session(client):
    user = User.objects.create_user(email="user@example.com", password="StrongPassword123")
    client.force_login(user)

    response = client.post(reverse("accounts:logout"))

    assert response.status_code == 302
    assert response.headers["Location"] == reverse("accounts:login")


@pytest.mark.django_db
def test_login_page_uses_email_field_label(client):
    response = client.get(reverse("accounts:login"))

    assert response.status_code == 200
    assert "Email" in response.content.decode()
