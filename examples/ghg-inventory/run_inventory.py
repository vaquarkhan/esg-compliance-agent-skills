#!/usr/bin/env python3
"""Build GHG inventory from activity CSV using MCP emission factor server logic."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ACTIVITY_CSV = Path(__file__).resolve().parent / "activity_data.csv"
OUTPUT = Path(__file__).resolve().parent / "ghg_inventory.json"
PROVENANCE = Path(__file__).resolve().parent / "factor_provenance.json"


def _load_server():
    sys.path.insert(0, str(ROOT / "mcp"))
    sys.path.insert(0, str(ROOT / "mcp" / "common"))
    path = ROOT / "mcp" / "emissions-factor-server" / "server.py"
    spec = importlib.util.spec_from_file_location("emissions_server", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    server = _load_server()
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
                result = server.get_grid_factors_by_country(country)
                factor = result["grid_factor"]["factor"]
                unit = result["grid_factor"]["unit"]
                emissions_kg = activity * factor
                record = {"type": "grid", "country": country, "result": result}
            else:
                result = server.get_emission_factor(source, factor_key)
                factor = result["factor"]["factor"]
                unit = result["factor"]["unit"]
                if "kWh" in unit and "MMBtu" not in unit:
                    emissions_kg = activity * factor
                elif "MMBtu" in unit:
                    emissions_kg = activity * factor
                elif "gallon" in unit:
                    emissions_kg = activity * factor
                elif "passenger-km" in unit:
                    emissions_kg = activity * factor
                else:
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
                {
                    "line": row,
                    "emissions_tCO2e": round(tco2e, 4),
                    "factor_record": record,
                    "computed_at": datetime.now(timezone.utc).isoformat(),
                }
            )

    inventory = {
        "reporting_period": "FY2025",
        "boundary": "operational_control",
        "scopes": {
            "scope_1_tCO2e": round(scope_1, 4),
            "scope_2_location_tCO2e": round(scope_2, 4),
            "scope_3_tCO2e": round(scope_3, 4),
            "total_tCO2e": round(scope_1 + scope_2 + scope_3, 4),
        },
        "gwp_standard": "IPCC AR6 GWP100",
        "activity_file_sha256": sha256_file(ACTIVITY_CSV),
        "human_review_required": True,
        "assurance_status": "pending_sustainability_assurance_sign_off",
    }

    OUTPUT.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
    PROVENANCE.write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} (total {inventory['scopes']['total_tCO2e']} tCO2e)")
    print(f"Wrote {PROVENANCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
