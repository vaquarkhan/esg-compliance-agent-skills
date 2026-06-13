"""Load knowledge base JSON stubs."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KB = ROOT / "knowledge_base"


@lru_cache(maxsize=8)
def load_json(name: str) -> dict:
    path = KB / name
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)
