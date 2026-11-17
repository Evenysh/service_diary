"""View-функции дневниковых записей."""

from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from categories.models import Category
from entries.models import Entry
from users.models import User

SORT_FIELDS = {
    "date": "entry_date__value",
    "category": "category__name",
    "title": "title",
    "mood": "mood_score",
}


def entries_list(request: HttpRequest) -> HttpResponse:
    """Список записей с фильтром, поиском, сортировкой и пагинацией."""
    entry_date = request.GET.get("date", "").strip()
    category_id = request.GET.get("category", "").strip()
    user_id = request.GET.get("user", "").strip()
    visibility = request.GET.get("visibility", "").strip()
    query = request.GET.get("q", "").strip()
    author = request.GET.get("author", "").strip()
    sort = request.GET.get("sort", "date")
    error = None

    entries_data = Entry.objects.all()

    if visibility == "public":
        entries_data = entries_data.public()
    elif visibility == "private":
        entries_data = entries_data.private()
    elif visibility == "archived":
        entries_data = entries_data.archived()

    if entry_date:
        try:
            selected_date = datetime.strptime(entry_date, "%Y-%m-%d").date()
        except ValueError:
            error = "Укажите корректную дату."
        else:
            entries_data = entries_data.for_date(selected_date)

    if category_id.isdigit():
        entries_data = entries_data.filter(category_id=int(category_id))
    if user_id.isdigit():
        entries_data = entries_data.filter(user_id=int(user_id))

    if query:
        entries_data = entries_data.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    if author:
        entries_data = entries_data.filter(user__name__icontains=author)

    sort_field = SORT_FIELDS.get(sort, "entry_date__value")
    entries_data = (
        entries_data.select_related("user", "category", "entry_date")
        .annotate(
            category_name=F("category__name"),
            user_name=F("user__name"),
        )
        .order_by(sort_field, "id")
        .values(
            "id",
            "title",
            "status",
            "category_name",
            "user_name",
        )
    )

    paginator = Paginator(entries_data, 2)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "entries": page_obj,
        "page_obj": page_obj,
        "entry_date": entry_date,
        "selected_category": category_id,
        "selected_user": user_id,
        "visibility": visibility,
        "query": query,
        "author": author,
        "sort": sort,
        "categories": Category.objects.order_by("name"),
        "users": User.objects.order_by("name"),
        "error": error,
    }
    return render(request, "entries/entry_list.html", context)


def entries_by_date(request: HttpRequest) -> HttpResponse:
    """Поиск записей на выбранную дату."""
    entry_date = request.GET.get("date", "").strip()
    entries = []
    error = None
    if entry_date:
        try:
            selected_date = datetime.strptime(entry_date, "%Y-%m-%d").date()
        except ValueError:
            error = "Укажите корректную дату."
        else:
            entries = (
                Entry.objects.for_date(selected_date)
                .select_related("user", "category")
                .annotate(
                    category_name=F("category__name"),
                    user_name=F("user__name"),
                )
                .order_by("title")
            )
    context = {
        "entries": entries,
        "entry_date": entry_date,
        "error": error,
    }
    return render(request, "entries/entries_by_date.html", context)


def statistics(request: HttpRequest) -> HttpResponse:
    """Статистика: категории, статусы записей и среднее настроение."""
    statistics_data = (
        Category.objects.annotate(
            entries_count=Count("entries"),
            category_name=F("name"),
        )
        .values("category_name", "entries_count")
        .order_by("-entries_count")
    )
    mood_stats = Entry.objects.aggregate(
        avg_mood=Avg("mood_score"),
        entries_total=Count("id"),
        public_entries=Count(
            "id",
            filter=Q(status=Entry.Status.PUBLIC),
        ),
        private_entries=Count(
            "id",
            filter=Q(status=Entry.Status.PRIVATE),
        ),
        archived_entries=Count(
            "id",
            filter=Q(status=Entry.Status.ARCHIVED),
        ),
    )
    context = {
        "statistics": statistics_data,
        "mood_stats": mood_stats,
    }
    return render(request, "entries/statistics.html", context)


def entry_detail(request: HttpRequest, entry_id: int) -> HttpResponse:
    """Страница одной дневниковой записи."""
    entry = get_object_or_404(
        Entry.objects.select_related("user", "category", "entry_date"),
        pk=entry_id,
    )
    context = {
        "entry": entry,
    }
    return render(request, "entries/entry_detail.html", context)
