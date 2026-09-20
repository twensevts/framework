from series import add_series

def test_add_series():
    series_list = []
    add_series(series_list, "Бэтмен")
    
    assert len(series_list) == 1
    assert series_list[0]["name"] == "Бэтмен"