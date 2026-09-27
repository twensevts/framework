"""Консольный интерфейс системы коллекционирования комиксов."""

from models.collections import (
    add_collection,
    show_collection,
)
from models.issues import add_issue, find_issue_by_id
from models.series import add_series, find_series_by_id, show_series
from models.users import add_user, find_user_by_id, show_users
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
from utils import input_int, input_rating

DATA_FILES = {
    "users": "data/users.json",
    "series": "data/series.json",
    "issues": "data/issues.json",
    "collections": "data/collections.json",
}


def load_all() -> dict:
    """Загрузить объекты и восстановить связи между ними."""
    users = load_users(DATA_FILES["users"])
    series = load_series(DATA_FILES["series"])
    issues = load_issues(DATA_FILES["issues"], series)
    collections = load_collections(
        DATA_FILES["collections"], users, issues
    )
    return {
        "users": users,
        "series": series,
        "issues": issues,
        "collections": collections,
    }


def save_all(data: dict) -> None:
    """Сохранить все объекты приложения в JSON."""
    save_users(DATA_FILES["users"], data["users"])
    save_series(DATA_FILES["series"], data["series"])
    save_issues(DATA_FILES["issues"], data["issues"])
    save_collections(DATA_FILES["collections"], data["collections"])


def show_menu() -> None:
    """Вывести главное меню."""
    print("\n=== Система коллекционирования комиксов ===")
    print("1. Показать серии")
    print("2. Добавить серию")
    print("3. Показать пользователей")
    print("4. Добавить пользователя")
    print("5. Добавить выпуск в коллекцию")
    print("6. Показать коллекцию")
    print("7. Удалить выпуск из коллекции")
    print("8. Отметить выпуск прочитанным")
    print("9. Оценить выпуск")
    print("10. Показать недостающие выпуски")
    print("11. Показать статистику")
    print("0. Сохранить и выйти")


def select_collection(data: dict):
    """Запросить пользователя и вернуть его коллекцию."""
    user_id = input_int("ID пользователя: ", 1)
    user = find_user_by_id(data["users"], user_id)
    if user is None:
        print("Пользователь не найден.")
        return None
    return add_collection(data["collections"], user)


def add_issue_to_collection(data: dict) -> None:
    """Создать выпуск при необходимости и добавить в коллекцию."""
    collection = select_collection(data)
    if collection is None:
        return
    series_id = input_int("ID серии: ", 1)
    series = find_series_by_id(data["series"], series_id)
    if series is None:
        print("Серия не найдена.")
        return
    number = input_int("Номер выпуска: ", 1)
    issue = add_issue(data["issues"], series, number)
    if collection.add_issue(issue):
        print("Выпуск добавлен.")
    else:
        print("Выпуск уже находится в коллекции.")


def edit_issue(data: dict, action: str) -> None:
    """Изменить статус или оценку выпуска из коллекции."""
    collection = select_collection(data)
    if collection is None:
        return
    issue_id = input_int("ID выпуска: ", 1)
    issue = find_issue_by_id(collection.issues, issue_id)
    if issue is None:
        print("Выпуск не найден в коллекции.")
        return
    if action == "read":
        issue.mark_as_read()
        print("Выпуск отмечен как прочитанный.")
    else:
        issue.rate(input_rating("Оценка: "))
        print("Оценка сохранена.")


def handle_collection_action(data: dict, choice: str) -> None:
    """Обработать просмотр, удаление и аналитику коллекции."""
    collection = select_collection(data)
    if collection is None:
        return
    if choice == "6":
        show_collection(collection)
    elif choice == "7":
        issue_id = input_int("ID выпуска: ", 1)
        message = (
            "Выпуск удалён."
            if collection.remove_issue(issue_id)
            else "Выпуск не найден в коллекции."
        )
        print(message)
    elif choice == "10":
        series_id = input_int("ID серии: ", 1)
        series = find_series_by_id(data["series"], series_id)
        if series is None:
            print("Серия не найдена.")
            return
        missing = list(collection.missing_issue_numbers(series))
        print(f"Недостающие выпуски: {missing or 'нет'}")
    else:
        print(collection.statistics())


def main() -> None:
    """Запустить цикл обработки команд пользователя."""
    data = load_all()
    while True:
        show_menu()
        choice = input("Выберите действие: ").strip()
        try:
            if choice == "1":
                show_series(data["series"])
            elif choice == "2":
                add_series(
                    data["series"],
                    input("Название: "),
                    input("Автор: "),
                    input_int("Количество выпусков: ", 1),
                )
            elif choice == "3":
                show_users(data["users"])
            elif choice == "4":
                user = add_user(
                    data["users"], input("Имя: "), input("Email: ")
                )
                add_collection(data["collections"], user)
            elif choice == "5":
                add_issue_to_collection(data)
            elif choice in {"6", "7", "10", "11"}:
                handle_collection_action(data, choice)
            elif choice == "8":
                edit_issue(data, "read")
            elif choice == "9":
                edit_issue(data, "rate")
            elif choice == "0":
                save_all(data)
                print("Данные сохранены.")
                break
            else:
                print("Неизвестная команда.")
        except ValueError as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
