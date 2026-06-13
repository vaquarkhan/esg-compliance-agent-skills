#!/usr/bin/env python3
"""Validate SME provenance footers on reference checklists."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "references"
REQUIRED = ("## Authoritative sources", "## Provenance")


def main() -> int:
    if not REFS.exists():
        print("No references/ directory — skipping")
        return 0
    errors: list[str] = []
    for path in REFS.glob("*checklist*.md"):
        text = path.read_text(encoding="utf-8")
        for section in REQUIRED:
            if section not in text:
                errors.append(f"{path.name}: missing {section}")
        if not re.search(r"\*\*Last reviewed\*\*", text):
            errors.append(f"{path.name}: missing Last reviewed row")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated {len(list(REFS.glob('*checklist*.md')))} checklist(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
