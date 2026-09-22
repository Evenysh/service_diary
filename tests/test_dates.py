"""Тесты класса DateEntity и функций работы с датами."""

from datetime import date

from models import DateEntity
from models.dates import add_date, find_date, find_date_by_id


def test_date_creation() -> None:
    item = DateEntity(1, date(2026, 9, 8))
    assert item.id == 1
    assert item.value == date(2026, 9, 8)


def test_date_str() -> None:
    item = DateEntity(1, date(2026, 9, 8))
    assert str(item) == "[1] 08.09.2026"


def test_date_from_data() -> None:
    item = DateEntity.from_data({"id": 2, "value": "2026-09-10"})
    assert item.id == 2
    assert item.value == date(2026, 9, 10)
    assert item.to_iso() == "2026-09-10"


def test_date_is_future() -> None:
    today = date(2026, 9, 12)
    assert DateEntity(1, date(2026, 9, 20)).is_future(today)
    assert not DateEntity(2, date(2026, 9, 8)).is_future(today)
    assert DateEntity.validate_not_future(date(2026, 9, 8), today)
    assert not DateEntity.validate_not_future(date(2026, 9, 20), today)


def test_add_date_reuses_existing() -> None:
    dates: list[DateEntity] = []
    first = add_date(dates, date(2026, 9, 8))
    second = add_date(dates, date(2026, 9, 8))
    assert first is second
    assert len(dates) == 1
    assert find_date(dates, date(2026, 9, 8)) is first
    assert find_date_by_id(dates, first.id) is first
