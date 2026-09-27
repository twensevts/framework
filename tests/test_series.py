import pytest

from models.series import (
    Series,
    add_series,
    find_series,
    find_series_by_id,
    sort_series,
)


def test_series_properties_and_methods():
    series = Series(1, "Бэтмен", "Джеф Лоуб", 13)

    assert series.has_issue(1)
    assert series.has_issue(13)
    assert not series.has_issue(14)
    assert "Бэтмен" in str(series)


def test_add_find_and_sort_series():
    catalog = []
    long = add_series(catalog, "Длинная", "Автор", 20)
    short = add_series(catalog, "Короткая", "Автор", 5)

    assert find_series_by_id(catalog, 2) is short
    assert find_series(catalog, "длин") == [long]
    assert sort_series(catalog, "total_issues") == [short, long]


def test_invalid_series_is_forbidden():
    with pytest.raises(ValueError):
        Series(1, "Название", "Автор", 0)

    with pytest.raises(ValueError):
        Series(1, "", "Автор", 3)


def test_unknown_sort_field_is_forbidden():
    with pytest.raises(ValueError):
        sort_series([], "unknown")
