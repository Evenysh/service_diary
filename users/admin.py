"""Панель администрирования пользователей дневника."""

from django.contrib import admin

from entries.admin import EntryInline
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Настройка списка авторов и связанных записей."""

    list_display = ("id", "name", "email")
    list_display_links = ("name",)
    search_fields = ("name", "email")
    list_filter = ("name",)
    ordering = ("name",)
    list_per_page = 20
    inlines = (EntryInline,)
