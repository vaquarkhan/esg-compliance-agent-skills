"""Pure filing logic — no FastMCP import required."""

from __future__ import annotations

import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


def _with_attestation(payload: dict[str, Any], artifact_type: str) -> dict[str, Any]:
    sys.path.insert(0, str(ROOT))
    from orchestration.attestation import attach_attestation

    return attach_attestation(payload, artifact_type=artifact_type)


def submit_csrd_filing(entity_id: str, package_uri: str, human_approval_token: str) -> dict[str, Any]:
    if not human_approval_token or human_approval_token == "PENDING":
        return _with_attestation(
            {"status": "rejected", "reason": "Human approval token required"},
            artifact_type="csrd_filing_submission",
        )
    filing_id = str(uuid.uuid4())
    return _with_attestation(
        {
            "status": "accepted_stub",
            "filing_id": filing_id,
            "entity_id": entity_id,
            "package_uri": package_uri,
            "registry": "ESMA ESEF (mock)",
            "submitted_at": datetime.now(timezone.utc).isoformat(),
        },
        artifact_type="csrd_filing_submission",
    )
