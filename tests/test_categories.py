"""Тесты класса CategoryEntity и функций работы с категориями."""

from models import CategoryEntity
from models.categories import add_category, find_category, find_category_by_id


def test_category_creation() -> None:
    category = CategoryEntity(1, "учеба")
    assert category.id == 1
    assert category.name == "учеба"


def test_category_str() -> None:
    category = CategoryEntity(2, "работа")
    assert str(category) == "[2] работа"


def test_category_from_data() -> None:
    category = CategoryEntity.from_data({"id": 3, "name": "личное"})
    assert category.id == 3
    assert category.name == "личное"


def test_add_and_find_category() -> None:
    categories: list[CategoryEntity] = []
    category = add_category(categories, "учеба")
    assert category is not None
    assert find_category(categories, "Учеба") is category
    assert find_category_by_id(categories, category.id) is category


def test_add_duplicate_category() -> None:
    categories: list[CategoryEntity] = []
    add_category(categories, "учеба")
    assert add_category(categories, "учеба") is None
    assert len(categories) == 1
