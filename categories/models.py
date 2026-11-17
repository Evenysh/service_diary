"""Модель категории дневника."""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class Category(models.Model):
    """Тематика дневниковой записи."""

    name = models.CharField(
        max_length=200,
        verbose_name="Название категории",
        help_text="Краткое название тематики записей, например «учёба».",
    )
    slug = models.SlugField(
        max_length=180,
        unique=True,
        editable=False,
        verbose_name="URL-идентификатор",
    )

    def save(self, *args, **kwargs) -> None:
        """Сформировать slug при первом сохранении категории."""
        if not self.slug:
            transliterated_name = unidecode(self.name)
            base_slug = slugify(transliterated_name) or "category"
            if self.pk:
                self.slug = f"{base_slug[:160]}-{self.pk}"
            else:
                super().save(*args, **kwargs)
                self.slug = f"{base_slug[:160]}-{self.pk}"
                super().save(update_fields=["slug"])
                return
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """Вернуть URL подробной страницы категории."""
        return reverse("categories:detail", kwargs={"slug": self.slug})

    def __str__(self) -> str:
        """Вернуть название категории."""
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
