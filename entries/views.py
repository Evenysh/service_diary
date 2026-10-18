"""View-функции дневниковых записей."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import get_connection
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
    """Список записей из SQLite со связанными данными."""
    conn = get_connection()
    entries = conn.execute(
        """
        SELECT
            entries.id,
            entries.title,
            entries.is_private,
            users.name AS user_name,
            categories.name AS category_name,
            dates.value AS entry_date
        FROM entries
        JOIN users
            ON entries.user_id = users.id
        JOIN categories
            ON entries.category_id = categories.id
        JOIN dates
            ON entries.date_id = dates.id
        ORDER BY dates.value;
        """
    ).fetchall()
    conn.close()
    context = {
        "entries": entries,
    }
    return render(request, "entries/entry_list.html", context)


def entries_by_date(request: HttpRequest) -> HttpResponse:
    """Поиск записей на выбранную дату."""
    entry_date = request.GET.get("date")
    entries = []
    if entry_date:
        conn = get_connection()
        entries = conn.execute(
            """
            SELECT
                entries.id,
                entries.title,
                users.name AS user_name,
                categories.name AS category_name
            FROM entries
            JOIN dates
                ON entries.date_id = dates.id
            JOIN users
                ON entries.user_id = users.id
            JOIN categories
                ON entries.category_id = categories.id
            WHERE dates.value = ?
            ORDER BY entries.title;
            """,
            [entry_date],
        ).fetchall()
        conn.close()
    context = {
        "entries": entries,
        "entry_date": entry_date,
    }
    return render(request, "entries/entries_by_date.html", context)


def statistics(request: HttpRequest) -> HttpResponse:
    """Статистика: число записей по категориям."""
    conn = get_connection()
    statistics_data = conn.execute(
        """
        SELECT
            categories.name AS category_name,
            COUNT(entries.id) AS entries_count
        FROM categories
        LEFT JOIN entries
            ON categories.id = entries.category_id
        GROUP BY categories.id, categories.name
        ORDER BY entries_count DESC;
        """
    ).fetchall()
    conn.close()
    context = {
        "statistics": statistics_data,
    }
    return render(request, "entries/statistics.html", context)


def entry_detail(request: HttpRequest, entry_id: int) -> HttpResponse:
    """Страница одной дневниковой записи (объекты ПР3)."""
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
