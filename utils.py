"""Вспомогательные функции ввода данных."""

from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате ДД.ММ.ГГГГ."""
    while True:
        value = input(prompt)
        try:
            return datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: используйте формат ДД.ММ.ГГГГ.")


def input_str(prompt: str) -> str:
    """Запросить у пользователя непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: поле не может быть пустым.")
