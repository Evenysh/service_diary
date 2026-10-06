"""View-функции категорий дневника."""

from django.http import HttpRequest, HttpResponse

from homepage.views import page
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
    """Страница списка категорий."""
    items = ""
    for category in load_categories(CATEGORIES_FILE):
        items += (
            '<li class="list-group-item">'
            f'<a href="/categories/{category.id}/">{category.name}</a>'
            "</li>"
        )
    content = f"""
<h1>Категории</h1>
<ul class="list-group">{items}</ul>
"""
    return HttpResponse(page("Дневник – категории", content))


def category_detail(request: HttpRequest, category_id: int) -> HttpResponse:
    """Страница одной категории."""
    categories = load_categories(CATEGORIES_FILE)
    category = find_category_by_id(categories, category_id)
    if category is None:
        content = """
<h1 class="text-danger">Категория не найдена</h1>
<a href="/categories/" class="btn btn-outline-secondary">
← к списку категорий
</a>
"""
        return HttpResponse(
            page("Категория не найдена", content),
            status=404,
        )

    items = ""
    for entry in filter_entries_by_category(_load_entries(), category):
        items += (
            '<li class="list-group-item">'
            f'<a href="/entries/{entry.id}/">{entry.title}</a>'
            "</li>"
        )
    if not items:
        items = '<li class="list-group-item">Записей в этой категории нет.</li>'

    content = f"""
<div class="card">
<div class="card-body">
<h5 class="card-title">{category.name}</h5>
<p class="card-text"><strong>ID:</strong> {category.id}</p>
<h6 class="mt-3">Записи категории</h6>
<ul class="list-group">{items}</ul>
<a href="/categories/" class="btn btn-outline-secondary mt-3">
← к списку категорий
</a>
</div>
</div>
"""
    return HttpResponse(page(category.name, content), status=200)
