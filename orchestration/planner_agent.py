"""LLM-driven task planner — decomposes ESG tasks and selects MCP tools dynamically.

Use when ``ESG_ORCHESTRATION_MODE=planner``. Falls back to a structured heuristic plan
when no LLM API key is configured (CI-safe).
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field

from orchestration.attestation import attach_attestation
from orchestration.mcp_client import call_mcp
from orchestration.tool_catalog import MCP_TOOL_CATALOG, WORKER_SKILLS

WorkerKey = Literal["compliance", "disclosure", "calculation", "monitoring"]
ServerKey = Literal["regulatory", "emissions", "taxonomy", "filing", "sanctions"]

ROOT = Path(__file__).resolve().parents[1]
SKILLS_MANIFEST = ROOT / "registry" / "skills.json"


class MCPToolCall(BaseModel):
    server: ServerKey
    tool: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class PlanStep(BaseModel):
    step_id: int
    description: str
    worker: WorkerKey
    primary_skill: str
    mcp_calls: list[MCPToolCall] = Field(default_factory=list)


class TaskPlan(BaseModel):
    task_summary: str
    steps: list[PlanStep]
    orchestration_mode: str = "planner"
    human_review_required: bool = True


def _has_llm_credentials() -> bool:
    return bool(os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY"))


def _load_skills_manifest() -> dict[str, Any]:
    if SKILLS_MANIFEST.exists():
        return json.loads(SKILLS_MANIFEST.read_text(encoding="utf-8"))
    return {"domain_skills": [], "meta_skills": []}


def build_heuristic_plan(task: str) -> TaskPlan:
    """Structured multi-step plan without LLM — still decomposes and picks tools by intent."""
    task_l = task.lower()
    steps: list[PlanStep] = []
    step_id = 1

    if re.search(r"csrd|esrs|omnibus|data.?map|materiality", task_l):
        steps.append(
            PlanStep(
                step_id=step_id,
                description="Fetch CSRD framework requirements and ESRS datapoint definitions",
                worker="compliance",
                primary_skill="data-ingestion-validation",
                mcp_calls=[
                    MCPToolCall(
                        server="regulatory",
                        tool="get_framework_requirements",
                        arguments={"framework": "CSRD"},
                    ),
                    MCPToolCall(
                        server="regulatory",
                        tool="get_data_point_definitions",
                        arguments={"standard": "ESRS E1", "topic": "E1"},
                    ),
                ],
            )
        )
        step_id += 1
        if "materiality" in task_l:
            steps.append(
                PlanStep(
                    step_id=step_id,
                    description="Document double materiality inputs (human SME required)",
                    worker="compliance",
                    primary_skill="double-materiality-assessment",
                    mcp_calls=[],
                )
            )
            step_id += 1

    if re.search(r"taxonomy|nace|dnsh|tsc", task_l):
        steps.append(
            PlanStep(
                step_id=step_id,
                description="Evaluate EU Taxonomy TSC/DNSH for relevant NACE activity",
                worker="disclosure",
                primary_skill="eu-taxonomy-alignment",
                mcp_calls=[
                    MCPToolCall(
                        server="taxonomy",
                        tool="get_tsc_for_activity",
                        arguments={"nace_code": "D35.11"},
                    ),
                    MCPToolCall(server="taxonomy", tool="get_minimum_safeguards", arguments={}),
                ],
            )
        )
        step_id += 1

    if re.search(r"sfdr|pai", task_l):
        steps.append(
            PlanStep(
                step_id=step_id,
                description="Load SFDR framework requirements for PAI computation",
                worker="disclosure",
                primary_skill="sfdr-pai-computation",
                mcp_calls=[
                    MCPToolCall(
                        server="regulatory",
                        tool="get_framework_requirements",
                        arguments={"framework": "SFDR"},
                    )
                ],
            )
        )
        step_id += 1

    if re.search(r"ghg|scope|emission|sbti|gwp", task_l):
        steps.append(
            PlanStep(
                step_id=step_id,
                description="Resolve GWP standard and emission factor sources",
                worker="calculation",
                primary_skill="ghg-emissions-calculation",
                mcp_calls=[
                    MCPToolCall(
                        server="emissions",
                        tool="get_gwp_values",
                        arguments={"standard": "IPCC AR6 GWP100"},
                    ),
                    MCPToolCall(server="emissions", tool="list_factor_sources", arguments={}),
                ],
            )
        )
        step_id += 1

    if re.search(r"tnfd|biodiversity|leap", task_l):
        steps.append(
            PlanStep(
                step_id=step_id,
                description="Search TNFD regulatory context for LEAP assessment",
                worker="calculation",
                primary_skill="biodiversity-tnfd-analytics",
                mcp_calls=[
                    MCPToolCall(
                        server="regulatory",
                        tool="search_regulatory_text",
                        arguments={"query": "TNFD LEAP", "framework": "TNFD"},
                    )
                ],
            )
        )
        step_id += 1

    if re.search(r"deadline|csddd|uflpa|sanction|supply", task_l):
        steps.append(
            PlanStep(
                step_id=step_id,
                description="Screen supply-chain entities and fetch regulatory deadlines",
                worker="monitoring",
                primary_skill="supply-chain-due-diligence",
                mcp_calls=[
                    MCPToolCall(
                        server="sanctions",
                        tool="screen_entity",
                        arguments={"name": "Example Supplier GmbH", "country": "DE"},
                    ),
                    MCPToolCall(
                        server="regulatory",
                        tool="get_deadlines",
                        arguments={"jurisdiction": "EU", "framework": "CSRD", "fiscal_year": 2025},
                    ),
                ],
            )
        )
        step_id += 1

    if re.search(r"dpdp|pipl|pdpl|cross-border|localization", task_l):
        jurisdiction = "IN" if "dpdp" in task_l else "CN" if "pipl" in task_l else "SA"
        steps.append(
            PlanStep(
                step_id=step_id,
                description="Fetch cross-border localization rules for target jurisdiction",
                worker="monitoring",
                primary_skill="cross-border-data-transfer",
                mcp_calls=[
                    MCPToolCall(
                        server="regulatory",
                        tool="get_jurisdiction_rules",
                        arguments={"jurisdiction": jurisdiction},
                    )
                ],
            )
        )
        step_id += 1

    if re.search(r"ixbrl|esef|audit|filing", task_l):
        steps.append(
            PlanStep(
                step_id=step_id,
                description="Validate iXBRL/ESEF tagging before filing package assembly",
                worker="disclosure",
                primary_skill="audit-trail-reporting",
                mcp_calls=[
                    MCPToolCall(
                        server="filing",
                        tool="validate_xbrl_tagging",
                        arguments={"instance_path": "report.xhtml", "taxonomy": "ESRS"},
                    )
                ],
            )
        )
        step_id += 1

    if not steps:
        steps.append(
            PlanStep(
                step_id=1,
                description="Default CSRD scoping — framework + ESRS E1 datapoints",
                worker="compliance",
                primary_skill="data-ingestion-validation",
                mcp_calls=[
                    MCPToolCall(
                        server="regulatory",
                        tool="get_framework_requirements",
                        arguments={"framework": "CSRD"},
                    ),
                    MCPToolCall(
                        server="regulatory",
                        tool="get_data_point_definitions",
                        arguments={"standard": "ESRS E1", "topic": "E1"},
                    ),
                ],
            )
        )

    return TaskPlan(
        task_summary=task[:200],
        steps=steps,
        orchestration_mode="planner_heuristic",
    )


async def plan_with_llm(task: str) -> TaskPlan:
    """Use Pydantic AI to decompose the task and select MCP tools."""
    from pydantic_ai import Agent

    model = os.environ.get("ESG_AGENT_MODEL", "openai:gpt-4o")
    catalog_json = json.dumps(MCP_TOOL_CATALOG, indent=2)
    skills_json = json.dumps(_load_skills_manifest(), indent=2)
    workers_json = json.dumps(WORKER_SKILLS, indent=2)

    planner = Agent(
        model=model,
        output_type=TaskPlan,
        instructions=(
            "You are an ESG compliance task planner. Decompose the user task into ordered steps. "
            "Each step assigns one worker (compliance, disclosure, calculation, monitoring), "
            "one primary_skill from the manifest, and zero or more MCP tool calls using ONLY "
            "tools listed in the catalog. Never invent emission factors or legal conclusions. "
            "Always set human_review_required=true. Do not submit filings."
        ),
    )

    prompt = (
        f"Task: {task}\n\n"
        f"MCP tool catalog:\n{catalog_json}\n\n"
        f"Worker → skills map:\n{workers_json}\n\n"
        f"Skills manifest:\n{skills_json}\n\n"
        "Return a TaskPlan with at least one step."
    )
    result = await planner.run(prompt)
    plan = result.output
    plan.orchestration_mode = "planner_llm"
    return plan


class PlannerAgent:
    """Agentic orchestration: plan → execute MCP calls → attach pending assurance attestation."""

    async def plan(self, task: str) -> TaskPlan:
        if _has_llm_credentials():
            try:
                return await plan_with_llm(task)
            except Exception:
                return build_heuristic_plan(task)
        return build_heuristic_plan(task)

    async def execute(self, plan: TaskPlan) -> list[dict[str, Any]]:
        executed: list[dict[str, Any]] = []
        for step in plan.steps:
            tool_results: list[dict[str, Any]] = []
            for call in step.mcp_calls:
                tool_results.append(
                    {
                        "server": call.server,
                        "tool": call.tool,
                        "arguments": call.arguments,
                        "result": await call_mcp(call.server, call.tool, **call.arguments),
                    }
                )
            executed.append(
                {
                    "step_id": step.step_id,
                    "description": step.description,
                    "worker": step.worker,
                    "primary_skill": step.primary_skill,
                    "tool_results": tool_results,
                }
            )
        return executed

    async def handle(self, task: str) -> dict[str, Any]:
        plan = await self.plan(task)
        execution = await self.execute(plan)
        payload = {
            "supervisor": "esg-compliance-planner",
            "orchestration_mode": plan.orchestration_mode,
            "plan": plan.model_dump(),
            "execution": execution,
            "human_review_required": True,
        }
        return attach_attestation(payload, artifact_type="planner_orchestration_result")
