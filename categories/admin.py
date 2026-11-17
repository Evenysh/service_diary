"""Панель администрирования категорий."""

from django.contrib import admin
from django.db.models import Count, QuerySet
from django.http import HttpRequest

from categories.models import Category
from entries.admin import EntryInline


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка списка категорий и подсчёта записей."""

    list_display = ("id", "name", "slug", "entries_count")
    list_display_links = ("name",)
    search_fields = ("name", "slug")
    list_filter = ("name",)
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("slug",)
    inlines = (EntryInline,)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """Добавить число записей без N+1 запросов."""
        queryset = super().get_queryset(request)
        return queryset.annotate(entries_count=Count("entries"))

    @admin.display(description="Записей", ordering="entries_count")
    def entries_count(self, obj: Category) -> int:
        """Вернуть число записей категории."""
        return obj.entries_count
