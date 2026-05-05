from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("accounts/", include("app.accounts.urls")),
    path("", include("app.silent_code.urls")),
    path("admin/", admin.site.urls),
]
