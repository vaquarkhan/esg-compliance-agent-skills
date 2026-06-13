#!/usr/bin/env python3
"""Produce CSRD E1 mapping matrix stub from local knowledge base."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KB = ROOT / "knowledge_base" / "esrs_data_points.json"
OUTPUT = Path(__file__).resolve().parent / "mapping_matrix.json"

# Import attestation helper without pulling MCP stack
import sys

sys.path.insert(0, str(ROOT))
from orchestration.attestation import attach_attestation


def main() -> int:
    catalog = json.loads(KB.read_text(encoding="utf-8"))
    matrix = attach_attestation(
        {
            "framework": "CSRD",
            "topic": catalog["standard"],
            "data_points": catalog["data_points"],
            "mappings": [],
            "note": "Populate mappings from source systems — stub output",
            "source": catalog.get("source"),
        },
        artifact_type="csrd_e1_mapping_matrix",
    )
    OUTPUT.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(matrix['data_points'])} ESRS E1 datapoints")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
