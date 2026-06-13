#!/usr/bin/env python3
"""Package filing artifacts for human-approved submission (/ship)."""

from __future__ import annotations

import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path

from scripts.lifecycle.common import ARTIFACTS_DIR, attach, ensure_artifacts_dir, load_json, write_json

ROOT = Path(__file__).resolve().parents[2]
import sys

sys.path.insert(0, str(ROOT / "mcp" / "common"))
from filing_logic import submit_csrd_filing  # noqa: E402
PENDING = "pending_sustainability_assurance_sign_off"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Package filing bundle (human gate on submit)")
    parser.add_argument("--build-dir", type=Path, default=ARTIFACTS_DIR / "build")
    parser.add_argument("--review", type=Path, default=ARTIFACTS_DIR / "review_record.json")
    parser.add_argument("--entity-id", default="demo-entity-001")
    parser.add_argument("--human-approval-token", default="PENDING")
    parser.add_argument("--output", type=Path, default=ensure_artifacts_dir() / "filing_package.json")
    args = parser.parse_args()

    if not args.build_dir.exists():
        print(f"Missing build dir: {args.build_dir}. Run scripts/lifecycle/build.py first.", file=sys.stderr)
        return 1

    artifact_files = sorted(args.build_dir.glob("*.json"))
    manifest_entries = [
        {"path": str(p.relative_to(ROOT)), "sha256": _sha256(p)} for p in artifact_files
    ]

    package = attach(
        {
            "lifecycle": "ship",
            "packaged_at": datetime.now(timezone.utc).isoformat(),
            "entity_id": args.entity_id,
            "artifact_manifest": manifest_entries,
            "human_approval_token": args.human_approval_token,
            "submission": None,
        },
        artifact_type="filing_package",
    )

    package_uri = f"file://{args.output.resolve()}"
    submission = submit_csrd_filing(
        args.entity_id, package_uri, args.human_approval_token
    )
    package["submission"] = submission

    if args.human_approval_token in ("", "PENDING"):
        package["attestation"]["notes"] = (
            "Package staged with pending token — submission rejected until valid human_approval_token."
        )
        package["ship_status"] = "staged_pending_human_approval"
    else:
        package["ship_status"] = submission.get("status", "unknown")

    if args.review.exists():
        review = load_json(args.review)
        package["review_record_sha256"] = _sha256(args.review)
        if review.get("assurance_status") != PENDING:
            package["attestation"]["notes"] = "Review record assurance still pending."

    write_json(args.output, package)
    print(f"Wrote {args.output} (ship_status={package['ship_status']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
