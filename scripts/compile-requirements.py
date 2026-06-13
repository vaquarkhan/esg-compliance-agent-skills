#!/usr/bin/env python3
"""Compile requirements-lock.txt from requirements.in using pip-tools."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    cmd = [
        sys.executable,
        "-m",
        "piptools",
        "compile",
        str(ROOT / "requirements.in"),
        "-o",
        str(ROOT / "requirements-lock.txt"),
        "--strip-extras",
    ]
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
