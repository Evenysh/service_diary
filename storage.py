"""Функции сохранения и загрузки данных проекта."""

import json
from pathlib import Path


def load_entries(filename: str) -> dict[int, dict]:
    """Загрузить записи из JSON-файла."""
    path = Path(filename)
    if not path.exists():
        return {}

    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}

    return {entry["id"]: entry for entry in data}


def save_entries(filename: str, entries: dict[int, dict]) -> None:
    """Сохранить записи в JSON-файл."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(list(entries.values()), file, ensure_ascii=False, indent=2)


def load_categories(filename: str) -> list[str]:
    """Загрузить список категорий из JSON-файла."""
    path = Path(filename)
    if not path.exists():
        return ["личное", "учёба", "работа"]

    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return ["личное", "учёба", "работа"]


def save_categories(filename: str, categories: list[str]) -> None:
    """Сохранить список категорий в JSON-файл."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(categories, file, ensure_ascii=False, indent=2)
