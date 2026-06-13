#!/usr/bin/env python3
"""Produce CSRD E1 mapping matrix stub from local knowledge base."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KB = ROOT / "knowledge_base" / "esrs_data_points.json"
OUTPUT = Path(__file__).resolve().parent / "mapping_matrix.json"


def main() -> int:
    catalog = json.loads(KB.read_text(encoding="utf-8"))
    matrix = {
        "framework": "CSRD",
        "topic": catalog["standard"],
        "data_points": catalog["data_points"],
        "mappings": [],
        "human_review_required": True,
        "note": "Populate mappings from source systems — stub output",
        "source": catalog.get("source"),
    }
    OUTPUT.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(matrix['data_points'])} ESRS E1 datapoints")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
