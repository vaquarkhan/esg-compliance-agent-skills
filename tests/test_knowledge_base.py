"""Knowledge base stub tests."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_emission_factors_loads():
    data = json.loads((ROOT / "knowledge_base" / "emission_factors.json").read_text())
    assert "factors" in data
    assert "gwp" in data


def test_taxonomy_criteria_loads():
    data = json.loads((ROOT / "knowledge_base" / "taxonomy_criteria.json").read_text())
    assert "activities" in data
