from collection import (
    add_to_collection,
    get_collection,
    get_collection_issues,
    get_statistics,
    missing_issue_numbers,
    remove_from_collection,
)


def test_add_and_remove_issue_from_collection():
    collections = []

    assert add_to_collection(collections, 1, 10)
    assert not add_to_collection(collections, 1, 10)
    assert remove_from_collection(collections, 1, 10)
    assert not remove_from_collection(collections, 1, 10)


def test_get_collection_issues():
    collection = {"user_id": 1, "issue_ids": [2]}
    issues = [
        {"id": 1, "series_id": 1, "number": 1},
        {"id": 2, "series_id": 1, "number": 2},
    ]

    assert get_collection_issues(collection, issues) == [issues[1]]


def test_missing_issue_numbers_uses_generator():
    series = {"id": 1, "total_issues": 4}
    issues = [{"series_id": 1, "number": 1}, {"series_id": 1, "number": 3}]

    assert list(missing_issue_numbers(series, issues)) == [2, 4]


def test_collection_statistics():
    collections = []
    collection = get_collection(collections, 1)
    collection["issue_ids"] = [1, 2]
    issues = [
        {"id": 1, "is_read": True, "rating": 5},
        {"id": 2, "is_read": False, "rating": 3},
    ]

    assert get_statistics(collection, issues) == {
        "total": 2,
        "read": 1,
        "unread": 1,
        "average_rating": 4.0,
    }
