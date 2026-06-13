"""Run FastMCP SSE endpoints behind a FastAPI ASGI application."""

from __future__ import annotations

import os
from typing import Any

import uvicorn
from fastapi import FastAPI


def run_fastapi_sse(mcp_instance: Any, title: str | None = None) -> None:
    """Expose MCP SSE transport via FastAPI + Uvicorn."""
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8000"))
    app = FastAPI(title=title or getattr(mcp_instance, "name", "esg-mcp-server"))
    app.mount("/", mcp_instance.sse_app())

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "transport": "sse"}

    uvicorn.run(app, host=host, port=port)
