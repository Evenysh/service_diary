"""Класс дневниковой записи и функции работы с коллекцией записей."""

from datetime import date
from typing import Optional

from validation import is_entry_valid

from .categories import CategoryEntity
from .dates import DateEntity
from .users import UserEntity


class EntryEntity:
    """Дневниковая запись (инкапсуляция, композиция с User/Category/Date)."""

    def __init__(
        self,
        entry_id: int,
        user: UserEntity,
        category: CategoryEntity,
        title: str,
        content: str,
        entry_date: DateEntity,
        mood_score: int,
        is_private: bool = False,
    ) -> None:
        """Создать объект дневниковой записи."""
        self.id = entry_id
        self.user = user
        self.category = category
        self.title = title
        self.content = content
        self.entry_date = entry_date
        self.mood_score = mood_score
        self.is_private = is_private

    @staticmethod
    def validate_mood(mood_score: int) -> bool:
        """Проверить, что оценка настроения находится в диапазоне 1-10."""
        return 1 <= mood_score <= 10

    @classmethod
    def from_data(
        cls,
        data: dict,
        user: UserEntity,
        category: CategoryEntity,
        entry_date: DateEntity,
    ) -> "EntryEntity":
        """Создать запись из данных JSON и связанных объектов."""
        is_private = bool(data.get("is_private", False))
        factory = PrivateEntryEntity if is_private else PublicEntryEntity
        return factory(
            entry_id=data["id"],
            user=user,
            category=category,
            title=data["title"],
            content=data["content"],
            entry_date=entry_date,
            mood_score=data["mood_score"],
        )

    @property
    def visibility(self) -> str:
        """Вернуть текстовый признак приватности записи."""
        return "приватная" if self.is_private else "публичная"

    def matches_title(self, query: str) -> bool:
        """Проверить, содержится ли подстрока в заголовке записи."""
        return query.lower() in self.title.lower()

    def belongs_to_category(self, category: CategoryEntity) -> bool:
        """Проверить, относится ли запись к указанной категории."""
        return self.category.id == category.id

    def belongs_to_date(self, entry_date: DateEntity) -> bool:
        """Проверить, относится ли запись к указанной дате."""
        return self.entry_date.matches(entry_date)

    def can_be_saved(self, today: date) -> bool:
        """Проверить, можно ли сохранить запись на текущую дату."""
        return is_entry_valid(
            self.entry_date.value,
            self.mood_score,
            self.category.name,
            today,
        )

    def content_for_display(self) -> str:
        """Вернуть содержание, которое можно показать пользователю."""
        return self.content

    def __str__(self) -> str:
        """Вернуть строковое представление записи."""
        return (
            f"[{self.id}] {self.title} | {self.user.name} | "
            f"{self.category.name} | {self.entry_date.to_iso()} | "
            f"настроение {self.mood_score} | {self.visibility}"
        )


class PublicEntryEntity(EntryEntity):
    """Публичная дневниковая запись (наследование)."""

    def __init__(
        self,
        entry_id: int,
        user: UserEntity,
        category: CategoryEntity,
        title: str,
        content: str,
        entry_date: DateEntity,
        mood_score: int,
    ) -> None:
        """Создать публичную запись."""
        super().__init__(
            entry_id,
            user,
            category,
            title,
            content,
            entry_date,
            mood_score,
            is_private=False,
        )

    def __str__(self) -> str:
        """Вернуть представление публичной записи с содержанием (полиморфизм)."""
        base = super().__str__()
        return f"{base}\n    Содержание: {self.content_for_display()}"


