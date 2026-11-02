"""Fixtures shared by unit and integration tests."""

import json
from pathlib import Path

import pytest

GOLDEN_PATH = Path(__file__).parent / "data" / "golden_intimations.json"


@pytest.fixture(autouse=True)
def no_artificial_delay(monkeypatch):
    """Remove the sample-data pause so tests stay fast.

    The service still waits 0.5s in production. This patch only affects pytest.
    """
    monkeypatch.setattr("app.service.time.sleep", lambda *_args, **_kwargs: None)


@pytest.fixture
def golden():
    """Deterministic input/output pairs for regression checks."""
    return json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
