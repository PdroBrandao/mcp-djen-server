import pytest

from app.service import list_courts


def test_court_catalog_size():
    assert len(list_courts()) == 4


@pytest.mark.skip(reason="TODO(STUDENT) desafio 1: conferir códigos e nomes dos tribunais. Remova este skip ao implementar.")
def test_court_codes_match_catalog():
    # TODO(STUDENT): confira código e nome de cada tribunal devolvido por list_courts().
    pytest.fail("TODO(STUDENT): implementar")
