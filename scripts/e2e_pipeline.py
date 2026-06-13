#!/usr/bin/env python3
"""Run full lifecycle E2E: /spec → /plan → /build → /validate → /review → /ship."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
STEPS = [
    "scripts.lifecycle.spec",
    "scripts.lifecycle.plan",
    "scripts.lifecycle.build",
    "scripts.lifecycle.validate",
    "scripts.lifecycle.review",
    "scripts.lifecycle.ship",
]


def main() -> int:
    print("=== ESG lifecycle E2E pipeline ===")
    for module in STEPS:
        name = module.rsplit(".", 1)[-1]
        print(f"\n--- /{name} ---")
        result = subprocess.run([PYTHON, "-m", module], cwd=str(ROOT))
        if result.returncode != 0:
            print(f"E2E failed at /{name}", file=sys.stderr)
            return result.returncode
    print("\n=== E2E pipeline complete ===")
    print("Artifacts: artifacts/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
