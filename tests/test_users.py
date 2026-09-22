"""Тесты класса UserEntity и функций работы с пользователями."""

from models import UserEntity
from models.users import add_user, find_user, find_user_by_id


def test_user_creation() -> None:
    user = UserEntity(1, "Анна Разина", "anna@example.com")
    assert user.id == 1
    assert user.name == "Анна Разина"
    assert user.email == "anna@example.com"


def test_user_str() -> None:
    user = UserEntity(1, "Анна Разина", "anna@example.com")
    text = str(user)
    assert "[1]" in text
    assert "Анна Разина" in text
    assert "anna@example.com" in text


def test_user_from_data() -> None:
    user = UserEntity.from_data(
        {"id": 2, "name": "Иван Петров", "email": "ivan@example.com"}
    )
    assert user.id == 2
    assert user.name == "Иван Петров"
    assert user.email == "ivan@example.com"


def test_validate_email() -> None:
    assert UserEntity.validate_email("anna@example.com")
    assert not UserEntity.validate_email("не-почта")


def test_add_and_find_user() -> None:
    users: list[UserEntity] = []
    user = add_user(users, "Анна", "anna@example.com")
    assert user is not None
    assert len(users) == 1
    assert find_user(users, "анна")
    assert find_user_by_id(users, user.id) is user


def test_add_user_invalid_email() -> None:
    users: list[UserEntity] = []
    assert add_user(users, "Анна", "без-собаки") is None
    assert users == []
