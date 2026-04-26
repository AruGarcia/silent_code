import pytest
from django.apps import apps
from django.test import Client
from django.urls import resolve, reverse

from app.silent_code.views import hello_world


@pytest.mark.django_db
def test_home_page_returns_hello_world():
    response = Client().get("/")

    assert response.status_code == 200
    assert response.content.decode() == "Hello, world!"


def test_root_url_resolves_to_hello_world():
    match = resolve(reverse("hello-world"))

    assert match.func == hello_world


def test_app_config_is_registered_with_expected_name_and_label():
    app_config = apps.get_app_config("silent_code")

    assert app_config.name == "app.silent_code"
    assert app_config.label == "silent_code"
