"""Тесты классов записей и функций работы с коллекцией записей."""

from datetime import date

from models import (
    CategoryEntity,
    DateEntity,
    PrivateEntryEntity,
    PublicEntryEntity,
    UserEntity,
)
from models.entries import (
    add_entry,
    create_entry,
    delete_entry,
    filter_entries_by_category,
    filter_entries_by_date,
    find_entry,
    sort_entries,
)


def _sample_user() -> UserEntity:
    return UserEntity(1, "Анна", "anna@example.com")


def _sample_category(name: str = "учеба") -> CategoryEntity:
    return CategoryEntity(1, name)


def _sample_date(day: int = 8, date_id: int = 1) -> DateEntity:
    return DateEntity(date_id, date(2026, 9, day))


def test_entry_creation() -> None:
    user = _sample_user()
    category = _sample_category()
    entry_date = _sample_date()
    entry = PublicEntryEntity(
        1,
        user,
        category,
        "Итоги дня",
        "Текст",
        entry_date,
        7,
    )
    assert entry.id == 1
    assert entry.user is user
    assert entry.category is category
    assert entry.entry_date is entry_date
    assert entry.title == "Итоги дня"
    assert entry.mood_score == 7
    assert not entry.is_private
    assert entry.visibility == "публичная"


def test_entry_str() -> None:
    entry = PublicEntryEntity(
        1,
        _sample_user(),
        _sample_category(),
        "Итоги дня",
        "Текст записи",
        _sample_date(),
        7,
    )
    text = str(entry)
    assert "Итоги дня" in text
    assert "Анна" in text
    assert "учеба" in text
    assert "Текст записи" in text
    assert "2026-09-08" in text


def test_private_entry_hides_content() -> None:
    entry = PrivateEntryEntity(
        1,
        _sample_user(),
        _sample_category("личное"),
        "Секреты",
        "Не показывать",
        _sample_date(),
        5,
    )
    assert entry.is_private
    assert "(скрыто)" in str(entry)
    assert "Не показывать" not in str(entry)


def test_entry_from_data() -> None:
    user = _sample_user()
    category = _sample_category()
    entry_date = _sample_date()
    from models import EntryEntity

    entry = EntryEntity.from_data(
        {
            "id": 4,
            "title": "Заголовок",
            "content": "Текст",
            "mood_score": 6,
            "is_private": True,
        },
        user,
        category,
        entry_date,
    )
    assert isinstance(entry, PrivateEntryEntity)
    assert entry.user is user
    assert entry.category is category
    assert entry.entry_date is entry_date


def test_validate_mood() -> None:
    from models import EntryEntity

    assert EntryEntity.validate_mood(7)
    assert not EntryEntity.validate_mood(0)
    assert not EntryEntity.validate_mood(11)


def test_add_entry() -> None:
    entries = []
    add_entry(
        entries,
        _sample_user(),
        _sample_category(),
        "Тест",
        "Содержание",
        _sample_date(),
        7,
        True,
    )
    assert len(entries) == 1
    assert entries[0].title == "Тест"


def test_find_entry() -> None:
    entries = []
    add_entry(
        entries,
        _sample_user(),
        _sample_category(),
        "Итоги учебного дня",
        "Текст",
        _sample_date(),
        7,
        True,
    )
    assert find_entry(entries, "учебного")


def test_sort_entries() -> None:
    entries = []
    user = _sample_user()
    category = _sample_category("личное")
    add_entry(
        entries,
        user,
        category,
        "Старая",
        "Текст",
        _sample_date(1, 1),
        5,
        True,
    )
    add_entry(
        entries,
        user,
        _sample_category("учеба"),
        "Новая",
        "Текст",
        _sample_date(10, 2),
        8,
        False,
    )
    sorted_entries = sort_entries(entries)
    assert sorted_entries[0].title == "Новая"


def test_filter_entries_by_category() -> None:
    entries = []
    user = _sample_user()
    study = CategoryEntity(1, "учеба")
    work = CategoryEntity(2, "работа")
    day = _sample_date()
    add_entry(entries, user, study, "Учеба", "Текст", day, 7, False)
    add_entry(entries, user, work, "Работа", "Текст", day, 6, False)
    filtered = filter_entries_by_category(entries, study)
    assert len(filtered) == 1
    assert filtered[0].title == "Учеба"


def test_filter_entries_by_date() -> None:
    entries = []
    user = _sample_user()
    category = _sample_category()
    first_day = _sample_date(8, 1)
    second_day = _sample_date(10, 2)
    add_entry(entries, user, category, "Первая", "Текст", first_day, 7, False)
    add_entry(entries, user, category, "Вторая", "Текст", second_day, 6, False)
    filtered = filter_entries_by_date(entries, first_day)
    assert len(filtered) == 1
    assert filtered[0].title == "Первая"


def test_create_entry() -> None:
    entries = []
    today = date(2026, 9, 12)
    result = create_entry(
        entries,
        _sample_user(),
        _sample_category("личное"),
        "Заголовок",
        "Текст",
        _sample_date(),
        6,
        True,
        today,
        ["личное", "учеба", "работа"],
    )
    assert result is not None
    assert len(entries) == 1
    assert result.user.name == "Анна"
    assert result.category.name == "личное"
    assert result.entry_date.value == date(2026, 9, 8)


def test_create_entry_invalid_category() -> None:
    entries = []
    today = date(2026, 9, 12)
    result = create_entry(
        entries,
        _sample_user(),
        CategoryEntity(9, "спорт"),
        "Заголовок",
        "Текст",
        _sample_date(),
        6,
        True,
        today,
        ["личное", "учеба", "работа"],
    )
    assert result is None
    assert entries == []


def test_delete_entry() -> None:
    entries = []
    entry = add_entry(
        entries,
        _sample_user(),
        _sample_category(),
        "Удалить",
        "Текст",
        _sample_date(),
        7,
        False,
    )
    assert delete_entry(entries, entry.id)
    assert entries == []
    assert not delete_entry(entries, entry.id)
