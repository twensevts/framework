import pytest

from models.issues import (
    Issue,
    add_issue,
    find_issue_by_id,
    find_issues,
    sort_issues,
)
from models.series import Series


def test_issue_reading_status_and_rating():
    issue = Issue(1, Series(1, "Бэтмен", "Автор", 5), 2)

    issue.mark_as_read()
    issue.rate(5)

    assert issue.is_read is True
    assert issue.rating == 5
    assert "прочитан" in str(issue)


def test_invalid_issue_number_and_rating_are_forbidden():
    series = Series(1, "Бэтмен", "Автор", 2)

    with pytest.raises(ValueError):
        Issue(1, series, 3)

    issue = Issue(1, series, 1)
    with pytest.raises(ValueError):
        issue.rate(6)


def test_add_issue_returns_existing_object():
    series = Series(1, "Бэтмен", "Автор", 5)
    issues = []

    first = add_issue(issues, series, 1)
    second = add_issue(issues, series, 1)

    assert first is second
    assert len(issues) == 1


def test_find_filter_and_sort_issues():
    first_series = Series(1, "Альфа", "Автор", 5)
    second_series = Series(2, "Бета", "Автор", 5)
    issues = [Issue(1, second_series, 2), Issue(2, first_series, 3)]

    assert find_issue_by_id(issues, 1) is issues[0]
    assert find_issues(issues, first_series) == [issues[1]]
    assert sort_issues(issues) == [issues[1], issues[0]]
