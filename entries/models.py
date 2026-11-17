"""Модель дневниковой записи."""

from datetime import date

from django.db import models
from django.db.models import BooleanField, Case, GeneratedField, Value, When

from categories.models import Category
from dates.models import DiaryDate
from users.models import User


class EntryQuerySet(models.QuerySet):
    """Повторно используемые выборки дневниковых записей."""

    def public(self) -> models.QuerySet:
        """Вернуть открытые записи."""
        return self.filter(status=self.model.Status.PUBLIC)

    def private(self) -> models.QuerySet:
        """Вернуть приватные записи."""
        return self.filter(status=self.model.Status.PRIVATE)

    def archived(self) -> models.QuerySet:
        """Вернуть архивные записи."""
        return self.filter(status=self.model.Status.ARCHIVED)

    def for_date(self, selected_date: date) -> models.QuerySet:
        """Вернуть записи указанного календарного дня."""
        return self.filter(entry_date__value=selected_date)


class EntryManager(models.Manager.from_queryset(EntryQuerySet)):
    """Менеджер записей на основе EntryQuerySet."""


class Entry(models.Model):
    """Дневниковая запись пользователя."""

    class Status(models.TextChoices):
        PUBLIC = "public", "Открытая"
        PRIVATE = "private", "Приватная"
        ARCHIVED = "archived", "Архивная"

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
        help_text="Целое число от 1 до 10.",
    )
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.PUBLIC,
        verbose_name="Статус записи",
        help_text="Открытая, приватная или архивная запись.",
    )
    is_high_mood = GeneratedField(
        expression=Case(
            When(mood_score__gte=8, then=Value(True)),
            default=Value(False),
        ),
        output_field=BooleanField(),
        db_persist=True,
        verbose_name="Высокое настроение",
    )

    objects = EntryManager()

    def content_for_display(self) -> str:
        """Скрыть текст приватной записи."""
        if self.status == self.Status.PRIVATE:
            return "(скрыто)"
        return self.content

    def make_private(self) -> None:
        """Сделать запись приватной."""
        self.status = self.Status.PRIVATE
        self.save(update_fields=["status"])

    def make_public(self) -> None:
        """Сделать запись открытой."""
        self.status = self.Status.PUBLIC
        self.save(update_fields=["status"])

    def make_archived(self) -> None:
        """Перенести запись в архив."""
        self.status = self.Status.ARCHIVED
        self.save(update_fields=["status"])

    def __str__(self) -> str:
        """Вернуть краткое представление записи."""
        return f"{self.title} ({self.user})"

    class Meta:
        ordering = ["entry_date", "pk"]
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
