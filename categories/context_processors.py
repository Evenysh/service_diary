"""Контекстный процессор приложения категорий."""

from django.http import HttpRequest

from categories.models import Category
from entries.models import Entry


def site_stats(request: HttpRequest) -> dict:
    """Добавить название сайта и счётчики в шаблоны."""
    return {
        "site_name": "Сервис ведения дневника",
        "categories_count": Category.objects.count(),
        "entries_count": Entry.objects.count(),
    }
