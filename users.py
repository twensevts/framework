"""Функции работы с пользователями."""


def _next_id(items: list[dict]) -> int:
    return max((item["id"] for item in items), default=0) + 1


def add_user(users: list[dict], name: str, email: str) -> dict:
    """Создать пользователя и добавить его в коллекцию."""
    if not name.strip() or "@" not in email:
        raise ValueError("Некорректные данные пользователя.")
    if any(user["email"].lower() == email.lower() for user in users):
        raise ValueError("Пользователь с таким email уже существует.")

    user = {"id": _next_id(users), "name": name.strip(), "email": email}
    users.append(user)
    return user


def find_user_by_id(users: list[dict], user_id: int) -> dict | None:
    """Найти пользователя по идентификатору."""
    return next((user for user in users if user["id"] == user_id), None)


def find_users(users: list[dict], query: str) -> list[dict]:
    """Найти пользователей по имени или email."""
    normalized = query.lower()
    return [
        user
        for user in users
        if normalized in user["name"].lower()
        or normalized in user["email"].lower()
    ]
