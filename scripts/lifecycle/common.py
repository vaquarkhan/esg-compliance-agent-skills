"""Shared lifecycle artifact paths and helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = ROOT / "artifacts"
DEFAULT_SCOPE_TEMPLATE = ROOT / "templates" / "csrd-scope.yaml"


def ensure_artifacts_dir() -> Path:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    return ARTIFACTS_DIR


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def attach(payload: dict[str, Any], *, artifact_type: str) -> dict[str, Any]:
    import sys

    sys.path.insert(0, str(ROOT))
    from orchestration.attestation import attach_attestation

    return attach_attestation(payload, artifact_type=artifact_type)
