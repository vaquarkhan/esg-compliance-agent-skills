#!/usr/bin/env python3
"""Build GHG inventory from activity CSV using knowledge base emission factors."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "mcp" / "common"))

from emissions_logic import get_emission_factor, get_grid_factors_by_country  # noqa: E402
from orchestration.attestation import attach_attestation  # noqa: E402

ACTIVITY_CSV = Path(__file__).resolve().parent / "activity_data.csv"
OUTPUT = Path(__file__).resolve().parent / "ghg_inventory.json"
PROVENANCE = Path(__file__).resolve().parent / "factor_provenance.json"
KB = ROOT / "knowledge_base" / "emission_factors.json"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    scope_1 = 0.0
    scope_2 = 0.0
    scope_3 = 0.0
    provenance: list[dict] = []

    with ACTIVITY_CSV.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            scope = row["scope"]
            activity = float(row["activity"])
            source = row["factor_source"]
            factor_key = row["factor_activity"]
            country = row.get("country_code", "")

            if scope == "scope_2_location" and country:
                result = get_grid_factors_by_country(country)
                factor = result["grid_factor"]["factor"]
                emissions_kg = activity * factor
                record = {"type": "grid", "country": country, "result": result}
            else:
                result = get_emission_factor(source, factor_key)
                factor = result["factor"]["factor"]
                emissions_kg = activity * factor
                record = {"type": "activity", "result": result}

            tco2e = emissions_kg / 1000.0
            if scope.startswith("scope_1"):
                scope_1 += tco2e
            elif scope.startswith("scope_2"):
                scope_2 += tco2e
            else:
                scope_3 += tco2e

            provenance.append(
                attach_attestation(
                    {
                        "line": row,
                        "emissions_tCO2e": round(tco2e, 4),
                        "factor_record": record,
                        "computed_at": datetime.now(timezone.utc).isoformat(),
                    },
                    artifact_type="factor_provenance_line",
                )
            )

    kb_meta = json.loads(KB.read_text(encoding="utf-8"))["metadata"]
    inventory = attach_attestation(
        {
            "reporting_period": "FY2025",
            "boundary": "operational_control",
            "scopes": {
                "scope_1_tCO2e": round(scope_1, 4),
                "scope_2_location_tCO2e": round(scope_2, 4),
                "scope_3_tCO2e": round(scope_3, 4),
                "total_tCO2e": round(scope_1 + scope_2 + scope_3, 4),
            },
            "gwp_standard": "IPCC AR6 GWP100",
            "factor_source_metadata": kb_meta,
            "activity_file_sha256": sha256_file(ACTIVITY_CSV),
        },
        artifact_type="ghg_inventory",
    )

    provenance_envelope = attach_attestation(
        {"lines": provenance, "line_count": len(provenance)},
        artifact_type="factor_provenance",
    )

    OUTPUT.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
    PROVENANCE.write_text(json.dumps(provenance_envelope, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} (total {inventory['scopes']['total_tCO2e']} tCO2e)")
    print(f"Wrote {PROVENANCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
