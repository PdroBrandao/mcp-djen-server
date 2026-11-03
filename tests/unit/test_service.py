
from tkinter.constants import NO
import pytest
from app.service import search_intimations, InvalidRequest, list_courts, get_case_by_number, NotFound

# search_intimations
# 1. HAPPY PATH "id": "INPUT_OK"
def test_search_intimations_ok(golden):
    item_golden = next(s for s in golden["search_intimations"] if s["id"] == "INPUT_OK")
    r = search_intimations(**item_golden["input"])
    actual = [i["case_number"] for i in r]
    assert actual == item_golden["expected_case_numbers"]
    assert all (i["court"] == item_golden["input"]["court"] for i in r)

## ++ "id": "MISMATCH_COURT"
def test_search_intimations_mismatch_court(golden):
    item_golden = next(s for s in golden["search_intimations"] if s["id"] == "MISMATCH_COURT")
    r = search_intimations(**item_golden["input"])
    assert len(r) == 0

## ++ "id": "MISMATCH_OAB"
def test_search_intimations_mismatch_oab(golden):
    item_golden = next(s for s in golden["search_intimations"]  if s["id"] == "MISMATCH_OAB")
    r = search_intimations(**item_golden["input"])
    assert len(r) == 0

## "id": "NAME_LOWERCASE"
def test_search_intimations_name_lowercase(golden):
    item_golden = next(s for s in golden["search_intimations"] if s["id"] == "NAME_LOWERCASE")
    r = search_intimations(**item_golden["input"])
    a = [i["case_number"] for i in r]
    assert item_golden["expected_case_numbers"] == a


# "id": "NAME_DOES_NOT_EXIST",
def test_search_intimations_name_does_not_exist(golden):
    item_golden = next(s for s in golden["search_intimations"] if s["id"] == "NAME_DOES_NOT_EXIST")
    r = search_intimations(**item_golden["input"])
    assert len(r) == 0


# "id": "INVALID_DATE_START",
def test_search_intimations_invalid_date_start(golden):
    with pytest.raises(InvalidRequest, match="Invalid date format. Use YYYY-MM-DD"):
        item_golden = next(s for s in golden["search_intimations"] if s["id"]=="INVALID_DATE_START")
        search_intimations(**item_golden["input"])

# "id": "INVALID_DATE_END",
def test_search_intimations_invalid_date_end(golden):
    with pytest.raises(InvalidRequest, match="Invalid date format. Use YYYY-MM-DD"):
        item_golden = next(s for s in golden["search_intimations"] if s["id"]=="INVALID_DATE_END")
        search_intimations(**item_golden["input"])

# "id": "INVALID_RANGE_DATE",
def test_search_intimations_invalid_range_date(golden):
    with pytest.raises(InvalidRequest, match="Invalid range date. Date end needs to be greater than Date start"):
        item_golden = next(s for s in golden["search_intimations"] if s["id"]=="INVALID_RANGE_DATE")
        search_intimations(**item_golden["input"])


# get_case_by_number
# "id": "GET_CASE_BY_NUMBER_TOMAR_CIÊNCIA",
def test_get_case_by_number_tomar_ciencia(golden):
    item_golden = next(s for s in golden["get_case_by_number"] if s["id"] == "GET_CASE_BY_NUMBER_TOMAR_CIÊNCIA")
    r = get_case_by_number(item_golden["input"])
    assert item_golden["expected_type"] == r["type"] 

# "id": "GET_CASE_BY_NUMBER_MANIFESTAR_SE",
def test_get_case_by_number_manifestar(golden):
    item_golden = next(s for s in golden["get_case_by_number"] if s["id"] == "GET_CASE_BY_NUMBER_MANIFESTAR_SE")
    r = get_case_by_number(item_golden["input"])
    assert item_golden["expected_type"] == r["type"] 

# "id": "GET_CASE_BY_NUMBER_CITAR",
def test_get_case_by_number_citar(golden):
    item_golden = next(s for s in golden["get_case_by_number"] if s["id"] == "GET_CASE_BY_NUMBER_CITAR")
    r = get_case_by_number(item_golden["input"])
    assert item_golden["expected_type"] == r["type"] 

# "id": "GET_CASE_BY_NUMBER_NOT_FOUND",
def test_get_case_by_number_not_found(golden):
    with pytest.raises(NotFound):
        item_golden = next(s for s in golden["get_case_by_number"] if s["id"] == "GET_CASE_BY_NUMBER_NOT_FOUND")
        get_case_by_number(item_golden["input"])


# 7. HAPPY PATH
@pytest.mark.parametrize("index, code, name",[
    (0, "TJMG", "Tribunal de Justiça de Minas Gerais"),
    (1, "TJSP", "Tribunal de Justiça de São Paulo"),
    (2, "TJRJ", "Tribunal de Justiça do Rio de Janeiro"),
    (3, "TRT3", "Tribunal Regional do Trabalho 3ª Região"),
])
def test_list_courts_success(index, code, name):
    result = list_courts()
    item = result[index]
    assert code == item["code"]
    assert name == item["name"]


