"""Перенос данных из JSON-файлов в SQLite."""

import json
from pathlib import Path

from db.database import get_connection

SCHEMA_FILE = Path("sql/schema.sql")

USERS_FILE = "data/users.json"
CATEGORIES_FILE = "data/categories.json"
DATES_FILE = "data/dates.json"
ENTRIES_FILE = "data/entries.json"


def load_json(filename: str) -> list:
    """Прочитать список объектов из JSON-файла."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_users(conn) -> None:
    """Вставить пользователей."""
    users = load_json(USERS_FILE)
    conn.executemany(
        """
        INSERT INTO users (id, name, email)
        VALUES (?, ?, ?)
        """,
        [(user["id"], user["name"], user["email"]) for user in users],
    )


def import_categories(conn) -> None:
    """Вставить категории."""
    categories = load_json(CATEGORIES_FILE)
    conn.executemany(
        """
        INSERT INTO categories (id, name)
        VALUES (?, ?)
        """,
        [(item["id"], item["name"]) for item in categories],
    )


def import_dates(conn) -> None:
    """Вставить даты."""
    dates = load_json(DATES_FILE)
    conn.executemany(
        """
        INSERT INTO dates (id, value)
        VALUES (?, ?)
        """,
        [(item["id"], item["value"]) for item in dates],
    )


def import_entries(conn) -> None:
    """Вставить дневниковые записи."""
    entries = load_json(ENTRIES_FILE)
    conn.executemany(
        """
        INSERT INTO entries (
            id,
            user_id,
            category_id,
            date_id,
            title,
            content,
            mood_score,
            is_private
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                entry["id"],
                entry["user_id"],
                entry["category_id"],
                entry["date_id"],
                entry["title"],
                entry["content"],
                entry["mood_score"],
                int(entry["is_private"]),
            )
            for entry in entries
        ],
    )


def ensure_schema(conn) -> None:
    """Создать таблицы по sql/schema.sql, если их ещё нет."""
    conn.executescript(SCHEMA_FILE.read_text(encoding="utf-8"))


def main() -> None:
    """Очистить таблицы и загрузить данные из JSON."""
    conn = get_connection()
    try:
        ensure_schema(conn)
        conn.execute("DELETE FROM entries")
        conn.execute("DELETE FROM dates")
        conn.execute("DELETE FROM categories")
        conn.execute("DELETE FROM users")
        import_users(conn)
        import_categories(conn)
        import_dates(conn)
        import_entries(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
