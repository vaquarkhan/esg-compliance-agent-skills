"""Pure emission factor logic — no FastMCP import required."""

from __future__ import annotations

from typing import Any

from kb_loader import load_json


def get_emission_factor(source: str, activity: str) -> dict[str, Any]:
    data = load_json("emission_factors.json")
    matches = [
        f
        for f in data["factors"]
        if f["source"].lower() == source.lower() and activity.lower() in f["activity"].lower()
    ]
    if not matches:
        return {"error": "Factor not found", "source": source, "activity": activity}
    return {"factor": matches[0], "metadata": data["metadata"]}


def get_gwp_values(standard: str = "IPCC AR6 GWP100") -> dict[str, Any]:
    data = load_json("emission_factors.json")
    return {"standard": data["gwp"]["standard"], "values": data["gwp"]["values"]}


def get_grid_factors_by_country(country_code: str) -> dict[str, Any]:
    data = load_json("emission_factors.json")
    code = country_code.upper()
    factor = data["grid_factors_by_country"].get(code)
    if not factor:
        return {"error": f"No grid factor for {code}", "available": list(data["grid_factors_by_country"].keys())}
    return {"country_code": code, "grid_factor": factor}
