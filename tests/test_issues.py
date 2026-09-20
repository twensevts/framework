import pytest

from issues import (
    add_issue,
    find_issues,
    mark_as_read,
    rate_issue,
    sort_issues,
)


def test_add_issue_and_prevent_duplicate():
    issues = []
    created = add_issue(issues, 1, 2)

    assert created["number"] == 2
    assert created["is_read"] is False
    with pytest.raises(ValueError):
        add_issue(issues, 1, 2)


def test_mark_issue_as_read_and_rate():
    issues = []
    created = add_issue(issues, 1, 1)

    assert mark_as_read(issues, created["id"])
    assert rate_issue(issues, created["id"], 5)
    assert created["is_read"] is True
    assert created["rating"] == 5


def test_find_and_sort_issues():
    issues = []
    add_issue(issues, 2, 3)
    add_issue(issues, 1, 2)

    assert len(find_issues(issues, 1)) == 1
    assert [item["series_id"] for item in sort_issues(issues)] == [1, 2]


def test_invalid_rating_is_forbidden():
    with pytest.raises(ValueError):
        rate_issue([], 1, 6)
