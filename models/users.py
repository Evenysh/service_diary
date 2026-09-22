"""Класс пользователя и функции работы с коллекцией пользователей."""

from typing import Optional


class UserEntity:
    """Пользователь сервиса ведения дневника (инкапсуляция)."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        """Создать объект пользователя."""
        self.id = user_id
        self.name = name
        self.email = email

    @staticmethod
    def validate_email(email: str) -> bool:
        """Проверить, что адрес электронной почты содержит символ @."""
        return "@" in email and "." in email.split("@")[-1]

    @classmethod
    def from_data(cls, data: dict) -> "UserEntity":
        """Создать пользователя из набора данных JSON."""
        return cls(
            user_id=data["id"],
            name=data["name"],
            email=data["email"],
        )

    def matches(self, query: str) -> bool:
        """Проверить, подходит ли пользователь по имени или почте."""
        query_lower = query.lower()
        return query_lower in self.name.lower() or query_lower in self.email.lower()

    def __str__(self) -> str:
        """Вернуть строковое представление пользователя."""
        return f"[{self.id}] {self.name} <{self.email}>"


def next_user_id(users: list[UserEntity]) -> int:
    """Вернуть следующий идентификатор пользователя."""
    return max((user.id for user in users), default=0) + 1


def add_user(users: list[UserEntity], name: str, email: str) -> Optional[UserEntity]:
    """Создать объект UserEntity и добавить его в коллекцию."""
    if not UserEntity.validate_email(email):
        return None
    user = UserEntity(next_user_id(users), name, email)
    users.append(user)
    return user


def find_user(users: list[UserEntity], query: str) -> list[UserEntity]:
    """Найти пользователей по имени или адресу электронной почты."""
    return [user for user in users if user.matches(query)]


def find_user_by_id(users: list[UserEntity], user_id: int) -> Optional[UserEntity]:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def show_users(users: list[UserEntity]) -> None:
    """Вывести информацию об объектах UserEntity."""
    if not users:
        print("Пользователей пока нет.")
        return
    for user in users:
        print(user)