class PrivateEntryEntity(EntryEntity):
    """Приватная дневниковая запись (наследование)."""

    def __init__(
        self,
        entry_id: int,
        user: UserEntity,
        category: CategoryEntity,
        title: str,
        content: str,
        entry_date: DateEntity,
        mood_score: int,
    ) -> None:
        """Создать приватную запись."""
        super().__init__(
            entry_id,
            user,
            category,
            title,
            content,
            entry_date,
            mood_score,
            is_private=True,
        )

    def content_for_display(self) -> str:
        """Скрыть содержание приватной записи при выводе (полиморфизм)."""
        return "(скрыто)"

    def __str__(self) -> str:
        """Вернуть представление приватной записи без текста (полиморфизм)."""
        base = EntryEntity.__str__(self)
        return f"{base}\n    Содержание: {self.content_for_display()}"


def next_entry_id(entries: list[EntryEntity]) -> int:
    """Вернуть следующий идентификатор записи."""
    return max((entry.id for entry in entries), default=0) + 1


def add_entry(
    entries: list[EntryEntity],
    user: UserEntity,
    category: CategoryEntity,
    title: str,
    content: str,
    entry_date: DateEntity,
    mood_score: int,
    is_private: bool,
) -> EntryEntity:
    """Создать объект записи и добавить его в коллекцию."""
    factory = PrivateEntryEntity if is_private else PublicEntryEntity
    entry = factory(
        next_entry_id(entries),
        user,
        category,
        title,
        content,
        entry_date,
        mood_score,
    )
    entries.append(entry)
    return entry


def find_entry(entries: list[EntryEntity], query: str) -> list[EntryEntity]:
    """Найти записи по подстроке в заголовке."""
    return [entry for entry in entries if entry.matches_title(query)]


def find_entry_by_id(
    entries: list[EntryEntity],
    entry_id: int,
) -> Optional[EntryEntity]:
    """Найти запись по идентификатору."""
    for entry in entries:
        if entry.id == entry_id:
            return entry
    return None


def filter_entries_by_category(
    entries: list[EntryEntity],
    category: CategoryEntity,
) -> list[EntryEntity]:
    """Отобрать записи по объекту категории."""
    return [entry for entry in entries if entry.belongs_to_category(category)]


def filter_entries_by_date(
    entries: list[EntryEntity],
    entry_date: DateEntity,
) -> list[EntryEntity]:
    """Отобрать записи по объекту даты."""
    return [entry for entry in entries if entry.belongs_to_date(entry_date)]


def sort_entries(entries: list[EntryEntity]) -> list[EntryEntity]:
    """Отсортировать записи по дате (от новых к старым)."""
    return sorted(
        entries,
        key=lambda entry: entry.entry_date.value,
        reverse=True,
    )


def get_entries_statistics(entries: list[EntryEntity]) -> dict[str, int | float]:
    """Вернуть статистику по записям: количество и среднее настроение."""
    if not entries:
        return {"count": 0, "avg_mood": 0.0}

    moods = [entry.mood_score for entry in entries]
    return {
        "count": len(entries),
        "avg_mood": round(sum(moods) / len(moods), 1),
    }


def create_entry(
    entries: list[EntryEntity],
    user: UserEntity,
    category: CategoryEntity,
    title: str,
    content: str,
    entry_date: DateEntity,
    mood_score: int,
    is_private: bool,
    today: date,
    valid_categories: list[str],
) -> Optional[EntryEntity]:
    """Создать новую запись, если параметры корректны."""
    if not is_entry_valid(
        entry_date.value,
        mood_score,
        category.name,
        today,
        valid_categories,
    ):
        return None

    return add_entry(
        entries,
        user,
        category,
        title,
        content,
        entry_date,
        mood_score,
        is_private,
    )


def delete_entry(entries: list[EntryEntity], entry_id: int) -> bool:
    """Удалить запись по идентификатору."""
    entry = find_entry_by_id(entries, entry_id)
    if entry is None:
        return False
    entries.remove(entry)
    return True


def show_entries(entries: list[EntryEntity]) -> None:
    """Вывести список записей."""
    if not entries:
        print("Записей пока нет.")
        return

    for entry in sort_entries(entries):
        print("-" * 60)
        print(entry)
    print("-" * 60)
