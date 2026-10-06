"""Маршруты приложения записей."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.entries_list, name="entries"),
    path("<int:entry_id>/", views.entry_detail, name="entry_detail"),
]
