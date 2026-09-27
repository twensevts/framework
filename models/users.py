"""Класс пользователя и операции над коллекцией пользователей."""

from __future__ import annotations


class User:
    """Пользователь системы и владелец коллекции."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        if not name.strip() or not self.validate_email(email):
            raise ValueError("Некорректные данные пользователя.")
        self.id = user_id
        self.name = name.strip()
        self.email = email.strip().lower()

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"

    @staticmethod
    def validate_email(email: str) -> bool:
        """Выполнить простую проверку адреса электронной почты."""
        local, separator, domain = email.strip().partition("@")
        return bool(local and separator and "." in domain)

    @classmethod
    def from_data(cls, data: dict) -> User:
        """Создать пользователя из данных JSON."""
        return cls(data["id"], data["name"], data["email"])


def add_user(users: list[User], name: str, email: str) -> User:
    """Создать пользователя и добавить его в коллекцию."""
    if any(user.email == email.strip().lower() for user in users):
        raise ValueError("Пользователь с таким email уже существует.")
    user_id = max((user.id for user in users), default=0) + 1
    user = User(user_id, name, email)
    users.append(user)
    return user


def find_user_by_id(users: list[User], user_id: int) -> User | None:
    """Найти пользователя по идентификатору."""
    return next((user for user in users if user.id == user_id), None)


def find_users(users: list[User], query: str) -> list[User]:
    """Найти пользователей по имени или email."""
    normalized = query.lower()
    return [
        user
        for user in users
        if normalized in user.name.lower() or normalized in user.email
    ]


def show_users(users: list[User]) -> None:
    """Вывести пользователей."""
    for user in users:
        print(f"{user.id}: {user}")
