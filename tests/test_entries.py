"""Тесты функций работы с записями."""

from datetime import date

from entries import add_entry, find_entry, sort_entries


def test_add_entry():
    entries = {}
    add_entry(
        entries, "Тест", "Содержание", "учёба",
        date(2026, 9, 8), 7, "Анна", True,
    )
    assert len(entries) == 1


def test_find_entry():
    entries = {}
    add_entry(
        entries, "Итоги учебного дня", "Текст", "учёба",
        date(2026, 9, 8), 7, "Анна", True,
    )
    assert find_entry(entries, "учебного")


def test_sort_entries():
    entries = {}
    add_entry(
        entries, "Старая", "Текст", "личное",
        date(2026, 9, 1), 5, "Анна", True,
    )
    add_entry(
        entries, "Новая", "Текст", "учёба",
        date(2026, 9, 10), 8, "Анна", True,
    )
    sorted_entries = sort_entries(entries)
    assert sorted_entries[0]["title"] == "Новая"
