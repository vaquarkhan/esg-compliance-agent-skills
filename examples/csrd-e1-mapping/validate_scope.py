#!/usr/bin/env python3
"""Validate CSRD scope example YAML."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCOPE = ROOT / "templates" / "csrd-scope.yaml"


def main() -> int:
    data = yaml.safe_load(SCOPE.read_text(encoding="utf-8"))
    required = ["entity", "reporting_period", "frameworks", "jurisdictions"]
    missing = [k for k in required if k not in data]
    if missing:
        print(f"Missing keys in csrd-scope.yaml: {missing}", file=sys.stderr)
        return 1
    print("CSRD scope template OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
