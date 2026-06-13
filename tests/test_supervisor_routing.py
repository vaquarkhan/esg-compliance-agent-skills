"""Supervisor routing tests."""

from orchestration.supervisor_agent import SupervisorAgent


def test_routes_ghg_to_calculation():
    s = SupervisorAgent()
    assert s.route("Calculate Scope 2 GHG emissions") == "calculation"


def test_routes_csrd_to_compliance():
    s = SupervisorAgent()
    assert s.route("CSRD Omnibus data mapping") == "compliance"
