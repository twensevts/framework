"""Функции безопасного пользовательского ввода."""


def input_int(prompt: str, minimum: int | None = None) -> int:
    """Запросить целое число с необязательной нижней границей."""
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                raise ValueError
            return value
        except ValueError:
            print("Введите корректное целое число.")


def input_rating(prompt: str) -> int:
    """Запросить оценку от 1 до 5."""
    while True:
        rating = input_int(prompt)
        if 1 <= rating <= 5:
            return rating
        print("Оценка должна находиться в диапазоне от 1 до 5.")
