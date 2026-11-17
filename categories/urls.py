"""Маршруты приложения категорий."""

from django.urls import path

from . import views

app_name = "categories"

urlpatterns = [
    path("", views.categories_list, name="list"),
    path("<int:category_id>/", views.category_detail_by_id, name="detail_by_id"),
    path("<slug:slug>/", views.category_detail, name="detail"),
]
