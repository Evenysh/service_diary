"""Подключение к базе данных SQLite."""

import sqlite3

DB_PATH = "data/diary.sqlite"


def get_connection() -> sqlite3.Connection:
    """Открыть соединение и включить проверку внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn
