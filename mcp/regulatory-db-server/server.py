"""MCP server: regulatory-db-server — SSE transport via FastMCP."""

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
    name="regulatory-db-server",
    host=os.getenv("MCP_HOST", "0.0.0.0"),
    port=int(os.getenv("MCP_PORT", "8001")),
)


@mcp.tool()
def get_framework_requirements(framework: str, version: str = "latest") -> dict[str, Any]:
    """Return structured requirements for a reporting framework."""
    catalog = {
        "CSRD": {"articles": ["19a", "29a"], "standards": ["ESRS E1", "ESRS S1"], "assurance": "limited_then_reasonable"},
        "SFDR": {"articles": ["6", "8", "9"], "disclosures": ["PAI", "principal_adverse_impacts"]},
        "SEC_CLIMATE": {"rules": ["10-K climate disclosure", "Scope 1/2 material emitters"]},
    }
    key = framework.upper().replace("-", "_").replace(" ", "_")
    if key not in catalog and framework.upper() not in catalog:
        return {"error": f"Unknown framework: {framework}", "supported": list(catalog.keys())}
    data = catalog.get(key) or catalog.get(framework.upper())
    return {"framework": framework, "version": version, "requirements": data, "retrieved_at": _now()}


@mcp.tool()
def get_data_point_definitions(standard: str, topic: str = "") -> dict[str, Any]:
    """Return ESRS/CSRD data point definitions (sample subset)."""
    points = [
        {"id": "E1-1", "name": "Transition plan for climate change mitigation", "datatype": "narrative"},
        {"id": "E1-6", "name": "Gross Scope 1 GHG emissions", "datatype": "monetary/energy", "unit": "tCO2e"},
        {"id": "E1-7", "name": "Gross Scope 2 GHG emissions", "datatype": "monetary/energy", "unit": "tCO2e"},
    ]
    if topic:
        points = [p for p in points if topic.lower() in p["id"].lower() or topic.lower() in p["name"].lower()]
    return {"standard": standard, "data_points": points, "count": len(points)}


@mcp.tool()
def get_deadlines(jurisdiction: str, framework: str, fiscal_year: int) -> dict[str, Any]:
    """Return filing deadlines for jurisdiction and framework."""
    deadlines = {
        ("EU", "CSRD", 2025): {"publish": "2026-06-30", "assurance": "2026-09-30"},
        ("US", "SEC_CLIMATE", 2025): {"publish": "2026-03-31"},
    }
    key = (jurisdiction.upper()[:2] if len(jurisdiction) > 2 else jurisdiction.upper(), framework.upper(), fiscal_year)
    entry = deadlines.get(key, {"publish": "TBD", "note": "Consult official registry"})
    return {"jurisdiction": jurisdiction, "framework": framework, "fiscal_year": fiscal_year, "deadlines": entry}


@mcp.tool()
def get_jurisdiction_rules(jurisdiction: str) -> dict[str, Any]:
    """Return localization and reporting rules by jurisdiction."""
    rules = {
        "EU": {"localization": "GDPR", "language": ["en", "local"], "formats": ["XHTML", "iXBRL"]},
        "IN": {"localization": "DPDP", "data_residency": "sensitive_personal_data", "consent": "explicit"},
        "CN": {"localization": "PIPL", "data_residency": "critical/important_data", "security_assessment": True},
        "SA": {"localization": "PDPL", "data_residency": "personal_data", "cross_border": "adequacy_or_consent"},
    }
    code = jurisdiction.upper()
    return {"jurisdiction": code, "rules": rules.get(code, {"note": "No stub rules; escalate to legal"})}


@mcp.tool()
def search_regulatory_text(query: str, framework: str = "", limit: int = 5) -> dict[str, Any]:
    """Search mock regulatory text snippets."""
    corpus = [
        {"framework": "CSRD", "ref": "ESRS E1.6", "text": "The undertaking shall disclose gross Scope 1 GHG emissions in tonnes of CO2eq."},
        {"framework": "EU Taxonomy", "ref": "Annex I", "text": "Substantial contribution thresholds apply per activity in the delegated acts."},
        {"framework": "SFDR", "ref": "RTS Annex I", "text": "Principal adverse impacts on sustainability factors shall be disclosed."},
    ]
    hits = [c for c in corpus if query.lower() in c["text"].lower() or (framework and framework.lower() in c["framework"].lower())]
    return {"query": query, "results": hits[:limit], "total": len(hits)}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()



def main() -> None:
    """Run MCP server with SSE transport via FastAPI + Uvicorn."""
    sys.path.insert(0, str(ROOT / "mcp"))
    from fastapi_runner import run_fastapi_sse  # noqa: E402

    run_fastapi_sse(mcp, title="regulatory-db-server")


if __name__ == "__main__":
    main()
