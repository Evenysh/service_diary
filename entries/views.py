"""View-функции дневниковых записей."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models import EntryEntity
from models.entries import find_entry_by_id
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


def entries_list(request: HttpRequest) -> HttpResponse:
    """Страница списка записей."""
    context = {
        "entries": _load_entries(),
    }
    return render(request, "entries/entry_list.html", context)


def entry_detail(request: HttpRequest, entry_id: int) -> HttpResponse:
    """Страница одной дневниковой записи."""
    entry = find_entry_by_id(_load_entries(), entry_id)
    context = {
        "entry": entry,
    }
    return render(
        request,
        "entries/entry_detail.html",
        context,
        status=404 if entry is None else 200,
    )
