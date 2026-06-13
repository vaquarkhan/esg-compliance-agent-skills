"""ESG compliance agent entry point.

Orchestrates Pydantic AI with Agent Skills (progressive disclosure) and a PII
redaction gate so personal identifiers never reach the model reasoning engine.

Deanonymization is opt-in only. Set ``ESG_AGENT_DEANONYMIZE=1`` or pass
``deanonymize_output=True`` for authorized downstream channels.
"""

from __future__ import annotations

import asyncio
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import cast

from pydantic_ai import Agent, RunContext

from redaction import ESGPIIRedactor, RedactionResult

SKILLS_DIR = Path(__file__).resolve().parent / "skills"
DEFAULT_MODEL = os.environ.get("ESG_AGENT_MODEL", "openai:gpt-4o")
DEANONYMIZE_ENV = "ESG_AGENT_DEANONYMIZE"


def _env_deanonymize_enabled() -> bool:
    return os.environ.get(DEANONYMIZE_ENV, "").strip().lower() in ("1", "true", "yes")


def _resolve_model() -> str | object:
    if os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY"):
        return DEFAULT_MODEL
    from pydantic_ai.models.test import TestModel

    return TestModel()


@dataclass
class ESGDeps:
    redactor: ESGPIIRedactor = field(default_factory=ESGPIIRedactor)
    last_redaction: RedactionResult | None = None
    deanonymize_authorized: bool = False


def _build_agent() -> Agent[ESGDeps, str]:
    try:
        from pydantic_ai_skills import SkillsCapability

        capabilities = [
            SkillsCapability(directories=[str(SKILLS_DIR)], validate=True),
        ]
    except ImportError:
        capabilities = []

    return Agent(  # type: ignore[call-overload]
        model=_resolve_model(),
        deps_type=ESGDeps,
        instructions=(
            "You are a deterministic ESG compliance assistant for CSRD, EU Taxonomy, "
            "SFDR, SEC climate, TNFD, and cross-border data localization. "
            "Follow loaded Agent Skills exactly—never invent emission factors, "
            "taxonomy eligibility, or legal conclusions. "
            "Human approval is required for final filings."
        ),
        capabilities=capabilities,
    )


esg_agent = _build_agent()


@esg_agent.system_prompt
async def redaction_context(ctx: RunContext[ESGDeps]) -> str:
    if ctx.deps.last_redaction and ctx.deps.last_redaction.entity_count:
        entities = ", ".join(ctx.deps.last_redaction.entities_detected)
        return (
            f"PII redaction active: {ctx.deps.last_redaction.entity_count} "
            f"entity(ies) masked ({entities}). Tokens like <EMAIL_1> are intentional."
        )
    return "PII redaction active: no sensitive entities detected in the user prompt."


@esg_agent.tool
def deanonymize_response(ctx: RunContext[ESGDeps], text: str) -> str:
    if not ctx.deps.deanonymize_authorized:
        raise PermissionError(
            "Deanonymization is not authorized. "
            f"Re-run with deanonymize_output=True or set {DEANONYMIZE_ENV}=1."
        )
    return ctx.deps.redactor.deanonymize(text)


@esg_agent.tool
def redaction_status(ctx: RunContext[ESGDeps]) -> dict[str, int | list[str]]:
    last = ctx.deps.last_redaction
    return {
        "active_tokens": ctx.deps.redactor.active_token_count,
        "deanonymize_authorized": int(ctx.deps.deanonymize_authorized),
        "last_pass_entities": last.entities_detected if last else [],
        "last_pass_entity_count": last.entity_count if last else 0,
    }


async def run_esg_agent(
    user_prompt: str,
    *,
    deps: ESGDeps | None = None,
    deanonymize_output: bool | None = None,
) -> str:
    run_deps = deps or ESGDeps()
    if deanonymize_output is None:
        deanonymize_output = _env_deanonymize_enabled()
    run_deps.deanonymize_authorized = bool(deanonymize_output)

    run_deps.redactor.reset_session()
    redaction = run_deps.redactor.redact(user_prompt)
    run_deps.last_redaction = redaction

    result = await esg_agent.run(redaction.redacted_text, deps=run_deps)
    output = cast(str, result.output)
    if deanonymize_output:
        return run_deps.redactor.deanonymize(output)
    return output


def run_esg_agent_sync(
    user_prompt: str,
    *,
    deps: ESGDeps | None = None,
    deanonymize_output: bool | None = None,
) -> str:
    return asyncio.run(
        run_esg_agent(user_prompt, deps=deps, deanonymize_output=deanonymize_output)
    )


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) or (
        "Map CSRD ESRS E1 data points for FY2025 scope 1 emissions review."
    )
    print(run_esg_agent_sync(prompt))
