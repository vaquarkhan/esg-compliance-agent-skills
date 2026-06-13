#!/usr/bin/env python3
"""Validate registry/assets.json paths exist."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "registry" / "assets.json"


def collect_paths(data: dict) -> list[tuple[str, str]]:
    paths: list[tuple[str, str]] = []
    for item in data.get("templates", []):
        paths.append(("templates", item["path"]))
    for item in data.get("starter_packs", []):
        paths.append(("starter_packs", item["path"]))
    for item in data.get("examples", []):
        paths.append(("examples", item["path"]))
    for item in data.get("mcp_servers", []):
        paths.append(("mcp_servers", item if isinstance(item, str) else item["path"]))
    for item in data.get("plugin_packages", []):
        paths.append(("plugin_packages", item["path"]))
    for key in ("presets", "references", "agents", "skills", "knowledge_base"):
        for p in data.get(key, []):
            rel = p if isinstance(p, str) else p.get("path", "")
            if rel:
                paths.append((key, rel))
    return paths


def main() -> int:
    data = json.loads(ASSETS.read_text(encoding="utf-8"))
    missing: list[str] = []
    for section, rel in collect_paths(data):
        full = ROOT / rel
        if not full.exists():
            missing.append(f"[{section}] {rel}")
            print(f"MISSING {rel}")
        else:
            print(f"OK {rel}")
    print(f"\nChecked paths, {len(missing)} missing")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
