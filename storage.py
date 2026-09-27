"""Преобразование объектной модели в JSON и обратно."""

import json
from pathlib import Path

from models import Collection, Issue, Series, User
from models.issues import find_issue_by_id
from models.series import find_series_by_id
from models.users import find_user_by_id


def _load_json(filename: str) -> list[dict]:
    path = Path(filename)
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return []
    return data if isinstance(data, list) else []


def _save_json(filename: str, data: list[dict]) -> None:
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_users(filename: str) -> list[User]:
    """Загрузить пользователей."""
    result = []
    for data in _load_json(filename):
        try:
            result.append(User.from_data(data))
        except (KeyError, TypeError, ValueError):
            continue
    return result


def save_users(filename: str, users: list[User]) -> None:
    """Сохранить пользователей."""
    _save_json(
        filename,
        [
            {"id": user.id, "name": user.name, "email": user.email}
            for user in users
        ],
    )


def load_series(filename: str) -> list[Series]:
    """Загрузить серии."""
    result = []
    for data in _load_json(filename):
        try:
            result.append(Series.from_data(data))
        except (KeyError, TypeError, ValueError):
            continue
    return result


def save_series(filename: str, series: list[Series]) -> None:
    """Сохранить серии."""
    _save_json(
        filename,
        [
            {
                "id": item.id,
                "title": item.title,
                "author": item.author,
                "total_issues": item.total_issues,
            }
            for item in series
        ],
    )


def load_issues(filename: str, series: list[Series]) -> list[Issue]:
    """Загрузить выпуски и восстановить связи с сериями."""
    result = []
    for data in _load_json(filename):
        try:
            parent = find_series_by_id(series, data["series_id"])
            if parent is None:
                continue
            issue = Issue(data["id"], parent, data["number"])
            if data.get("is_read", False):
                issue.mark_as_read()
            if data.get("rating") is not None:
                issue.rate(data["rating"])
            result.append(issue)
        except (KeyError, TypeError, ValueError):
            continue
    return result


def save_issues(filename: str, issues: list[Issue]) -> None:
    """Сохранить выпуски через идентификаторы серий."""
    _save_json(
        filename,
        [
            {
                "id": issue.id,
                "series_id": issue.series.id,
                "number": issue.number,
                "is_read": issue.is_read,
                "rating": issue.rating,
            }
            for issue in issues
        ],
    )


def load_collections(
    filename: str, users: list[User], issues: list[Issue]
) -> list[Collection]:
    """Загрузить коллекции и восстановить объектные связи."""
    result = []
    for position, data in enumerate(_load_json(filename), start=1):
        try:
            user = find_user_by_id(users, data["user_id"])
            if user is None:
                continue
            collection_issues = [
                issue
                for issue_id in data.get("issue_ids", [])
                if (issue := find_issue_by_id(issues, issue_id)) is not None
            ]
            result.append(
                Collection(data.get("id", position), user, collection_issues)
            )
        except (KeyError, TypeError, ValueError):
            continue
    return result


def save_collections(
    filename: str, collections: list[Collection]
) -> None:
    """Сохранить коллекции через идентификаторы связанных объектов."""
    _save_json(
        filename,
        [
            {
                "id": collection.id,
                "user_id": collection.user.id,
                "issue_ids": [issue.id for issue in collection.issues],
            }
            for collection in collections
        ],
    )
