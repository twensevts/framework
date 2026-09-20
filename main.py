"""Консольный интерфейс системы коллекционирования комиксов."""

from collection import (
    add_to_collection,
    get_collection,
    get_collection_issues,
    get_statistics,
    missing_issue_numbers,
)
from issues import add_issue, mark_as_read, rate_issue, sort_issues
from series import add_series, find_series_by_id, sort_series
from storage import load_data, save_data
from users import add_user, find_user_by_id
from utils import input_int, input_rating

DATA_FILES = {
    "users": "data/users.json",
    "series": "data/series.json",
    "issues": "data/issues.json",
    "collections": "data/collections.json",
}


def show_menu() -> None:
    """Вывести главное меню."""
    print("\n=== Система коллекционирования комиксов ===")
    print("1. Показать серии")
    print("2. Добавить серию")
    print("3. Добавить пользователя")
    print("4. Добавить выпуск в коллекцию")
    print("5. Показать коллекцию")
    print("6. Отметить выпуск прочитанным")
    print("7. Оценить выпуск")
    print("8. Показать недостающие выпуски")
    print("9. Показать статистику")
    print("0. Сохранить и выйти")


def show_series(series: list[dict]) -> None:
    """Вывести каталог серий."""
    for item in sort_series(series):
        print(
            f"{item['id']}: {item['title']} — {item['author']} "
            f"({item['total_issues']} выпусков)"
        )


def show_collection(collection: dict, issues: list[dict]) -> None:
    """Вывести выпуски пользовательской коллекции."""
    collected = sort_issues(get_collection_issues(collection, issues))
    if not collected:
        print("Коллекция пуста.")
    for issue in collected:
        status = "прочитан" if issue["is_read"] else "не прочитан"
        print(
            f"ID {issue['id']}: серия {issue['series_id']}, "
            f"выпуск №{issue['number']}, {status}, "
            f"оценка: {issue['rating'] or 'нет'}"
        )


def save_all(data: dict[str, list[dict]]) -> None:
    """Сохранить все данные проекта."""
    for name, filename in DATA_FILES.items():
        save_data(filename, data[name])


def main() -> None:
    """Запустить цикл обработки команд пользователя."""
    data = {name: load_data(path) for name, path in DATA_FILES.items()}

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
                add_user(data["users"], input("Имя: "), input("Email: "))
            elif choice in {"4", "5", "8", "9"}:
                user_id = input_int("ID пользователя: ", 1)
                if find_user_by_id(data["users"], user_id) is None:
                    print("Пользователь не найден.")
                    continue
                collection = get_collection(data["collections"], user_id)

                if choice == "4":
                    series_id = input_int("ID серии: ", 1)
                    series_item = find_series_by_id(data["series"], series_id)
                    if series_item is None:
                        print("Серия не найдена.")
                        continue
                    number = input_int("Номер выпуска: ", 1)
                    if number > series_item["total_issues"]:
                        print("Такого выпуска в серии нет.")
                        continue
                    try:
                        issue = add_issue(data["issues"], series_id, number)
                    except ValueError:
                        issue = next(
                            item
                            for item in data["issues"]
                            if item["series_id"] == series_id
                            and item["number"] == number
                        )
                    add_to_collection(
                        data["collections"], user_id, issue["id"]
                    )
                elif choice == "5":
                    show_collection(collection, data["issues"])
                elif choice == "8":
                    series_id = input_int("ID серии: ", 1)
                    series_item = find_series_by_id(data["series"], series_id)
                    if series_item is None:
                        print("Серия не найдена.")
                        continue
                    collected = get_collection_issues(
                        collection, data["issues"]
                    )
                    print(list(missing_issue_numbers(series_item, collected)))
                else:
                    print(get_statistics(collection, data["issues"]))
            elif choice == "6":
                mark_as_read(data["issues"], input_int("ID выпуска: ", 1))
            elif choice == "7":
                rate_issue(
                    data["issues"],
                    input_int("ID выпуска: ", 1),
                    input_rating("Оценка: "),
                )
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
