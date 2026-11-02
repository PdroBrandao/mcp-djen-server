from app.service import list_courts


def test_court_catalog_size():
    assert len(list_courts()) == 4
