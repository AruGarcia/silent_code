import config.settings.base as base

for setting_name in dir(base):
    if setting_name.isupper():
        globals()[setting_name] = getattr(base, setting_name)


SECRET_KEY = base.env("SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = base.env.list("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = base.env.list("CSRF_TRUSTED_ORIGINS", default=[])

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = base.env.int("SECURE_HSTS_SECONDS", default=31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = base.env.bool(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
SECURE_HSTS_PRELOAD = base.env.bool("SECURE_HSTS_PRELOAD", default=False)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
