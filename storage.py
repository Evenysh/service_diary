"""Функции сохранения и загрузки данных проекта."""

import json
from datetime import date as calendar_date
from pathlib import Path
from typing import Any

from models import CategoryEntity, DateEntity, EntryEntity, UserEntity
from models.categories import find_category_by_id
from models.dates import add_date, find_date_by_id
from models.users import find_user_by_id

DEFAULT_CATEGORIES = [
    {"id": 1, "name": "личное"},
    {"id": 2, "name": "учеба"},
    {"id": 3, "name": "работа"},
]


def _read_json(filename: str, default: Any) -> Any:
    """Прочитать JSON-файл или вернуть значение по умолчанию."""
    path = Path(filename)
    if not path.exists():
        return default

    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return default


def _write_json(filename: str, data: Any) -> None:
    """Сохранить данные в JSON-файл."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_users(filename: str) -> list[UserEntity]:
    """Загрузить пользователей из JSON-файла."""
    data = _read_json(filename, [])
    return [UserEntity.from_data(item) for item in data]


def save_users(filename: str, users: list[UserEntity]) -> None:
    """Сохранить объекты UserEntity в JSON-файл."""
    payload = [
        {"id": user.id, "name": user.name, "email": user.email} for user in users
    ]
    _write_json(filename, payload)


def load_categories(filename: str) -> list[CategoryEntity]:
    """Загрузить категории из JSON-файла."""
    data = _read_json(filename, DEFAULT_CATEGORIES)
    if data and isinstance(data[0], str):
        data = [
            {"id": index, "name": name} for index, name in enumerate(data, start=1)
        ]
    return [CategoryEntity.from_data(item) for item in data]


def save_categories(filename: str, categories: list[CategoryEntity]) -> None:
    """Сохранить объекты CategoryEntity в JSON-файл."""
    payload = [
        {"id": category.id, "name": category.name} for category in categories
    ]
    _write_json(filename, payload)


def load_dates(filename: str) -> list[DateEntity]:
    """Загрузить даты из JSON-файла."""
    data = _read_json(filename, [])
    return [DateEntity.from_data(item) for item in data]


def save_dates(filename: str, dates: list[DateEntity]) -> None:
    """Сохранить объекты DateEntity в JSON-файл."""
    payload = [{"id": item.id, "value": item.to_iso()} for item in dates]
    _write_json(filename, payload)


def load_entries(
    filename: str,
    users: list[UserEntity],
    categories: list[CategoryEntity],
    dates: list[DateEntity],
) -> list[EntryEntity]:
    """Загрузить записи и восстановить связи с entity-объектами."""
    data = _read_json(filename, [])
    entries: list[EntryEntity] = []

    for item in data:
        user = find_user_by_id(users, item.get("user_id"))
        category = find_category_by_id(categories, item.get("category_id"))
        entry_date = find_date_by_id(dates, item.get("date_id"))
        if entry_date is None and item.get("entry_date"):
            value = calendar_date.fromisoformat(item["entry_date"])
            entry_date = add_date(dates, value)
        if user is None or category is None or entry_date is None:
            continue
        entries.append(EntryEntity.from_data(item, user, category, entry_date))

    return entries


def save_entries(filename: str, entries: list[EntryEntity]) -> None:
    """Сохранить объекты EntryEntity в JSON-файл."""
    payload = [
        {
            "id": entry.id,
            "user_id": entry.user.id,
            "category_id": entry.category.id,
            "date_id": entry.entry_date.id,
            "title": entry.title,
            "content": entry.content,
            "mood_score": entry.mood_score,
            "is_private": entry.is_private,
        }
        for entry in entries
    ]
    _write_json(filename, payload)
