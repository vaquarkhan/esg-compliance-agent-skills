"""MCP tool unit tests (local import)."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_server(server_dir: str):
    import sys

    path = ROOT / "mcp" / server_dir / "server.py"
    sys.path.insert(0, str(ROOT / "mcp"))
    spec = importlib.util.spec_from_file_location(server_dir, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_regulatory_framework_requirements():
    mod = _load_server("regulatory-db-server")
    result = mod.get_framework_requirements("CSRD")
    assert "requirements" in result


def test_emissions_gwp():
    mod = _load_server("emissions-factor-server")
    result = mod.get_gwp_values()
    assert "values" in result
    assert result["values"]["CO2"] == 1.0


def test_filing_requires_approval():
    mod = _load_server("filing-submission-server")
    result = mod.submit_csrd_filing("entity-1", "s3://pkg", "PENDING")
    assert result["status"] == "rejected"
