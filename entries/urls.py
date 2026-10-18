"""Маршруты приложения записей."""

from django.urls import path

from . import views

app_name = "entries"

urlpatterns = [
    path("", views.entries_list, name="list"),
    path("by-date/", views.entries_by_date, name="by_date"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:entry_id>/", views.entry_detail, name="detail"),
]
