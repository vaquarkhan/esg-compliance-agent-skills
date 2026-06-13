"""Worker agent: monitoring."""

from __future__ import annotations

from orchestration.attestation import attach_attestation
from orchestration.mcp_client import call_mcp

SKILLS = ["regulatory-change-monitor", "supply-chain-due-diligence", "cross-border-data-transfer"]


class MonitoringAgent:
    async def run(self, task: str) -> dict:
        task_l = task.lower()
        if "sanction" in task_l or "uflpa" in task_l or "supply" in task_l:
            tool_result = await call_mcp("sanctions", "screen_entity", name="Example Supplier GmbH", country="DE")
        elif "dpdp" in task_l or "pipl" in task_l or "pdpl" in task_l or "cross-border" in task_l:
            jurisdiction = "IN" if "dpdp" in task_l else "CN" if "pipl" in task_l else "SA"
            tool_result = await call_mcp("regulatory", "get_jurisdiction_rules", jurisdiction=jurisdiction)
        else:
            tool_result = await call_mcp("regulatory", "get_deadlines", jurisdiction="EU", framework="CSRD", fiscal_year=2025)
        return attach_attestation(
            {"agent": "monitoring_agent", "skills": SKILLS, "task": task, "tool_result": tool_result, "human_review_required": True},
            artifact_type="monitoring_agent_result",
        )
