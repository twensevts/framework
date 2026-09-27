"""Класс серии комиксов и операции над каталогом серий."""

from __future__ import annotations


class Series:
    """Серия комиксов."""

    def __init__(
        self,
        series_id: int,
        title: str,
        author: str,
        total_issues: int,
    ) -> None:
        if not title.strip() or not author.strip():
            raise ValueError("Название и автор обязательны.")
        if not self.validate_total_issues(total_issues):
            raise ValueError("Количество выпусков должно быть положительным.")
        self.id = series_id
        self.title = title.strip()
        self.author = author.strip()
        self.total_issues = total_issues

    def __str__(self) -> str:
        return (
            f"{self.title} — {self.author} "
            f"({self.total_issues} выпусков)"
        )

    def has_issue(self, number: int) -> bool:
        """Проверить существование номера в серии."""
        return 1 <= number <= self.total_issues

    @staticmethod
    def validate_total_issues(total_issues: int) -> bool:
        """Проверить корректность размера серии."""
        return total_issues > 0

    @classmethod
    def from_data(cls, data: dict) -> Series:
        """Создать серию из данных JSON."""
        return cls(
            data["id"],
            data["title"],
            data["author"],
            data["total_issues"],
        )


def add_series(
    series: list[Series], title: str, author: str, total_issues: int
) -> Series:
    """Создать серию и добавить её в каталог."""
    series_id = max((item.id for item in series), default=0) + 1
    item = Series(series_id, title, author, total_issues)
    series.append(item)
    return item


def find_series_by_id(
    series: list[Series], series_id: int
) -> Series | None:
    """Найти серию по идентификатору."""
    return next((item for item in series if item.id == series_id), None)


def find_series(series: list[Series], query: str) -> list[Series]:
    """Найти серии по названию или автору."""
    normalized = query.lower()
    return [
        item
        for item in series
        if normalized in item.title.lower()
        or normalized in item.author.lower()
    ]


def sort_series(
    series: list[Series], by: str = "title"
) -> list[Series]:
    """Отсортировать серии по названию или числу выпусков."""
    if by not in {"title", "total_issues"}:
        raise ValueError("Неизвестное поле сортировки.")
    return sorted(series, key=lambda item: getattr(item, by))


def show_series(series: list[Series]) -> None:
    """Вывести каталог серий."""
    for item in sort_series(series):
        print(f"{item.id}: {item}")
