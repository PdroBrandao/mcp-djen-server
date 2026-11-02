import pytest

from app.service import InvalidRequest, search_intimations


def test_invalid_date_raises(golden):
    bad_date = golden["invalid_dates"][0]
    with pytest.raises(InvalidRequest, match="Invalid date format"):
        search_intimations("PEDRO BRANDÃO", bad_date, "2025-08-06")


@pytest.mark.skip(reason="TODO(STUDENT) desafio 2: cubra NotFound para processo ausente. Remova este skip ao implementar.")
def test_unknown_case_raises_not_found(golden):
    # TODO(STUDENT): o número em golden["missing_case"] deve levantar NotFound
    # e a mensagem deve identificar esse número.
    pytest.fail("TODO(STUDENT): implementar")
