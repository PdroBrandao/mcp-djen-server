from app.service import search_intimations

def test_intimations_TJSP():
    name = "PEDRO BRANDÃO"
    date_start = "2025-08-06"
    date_end = "2025-08-06"
    court = "TJSP"

    result = search_intimations(name=name, date_start=date_start, date_end=date_end, court=court)
    assert result == []

def test_intimations_TJMG():
    name = "PEDRO BRANDÃO"
    date_start = "2025-08-06"
    date_end = "2025-08-06"
    court = "TJMG"

    result = search_intimations(name=name, date_start=date_start, date_end=date_end, court=court)
    assert len(result) == 3
