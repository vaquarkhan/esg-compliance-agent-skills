"""Shared helpers for compliance test modules."""

from __future__ import annotations


def pydantic_ai_available() -> bool:
    try:
        import pydantic_ai  # noqa: F401
        return True
    except ImportError:
        return False
