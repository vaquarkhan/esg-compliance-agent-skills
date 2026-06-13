"""Load the official MCP Python SDK without shadowing from this repo's mcp/ directory."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[1]


def _is_local_mcp(module: ModuleType) -> bool:
    module_file = getattr(module, "__file__", None)
    if not module_file:
        return False
    try:
        return _REPO_ROOT.resolve() in Path(module_file).resolve().parents
    except OSError:
        return False


def purge_local_mcp_modules() -> None:
    for name in list(sys.modules):
        if name == "mcp" or name.startswith("mcp."):
            module = sys.modules[name]
            if _is_local_mcp(module):
                del sys.modules[name]


def import_mcp_sdk() -> ModuleType:
    """Import the installed `mcp` package (not this repository folder)."""
    purge_local_mcp_modules()
    filtered_path = [p for p in sys.path if p and Path(p).resolve() != _REPO_ROOT.resolve()]
    original_path = sys.path
    sys.path = filtered_path
    try:
        return importlib.import_module("mcp")
    finally:
        sys.path = original_path


def get_fastmcp(**kwargs: Any) -> Any:
    purge_local_mcp_modules()
    filtered_path = [p for p in sys.path if p and Path(p).resolve() != _REPO_ROOT.resolve()]
    original_path = sys.path
    sys.path = filtered_path
    try:
        from mcp.server.fastmcp import FastMCP

        return FastMCP(**kwargs)
    finally:
        sys.path = original_path
