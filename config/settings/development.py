import config.settings.base as base

for setting_name in dir(base):
    if setting_name.isupper():
        globals()[setting_name] = getattr(base, setting_name)


SECRET_KEY = base.env(
    "SECRET_KEY",
    default="django_django",
)
DEBUG = base.env.bool("DEBUG", default=True)
ALLOWED_HOSTS = base.env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost", "testserver"])
