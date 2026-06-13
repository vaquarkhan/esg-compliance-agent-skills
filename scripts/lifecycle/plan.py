#!/usr/bin/env python3
"""Generate plan.md from scope.json (/plan)."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from scripts.lifecycle.common import ARTIFACTS_DIR, attach, ensure_artifacts_dir, load_json, write_json

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate plan from scope.json")
    parser.add_argument("--scope", type=Path, default=ARTIFACTS_DIR / "scope.json")
    parser.add_argument("--output-md", type=Path, default=ensure_artifacts_dir() / "plan.md")
    parser.add_argument("--output-json", type=Path, default=ensure_artifacts_dir() / "plan.json")
    args = parser.parse_args()

    if not args.scope.exists():
        print(f"Missing scope: {args.scope}. Run scripts/lifecycle/spec.py first.", file=sys.stderr)
        return 1

    scope = load_json(args.scope)
    frameworks = scope.get("frameworks", ["CSRD"])
    period = scope.get("reporting_period", "FY2025")

    plan_body = f"""# ESG compliance plan — {period}

Generated: {datetime.now(timezone.utc).isoformat()}

## Scope summary

- Frameworks: {", ".join(frameworks)}
- Jurisdictions: {", ".join(scope.get("jurisdictions", [])) or "TBD"}
- Entity: {scope.get("entity") or "TBD"}

## Work breakdown

| Phase | Skill | MCP servers | Output |
| --- | --- | --- | --- |
| /spec | data-ingestion-validation | regulatory-db-server | scope.json |
| /build | ghg-emissions-calculation | emissions-factor-server | ghg_inventory.json |
| /build | data-ingestion-validation | regulatory-db-server | mapping_matrix.json |
| /validate | audit-trail-reporting | filing-submission-server | validation_report.json |
| /review | — | — | review_record.json (human SME) |
| /ship | — | filing-submission-server | filing_package.json (human token) |

## Assurance

All outputs carry `assurance_status: pending_sustainability_assurance_sign_off` until sustainability assuror sign-off.
"""
    args.output_md.write_text(plan_body + "\n", encoding="utf-8")

    plan_json = attach(
        {
            "lifecycle": "plan",
            "reporting_period": period,
            "frameworks": frameworks,
            "wbs": [
                {"phase": "build", "skill": "ghg-emissions-calculation", "example": "examples/ghg-inventory"},
                {"phase": "build", "skill": "data-ingestion-validation", "example": "examples/csrd-e1-mapping"},
            ],
            "plan_md": str(args.output_md.relative_to(ROOT)),
        },
        artifact_type="plan",
    )
    write_json(args.output_json, plan_json)
    print(f"Wrote {args.output_md} and {args.output_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
