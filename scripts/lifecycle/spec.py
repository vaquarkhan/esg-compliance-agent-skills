#!/usr/bin/env python3
"""Generate scope.json from CSRD scope YAML template (/spec)."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Install PyYAML: pip install pyyaml", file=sys.stderr)
    raise SystemExit(1) from None

from scripts.lifecycle.common import DEFAULT_SCOPE_TEMPLATE, attach, ensure_artifacts_dir, write_json

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate scope.json from YAML template")
    parser.add_argument("--input", type=Path, default=DEFAULT_SCOPE_TEMPLATE)
    parser.add_argument("--output", type=Path, default=ensure_artifacts_dir() / "scope.json")
    args = parser.parse_args()

    raw = yaml.safe_load(args.input.read_text(encoding="utf-8")) or {}
    scope = attach(
        {
            "lifecycle": "spec",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_template": str(args.input.relative_to(ROOT)),
            **raw,
        },
        artifact_type="scope",
    )
    write_json(args.output, scope)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
