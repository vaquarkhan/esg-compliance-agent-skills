"""Worker agent: calculation."""

from __future__ import annotations

from orchestration.mcp_client import call_mcp

SKILLS = ["ghg-emissions-calculation", "biodiversity-tnfd-analytics"]


class CalculationAgent:
    async def run(self, task: str) -> dict:
        if "tnfd" in task.lower() or "biodiversity" in task.lower():
            tool_result = await call_mcp("regulatory", "search_regulatory_text", query="TNFD LEAP", framework="TNFD")
        else:
            tool_result = await call_mcp("emissions", "get_gwp_values", standard="IPCC AR6 GWP100")
        return {"agent": "calculation_agent", "skills": SKILLS, "task": task, "tool_result": tool_result, "human_review_required": True}
