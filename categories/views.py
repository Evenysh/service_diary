"""View-функции категорий дневника."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import get_connection
from models import EntryEntity
from models.categories import find_category_by_id
from models.entries import filter_entries_by_category
from storage import load_categories, load_dates, load_entries, load_users

USERS_FILE = "data/users.json"
CATEGORIES_FILE = "data/categories.json"
DATES_FILE = "data/dates.json"
ENTRIES_FILE = "data/entries.json"


def _load_entries() -> list[EntryEntity]:
    """Загрузить записи вместе со связанными объектами ПР3."""
    users = load_users(USERS_FILE)
    categories = load_categories(CATEGORIES_FILE)
    dates = load_dates(DATES_FILE)
    return load_entries(ENTRIES_FILE, users, categories, dates)


def categories_list(request: HttpRequest) -> HttpResponse:
    """Страница списка категорий из SQLite."""
    conn = get_connection()
    categories = conn.execute(
        """
        SELECT
            id,
            name
        FROM categories
        ORDER BY name;
        """
    ).fetchall()
    conn.close()
    context = {
        "categories": categories,
    }
    return render(request, "categories/category_list.html", context)


def category_detail(request: HttpRequest, category_id: int) -> HttpResponse:
    """Страница одной категории (объекты ПР3)."""
    categories = load_categories(CATEGORIES_FILE)
    category = find_category_by_id(categories, category_id)
    entries: list[EntryEntity] = []
    if category is not None:
        entries = filter_entries_by_category(_load_entries(), category)
    context = {
        "category": category,
        "entries": entries,
    }
    return render(
        request,
        "categories/category_detail.html",
        context,
        status=404 if category is None else 200,
    )
