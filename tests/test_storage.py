import json

from models import Collection, Issue, Series, User
from storage import (
    load_collections,
    load_issues,
    load_series,
    load_users,
    save_collections,
    save_issues,
    save_series,
    save_users,
)


def test_round_trip_restores_objects_and_relationships(tmp_path):
    users_file = tmp_path / "users.json"
    series_file = tmp_path / "series.json"
    issues_file = tmp_path / "issues.json"
    collections_file = tmp_path / "collections.json"
    user = User(1, "Анна", "anna@example.com")
    series = Series(1, "Бэтмен", "Автор", 3)
    issue = Issue(1, series, 1)
    issue.mark_as_read()
    issue.rate(5)
    collection = Collection(1, user, [issue])

    save_users(str(users_file), [user])
    save_series(str(series_file), [series])
    save_issues(str(issues_file), [issue])
    save_collections(str(collections_file), [collection])
    loaded_users = load_users(str(users_file))
    loaded_series = load_series(str(series_file))
    loaded_issues = load_issues(str(issues_file), loaded_series)
    loaded_collections = load_collections(
        str(collections_file), loaded_users, loaded_issues
    )

    assert loaded_issues[0].series is loaded_series[0]
    assert loaded_collections[0].user is loaded_users[0]
    assert loaded_collections[0].issues[0] is loaded_issues[0]
    assert loaded_issues[0].rating == 5


def test_invalid_json_returns_empty_list(tmp_path):
    filename = tmp_path / "broken.json"
    filename.write_text("not json", encoding="utf-8")

    assert load_users(str(filename)) == []


def test_invalid_records_are_skipped(tmp_path):
    filename = tmp_path / "users.json"
    filename.write_text(
        json.dumps([{"id": 1, "name": "Без email"}]),
        encoding="utf-8",
    )

    assert load_users(str(filename)) == []
