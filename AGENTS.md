# AGENTS.md — ESG Compliance Agent Entry Point

Primary routing document for AI agents in this repository. Read before loading any skill.

## Mission

Execute **deterministic ESG compliance workflows** across CSRD/ESRS, EU Taxonomy, SFDR, SEC climate, TNFD, CSDDD, and cross-border data localization without inventing regulatory requirements or submitting filings autonomously.

## Mandatory rules

1. **Load skills progressively** — one primary skill per thread; use MCP tools for structured data.
2. **Never guess** emission factors, taxonomy eligibility, materiality scores, or legal conclusions.
3. **Human-in-the-loop** for final filings (`submit_*` MCP tools), legal assessments, and assurance sign-off.
4. **Block PII** — redact personal identifiers before model reasoning; enforce localization rules (Skill 10).
5. **Cite authoritative sources** — ESRS, EU Taxonomy Delegated Acts, SFDR RTS, GHG Protocol, IPCC AR6.
6. **Emit auditable artifacts** — JSON manifests with SHA-256 hashes, provenance, and reviewer attestations.

## Cognitive guardrails

| Guardrail | Action |
| --- | --- |
| Content filter | Reject prompts requesting fabricated compliance scores |
| PII blocking | Strip names, national IDs, account numbers from tool inputs |
| Filing gate | `/ship` requires explicit human approval token |
| Localization | Route India/China/Saudi data through Skill 10 before persistence |

## Lifecycle commands

| Command | Purpose | Outputs |
| --- | --- | --- |
| `/spec` | Scope frameworks, entities, reporting period, jurisdictions | `scope.json` |
| `/plan` | WBS, MCP tool map, evidence checklist | `plan.md` |
| `/build` | Run skills + MCP to draft calculations and disclosures | Draft artifacts |
| `/validate` | Schema, factor-source, XBRL, cross-border checks | Validation report |
| `/review` | SME/legal review (human required) | Signed review record |
| `/backfill` | Restate prior periods with audit trail | Restatement log |
| `/ship` | Package for human-approved submission only | Filing package |

Recommended flow: `/spec` → `/plan` → `/build` → `/validate` → `/review` → `/ship`

## Supervisor routing

| Signal | Worker agent | Skills |
| --- | --- | --- |
| Data mapping, CSRD Omnibus, materiality inputs | `compliance_checker_agent` | 01, 04 |
| Taxonomy, SFDR PAIs, iXBRL/ESEF | `disclosure_agent` | 03, 05, 06 |
| GHG scopes, LCA, TNFD metrics | `calculation_agent` | 02, 09 |
| Regulatory calendar, supply chain, data residency | `monitoring_agent` | 07, 08, 10 |
| Ambiguous / multi-domain | `supervisor_agent` | Decompose then delegate |

## MCP servers (SSE)

Configure base URLs (default local ports 8001–8005):

| Server | Tools |
| --- | --- |
| `regulatory-db-server` | Framework requirements, data points, deadlines |
| `emissions-factor-server` | EPA/DEFRA/IPCC factors, GWP, unit conversion |
| `taxonomy-criteria-server` | TSC, DNSH, NACE eligibility |
| `filing-submission-server` | CSRD/SEC submission stubs (human gate) |
| `sanctions-screening-server` | Entity screening, PEP, UFLPA risk |

See [mcp/README.md](mcp/README.md).

## Key files

| File | Role |
| --- | --- |
| `orchestration/supervisor_agent.py` | Task routing + MCP client orchestration |
| `knowledge_base/*.json` | Local regulatory stubs |
| `infrastructure/esg_compliance_stack.py` | AWS CDK multi-region stack |
| `skills-index.md` | Full skill catalog |

## Validation

```bash
python scripts/validate-skills.py
pytest tests/ -v
```
