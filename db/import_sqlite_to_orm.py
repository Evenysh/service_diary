"""Перенос данных из базы ПР7 в таблицы Django ORM."""

import os
import sys
import sqlite3
from datetime import date
from pathlib import Path

import django
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DB = BASE_DIR / "data" / "diary.sqlite"

sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "diary.settings")
django.setup()

from categories.models import Category  # noqa: E402
from dates.models import DiaryDate  # noqa: E402
from entries.models import Entry  # noqa: E402
from users.models import User  # noqa: E402


def main() -> None:
    """Прочитать исходную SQLite и записать объекты ORM."""
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Исходная база не найдена: {SOURCE_DB}")

    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row
        users = connection.execute(
            """
            SELECT id, name, email
            FROM users
            ORDER BY id
            """
        ).fetchall()
        categories = connection.execute(
            """
            SELECT id, name
            FROM categories
            ORDER BY id
            """
        ).fetchall()
        dates = connection.execute(
            """
            SELECT id, value
            FROM dates
            ORDER BY id
            """
        ).fetchall()
        entries = connection.execute(
            """
            SELECT
                id,
                user_id,
                category_id,
                date_id,
                title,
                content,
                mood_score,
                is_private
            FROM entries
            ORDER BY id
            """
        ).fetchall()

        with transaction.atomic():
            for row in users:
                User.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "name": row["name"],
                        "email": row["email"],
                    },
                )
            for row in categories:
                Category.objects.update_or_create(
                    pk=row["id"],
                    defaults={"name": row["name"]},
                )
            for row in dates:
                DiaryDate.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "value": date.fromisoformat(row["value"]),
                    },
                )
            for row in entries:
                Entry.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "user_id": row["user_id"],
                        "category_id": row["category_id"],
                        "entry_date_id": row["date_id"],
                        "title": row["title"],
                        "content": row["content"],
                        "mood_score": row["mood_score"],
                        "is_private": bool(row["is_private"]),
                    },
                )

    print("Перенос данных завершён.")
    print(f"Пользователей: {User.objects.count()}")
    print(f"Категорий: {Category.objects.count()}")
    print(f"Дат: {DiaryDate.objects.count()}")
    print(f"Записей: {Entry.objects.count()}")


if __name__ == "__main__":
    main()
