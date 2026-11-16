"""View-функции категорий дневника."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from categories.models import Category


def categories_list(request: HttpRequest) -> HttpResponse:
    """Страница списка категорий из ORM."""
    categories = Category.objects.order_by("name")
    context = {
        "categories": categories,
    }
    return render(request, "categories/category_list.html", context)


def category_detail(request: HttpRequest, category_id: int) -> HttpResponse:
    """Страница одной категории и её записей."""
    category = get_object_or_404(Category, pk=category_id)
    entries = category.entries.order_by("title")
    context = {
        "category": category,
        "entries": entries,
    }
    return render(request, "categories/category_detail.html", context)
