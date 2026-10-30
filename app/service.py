"""Court-notification queries shared by the REST API and the MCP server.

The data below is an in-memory sample. Nothing in this module calls the DJEN
API. ``app/adapter.py`` (``DJENAdapter``) knows how to reach
``https://comunicaapi.pje.jus.br``, but the REST routes and the MCP tools do
not import it.
"""

import time
from datetime import datetime
from typing import Any, Optional


class InvalidRequest(Exception):
    """Caller input that the HTTP layer maps to 400 and MCP maps to a tool error."""


class NotFound(Exception):
    """A case number that is not in the sample set."""


MOCK_INTIMATIONS: list[dict[str, Any]] = [
    {
        "date": "2025-08-06",
        "court": "TJMG",
        "lawyer_name": "PEDRO BRANDÃO",
        "oab": "123456/MG",
        "case_number": "1234567-89.2024.8.13.0001",
        "type": "TOMAR_CIÊNCIA",
        "summary": "Intimação para ciência de despacho proferido em 05/08/2025",
        "url": "https://www.tjmg.jus.br/djen/123",
        "deadline": "15 days",
        "actions": ["MANIFESTAR_SE", "CALCULAR_PRAZO"],
    },
    {
        "date": "2025-08-06",
        "court": "TJMG",
        "lawyer_name": "PEDRO BRANDÃO",
        "oab": "123456/MG",
        "case_number": "1234567-89.2024.8.13.0002",
        "type": "MANIFESTAR_SE",
        "summary": "Intimação para manifestar sobre impugnação de cálculos",
        "url": "https://www.tjmg.jus.br/djen/124",
        "deadline": "5 days",
        "actions": ["MANIFESTAR_SE", "PREPARAR_IMPUGNACAO"],
    },
    {
        "date": "2025-08-06",
        "court": "TJMG",
        "lawyer_name": "PEDRO BRANDÃO",
        "oab": "123456/MG",
        "case_number": "1234567-89.2024.8.13.0003",
        "type": "CITAR",
        "summary": "Citação para audiência de conciliação",
        "url": "https://www.tjmg.jus.br/djen/125",
        "deadline": "10 days",
        "actions": ["PREPARAR_DOCUMENTOS", "AGENDAR_AUDIENCIA"],
    },
]

COURTS: list[dict[str, str]] = [
    {"code": "TJMG", "name": "Tribunal de Justiça de Minas Gerais"},
    {"code": "TJSP", "name": "Tribunal de Justiça de São Paulo"},
    {"code": "TJRJ", "name": "Tribunal de Justiça do Rio de Janeiro"},
    {"code": "TRT3", "name": "Tribunal Regional do Trabalho 3ª Região"},
]


def _require_iso_date(value: str) -> None:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise InvalidRequest("Invalid date format. Use YYYY-MM-DD") from exc


def search_intimations(
    name: str,
    date_start: str,
    date_end: str,
    oab: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Filter the sample notifications by name, date range, and optional OAB."""
    _require_iso_date(date_start)
    _require_iso_date(date_end)

    # Kept so the REST response time matches the previous handler.
    time.sleep(0.5)

    filtered = [
        item
        for item in MOCK_INTIMATIONS
        if date_start <= item["date"] <= date_end
    ]

    if name:
        filtered = [
            item for item in filtered if name.upper() in item["lawyer_name"].upper()
        ]

    if oab:
        filtered = [item for item in filtered if oab.upper() in item["oab"].upper()]

    return filtered


def get_case_by_number(case_number: str) -> dict[str, Any]:
    """Return one sample notification, or raise ``NotFound``."""
    case = next(
        (item for item in MOCK_INTIMATIONS if item["case_number"] == case_number),
        None,
    )
    if case is None:
        raise NotFound(f"Case {case_number} not found")
    return case


def list_courts() -> list[dict[str, str]]:
    """Return the fixed list of court codes exposed by the API."""
    return [dict(court) for court in COURTS]
