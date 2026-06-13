"""MCP server: filing-submission-server — SSE transport via FastMCP."""

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
    name="filing-submission-server",
    host=os.getenv("MCP_HOST", "0.0.0.0"),
    port=int(os.getenv("MCP_PORT", "8004")),
)


@mcp.tool()
def submit_csrd_filing(entity_id: str, package_uri: str, human_approval_token: str) -> dict[str, Any]:
    """Submit CSRD filing stub — requires human approval token."""
    if not human_approval_token or human_approval_token == "PENDING":
        return {"status": "rejected", "reason": "Human approval token required"}
    filing_id = str(uuid.uuid4())
    return {
        "status": "accepted_stub",
        "filing_id": filing_id,
        "entity_id": entity_id,
        "package_uri": package_uri,
        "registry": "ESMA ESEF (mock)",
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def submit_sec_filing(cik: str, form_type: str, package_uri: str, human_approval_token: str) -> dict[str, Any]:
    """Submit SEC filing stub — requires human approval token."""
    if not human_approval_token or human_approval_token == "PENDING":
        return {"status": "rejected", "reason": "Human approval token required"}
    return {
        "status": "accepted_stub",
        "accession_number": f"0000320193-{datetime.now(timezone.utc).strftime('%y%m%d')}-000001",
        "cik": cik,
        "form_type": form_type,
        "package_uri": package_uri,
    }


@mcp.tool()
def validate_xbrl_tagging(instance_path: str, taxonomy: str = "ESRS") -> dict[str, Any]:
    """Validate XBRL tagging (mock validation)."""
    errors = []
    if not instance_path.endswith((".xhtml", ".xml", ".zip")):
        errors.append("Invalid instance extension")
    return {
        "instance_path": instance_path,
        "taxonomy": taxonomy,
        "valid": len(errors) == 0,
        "errors": errors,
        "facts_checked": 42,
    }


@mcp.tool()
def get_filing_status(filing_id: str) -> dict[str, Any]:
    """Return mock filing status."""
    return {"filing_id": filing_id, "status": "processing", "last_updated": datetime.now(timezone.utc).isoformat()}


@mcp.tool()
def generate_esef_package(report_html: str, taxonomy_version: str = "2024") -> dict[str, Any]:
    """Generate mock ESEF package descriptor."""
    package_id = str(uuid.uuid4())
    return {
        "package_id": package_id,
        "taxonomy_version": taxonomy_version,
        "artifacts": ["report.xhtml", "calculations.xml", "labels.json"],
        "report_size_bytes": len(report_html.encode("utf-8")),
        "human_review_required": True,
    }



def main() -> None:
    """Run MCP server with SSE transport via FastAPI + Uvicorn."""
    sys.path.insert(0, str(ROOT / "mcp"))
    from fastapi_runner import run_fastapi_sse  # noqa: E402

    run_fastapi_sse(mcp, title="filing-submission-server")


if __name__ == "__main__":
    main()
