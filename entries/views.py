"""View-функции дневниковых записей."""

from django.http import HttpRequest, HttpResponse

from homepage.views import page
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
    items = ""
    for entry in _load_entries():
        badge = "bg-secondary" if entry.is_private else "bg-success"
        items += f"""
<li class="list-group-item d-flex justify-content-between">
<a href="/entries/{entry.id}/">{entry.title}</a>
<span class="badge {badge}">{entry.visibility}</span>
</li>
"""
    content = f"""
<h1>Записи</h1>
<ul class="list-group">{items}</ul>
"""
    return HttpResponse(page("Дневник – записи", content))


def entry_detail(request: HttpRequest, entry_id: int) -> HttpResponse:
    """Страница одной дневниковой записи."""
    entries = _load_entries()
    entry = find_entry_by_id(entries, entry_id)
    if entry is None:
        content = """
<h1 class="text-danger">Запись не найдена</h1>
<a href="/entries/" class="btn btn-outline-secondary">
← к списку записей
</a>
"""
        return HttpResponse(
            page("Запись не найдена", content),
            status=404,
        )

    badge = "bg-secondary" if entry.is_private else "bg-success"
    content = f"""
<div class="card">
<div class="card-body">
<h5 class="card-title">{entry.title}</h5>
<p class="card-text"><strong>ID:</strong> {entry.id}</p>
<p class="card-text"><strong>Автор:</strong> {entry.user.name}</p>
<p class="card-text">
<strong>Категория:</strong> {entry.category.name}
</p>
<p class="card-text">
<strong>Дата:</strong> {entry.entry_date.to_iso()}
</p>
<p class="card-text">
<strong>Настроение:</strong> {entry.mood_score}
</p>
<p class="card-text">
Статус:
<span class="badge {badge}">{entry.visibility}</span>
</p>
<p class="card-text">
<strong>Содержание:</strong> {entry.content_for_display()}
</p>
<a href="/entries/" class="btn btn-outline-secondary">
← к списку записей
</a>
</div>
</div>
"""
    return HttpResponse(
        page(entry.title, content),
        status=200,
    )
