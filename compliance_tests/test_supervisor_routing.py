"""Supervisor routing tests."""

import pytest

from orchestration.supervisor_agent import SupervisorAgent


def test_routes_ghg_to_calculation():
    s = SupervisorAgent()
    assert s.route("Calculate Scope 2 GHG emissions") == "calculation"


def test_routes_csrd_to_compliance():
    s = SupervisorAgent()
    assert s.route("CSRD Omnibus data mapping") == "compliance"


@pytest.mark.asyncio
async def test_worker_result_includes_pending_assurance():
    from orchestration.compliance_checker_agent import ComplianceCheckerAgent

    agent = ComplianceCheckerAgent()
    result = await agent.run("CSRD data mapping")
    assert result["assurance_status"] == "pending_sustainability_assurance_sign_off"
    assert result["attestation"]["human_review_required"] is True
