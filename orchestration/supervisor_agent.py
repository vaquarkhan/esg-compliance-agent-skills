"""Deterministic routing layer + optional LLM planner for ESG tasks.

Two orchestration modes (see docs/architecture.md):

- **deterministic** (default): regex keyword → worker → largely fixed MCP call.
- **planner**: LLM task decomposition + dynamic MCP tool selection via ``PlannerAgent``.

For full agentic skill loading (progressive disclosure), use ``agent.py``.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
from typing import Any

from orchestration.compliance_checker_agent import ComplianceCheckerAgent
from orchestration.disclosure_agent import DisclosureAgent
from orchestration.calculation_agent import CalculationAgent
from orchestration.monitoring_agent import MonitoringAgent

ROUTING_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"csrd|omnibus|materiality|data.?map", re.I), "compliance"),
    (re.compile(r"taxonomy|sfdr|pai|ixbrl|esef|disclosure", re.I), "disclosure"),
    (re.compile(r"ghg|scope|emission|tnfd|biodiversity|lca|sbti", re.I), "calculation"),
    (re.compile(r"deadline|csddd|uflpa|sanction|dpdp|pipl|pdpl|supply", re.I), "monitoring"),
]

WORKERS = {
    "compliance": ComplianceCheckerAgent(),
    "disclosure": DisclosureAgent(),
    "calculation": CalculationAgent(),
    "monitoring": MonitoringAgent(),
}


def orchestration_mode() -> str:
    return os.getenv("ESG_ORCHESTRATION_MODE", "deterministic").strip().lower()


class SupervisorAgent:
    """Regex-based router — deterministic, not agentic. See ``PlannerAgent`` for LLM planning."""

    def route(self, task: str) -> str:
        for pattern, worker in ROUTING_RULES:
            if pattern.search(task):
                return worker
        return "compliance"

    async def handle_deterministic(self, task: str) -> dict[str, Any]:
        worker_key = self.route(task)
        worker = WORKERS[worker_key]
        result = await worker.run(task)
        return {
            "supervisor": "esg-compliance-deterministic",
            "orchestration_mode": "deterministic",
            "routing_method": "regex_keyword_table",
            "routed_to": worker_key,
            "result": result,
            "human_review_required": True,
            "assurance_status": result.get("assurance_status"),
            "attestation": result.get("attestation"),
            "note": (
                "Deterministic routing only — one worker, largely fixed MCP call. "
                "Use ESG_ORCHESTRATION_MODE=planner or agent.py for agentic orchestration."
            ),
        }

    async def handle(self, task: str) -> dict[str, Any]:
        if orchestration_mode() == "planner":
            from orchestration.planner_agent import PlannerAgent

            return await PlannerAgent().handle(task)
        return await self.handle_deterministic(task)


async def main() -> None:
    task = " ".join(sys.argv[1:]) or "Map CSRD ESRS E1 data points for FY2025"
    supervisor = SupervisorAgent()
    outcome = await supervisor.handle(task)
    print(outcome)


if __name__ == "__main__":
    asyncio.run(main())
