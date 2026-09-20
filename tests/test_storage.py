from storage import load_data, save_data


def test_save_and_load_data(tmp_path):
    filename = tmp_path / "nested" / "data.json"
    expected = [{"id": 1, "title": "Бэтмен"}]

    save_data(str(filename), expected)

    assert load_data(str(filename)) == expected


def test_invalid_json_returns_empty_list(tmp_path):
    filename = tmp_path / "broken.json"
    filename.write_text("not json", encoding="utf-8")

    assert load_data(str(filename)) == []
