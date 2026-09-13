"""Начальный сценарий системы коллекционирования комиксов."""

from datetime import date


def get_reading_status(is_read: bool) -> str:
    """Вернуть текстовый статус чтения выпуска."""
    if is_read:
        return "Вы уже прочитали этот комикс."
    return "Этот комикс ещё не прочитан."


def get_collection_progress(total: int | str, collected: int | str) -> str:
    """Рассчитать, сколько выпусков серии осталось собрать."""
    total_issues = int(total)
    collected_issues = int(collected)
    remaining = total_issues - collected_issues

    if remaining == 0:
        return "Вы собрали всю серию."
    if remaining > 0:
        return f"Осталось собрать выпусков: {remaining}."
    return "Ошибка: собрано больше выпусков, чем существует."


def get_rating_message(score: int | str) -> str:
    """Проверить оценку и вернуть сообщение для пользователя."""
    rating = int(score)

    if rating < 1:
        return "Ошибка: оценка не может быть меньше 1."
    if rating > 5:
        return "Ошибка: оценка не может быть больше 5."
    return f"Ваша оценка комикса: {rating} из 5."


comic_name = "Бэтмен. Долгий Хэллоуин"
comic_is_read = True
total_issues = "13"
collected_issues = "7"
comic_rating = "5"

print("Дата проверки:", date.today())
print("Комикс:", comic_name)
print(get_reading_status(comic_is_read))
print(get_collection_progress(total_issues, collected_issues))
print(get_rating_message(comic_rating))
