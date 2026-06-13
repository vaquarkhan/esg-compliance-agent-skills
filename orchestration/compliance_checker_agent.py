"""Worker agent: compliance checker."""

from __future__ import annotations

from typing import Any

from orchestration.mcp_client import call_mcp

SKILLS = ["data-ingestion-validation", "double-materiality-assessment"]


class ComplianceCheckerAgent:
    async def run(self, task: str) -> dict[str, Any]:
        if "materiality" in task.lower():
            tool_result = await call_mcp("regulatory", "get_framework_requirements", framework="CSRD")
        else:
            tool_result = await call_mcp("regulatory", "get_data_point_definitions", standard="ESRS E1", topic="E1")
        return {
            "agent": "compliance_checker_agent",
            "skills": SKILLS,
            "task": task,
            "tool_result": tool_result,
            "human_review_required": True,
        }
