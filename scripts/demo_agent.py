#!/usr/bin/env python3
"""Demo agent using TestModel (no API key required)."""

from __future__ import annotations

import sys

from agent import run_esg_agent_sync


def main() -> None:
    prompt = " ".join(sys.argv[1:]) or "Scope CSRD ESRS E1 disclosure for FY2025."
    print(run_esg_agent_sync(prompt))


if __name__ == "__main__":
    main()
