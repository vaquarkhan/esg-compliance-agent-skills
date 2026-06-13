#!/usr/bin/env python3
"""Run runnable examples and copy outputs to artifacts/ (/build)."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from scripts.lifecycle.common import ARTIFACTS_DIR, attach, ensure_artifacts_dir, write_json

ROOT = Path(__file__).resolve().parents[2]
PYTHON = sys.executable


def _run(script: Path) -> None:
    subprocess.run([PYTHON, str(script)], check=True, cwd=str(ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build draft artifacts from examples")
    parser.add_argument("--output-dir", type=Path, default=ensure_artifacts_dir() / "build")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    _run(ROOT / "examples" / "ghg-inventory" / "run_inventory.py")
    _run(ROOT / "examples" / "csrd-e1-mapping" / "run_mapping.py")

    copies = {
        ROOT / "examples" / "ghg-inventory" / "ghg_inventory.json": args.output_dir / "ghg_inventory.json",
        ROOT / "examples" / "ghg-inventory" / "factor_provenance.json": args.output_dir / "factor_provenance.json",
        ROOT / "examples" / "csrd-e1-mapping" / "mapping_matrix.json": args.output_dir / "mapping_matrix.json",
    }
    for src, dst in copies.items():
        shutil.copy2(src, dst)

    manifest = attach(
        {
            "lifecycle": "build",
            "built_at": datetime.now(timezone.utc).isoformat(),
            "artifacts": [str(p.relative_to(ROOT)) for p in copies.values()],
        },
        artifact_type="build_manifest",
    )
    write_json(args.output_dir / "build_manifest.json", manifest)
    print(f"Build complete -> {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
