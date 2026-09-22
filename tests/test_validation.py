"""Тесты функций проверки возможности сохранения записей."""

from datetime import date

from validation import can_save_entry, is_entry_valid


def test_is_entry_valid() -> None:
    today = date(2026, 9, 12)
    assert is_entry_valid(date(2026, 9, 8), 7, "учеба", today)


def test_invalid_future_date() -> None:
    today = date(2026, 9, 12)
    assert not is_entry_valid(date(2027, 1, 1), 7, "учеба", today)


def test_can_save_entry_message() -> None:
    today = date(2026, 9, 12)
    message = can_save_entry(date(2026, 9, 8), 7, "учеба", today)
    assert message == "Запись можно сохранить в дневник"


def test_invalid_mood() -> None:
    today = date(2026, 9, 12)
    assert not is_entry_valid(date(2026, 9, 8), 0, "учеба", today)
