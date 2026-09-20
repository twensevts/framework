"""Загрузка и сохранение данных проекта в JSON."""

import json
from pathlib import Path


def load_data(filename: str) -> list[dict]:
    """Загрузить список словарей или вернуть пустой список."""
    path = Path(filename)
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return []

    return data if isinstance(data, list) else []


def save_data(filename: str, data: list[dict]) -> None:
    """Сохранить список словарей в JSON-файл."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
