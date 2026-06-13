"""Supervisor agent — routes ESG tasks to specialized workers."""

from __future__ import annotations

import asyncio
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


class SupervisorAgent:
    """Decompose tasks and delegate to worker agents."""

    def route(self, task: str) -> str:
        for pattern, worker in ROUTING_RULES:
            if pattern.search(task):
                return worker
        return "compliance"

    async def handle(self, task: str) -> dict[str, Any]:
        worker_key = self.route(task)
        worker = WORKERS[worker_key]
        result = await worker.run(task)
        return {"supervisor": "esg-compliance", "routed_to": worker_key, "result": result}


async def main() -> None:
    task = " ".join(sys.argv[1:]) or "Map CSRD ESRS E1 data points for FY2025"
    supervisor = SupervisorAgent()
    outcome = await supervisor.handle(task)
    print(outcome)


if __name__ == "__main__":
    asyncio.run(main())
