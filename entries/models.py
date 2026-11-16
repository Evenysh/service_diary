"""Модель дневниковой записи."""

from django.db import models

from categories.models import Category
from dates.models import DiaryDate
from users.models import User


class Entry(models.Model):
    """Дневниковая запись пользователя."""

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="entries",
        verbose_name="Автор",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="entries",
        verbose_name="Категория",
    )
    entry_date = models.ForeignKey(
        DiaryDate,
        on_delete=models.PROTECT,
        related_name="entries",
        verbose_name="Дата",
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
    )
    content = models.TextField(
        verbose_name="Содержание",
    )
    mood_score = models.PositiveIntegerField(
        verbose_name="Оценка настроения",
    )
    is_private = models.BooleanField(
        default=False,
        verbose_name="Приватная запись",
    )

    def content_for_display(self) -> str:
        """Скрыть текст приватной записи."""
        if self.is_private:
            return "(скрыто)"
        return self.content

    def __str__(self) -> str:
        """Вернуть краткое представление записи."""
        return f"{self.title} ({self.user})"

    class Meta:
        ordering = ["entry_date", "pk"]
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
