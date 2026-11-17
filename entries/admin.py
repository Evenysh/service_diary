"""Панель администрирования дневниковых записей."""

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from entries.models import Entry


class EntryInline(admin.TabularInline):
    """Встроенный список записей у категории или автора."""

    model = Entry
    extra = 0
    show_change_link = True
    autocomplete_fields = ("user", "category", "entry_date")
    fields = ("title", "user", "category", "entry_date", "status")


@admin.action(description="Сделать выбранные записи приватными")
def make_private(
    modeladmin: admin.ModelAdmin,
    request: HttpRequest,
    queryset: QuerySet,
) -> None:
    """Массово назначить статус «приватная»."""
    updated = queryset.update(status=Entry.Status.PRIVATE)
    modeladmin.message_user(
        request,
        f"Приватными отмечены записи: {updated}.",
    )


@admin.action(description="Сделать выбранные записи открытыми")
def make_public(
    modeladmin: admin.ModelAdmin,
    request: HttpRequest,
    queryset: QuerySet,
) -> None:
    """Массово назначить статус «открытая»."""
    updated = queryset.update(status=Entry.Status.PUBLIC)
    modeladmin.message_user(
        request,
        f"Открытыми отмечены записи: {updated}.",
    )


@admin.action(description="Перенести выбранные записи в архив")
def make_archived(
    modeladmin: admin.ModelAdmin,
    request: HttpRequest,
    queryset: QuerySet,
) -> None:
    """Массово назначить статус «архивная»."""
    updated = queryset.update(status=Entry.Status.ARCHIVED)
    modeladmin.message_user(
        request,
        f"В архив перенесены записи: {updated}.",
    )


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    """Список записей с поиском, фильтром и связанными объектами."""

    list_display = (
        "id",
        "title",
        "user",
        "category",
        "entry_date",
        "mood_score",
        "status",
        "is_high_mood",
    )
    list_display_links = ("title",)
    list_editable = ("status",)
    search_fields = (
        "title",
        "content",
        "user__name",
        "category__name",
    )
    list_filter = ("status", "is_high_mood", "category", "user")
    ordering = ("-id",)
    list_per_page = 20
    list_select_related = ("user", "category", "entry_date")
    autocomplete_fields = ("user", "category", "entry_date")
    readonly_fields = ("is_high_mood",)
    actions = (make_private, make_public, make_archived)
