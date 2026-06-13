#!/usr/bin/env python3
"""Validate attestation envelopes on filing-bound JSON artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PENDING = "pending_sustainability_assurance_sign_off"
REQUIRED = ("assurance_status", "attestation", "human_review_required")

# Committed example outputs + lifecycle artifact paths (when present)
DEFAULT_PATHS = [
    ROOT / "examples" / "ghg-inventory" / "ghg_inventory.json",
    ROOT / "examples" / "csrd-e1-mapping" / "mapping_matrix.json",
    ROOT / "artifacts" / "scope.json",
    ROOT / "artifacts" / "build" / "ghg_inventory.json",
    ROOT / "artifacts" / "build" / "mapping_matrix.json",
    ROOT / "artifacts" / "filing_package.json",
]


def validate_json(path: Path) -> list[str]:
    if not path.exists():
        return []
    errors: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in REQUIRED:
        if key not in data:
            errors.append(f"{path.relative_to(ROOT)}: missing {key}")
    if data.get("assurance_status") != PENDING:
        errors.append(f"{path.relative_to(ROOT)}: assurance_status must be {PENDING!r}")
    att = data.get("attestation", {})
    if not att.get("assurance_status"):
        errors.append(f"{path.relative_to(ROOT)}: attestation.assurance_status missing")
    return errors


def main() -> int:
    paths = [Path(p) for p in sys.argv[1:]] if len(sys.argv) > 1 else DEFAULT_PATHS
    checked = [p for p in paths if p.exists()]
    if not checked:
        print("No artifact paths to validate (run e2e_pipeline.py first for full set)")
        return 0

    errors: list[str] = []
    for path in checked:
        errors.extend(validate_json(path))

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"Attestation OK on {len(checked)} artifact(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
