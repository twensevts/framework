"""Функции работы с пользовательскими коллекциями."""


def get_collection(collections: list[dict], user_id: int) -> dict:
    """Получить коллекцию пользователя, создав её при необходимости."""
    collection = next(
        (item for item in collections if item["user_id"] == user_id), None
    )
    if collection is None:
        collection = {"user_id": user_id, "issue_ids": []}
        collections.append(collection)
    return collection


def add_to_collection(
    collections: list[dict], user_id: int, issue_id: int
) -> bool:
    """Добавить выпуск в коллекцию пользователя."""
    collection = get_collection(collections, user_id)
    if issue_id in collection["issue_ids"]:
        return False
    collection["issue_ids"].append(issue_id)
    return True


def remove_from_collection(
    collections: list[dict], user_id: int, issue_id: int
) -> bool:
    """Удалить выпуск из коллекции пользователя."""
    collection = get_collection(collections, user_id)
    if issue_id not in collection["issue_ids"]:
        return False
    collection["issue_ids"].remove(issue_id)
    return True


def get_collection_issues(
    collection: dict, issues: list[dict]
) -> list[dict]:
    """Вернуть объекты данных выпусков из коллекции."""
    issue_ids = set(collection["issue_ids"])
    return [issue for issue in issues if issue["id"] in issue_ids]


def missing_issue_numbers(
    series: dict, collection_issues: list[dict]
):
    """Последовательно выдать номера недостающих выпусков серии."""
    collected_numbers = {
        issue["number"]
        for issue in collection_issues
        if issue["series_id"] == series["id"]
    }
    for number in range(1, series["total_issues"] + 1):
        if number not in collected_numbers:
            yield number


def get_statistics(collection: dict, issues: list[dict]) -> dict:
    """Рассчитать статистику пользовательской коллекции."""
    collected = get_collection_issues(collection, issues)
    read_count = sum(issue["is_read"] for issue in collected)
    ratings = [issue["rating"] for issue in collected if issue["rating"]]
    average = sum(ratings) / len(ratings) if ratings else 0.0
    return {
        "total": len(collected),
        "read": read_count,
        "unread": len(collected) - read_count,
        "average_rating": round(average, 2),
    }
