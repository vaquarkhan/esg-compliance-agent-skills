"""Planner orchestration tests."""

import pytest

from orchestration.planner_agent import PlannerAgent, build_heuristic_plan
from orchestration.supervisor_agent import SupervisorAgent


def test_heuristic_plan_decomposes_multi_domain_task():
    plan = build_heuristic_plan(
        "Map CSRD ESRS E1, calculate Scope 2 GHG, and screen supply chain sanctions"
    )
    assert len(plan.steps) >= 2
    workers = {step.worker for step in plan.steps}
    assert "compliance" in workers
    assert "calculation" in workers or "monitoring" in workers


def test_heuristic_plan_includes_mcp_calls():
    plan = build_heuristic_plan("Calculate Scope 1 GHG with IPCC GWP")
    assert any(step.mcp_calls for step in plan.steps)
    first_call = plan.steps[0].mcp_calls[0]
    assert first_call.server == "emissions"


@pytest.mark.asyncio
async def test_planner_handle_attaches_pending_assurance():
    planner = PlannerAgent()
    result = await planner.handle("CSRD ESRS E1 mapping for FY2025")
    assert result["orchestration_mode"].startswith("planner")
    assert result["assurance_status"] == "pending_sustainability_assurance_sign_off"
    assert result["attestation"]["sustainability_assuror_sign_off"] is None
    assert result["human_review_required"] is True
    assert len(result["execution"]) >= 1


@pytest.mark.asyncio
async def test_deterministic_supervisor_passes_worker_attestation():
    supervisor = SupervisorAgent()
    result = await supervisor.handle_deterministic("CSRD Omnibus data mapping")
    assert result["orchestration_mode"] == "deterministic"
    assert result["routing_method"] == "regex_keyword_table"
    assert result["assurance_status"] == "pending_sustainability_assurance_sign_off"
    assert result["result"]["attestation"]["human_review_required"] is True
