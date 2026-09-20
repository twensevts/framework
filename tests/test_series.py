import pytest

from series import add_series, find_series, find_series_by_id, sort_series


def test_add_and_find_series():
    series = []
    created = add_series(series, "Бэтмен", "Джеф Лоуб", 13)

    assert created["total_issues"] == 13
    assert find_series_by_id(series, 1) is created
    assert find_series(series, "бэт") == [created]


def test_sort_series_by_total_issues():
    series = []
    add_series(series, "Длинная", "Автор", 20)
    add_series(series, "Короткая", "Автор", 5)

    result = sort_series(series, "total_issues")

    assert [item["total_issues"] for item in result] == [5, 20]


def test_series_requires_positive_issue_count():
    with pytest.raises(ValueError):
        add_series([], "Название", "Автор", 0)
