from comics import add_comic, mark_as_read

def test_add_comic():
    comics_list = []
    add_comic(comics_list, 1, 5)
    
    assert len(comics_list) == 1
    assert comics_list[0]["issue"] == 5
    assert comics_list[0]["is_read"] == False

def test_mark_as_read():
    comics_list = [{"id": 1, "series_id": 1, "issue": 5, "is_read": False}]
    result = mark_as_read(comics_list, 1)
    
    assert result == True
    assert comics_list[0]["is_read"] == True