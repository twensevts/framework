"""Класс коллекции и операции над коллекциями пользователей."""

from __future__ import annotations

from .issues import Issue, sort_issues
from .series import Series
from .users import User


class Collection:
    """Личная коллекция выпусков пользователя."""

    def __init__(
        self,
        collection_id: int,
        user: User,
        issues: list[Issue] | None = None,
    ) -> None:
        self.id = collection_id
        self.user = user
        self.issues = list(issues or [])

    def __str__(self) -> str:
        return f"Коллекция {self.user.name}: {len(self.issues)} выпусков"

    def add_issue(self, issue: Issue) -> bool:
        """Добавить выпуск, если его ещё нет в коллекции."""
        if any(item.id == issue.id for item in self.issues):
            return False
        self.issues.append(issue)
        return True

    def remove_issue(self, issue_id: int) -> bool:
        """Удалить выпуск из коллекции."""
        issue = next(
            (item for item in self.issues if item.id == issue_id), None
        )
        if issue is None:
            return False
        self.issues.remove(issue)
        return True

    def get_series_issues(self, series: Series) -> list[Issue]:
        """Вернуть собранные выпуски выбранной серии."""
        return [
            issue for issue in self.issues if issue.series.id == series.id
        ]

    def missing_issue_numbers(self, series: Series):
        """Последовательно выдать номера недостающих выпусков."""
        collected = {
            issue.number for issue in self.get_series_issues(series)
        }
        for number in range(1, series.total_issues + 1):
            if number not in collected:
                yield number

    def statistics(self) -> dict:
        """Рассчитать статистику коллекции."""
        read_count = sum(issue.is_read for issue in self.issues)
        ratings = [
            issue.rating for issue in self.issues if issue.rating is not None
        ]
        average = sum(ratings) / len(ratings) if ratings else 0.0
        return {
            "total": len(self.issues),
            "read": read_count,
            "unread": len(self.issues) - read_count,
            "average_rating": round(average, 2),
        }


def add_collection(collections: list[Collection], user: User) -> Collection:
    """Создать коллекцию пользователя."""
    existing = find_collection_by_user(collections, user.id)
    if existing is not None:
        return existing
    collection_id = max((item.id for item in collections), default=0) + 1
    collection = Collection(collection_id, user)
    collections.append(collection)
    return collection


def find_collection_by_user(
    collections: list[Collection], user_id: int
) -> Collection | None:
    """Найти коллекцию по идентификатору владельца."""
    return next(
        (item for item in collections if item.user.id == user_id), None
    )


def show_collection(collection: Collection) -> None:
    """Вывести коллекцию пользователя."""
    print(collection)
    for issue in sort_issues(collection.issues):
        print(f"{issue.id}: {issue}")
