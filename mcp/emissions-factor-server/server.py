"""MCP server: emissions-factor-server — SSE transport via FastMCP."""

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
    name="emissions-factor-server",
    host=os.getenv("MCP_HOST", "0.0.0.0"),
    port=int(os.getenv("MCP_PORT", "8002")),
)


@mcp.tool()
def get_emission_factor(source: str, activity: str) -> dict[str, Any]:
    """Look up emission factor from knowledge base."""
    data = load_json("emission_factors.json")
    matches = [f for f in data["factors"] if f["source"].lower() == source.lower() and activity.lower() in f["activity"].lower()]
    if not matches:
        return {"error": "Factor not found", "source": source, "activity": activity}
    return {"factor": matches[0], "metadata": data["metadata"]}


@mcp.tool()
def list_factor_sources() -> dict[str, Any]:
    """List available emission factor sources."""
    data = load_json("emission_factors.json")
    sources = sorted({f["source"] for f in data["factors"]})
    return {"sources": sources, "metadata": data["metadata"]}


@mcp.tool()
def get_gwp_values(standard: str = "IPCC AR6 GWP100") -> dict[str, Any]:
    """Return GWP values from knowledge base."""
    data = load_json("emission_factors.json")
    return {"standard": data["gwp"]["standard"], "values": data["gwp"]["values"]}


@mcp.tool()
def convert_units(value: float, from_unit: str, to_unit: str, substance: str = "CO2e") -> dict[str, Any]:
    """Convert common GHG units (mock conversion table)."""
    conversions = {
        ("tCO2e", "kgCO2e"): 1000.0,
        ("kgCO2e", "tCO2e"): 0.001,
        ("MMBtu", "kWh"): 293.071,
        ("kWh", "MMBtu"): 0.003412,
    }
    key = (from_unit, to_unit)
    if key not in conversions:
        return {"error": f"Unsupported conversion: {from_unit} -> {to_unit}"}
    converted = value * conversions[key]
    return {"input": value, "from_unit": from_unit, "to_unit": to_unit, "substance": substance, "output": converted}


@mcp.tool()
def get_grid_factors_by_country(country_code: str) -> dict[str, Any]:
    """Return grid emission factors by ISO country code."""
    data = load_json("emission_factors.json")
    code = country_code.upper()
    factor = data["grid_factors_by_country"].get(code)
    if not factor:
        return {"error": f"No grid factor for {code}", "available": list(data["grid_factors_by_country"].keys())}
    return {"country_code": code, "grid_factor": factor}



def main() -> None:
    """Run MCP server with SSE transport via FastAPI + Uvicorn."""
    sys.path.insert(0, str(ROOT / "mcp"))
    from fastapi_runner import run_fastapi_sse  # noqa: E402

    run_fastapi_sse(mcp, title="emissions-factor-server")


if __name__ == "__main__":
    main()
