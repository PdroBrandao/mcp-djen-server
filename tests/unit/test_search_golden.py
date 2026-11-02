import pytest

from app.service import search_intimations


def _case_numbers(rows):
    return [item["case_number"] for item in rows]


def test_golden_happy_path(golden):
    case = next(item for item in golden["search"] if item["id"] == "pedro_on_sample_day")
    result = search_intimations(**case["input"])
    assert _case_numbers(result) == case["expected_case_numbers"]


@pytest.mark.parametrize("name", ["PEDRO BRANDÃO", "pedro brandão"])
def test_name_match_is_case_insensitive(name):
    result = search_intimations(name, "2025-08-06", "2025-08-06")
    assert len(result) == 3


@pytest.mark.skip(reason="TODO(STUDENT) desafio 3: parametrize os demais casos de busca do golden. Remova este skip ao implementar.")
def test_remaining_golden_cases(golden):
    # TODO(STUDENT): use @pytest.mark.parametrize nos casos de golden["search"]
    # que o teste do caminho feliz ainda não cobre. Compare os números de processo.
    pytest.fail("TODO(STUDENT): implementar")
