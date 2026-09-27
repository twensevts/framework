from models.collections import (
    Collection,
    add_collection,
    find_collection_by_user,
)
from models.issues import Issue
from models.series import Series
from models.users import User


def make_objects():
    user = User(1, "Анна", "anna@example.com")
    series = Series(1, "Бэтмен", "Автор", 4)
    return user, series


def test_add_and_remove_issue():
    user, series = make_objects()
    collection = Collection(1, user)
    issue = Issue(1, series, 1)

    assert collection.add_issue(issue)
    assert not collection.add_issue(issue)
    assert collection.remove_issue(issue.id)
    assert not collection.remove_issue(issue.id)


def test_missing_issue_numbers_uses_generator():
    user, series = make_objects()
    collection = Collection(
        1, user, [Issue(1, series, 1), Issue(2, series, 3)]
    )

    assert list(collection.missing_issue_numbers(series)) == [2, 4]


def test_collection_statistics():
    user, series = make_objects()
    first = Issue(1, series, 1)
    second = Issue(2, series, 2)
    first.mark_as_read()
    first.rate(5)
    second.rate(3)
    collection = Collection(1, user, [first, second])

    assert collection.statistics() == {
        "total": 2,
        "read": 1,
        "unread": 1,
        "average_rating": 4.0,
    }


def test_add_collection_preserves_one_collection_per_user():
    user, _ = make_objects()
    collections = []

    first = add_collection(collections, user)
    second = add_collection(collections, user)

    assert first is second
    assert find_collection_by_user(collections, user.id) is first
