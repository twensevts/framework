import pytest

from models.users import User, add_user, find_user_by_id, find_users


def test_user_properties_and_string():
    user = User(1, " Анна ", "ANNA@example.com")

    assert user.name == "Анна"
    assert user.email == "anna@example.com"
    assert str(user) == "Анна <anna@example.com>"


def test_add_and_find_user():
    users = []
    created = add_user(users, "Анна", "anna@example.com")

    assert created.id == 1
    assert find_user_by_id(users, 1) is created
    assert find_users(users, "ANNA") == [created]


def test_invalid_and_duplicate_email_are_forbidden():
    with pytest.raises(ValueError):
        User(1, "Анна", "invalid")

    users = [User(1, "Анна", "anna@example.com")]
    with pytest.raises(ValueError):
        add_user(users, "Другая Анна", "ANNA@example.com")


def test_user_from_data():
    user = User.from_data(
        {"id": 3, "name": "Иван", "email": "ivan@example.com"}
    )

    assert user.id == 3
    assert user.name == "Иван"
