"""MCP server: taxonomy-criteria-server — SSE transport via FastMCP."""

from __future__ import annotations

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "mcp"))
sys.path.insert(0, str(ROOT / "mcp" / "common"))
from kb_loader import load_json  # noqa: E402
from sdk_loader import get_fastmcp  # noqa: E402

KB = ROOT / "knowledge_base"

mcp = get_fastmcp(
    name="taxonomy-criteria-server",
    host=os.getenv("MCP_HOST", "0.0.0.0"),
    port=int(os.getenv("MCP_PORT", "8003")),
)


@mcp.tool()
def get_tsc_for_activity(nace_code: str) -> dict[str, Any]:
    """Return Technical Screening Criteria for a NACE activity."""
    data = load_json("taxonomy_criteria.json")
    matches = [a for a in data["activities"] if a["nace"] == nace_code]
    if not matches:
        return {"error": f"No TSC for NACE {nace_code}"}
    return {"activity": matches[0]}


@mcp.tool()
def get_dnsh_criteria(nace_code: str, objective: str = "") -> dict[str, Any]:
    """Return Do No Significant Harm criteria for an activity."""
    data = load_json("taxonomy_criteria.json")
    matches = [a for a in data["activities"] if a["nace"] == nace_code]
    if not matches:
        return {"error": f"No DNSH data for NACE {nace_code}"}
    activity = matches[0]
    dnsh = activity.get("dnsh", [])
    if objective:
        dnsh = [d for d in dnsh if objective.lower() in d.lower()]
    return {"nace_code": nace_code, "dnsh_criteria": dnsh}


@mcp.tool()
def check_nace_eligibility(nace_code: str, revenue_pct: float, capex_pct: float, opex_pct: float) -> dict[str, Any]:
    """Check mock taxonomy alignment KPI thresholds."""
    aligned = revenue_pct >= 0 or capex_pct >= 0  # stub: always evaluate
    return {
        "nace_code": nace_code,
        "kpis": {"revenue_pct": revenue_pct, "capex_pct": capex_pct, "opex_pct": opex_pct},
        "eligible_for_reporting": True,
        "requires_human_review": True,
        "note": "Mock logic — SME must confirm substantial contribution and DNSH",
    }


@mcp.tool()
def get_minimum_safeguards() -> dict[str, Any]:
    """Return EU Taxonomy minimum safeguards list."""
    data = load_json("taxonomy_criteria.json")
    return {"minimum_safeguards": data["minimum_safeguards"]}


@mcp.tool()
def get_objective_thresholds(objective: str) -> dict[str, Any]:
    """Return environmental objective thresholds."""
    data = load_json("taxonomy_criteria.json")
    thresholds = data["objective_thresholds"].get(objective, {"note": "See delegated act annex"})
    return {"objective": objective, "thresholds": thresholds}



def main() -> None:
    """Run MCP server with SSE transport via FastAPI + Uvicorn."""
    sys.path.insert(0, str(ROOT / "mcp"))
    from fastapi_runner import run_fastapi_sse  # noqa: E402

    run_fastapi_sse(mcp, title="taxonomy-criteria-server")


if __name__ == "__main__":
    main()
