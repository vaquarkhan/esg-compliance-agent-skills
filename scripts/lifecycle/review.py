#!/usr/bin/env python3
"""Create review_record.json stub for human SME sign-off (/review)."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from scripts.lifecycle.common import ARTIFACTS_DIR, attach, ensure_artifacts_dir, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Create pending SME review record")
    parser.add_argument("--reviewer", default="")
    parser.add_argument("--output", type=Path, default=ensure_artifacts_dir() / "review_record.json")
    args = parser.parse_args()

    record = attach(
        {
            "lifecycle": "review",
            "reviewer": args.reviewer or None,
            "reviewed_at": None,
            "outcome": "pending",
            "frameworks": ["CSRD", "ESRS"],
            "sustainability_assuror_sign_off": None,
            "notes": "Human sustainability assuror must sign before /ship with production token.",
        },
        artifact_type="review_record",
    )
    record["attestation"]["notes"] = (
        "Review record pending — assign reviewer and update outcome before filing."
    )
    write_json(args.output, record)
    print(f"Wrote {args.output} (outcome=pending)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
