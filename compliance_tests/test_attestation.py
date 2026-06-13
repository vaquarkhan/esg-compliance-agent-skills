"""Domain attestation envelope tests."""

from orchestration.attestation import (
    PENDING_SUSTAINABILITY_ASSURANCE,
    attach_attestation,
    build_attestation,
)


def test_build_attestation_defaults_pending():
    att = build_attestation(artifact_type="ghg_inventory")
    assert att["assurance_status"] == PENDING_SUSTAINABILITY_ASSURANCE
    assert att["sustainability_assuror_sign_off"] is None
    assert att["human_review_required"] is True


def test_attach_attestation_merges_payload():
    payload = attach_attestation({"total_tco2e": 100}, artifact_type="ghg_inventory")
    assert payload["total_tco2e"] == 100
    assert payload["assurance_status"] == PENDING_SUSTAINABILITY_ASSURANCE
    assert "attestation" in payload
