"""Модель пользователя дневника."""

from django.db import models


class User(models.Model):
    """Автор дневниковых записей (не пользователь Django Auth)."""

    name = models.CharField(
        max_length=200,
        verbose_name="Имя пользователя",
        help_text="Отображаемое имя автора записей.",
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
        help_text="Контактный адрес автора.",
    )

    def __str__(self) -> str:
        """Вернуть имя пользователя."""
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
