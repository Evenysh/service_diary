"""Тесты загрузки и сохранения объектной модели в JSON."""

from datetime import date
from pathlib import Path

from models import CategoryEntity, DateEntity, PublicEntryEntity, UserEntity
from storage import (
    load_categories,
    load_dates,
    load_entries,
    load_users,
    save_dates,
    save_entries,
)


def test_save_and_load_entries(tmp_path: Path) -> None:
    users = [UserEntity(1, "Анна", "anna@example.com")]
    categories = [CategoryEntity(1, "учеба")]
    dates = [DateEntity(1, date(2026, 9, 8))]
    entries = [
        PublicEntryEntity(
            1,
            users[0],
            categories[0],
            "Заголовок",
            "Текст",
            dates[0],
            8,
        )
    ]
    filename = tmp_path / "entries.json"
    save_entries(str(filename), entries)

    loaded = load_entries(str(filename), users, categories, dates)
    assert len(loaded) == 1
    assert loaded[0].title == "Заголовок"
    assert loaded[0].user is users[0]
    assert loaded[0].category is categories[0]
    assert loaded[0].entry_date is dates[0]


def test_save_and_load_dates(tmp_path: Path) -> None:
    dates = [DateEntity(1, date(2026, 9, 8))]
    filename = tmp_path / "dates.json"
    save_dates(str(filename), dates)
    loaded = load_dates(str(filename))
    assert len(loaded) == 1
    assert loaded[0].id == 1
    assert loaded[0].value == date(2026, 9, 8)


def test_load_users_missing_file(tmp_path: Path) -> None:
    assert load_users(str(tmp_path / "missing.json")) == []


def test_load_default_categories(tmp_path: Path) -> None:
    categories = load_categories(str(tmp_path / "missing.json"))
    names = [category.name for category in categories]
    assert names == ["личное", "учеба", "работа"]
