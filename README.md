# esg-compliance-agent-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/vaquarkhan/esg-compliance-agent-skills/actions/workflows/validate-and-package.yml/badge.svg)](https://github.com/vaquarkhan/esg-compliance-agent-skills/actions/workflows/validate-and-package.yml)
[![CodeQL](https://github.com/vaquarkhan/esg-compliance-agent-skills/actions/workflows/codeql.yml/badge.svg)](https://github.com/vaquarkhan/esg-compliance-agent-skills/actions/workflows/codeql.yml)
[![Coverage](https://img.shields.io/badge/coverage-%E2%89%A580%25-brightgreen.svg)](pyproject.toml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](requirements-lock.txt)
[![Skills](https://img.shields.io/badge/skills-10-orange.svg)](skills-index.md)

**Reference architecture for ESG compliance agents** — progressive-disclosure skills, PII redaction, five SSE MCP servers, **three-tier orchestration** (deterministic routing, LLM planner, full agent), AWS CDK scaffold, and IDE plugin templates for CSRD/ESRS, EU Taxonomy, SFDR, SEC climate, TNFD, CSDDD, and cross-border localization (APAC, LATAM, MENA).

> **Disclaimer:** Operational ESG reporting patterns only. **Not legal advice** and does not replace sustainability assurance, statutory audit, or legal counsel.

**Coverage:** 10 skills across CSRD, Taxonomy, SFDR, GHG, TNFD, supply chain, and data residency. See [docs/coverage-roadmap.md](docs/coverage-roadmap.md).

Pattern aligned with [compliance-agent-skills v1.6.0](https://github.com/vaquarkhan/compliance-agent-skills/releases).

---

## Why this exists

LLM agents can accelerate ESG reporting, but they must not:

- Invent emission factors or taxonomy eligibility
- Submit regulatory filings without human approval
- Process personal data without localization controls

This repository addresses that with:

1. **10 specialized skills** with human-in-the-loop gates and MCP tool maps
2. **PII redaction** (`redaction.py`) before model reasoning
3. **Lifecycle commands** — `/spec`, `/plan`, `/build`, `/validate`, `/review`, `/backfill`, `/ship`
4. **Five MCP SSE servers** for regulatory data, factors, taxonomy, filings, sanctions
5. **IDE install surfaces** — VS Code extension and JetBrains plugin scaffold

---

## Quick start

### Prerequisites

- Python **3.11+**
- Node.js **18+** (VS Code extension build; optional)
- JDK **17+** (JetBrains plugin build; optional)

### Bootstrap

**Windows:**

```powershell
git clone git@github.com:vaquarkhan/esg-compliance-agent-skills.git
cd esg-compliance-agent-skills
.\bootstrap.ps1
```

**macOS / Linux:**

```bash
git clone git@github.com:vaquarkhan/esg-compliance-agent-skills.git
cd esg-compliance-agent-skills
chmod +x bootstrap.sh && ./bootstrap.sh
```

### Run the agent locally

```bash
pip install -r requirements-lock.txt
export OPENAI_API_KEY=sk-...   # or ANTHROPIC_API_KEY
python agent.py "Scope CSRD ESRS E1 data points for FY2025"
```

Without API keys, the agent uses Pydantic AI `TestModel`.

### Orchestration modes

| Mode | Command | What it does |
| --- | --- | --- |
| **Deterministic** (default) | `python -m orchestration.supervisor_agent "Map CSRD ESRS E1"` | Regex → one worker → fixed MCP call. **Not agentic.** |
| **LLM planner** | `ESG_ORCHESTRATION_MODE=planner python -m orchestration.supervisor_agent "..."` | Task decomposition + dynamic MCP tool selection |
| **Full agent** | `python agent.py "..."` | Pydantic AI + progressive skill loading + PII redaction |

See [docs/architecture.md](docs/architecture.md) for honest framing of each tier.

```bash
python scripts/demo_agent.py
# or: make demo
```

### Validate

```bash
make validate
make test-all
make e2e
make lint
make security
```

### End-to-end lifecycle

```bash
make e2e
# /spec → /plan → /build → /validate → /review → /ship
# Artifacts in artifacts/ with pending sustainability assurance on every JSON output
```

**Engineering:** CI enforces Ruff, mypy, pip-audit, Bandit, detect-secrets, CodeQL, and ≥80% coverage on `agent.py` + `redaction.py`. See [docs/architecture.md](docs/architecture.md), [docs/sme-review.md](docs/sme-review.md), [docs/redaction-limitations.md](docs/redaction-limitations.md).

**Locked dependencies:** `requirements-lock.txt` (compile with `make lock` from `requirements.in`).

---

## Plugin installation

### Cursor

See [docs/cursor-setup.md](docs/cursor-setup.md). Installs `.cursor/rules/`, skills, and `mcp/esg-mcp-servers.mcp.json`.

### VS Code

```bash
cd vscode-extension && npm install -g @vscode/vsce && vsce package --no-dependencies
code --install-extension esg-compliance-agent-skills-*.vsix
```

See [docs/plugin-publishing.md](docs/plugin-publishing.md).

### JetBrains

```bash
cd jetbrains-plugin && ./gradlew buildPlugin
```

---

## Lifecycle commands

| Command | Purpose |
| --- | --- |
| `/spec` | Scope frameworks, entities, jurisdictions |
| `/plan` | WBS, MCP tool plan, evidence checklist |
| `/build` | Execute skills + MCP (draft artifacts) |
| `/validate` | Schema, XBRL, factor-source checks |
| `/review` | SME / legal sign-off (human required) |
| `/backfill` | Historical restatements |
| `/ship` | Human-approved filing package only |

Example: `/spec` → `/build` (ghg-emissions-calculation) → `/validate` → `/review` → `/ship`

---

## Skills catalog

| # | Skill | Focus |
| --- | --- | --- |
| 01 | `data-ingestion-validation` | CSRD Omnibus mapping |
| 02 | `ghg-emissions-calculation` | Scopes 1–3, SBTi |
| 03 | `eu-taxonomy-alignment` | NACE, TSC, DNSH |
| 04 | `double-materiality-assessment` | Impact / financial |
| 05 | `sfdr-pai-computation` | 18 PAIs |
| 06 | `audit-trail-reporting` | iXBRL/ESEF |
| 07 | `regulatory-change-monitor` | Deadline calendar |
| 08 | `supply-chain-due-diligence` | CSDDD, UFLPA |
| 09 | `biodiversity-tnfd-analytics` | TNFD LEAP |
| 10 | `cross-border-data-transfer` | DPDP, PIPL, PDPL |

Full catalog: [skills-index.md](skills-index.md). Routing: [AGENTS.md](AGENTS.md).

---

## Project structure

```
esg-compliance-agent-skills/
├── agent.py                 # Pydantic AI entry + SkillsCapability
├── redaction.py             # PII redaction gate
├── skills/                  # 10 Agent Skills
├── mcp/                     # 5 SSE MCP servers
├── orchestration/           # Deterministic router + LLM planner + attestation
├── infrastructure/          # AWS CDK stack
├── knowledge_base/          # JSON stubs pre-OpenSearch
├── presets/                 # CSRD, SFDR presets
├── starter-packs/           # Curated bundles
├── templates/               # YAML scaffolds
├── references/              # SME-reviewed checklists
├── registry/assets.json     # Machine-readable index
├── docs/                    # Architecture, SME review, plugins
├── .cursor/rules/           # Cursor agent rules
├── .claude/commands/        # Lifecycle slash commands
├── agents/                  # Persona prompts
├── examples/                # Runnable validators
├── vscode-extension/
└── jetbrains-plugin/
```

---

## MCP servers (SSE)

| Server | Port | Run |
| --- | --- | --- |
| regulatory-db-server | 8001 | `python mcp/regulatory-db-server/server.py` |
| emissions-factor-server | 8002 | `python mcp/emissions-factor-server/server.py` |
| taxonomy-criteria-server | 8003 | `python mcp/taxonomy-criteria-server/server.py` |
| filing-submission-server | 8004 | `python mcp/filing-submission-server/server.py` |
| sanctions-screening-server | 8005 | `python mcp/sanctions-screening-server/server.py` |

See [mcp/README.md](mcp/README.md).

---

## Documentation

| Doc | Topic |
| --- | --- |
| [docs/global-regulatory-landscape.md](docs/global-regulatory-landscape.md) | APAC, LATAM, MENA deadlines & localization |
| [docs/coverage-roadmap.md](docs/coverage-roadmap.md) | Framework coverage |
| [docs/getting-started.md](docs/getting-started.md) | First engagement |
| [docs/skill-anatomy.md](docs/skill-anatomy.md) | Authoring skills |
| [docs/plugin-publishing.md](docs/plugin-publishing.md) | VS Code / JetBrains releases |
| [AGENTS.md](AGENTS.md) | Agent routing |
| [CLAUDE.md](CLAUDE.md) | Claude entry |

---

## License

MIT — see [LICENSE](LICENSE).
