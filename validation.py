"""Функции проверки и создания дневниковых записей."""

from datetime import date

from entries import add_entry

VALID_CATEGORIES = ("личное", "учёба", "работа")


def can_save_entry(
    entry_date: date,
    mood_score: int,
    category: str,
    today: date,
) -> str:
    """Проверить, можно ли сохранить запись (функция из ПР1)."""
    if entry_date > today:
        return "Нельзя сохранить запись: указана будущая дата"
    if mood_score < 1 or mood_score > 10:
        return (
            "Нельзя сохранить запись: "
            "оценка настроения должна быть от 1 до 10"
        )
    if category not in VALID_CATEGORIES:
        return "Нельзя сохранить запись: неизвестная категория"
    return "Запись можно сохранить в дневник"


def is_entry_valid(
    entry_date: date,
    mood_score: int,
    category: str,
    today: date,
) -> bool:
    """Проверить, можно ли сохранить запись на указанную дату."""
    return can_save_entry(entry_date, mood_score, category, today) == (
        "Запись можно сохранить в дневник"
    )


def get_entry_status(is_valid: bool) -> str:
    """Вернуть текстовый статус возможности сохранения записи."""
    if is_valid:
        return "Запись можно сохранить в дневник"
    return "Нельзя сохранить запись"


def create_entry(
    entries: dict[int, dict],
    title: str,
    content: str,
    category: str,
    entry_date: date,
    mood_score: int,
    user_name: str,
    is_private: bool,
    today: date,
) -> dict | None:
    """Создать новую запись, если параметры корректны."""
    if not is_entry_valid(entry_date, mood_score, category, today):
        return None

    return add_entry(
        entries, title, content, category,
        entry_date, mood_score, user_name, is_private,
    )


def delete_entry(entries: dict[int, dict], entry_id: int) -> bool:
    """Удалить запись по идентификатору."""
    if entry_id not in entries:
        return False
    del entries[entry_id]
    return True
