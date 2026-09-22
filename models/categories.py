"""Класс категории и функции работы с коллекцией категорий."""

from typing import Optional


class CategoryEntity:
    """Категория дневниковой записи (инкапсуляция)."""

    def __init__(self, category_id: int, name: str) -> None:
        """Создать объект категории."""
        self.id = category_id
        self.name = name

    @staticmethod
    def validate_name(name: str) -> bool:
        """Проверить, что название категории непустое."""
        return bool(name.strip())

    @classmethod
    def from_data(cls, data: dict) -> "CategoryEntity":
        """Создать категорию из набора данных JSON."""
        return cls(
            category_id=data["id"],
            name=data["name"],
        )

    def matches(self, query: str) -> bool:
        """Проверить, совпадает ли категория с запросом по названию."""
        return self.name.lower() == query.lower()

    def __str__(self) -> str:
        """Вернуть строковое представление категории."""
        return f"[{self.id}] {self.name}"


def next_category_id(categories: list[CategoryEntity]) -> int:
    """Вернуть следующий идентификатор категории."""
    return max((category.id for category in categories), default=0) + 1


def add_category(
    categories: list[CategoryEntity],
    name: str,
) -> Optional[CategoryEntity]:
    """Создать объект CategoryEntity и добавить его в коллекцию."""
    if not CategoryEntity.validate_name(name):
        return None
    if find_category(categories, name):
        return None
    category = CategoryEntity(next_category_id(categories), name.strip())
    categories.append(category)
    return category


def find_category(
    categories: list[CategoryEntity],
    query: str,
) -> Optional[CategoryEntity]:
    """Найти категорию по названию."""
    for category in categories:
        if category.matches(query):
            return category
    return None


def find_category_by_id(
    categories: list[CategoryEntity],
    category_id: int,
) -> Optional[CategoryEntity]:
    """Найти категорию по идентификатору."""
    for category in categories:
        if category.id == category_id:
            return category
    return None


def get_category_names(categories: list[CategoryEntity]) -> list[str]:
    """Вернуть список названий категорий."""
    return [category.name for category in categories]


def show_categories(categories: list[CategoryEntity]) -> None:
    """Вывести информацию об объектах CategoryEntity."""
    if not categories:
        print("Категорий пока нет.")
        return
    for category in categories:
        print(category)
