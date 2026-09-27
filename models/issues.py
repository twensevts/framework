"""Класс выпуска комикса и операции над выпусками."""

from __future__ import annotations

from .series import Series


class Issue:
    """Конкретный выпуск серии комиксов."""

    def __init__(self, issue_id: int, series: Series, number: int) -> None:
        if not series.has_issue(number):
            raise ValueError("Такого номера в серии нет.")
        self.id = issue_id
        self.series = series
        self.number = number
        self._is_read = False
        self._rating: int | None = None

    def __str__(self) -> str:
        rating = self.rating if self.rating is not None else "нет"
        return (
            f"{self.series.title}, выпуск №{self.number}; "
            f"{self.status}; оценка: {rating}"
        )

    @property
    def is_read(self) -> bool:
        """Вернуть признак прочтения."""
        return self._is_read

    @property
    def rating(self) -> int | None:
        """Вернуть пользовательскую оценку."""
        return self._rating

    @property
    def status(self) -> str:
        """Вернуть текстовый статус чтения."""
        return "прочитан" if self.is_read else "не прочитан"

    def mark_as_read(self) -> None:
        """Отметить выпуск как прочитанный."""
        self._is_read = True

    def rate(self, rating: int) -> None:
        """Установить оценку от 1 до 5."""
        if not 1 <= rating <= 5:
            raise ValueError("Оценка должна находиться в диапазоне от 1 до 5.")
        self._rating = rating


def add_issue(issues: list[Issue], series: Series, number: int) -> Issue:
    """Создать выпуск и добавить его в общий каталог."""
    existing = next(
        (
            issue
            for issue in issues
            if issue.series.id == series.id and issue.number == number
        ),
        None,
    )
    if existing is not None:
        return existing
    issue_id = max((issue.id for issue in issues), default=0) + 1
    issue = Issue(issue_id, series, number)
    issues.append(issue)
    return issue


def find_issue_by_id(issues: list[Issue], issue_id: int) -> Issue | None:
    """Найти выпуск по идентификатору."""
    return next((issue for issue in issues if issue.id == issue_id), None)


def find_issues(issues: list[Issue], series: Series) -> list[Issue]:
    """Вернуть выпуски заданной серии."""
    return [issue for issue in issues if issue.series.id == series.id]


def sort_issues(issues: list[Issue]) -> list[Issue]:
    """Отсортировать выпуски по серии и номеру."""
    return sorted(issues, key=lambda item: (item.series.title, item.number))


def show_issues(issues: list[Issue]) -> None:
    """Вывести выпуски."""
    for issue in sort_issues(issues):
        print(f"{issue.id}: {issue}")
