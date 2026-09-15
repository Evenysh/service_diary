"""Функции для работы с дневниковыми записями."""

from datetime import date


def add_entry(
    entries: dict[int, dict],
    title: str,
    content: str,
    category: str,
    entry_date: date,
    mood_score: int,
    user_name: str,
    is_private: bool,
) -> dict:
    """Добавить запись в словарь entries и вернуть её."""
    entry_id = max(entries.keys(), default=0) + 1
    entry = {
        "id": entry_id,
        "user_name": user_name,
        "title": title,
        "content": content,
        "category": category,
        "entry_date": entry_date.isoformat(),
        "mood_score": mood_score,
        "is_private": is_private,
    }
    entries[entry_id] = entry
    return entry


def find_entry(entries: dict[int, dict], query: str) -> list[dict]:
    """Найти записи по подстроке в заголовке."""
    query_lower = query.lower()
    return [
        entry for entry in entries.values()
        if query_lower in entry["title"].lower()
    ]


def filter_entries_by_category(
    entries: dict[int, dict],
    category: str,
) -> list[dict]:
    """Отобрать записи по категории."""
    return [
        entry for entry in entries.values()
        if entry["category"] == category
    ]


def sort_entries(entries: dict[int, dict]) -> list[dict]:
    """Отсортировать записи по дате (от новых к старым)."""
    return sorted(
        entries.values(),
        key=lambda entry: entry["entry_date"],
        reverse=True,
    )


def get_entries_statistics(entries: dict[int, dict]) -> dict[str, int | float]:
    """Вернуть статистику по записям: количество и среднее настроение."""
    if not entries:
        return {"count": 0, "avg_mood": 0.0}

    moods = [entry["mood_score"] for entry in entries.values()]
    return {
        "count": len(entries),
        "avg_mood": round(sum(moods) / len(moods), 1),
    }
