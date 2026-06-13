#!/usr/bin/env python3
"""Sync VERSION to package manifests."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

VSCODE = ROOT / "vscode-extension" / "package.json"
GRADLE = ROOT / "jetbrains-plugin" / "gradle.properties"
REGISTRY = ROOT / "registry" / "assets.json"
CITATION = ROOT / "CITATION.cff"
PYPROJECT = ROOT / "pyproject.toml"


def main() -> None:
    if VSCODE.exists():
        pkg = json.loads(VSCODE.read_text(encoding="utf-8"))
        pkg["version"] = VERSION
        VSCODE.write_text(json.dumps(pkg, indent=2) + "\n", encoding="utf-8")
        print(f"Updated {VSCODE}")

    if GRADLE.exists():
        text = GRADLE.read_text(encoding="utf-8")
        text = re.sub(r"pluginVersion=.*", f"pluginVersion={VERSION}", text)
        GRADLE.write_text(text, encoding="utf-8")
        print(f"Updated {GRADLE}")

    if REGISTRY.exists():
        reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
        reg["version"] = VERSION
        REGISTRY.write_text(json.dumps(reg, indent=2) + "\n", encoding="utf-8")
        print(f"Updated {REGISTRY}")

    if CITATION.exists():
        text = CITATION.read_text(encoding="utf-8")
        text = re.sub(r"^version: .+$", f"version: {VERSION}", text, flags=re.M)
        CITATION.write_text(text, encoding="utf-8")
        print(f"Updated {CITATION}")

    if PYPROJECT.exists():
        text = PYPROJECT.read_text(encoding="utf-8")
        text = re.sub(r'^version = ".*"$', f'version = "{VERSION}"', text, flags=re.M)
        PYPROJECT.write_text(text, encoding="utf-8")
        print(f"Updated {PYPROJECT}")

    print(f"Synced version {VERSION}")


if __name__ == "__main__":
    main()
