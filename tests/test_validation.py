"""Тесты функций проверки и создания записей."""

from datetime import date

from validation import create_entry, is_entry_valid


def test_is_entry_valid():
    today = date(2026, 9, 12)
    assert is_entry_valid(date(2026, 9, 8), 7, "учёба", today)


def test_invalid_future_date():
    today = date(2026, 9, 12)
    assert not is_entry_valid(date(2027, 1, 1), 7, "учёба", today)


def test_create_entry():
    entries = {}
    today = date(2026, 9, 12)
    result = create_entry(
        entries,
        "Заголовок",
        "Текст",
        "личное",
        date(2026, 9, 8),
        6,
        "Анна",
        True,
        today,
    )
    assert result is not None
    assert len(entries) == 1


def test_duplicate_invalid_category():
    entries = {}
    today = date(2026, 9, 12)
    result = create_entry(
        entries,
        "Заголовок",
        "Текст",
        "спорт",
        date(2026, 9, 8),
        6,
        "Анна",
        True,
        today,
    )
    assert result is None
