"""Панель администрирования календарных дат."""

from django.contrib import admin

from dates.models import DiaryDate


@admin.register(DiaryDate)
class DiaryDateAdmin(admin.ModelAdmin):
    """Настройка списка дат для автодополнения в записях."""

    list_display = ("id", "value")
    list_display_links = ("value",)
    search_fields = ("value",)
    list_filter = ("value",)
    ordering = ("value",)
    list_per_page = 20
    date_hierarchy = "value"
