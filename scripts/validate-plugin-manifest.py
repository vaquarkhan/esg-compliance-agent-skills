#!/usr/bin/env python3
"""Validate VS Code and JetBrains plugin manifests."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VSCODE = ROOT / "vscode-extension" / "package.json"
JETBRAINS = ROOT / "jetbrains-plugin" / "gradle.properties"


def main() -> int:
    errors: list[str] = []
    if not VSCODE.exists():
        errors.append("vscode-extension/package.json missing")
    else:
        pkg = json.loads(VSCODE.read_text(encoding="utf-8"))
        for key in ("name", "displayName", "version", "publisher"):
            if key not in pkg:
                errors.append(f"package.json missing {key}")
        print(f"OK vscode-extension {pkg.get('name')} v{pkg.get('version')}")

    if not JETBRAINS.exists():
        errors.append("jetbrains-plugin/gradle.properties missing")
    else:
        text = JETBRAINS.read_text(encoding="utf-8")
        if "pluginVersion=" not in text:
            errors.append("gradle.properties missing pluginVersion")
        print("OK jetbrains-plugin gradle.properties")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
