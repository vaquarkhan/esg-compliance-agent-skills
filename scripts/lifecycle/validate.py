#!/usr/bin/env python3
"""Validate build artifacts and attestation envelopes (/validate)."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from scripts.lifecycle.common import ARTIFACTS_DIR, attach, ensure_artifacts_dir, load_json, write_json

ROOT = Path(__file__).resolve().parents[2]
REQUIRED_KEYS = ("assurance_status", "attestation", "human_review_required")
PENDING = "pending_sustainability_assurance_sign_off"


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing: {path}"]
    data = load_json(path)
    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append(f"{path.name}: missing {key}")
    if data.get("assurance_status") != PENDING:
        errors.append(f"{path.name}: assurance_status must be {PENDING!r}")
    att = data.get("attestation", {})
    if att.get("assurance_status") != PENDING:
        errors.append(f"{path.name}: attestation.assurance_status must be {PENDING!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate lifecycle build artifacts")
    parser.add_argument("--build-dir", type=Path, default=ARTIFACTS_DIR / "build")
    parser.add_argument("--output", type=Path, default=ensure_artifacts_dir() / "validation_report.json")
    args = parser.parse_args()

    targets = [
        args.build_dir / "ghg_inventory.json",
        args.build_dir / "mapping_matrix.json",
        args.build_dir / "build_manifest.json",
    ]
    all_errors: list[str] = []
    checked: list[str] = []
    for path in targets:
        all_errors.extend(validate_file(path))
        if path.exists():
            checked.append(str(path.relative_to(ROOT)))

    report = attach(
        {
            "lifecycle": "validate",
            "validated_at": datetime.now(timezone.utc).isoformat(),
            "passed": len(all_errors) == 0,
            "checked": checked,
            "errors": all_errors,
        },
        artifact_type="validation_report",
    )
    write_json(args.output, report)

    if all_errors:
        print("\n".join(all_errors), file=sys.stderr)
        print(f"Validation FAILED - report at {args.output}", file=sys.stderr)
        return 1

    print(f"Validation passed - report at {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
