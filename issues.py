"""Функции работы с выпусками комиксов."""


def _next_id(items: list[dict]) -> int:
    return max((item["id"] for item in items), default=0) + 1


def add_issue(issues: list[dict], series_id: int, number: int) -> dict:
    """Добавить выпуск в общий каталог."""
    if number < 1:
        raise ValueError("Номер выпуска должен быть положительным.")
    if any(
        issue["series_id"] == series_id and issue["number"] == number
        for issue in issues
    ):
        raise ValueError("Такой выпуск уже существует.")

    issue = {
        "id": _next_id(issues),
        "series_id": series_id,
        "number": number,
        "is_read": False,
        "rating": None,
    }
    issues.append(issue)
    return issue


def find_issue_by_id(issues: list[dict], issue_id: int) -> dict | None:
    """Найти выпуск по идентификатору."""
    return next((issue for issue in issues if issue["id"] == issue_id), None)


def find_issues(issues: list[dict], series_id: int) -> list[dict]:
    """Вернуть выпуски указанной серии."""
    return [issue for issue in issues if issue["series_id"] == series_id]


def mark_as_read(issues: list[dict], issue_id: int) -> bool:
    """Отметить выпуск как прочитанный."""
    issue = find_issue_by_id(issues, issue_id)
    if issue is None:
        return False
    issue["is_read"] = True
    return True


def rate_issue(issues: list[dict], issue_id: int, rating: int) -> bool:
    """Установить оценку выпуска от 1 до 5."""
    if not 1 <= rating <= 5:
        raise ValueError("Оценка должна находиться в диапазоне от 1 до 5.")
    issue = find_issue_by_id(issues, issue_id)
    if issue is None:
        return False
    issue["rating"] = rating
    return True


def sort_issues(issues: list[dict]) -> list[dict]:
    """Отсортировать выпуски по серии и номеру."""
    return sorted(
        issues,
        key=lambda issue: (issue["series_id"], issue["number"]),
    )
