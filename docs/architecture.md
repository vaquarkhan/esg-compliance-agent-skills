# Architecture

## Components

1. **Skills** — Progressive-disclosure agent instructions in `skills/`
2. **MCP servers** — FastMCP SSE tool servers in `mcp/`
3. **Orchestration** — Three tiers (see below)
4. **Knowledge base** — JSON stubs synced to OpenSearch Serverless in production
5. **Infrastructure** — AWS CDK stack in `infrastructure/`

## Orchestration tiers (honest framing)

| Tier | Entry point | Behavior | Agentic? |
| --- | --- | --- | --- |
| **Deterministic routing** | `python -m orchestration.supervisor_agent` (default) | Regex keyword → one worker → largely fixed MCP call | **No** |
| **LLM planner** | `ESG_ORCHESTRATION_MODE=planner python -m orchestration.supervisor_agent` | Task decomposition + dynamic MCP tool selection via `PlannerAgent` | **Partial** — structured plan + tool execution |
| **Full agent** | `python agent.py` | Pydantic AI + SkillsCapability progressive disclosure + PII redaction | **Yes** — model-driven skill loading |

> The default supervisor is **not** a multi-agent LLM orchestrator. It is a deterministic routing layer for CI, demos, and MCP smoke tests. Use `agent.py` or planner mode when you need agentic behavior.

## Data flow

### Deterministic (default)

```
User request → regex router → single worker → fixed MCP call → attestation envelope (pending assurance)
```

### Planner mode

```
User request → LLM/heuristic plan → N steps × dynamic MCP calls → attestation envelope (pending assurance)
```

### Full agent

```
User request → PII redaction → Pydantic AI → Skills loaded on demand → human /ship gate
```

### Lifecycle E2E (runnable)

```
/spec → /plan → /build → /validate → /review → /ship
```

Run: `make e2e` or `python scripts/e2e_pipeline.py`

Outputs land in `artifacts/` with `pending_sustainability_assurance_sign_off` on every JSON artifact.

## Domain attestation

All orchestration outputs and filing-bound artifacts carry:

```json
{
  "assurance_status": "pending_sustainability_assurance_sign_off",
  "sustainability_assuror_sign_off": null,
  "signed_at": null,
  "human_review_required": true
}
```

See `orchestration/attestation.py`, `knowledge_base/attestation_schema.json`, and [docs/sme-review.md](sme-review.md).
