def add_comic(comics_list: list[dict], series_id: int, issue: int) -> None:
    """Добавление конкретного выпуска (тома) к серии."""
    new_id = len(comics_list) + 1
    comics_list.append({
        "id": new_id,
        "series_id": series_id,
        "issue": issue,
        "is_read": False
    })

def mark_as_read(comics_list: list[dict], comic_id: int) -> bool:
    """Смена статуса комикса на 'прочитано'."""
    for c in comics_list:
        if c["id"] == comic_id:
            c["is_read"] = True
            return True
    return False