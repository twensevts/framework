import pytest

from users import add_user, find_user_by_id, find_users


def test_add_and_find_user():
    users = []
    created = add_user(users, "Анна", "anna@example.com")

    assert created["id"] == 1
    assert find_user_by_id(users, 1) is created
    assert find_users(users, "ANNA") == [created]


def test_duplicate_email_is_forbidden():
    users = []
    add_user(users, "Анна", "anna@example.com")

    with pytest.raises(ValueError):
        add_user(users, "Другая Анна", "ANNA@example.com")
