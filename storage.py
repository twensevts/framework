import json
import os

def load_data(filename: str) -> list[dict]:
    """Чтение данных из json-файла."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_data(filename: str, data: list[dict]) -> None:
    """Запись списка в json-файл."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)