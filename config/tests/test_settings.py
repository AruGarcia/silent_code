import importlib


def test_development_settings_use_local_defaults(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("DEBUG", raising=False)
    monkeypatch.delenv("ALLOWED_HOSTS", raising=False)

    module = importlib.import_module("config.settings.development")
    development = importlib.reload(module)

    assert development.SECRET_KEY == "django_django"
    assert development.DEBUG is True
    assert development.ALLOWED_HOSTS == ["127.0.0.1", "localhost", "testserver"]
    assert development.AUTH_USER_MODEL == "accounts.User"
    assert development.LOGIN_URL == "accounts:login"


def test_production_settings_require_env_and_enable_security_defaults(monkeypatch):
    monkeypatch.setenv(
        "SECRET_KEY",
        "production-secret-key-with-enough-entropy-1234567890-abcdef",
    )
    monkeypatch.setenv("ALLOWED_HOSTS", "example.com,.example.com")
    monkeypatch.setenv("CSRF_TRUSTED_ORIGINS", "https://example.com,https://app.example.com")
    monkeypatch.delenv("SECURE_HSTS_SECONDS", raising=False)
    monkeypatch.delenv("SECURE_HSTS_INCLUDE_SUBDOMAINS", raising=False)
    monkeypatch.delenv("SECURE_HSTS_PRELOAD", raising=False)

    module = importlib.import_module("config.settings.production")
    production = importlib.reload(module)

    assert production.SECRET_KEY.startswith("production-secret-key")
    assert production.DEBUG is False
    assert production.ALLOWED_HOSTS == ["example.com", ".example.com"]
    assert production.CSRF_TRUSTED_ORIGINS == [
        "https://example.com",
        "https://app.example.com",
    ]
    assert production.SECURE_SSL_REDIRECT is True
    assert production.SECURE_HSTS_SECONDS == 31536000
    assert production.SECURE_HSTS_INCLUDE_SUBDOMAINS is True
    assert production.SECURE_HSTS_PRELOAD is False
    assert production.SESSION_COOKIE_SECURE is True
    assert production.CSRF_COOKIE_SECURE is True
