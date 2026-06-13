#!/usr/bin/env python3
"""Syntax smoke check for core Python modules."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = [
    ROOT / "agent.py",
    ROOT / "redaction.py",
    ROOT / "orchestration",
    ROOT / "mcp",
    ROOT / "examples",
    ROOT / "scripts",
    ROOT / "compliance_tests",
]


def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        errors.append(f"{path}: {exc}")
    return errors


def main() -> int:
    errors: list[str] = []
    for target in TARGETS:
        if target.is_file():
            errors.extend(check_file(target))
        else:
            for py in target.rglob("*.py"):
                errors.extend(check_file(py))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Syntax OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
