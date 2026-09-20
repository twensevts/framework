def add_series(series_list: list[dict], name: str) -> None:
    """Добавление новой серии комиксов."""
    new_id = len(series_list) + 1
    series_list.append({"id": new_id, "name": name})

def get_all_series(series_list: list[dict]) -> list[dict]:
    """Возвращает список всех серий."""
    return series_list