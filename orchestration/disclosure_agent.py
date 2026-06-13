"""Worker agent: disclosure."""

from __future__ import annotations

from orchestration.mcp_client import call_mcp

SKILLS = ["eu-taxonomy-alignment", "sfdr-pai-computation", "audit-trail-reporting"]


class DisclosureAgent:
    async def run(self, task: str) -> dict:
        if "taxonomy" in task.lower():
            tool_result = await call_mcp("taxonomy", "get_tsc_for_activity", nace_code="D35.11")
        elif "sfdr" in task.lower() or "pai" in task.lower():
            tool_result = await call_mcp("regulatory", "get_framework_requirements", framework="SFDR")
        else:
            tool_result = await call_mcp("filing", "validate_xbrl_tagging", instance_path="report.xhtml", taxonomy="ESRS")
        return {"agent": "disclosure_agent", "skills": SKILLS, "task": task, "tool_result": tool_result, "human_review_required": True}
