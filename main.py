"""Начальный сценарий сервиса ведения дневника

Проверяет, можно ли сохранить одну дневниковую запись.
Используются простые типы, операции, преобразование типов,
ветвления и импорт модуля
"""

from datetime import date


def can_save_entry(entry_date, mood_score, category, today):
    if entry_date > today:
        return "Нельзя сохранить запись: указана будущая дата"
    elif mood_score < 1 or mood_score > 10:
        return "Нельзя сохранить запись: оценка настроения должна быть от 1 до 10"
    elif category != "личное" and category != "учёба" and category != "работа":
        return "Нельзя сохранить запись: неизвестная категория"
    else:
        return "Запись можно сохранить в дневник"


user_name = "Анна"
entry_title = "Итоги учебного дня"
category = "учёба"
entry_date = date(2026, 9, 8)
is_private = True
mood_text = "7"
mood_score = int(mood_text)
today = date.today()

print(f"Пользователь: {user_name}")
print(f"Заголовок: {entry_title}")
print(f"Категория: {category}")
print(f"Дата записи: {entry_date}")
print(f"Приватная запись: {is_private}")
print(f"Оценка настроения: {mood_score}")

status = can_save_entry(entry_date, mood_score, category, today)
print(status)