"""MCP server: sanctions-screening-server — SSE transport via FastMCP."""

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
from sdk_loader import get_fastmcp  # noqa: E402

KB = ROOT / "knowledge_base"

mcp = get_fastmcp(
    name="sanctions-screening-server",
    host=os.getenv("MCP_HOST", "0.0.0.0"),
    port=int(os.getenv("MCP_PORT", "8005")),
)


@mcp.tool()
def screen_entity(name: str, country: str = "", identifiers: dict[str, str] | None = None) -> dict[str, Any]:
    """Screen entity against mock sanctions lists."""
    watchlist_hits = []
    high_risk_names = {"example sanctioned corp", "blocked industries ltd"}
    if name.lower() in high_risk_names:
        watchlist_hits.append({"list": "OFAC SDN (mock)", "match_score": 0.92})
    return {
        "entity": name,
        "country": country,
        "identifiers": identifiers or {},
        "hits": watchlist_hits,
        "risk_level": "high" if watchlist_hits else "low",
        "human_review_required": bool(watchlist_hits),
    }


@mcp.tool()
def check_pep_status(name: str, role: str = "") -> dict[str, Any]:
    """Check politically exposed person status (mock)."""
    pep = "minister" in role.lower() or "senator" in role.lower()
    return {"name": name, "role": role, "is_pep": pep, "source": "mock_pep_database"}


@mcp.tool()
def get_sanctions_lists(jurisdiction: str = "GLOBAL") -> dict[str, Any]:
    """List available sanctions lists."""
    lists = {
        "GLOBAL": ["OFAC SDN", "EU Consolidated", "UN Consolidated", "UK OFSI"],
        "US": ["OFAC SDN", "BIS Entity List"],
        "EU": ["EU Consolidated"],
    }
    key = jurisdiction.upper()
    return {"jurisdiction": key, "lists": lists.get(key, lists["GLOBAL"])}


@mcp.tool()
def monitor_entity_changes(entity_id: str, since: str = "") -> dict[str, Any]:
    """Return mock entity change events for ongoing monitoring."""
    return {
        "entity_id": entity_id,
        "since": since or "2026-01-01",
        "changes": [
            {"type": "address_update", "date": "2026-03-15"},
            {"type": "director_change", "date": "2026-04-02"},
        ],
    }


@mcp.tool()
def generate_screening_report(entity_ids: list[str]) -> dict[str, Any]:
    """Generate consolidated screening report."""
    report_id = str(uuid.uuid4())
    return {
        "report_id": report_id,
        "entity_count": len(entity_ids),
        "entities": entity_ids,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {"high_risk": 0, "medium_risk": 0, "low_risk": len(entity_ids)},
    }



def main() -> None:
    """Run MCP server with SSE transport via FastAPI + Uvicorn."""
    sys.path.insert(0, str(ROOT / "mcp"))
    from fastapi_runner import run_fastapi_sse  # noqa: E402

    run_fastapi_sse(mcp, title="sanctions-screening-server")


if __name__ == "__main__":
    main()
