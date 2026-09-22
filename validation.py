"""Функции проверки возможности сохранения дневниковых записей."""

from datetime import date

VALID_CATEGORIES = ("личное", "учеба", "работа")
SAVE_ALLOWED_MESSAGE = "Запись можно сохранить в дневник"


def can_save_entry(
    entry_date: date,
    mood_score: int,
    category: str,
    today: date,
    valid_categories: tuple[str, ...] | list[str] = VALID_CATEGORIES,
) -> str:
    """Проверить, можно ли сохранить запись (функция из ПР1)."""
    if entry_date > today:
        return "Нельзя сохранить запись: указана будущая дата"
    if mood_score < 1 or mood_score > 10:
        return (
            "Нельзя сохранить запись: оценка настроения должна быть от 1 до 10"
        )
    if category not in valid_categories:
        return "Нельзя сохранить запись: неизвестная категория"
    return SAVE_ALLOWED_MESSAGE


def is_entry_valid(
    entry_date: date,
    mood_score: int,
    category: str,
    today: date,
    valid_categories: tuple[str, ...] | list[str] = VALID_CATEGORIES,
) -> bool:
    """Проверить, можно ли сохранить запись на указанную дату."""
    return (
        can_save_entry(
            entry_date,
            mood_score,
            category,
            today,
            valid_categories,
        )
        == SAVE_ALLOWED_MESSAGE
    )


def get_entry_status(is_valid: bool) -> str:
    """Вернуть текстовый статус возможности сохранения записи."""
    if is_valid:
        return SAVE_ALLOWED_MESSAGE
    return "Нельзя сохранить запись"
