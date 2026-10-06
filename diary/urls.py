"""Корневая маршрутизация Django-проекта."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("categories/", include("categories.urls")),
    path("entries/", include("entries.urls")),
]
