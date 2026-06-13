"""Lightweight MCP SSE client for orchestration agents."""

from __future__ import annotations

import json
import os
from typing import Any

import httpx

DEFAULT_URLS = {
    "regulatory": os.getenv("MCP_REGULATORY_URL", "http://127.0.0.1:8001/sse"),
    "emissions": os.getenv("MCP_EMISSIONS_URL", "http://127.0.0.1:8002/sse"),
    "taxonomy": os.getenv("MCP_TAXONOMY_URL", "http://127.0.0.1:8003/sse"),
    "filing": os.getenv("MCP_FILING_URL", "http://127.0.0.1:8004/sse"),
    "sanctions": os.getenv("MCP_SANCTIONS_URL", "http://127.0.0.1:8005/sse"),
}


class MCPClient:
    """HTTP helper for MCP servers — uses direct REST fallback for local dev."""

    def __init__(self, base_url: str | None = None, server: str = "regulatory") -> None:
        self.base_url = base_url or DEFAULT_URLS[server]
        self.server = server

    async def call_tool(self, tool: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        """Invoke tool via local Python import fallback when SSE unavailable."""
        arguments = arguments or {}
        module_map = {
            "regulatory": "regulatory-db-server",
            "emissions": "emissions-factor-server",
            "taxonomy": "taxonomy-criteria-server",
            "filing": "filing-submission-server",
            "sanctions": "sanctions-screening-server",
        }
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(
                    self.base_url.replace("/sse", "/messages"),
                    json={"method": "tools/call", "params": {"name": tool, "arguments": arguments}},
                )
                if resp.status_code == 200:
                    return resp.json()
        except (httpx.HTTPError, OSError):
            pass
        return _invoke_local_tool(module_map[self.server], tool, arguments)


def _invoke_local_tool(server_dir: str, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
    import importlib.util
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "mcp"))
    server_path = root / "mcp" / server_dir / "server.py"
    spec = importlib.util.spec_from_file_location(f"mcp_{server_dir.replace('-', '_')}", server_path)
    if spec is None or spec.loader is None:
        return {"error": f"Cannot load server: {server_path}"}
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn = getattr(mod, tool, None)
    if fn is None:
        return {"error": f"Tool {tool} not found in {server_dir}"}
    result = fn(**arguments)
    return {"content": result}


async def call_mcp(server: str, tool: str, **kwargs: Any) -> dict[str, Any]:
    client = MCPClient(server=server)
    return await client.call_tool(tool, kwargs)
