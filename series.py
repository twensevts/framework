"""Функции работы с сериями комиксов."""


def _next_id(items: list[dict]) -> int:
    return max((item["id"] for item in items), default=0) + 1


def add_series(
    series: list[dict], title: str, author: str, total_issues: int
) -> dict:
    """Создать серию и добавить её в каталог."""
    if not title.strip() or not author.strip() or total_issues < 1:
        raise ValueError("Некорректные данные серии.")

    item = {
        "id": _next_id(series),
        "title": title.strip(),
        "author": author.strip(),
        "total_issues": total_issues,
    }
    series.append(item)
    return item


def find_series_by_id(series: list[dict], series_id: int) -> dict | None:
    """Найти серию по идентификатору."""
    return next((item for item in series if item["id"] == series_id), None)


def find_series(series: list[dict], query: str) -> list[dict]:
    """Найти серии по названию или автору."""
    normalized = query.lower()
    return [
        item
        for item in series
        if normalized in item["title"].lower()
        or normalized in item["author"].lower()
    ]


def sort_series(series: list[dict], by: str = "title") -> list[dict]:
    """Вернуть серии, отсортированные по названию или числу выпусков."""
    if by not in {"title", "total_issues"}:
        raise ValueError("Неизвестное поле сортировки.")
    return sorted(series, key=lambda item: item[by])
