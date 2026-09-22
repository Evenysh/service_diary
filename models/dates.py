"""Класс даты дневника и функции работы с коллекцией дат."""

from datetime import date
from typing import Optional, Union


class DateEntity:
    """Дата, к которой привязываются дневниковые записи (инкапсуляция)."""

    def __init__(self, date_id: int, value: date) -> None:
        """Создать объект даты."""
        self.id = date_id
        self.value = value

    @staticmethod
    def validate_not_future(value: date, today: date) -> bool:
        """Проверить, что дата не относится к будущему."""
        return value <= today

    @classmethod
    def from_data(cls, data: dict) -> "DateEntity":
        """Создать дату из набора данных JSON."""
        return cls(
            date_id=data["id"],
            value=date.fromisoformat(data["value"]),
        )

    def is_future(self, today: date) -> bool:
        """Проверить, относится ли дата к будущему относительно today."""
        return self.value > today

    def matches(self, other: Union["DateEntity", date]) -> bool:
        """Проверить совпадение с другой датой."""
        other_value = other.value if isinstance(other, DateEntity) else other
        return self.value == other_value

    def to_iso(self) -> str:
        """Вернуть дату в формате ISO YYYY-MM-DD."""
        return self.value.isoformat()

    def __eq__(self, other: object) -> bool:
        """Сравнить даты по календарному значению."""
        if isinstance(other, DateEntity):
            return self.value == other.value
        if isinstance(other, date):
            return self.value == other
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        """Сравнить даты для сортировки."""
        if isinstance(other, DateEntity):
            return self.value < other.value
        if isinstance(other, date):
            return self.value < other
        return NotImplemented

    def __str__(self) -> str:
        """Вернуть строковое представление даты."""
        formatted = self.value.strftime("%d.%m.%Y")
        return f"[{self.id}] {formatted}"


def next_date_id(dates: list[DateEntity]) -> int:
    """Вернуть следующий идентификатор даты."""
    return max((item.id for item in dates), default=0) + 1


def find_date(dates: list[DateEntity], value: date) -> Optional[DateEntity]:
    """Найти дату по календарному значению."""
    for item in dates:
        if item.matches(value):
            return item
    return None


def find_date_by_id(dates: list[DateEntity], date_id: int) -> Optional[DateEntity]:
    """Найти дату по идентификатору."""
    for item in dates:
        if item.id == date_id:
            return item
    return None


def add_date(dates: list[DateEntity], value: date) -> DateEntity:
    """Вернуть существующую дату или создать новый объект DateEntity."""
    existing = find_date(dates, value)
    if existing is not None:
        return existing
    item = DateEntity(next_date_id(dates), value)
    dates.append(item)
    return item


def show_dates(dates: list[DateEntity]) -> None:
    """Вывести информацию об объектах DateEntity."""
    if not dates:
        print("Дат пока нет.")
        return
    for item in sorted(dates, reverse=True):
        print(item)
