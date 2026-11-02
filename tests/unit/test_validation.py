import pytest

from app.service import InvalidRequest, search_intimations


def test_invalid_date_raises(golden):
    bad_date = golden["invalid_dates"][0]
    with pytest.raises(InvalidRequest, match="Invalid date format"):
        search_intimations("PEDRO BRANDÃO", bad_date, "2025-08-06")
