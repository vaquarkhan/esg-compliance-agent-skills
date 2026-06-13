"""Domain attestation envelope for ESG artifacts and orchestration outputs."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

# ESG filings require external sustainability assurance — never auto-approved.
PENDING_SUSTAINABILITY_ASSURANCE = "pending_sustainability_assurance_sign_off"
APPROVED_ASSURANCE = "sustainability_assurance_signed_off"


def build_attestation(
    *,
    artifact_type: str,
    assurance_status: str = PENDING_SUSTAINABILITY_ASSURANCE,
    sustainability_assuror: str | None = None,
    signed_at: str | None = None,
    notes: str | None = None,
) -> dict[str, Any]:
    """Return a standard attestation block for JSON manifests and worker responses."""
    return {
        "assurance_status": assurance_status,
        "sustainability_assuror_sign_off": sustainability_assuror,
        "signed_at": signed_at,
        "artifact_type": artifact_type,
        "human_review_required": assurance_status != APPROVED_ASSURANCE,
        "notes": notes
        or "Operational draft only — requires sustainability assuror sign-off before external filing.",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }


def attach_attestation(payload: dict[str, Any], *, artifact_type: str) -> dict[str, Any]:
    """Attach pending assurance attestation to an orchestration or example payload."""
    enriched = dict(payload)
    enriched.setdefault("human_review_required", True)
    enriched["attestation"] = build_attestation(artifact_type=artifact_type)
    enriched["assurance_status"] = enriched["attestation"]["assurance_status"]
    return enriched
