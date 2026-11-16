"""Модель календарной даты дневника."""

from django.db import models


class DiaryDate(models.Model):
    """Календарный день, к которому привязаны записи."""

    value = models.DateField(
        verbose_name="Дата",
    )

    def __str__(self) -> str:
        """Вернуть дату в формате ISO."""
        return self.value.isoformat()

    class Meta:
        ordering = ["value"]
        verbose_name = "Дата"
        verbose_name_plural = "Даты"
