"""End-to-end lifecycle pipeline tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("yaml")

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
PENDING = "pending_sustainability_assurance_sign_off"


@pytest.fixture(scope="module")
def e2e_artifacts() -> Path:
    result = subprocess.run([PYTHON, str(ROOT / "scripts" / "e2e_pipeline.py")], cwd=str(ROOT))
    assert result.returncode == 0, "e2e_pipeline.py failed"
    return ROOT / "artifacts"


def test_scope_has_attestation(e2e_artifacts: Path):
    scope = json.loads((e2e_artifacts / "scope.json").read_text(encoding="utf-8"))
    assert scope["assurance_status"] == PENDING
    assert scope["attestation"]["human_review_required"] is True


def test_build_outputs_attested(e2e_artifacts: Path):
    for name in ("ghg_inventory.json", "mapping_matrix.json", "build_manifest.json"):
        data = json.loads((e2e_artifacts / "build" / name).read_text(encoding="utf-8"))
        assert data["assurance_status"] == PENDING


def test_filing_package_staged_pending_token(e2e_artifacts: Path):
    package = json.loads((e2e_artifacts / "filing_package.json").read_text(encoding="utf-8"))
    assert package["ship_status"] == "staged_pending_human_approval"
    assert package["submission"]["status"] == "rejected"
    assert package["assurance_status"] == PENDING
