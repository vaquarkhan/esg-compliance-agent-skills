#!/usr/bin/env python3
"""Bootstrap script to materialize esg-compliance-agent-skills repository files."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write(path: str, content: str) -> None:
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content, encoding="utf-8")
    print(f"  wrote {path}")


def main() -> None:
    print(f"Generating repository under {ROOT}")
    generate_core()
    generate_knowledge_base()
    generate_mcp_shared()
    generate_mcp_servers()
    generate_skills()
    generate_orchestration()
    generate_infrastructure()
    generate_tests()
    generate_github()
    generate_docs()
    print("Done.")


def generate_core() -> None:
    write(
        "VERSION",
        "1.0.0\n",
    )
    write(
        "LICENSE",
        """MIT License

Copyright (c) 2026 ESG Compliance Agent Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
    )
    write(
        ".gitignore",
        """# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
.eggs/
dist/
build/
.venv/
venv/
.env
.env.*
!.env.example

# CDK
infrastructure/cdk.out/
*.swp

# IDE
.idea/
.vscode/
*.vsix

# Test / coverage
.coverage
coverage.xml
htmlcov/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# OS
.DS_Store
Thumbs.db

# Secrets
*.pem
*.key
.secrets.baseline.local
""",
    )
    write(
        "pytest.ini",
        """[pytest]
testpaths = tests
asyncio_mode = auto
filterwarnings =
    ignore::DeprecationWarning
""",
    )
    write(
        "requirements.txt",
        """mcp>=1.6.0
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
starlette>=0.41.0
httpx>=0.27.0
sse-starlette>=2.1.0
aws-cdk-lib>=2.170.0
constructs>=10.4.0
boto3>=1.35.0
pytz>=2024.1
pydantic>=2.9.0
python-dotenv>=1.0.0
""",
    )
    write(
        "requirements-dev.txt",
        """pytest>=8.3.0
pytest-asyncio>=0.24.0
pytest-cov>=6.0.0
ruff>=0.8.0
mypy>=1.13.0
""",
    )
    write(
        "pyproject.toml",
        """[project]
name = "esg-compliance-agent-skills"
version = "1.0.0"
description = "ESG compliance agent ecosystem with MCP servers and AWS CDK infrastructure"
readme = "README.md"
requires-python = ">=3.11"

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "W"]

[tool.mypy]
python_version = "3.11"
ignore_missing_imports = true
""",
    )
    write(
        "Makefile",
        """.PHONY: install test lint validate mcp-local cdk-synth

install:
\tpip install -r requirements.txt -r requirements-dev.txt

test:
\tpytest tests/ -v

lint:
\truff check .

validate:
\tpython scripts/validate-skills.py

mcp-local:
\tpython -m mcp.regulatory-db-server.server & \\
\tpython -m mcp.emissions-factor-server.server

cdk-synth:
\tcd infrastructure && cdk synth
""",
    )
    write(
        "bootstrap.sh",
        """#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
echo "ESG compliance agent skills bootstrapped."
""",
    )
    write(
        "bootstrap.ps1",
        """# Bootstrap ESG compliance agent skills (Windows)
python -m venv .venv
& .\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
Write-Host "ESG compliance agent skills bootstrapped."
""",
    )
    write(
        "skills-index.md",
        SKILLS_INDEX,
    )
    write("README.md", README)
    write("AGENTS.md", AGENTS)
    write("CHANGELOG.md", CHANGELOG)
    write("CONTRIBUTING.md", CONTRIBUTING)
    write("SECURITY.md", SECURITY)
    write(
        "scripts/validate-skills.py",
        """#!/usr/bin/env python3
\"\"\"Validate all SKILL.md files have required YAML frontmatter.\"\"\"
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
pattern = re.compile(r"^---\\nname: .+\\ndescription: .+\\n---", re.MULTILINE)
errors = []
for skill_md in SKILLS.glob("*/SKILL.md"):
    text = skill_md.read_text(encoding="utf-8")
    if not pattern.search(text):
        errors.append(str(skill_md))
if errors:
    print("Invalid SKILL.md frontmatter:", *errors, sep="\\n")
    sys.exit(1)
print(f"Validated {len(list(SKILLS.glob('*/SKILL.md')))} skills.")
""",
    )


README = r"""# esg-compliance-agent-skills

[![License: MIT](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](requirements.txt)
[![Skills](https://img.shields.io/badge/skills-10-orange.svg)](skills-index.md)

**Production-grade ESG compliance agent ecosystem** — Supervisor-Worker orchestration, 10 specialized Agent Skills, five SSE MCP servers, local knowledge-base stubs, and multi-region AWS CDK infrastructure for CSRD, EU Taxonomy, SFDR, SEC climate, TNFD, and cross-border data localization.

> **Disclaimer:** This repository provides operational ESG reporting patterns and automation templates. It is **not legal advice** and does not replace qualified sustainability assurance, statutory audit, or legal counsel for regulatory filings.

---

## Architecture

```mermaid
flowchart TB
    User[User / IDE Agent] --> Supervisor[Supervisor Agent]
    Supervisor --> CC[Compliance Checker]
    Supervisor --> DA[Disclosure Agent]
    Supervisor --> CA[Calculation Agent]
    Supervisor --> MA[Monitoring Agent]
    CC & DA & CA & MA --> MCP[MCP SSE Servers]
    MCP --> KB[(Knowledge Base JSON)]
    MCP --> AWS[AWS CDK Stack]
    AWS --> ECS[ECS Fargate]
    AWS --> OS[OpenSearch Serverless]
    AWS --> DDB[DynamoDB Audit]
    AWS --> S3[S3 + Glacier Archive]
```

### Supervisor-Worker pattern

The **supervisor** routes tasks by regulatory signal (CSRD disclosure, GHG inventory, taxonomy alignment, sanctions screening) to specialized **worker agents**. Each worker loads progressive-disclosure skills from `skills/` and invokes MCP tools over SSE. Final filings and legal assessments require **human-in-the-loop** approval.

### Multi-region CDK deployment

Infrastructure targets five AWS regions for data residency and latency:

| Region | Role |
| --- | --- |
| `eu-west-1` | EU CSRD / ESEF primary |
| `us-east-1` | SEC climate / SFDR US ops |
| `ap-south-1` | India DPDP localization |
| `ap-southeast-1` | APAC supply-chain due diligence |
| `me-south-1` | Middle East PDPL workloads |

See [infrastructure/esg_compliance_stack.py](infrastructure/esg_compliance_stack.py) for resource definitions.

---

## Quick start

```bash
git clone https://github.com/your-org/esg-compliance-agent-skills.git
cd esg-compliance-agent-skills
chmod +x bootstrap.sh && ./bootstrap.sh   # Windows: .\bootstrap.ps1
```

### Run MCP servers locally (SSE)

Each server exposes tools on a dedicated port:

| Server | Port | Module |
| --- | --- | --- |
| regulatory-db-server | 8001 | `python mcp/regulatory-db-server/server.py` |
| emissions-factor-server | 8002 | `python mcp/emissions-factor-server/server.py` |
| taxonomy-criteria-server | 8003 | `python mcp/taxonomy-criteria-server/server.py` |
| filing-submission-server | 8004 | `python mcp/filing-submission-server/server.py` |
| sanctions-screening-server | 8005 | `python mcp/sanctions-screening-server/server.py` |

### Orchestration

```bash
export MCP_REGULATORY_URL=http://127.0.0.1:8001/sse
python -m orchestration.supervisor_agent "Map CSRD ESRS E1 data points for FY2025"
```

### Deploy infrastructure

```bash
cd infrastructure
pip install -r requirements.txt
cdk bootstrap
cdk deploy --all
```

---

## Lifecycle commands

| Command | Purpose |
| --- | --- |
| `/spec` | Define scope, frameworks, jurisdictions, material topics |
| `/plan` | Produce work breakdown, MCP tool plan, evidence checklist |
| `/build` | Execute skills + MCP tools to produce draft artifacts |
| `/validate` | Schema, XBRL, factor-source, and cross-border checks |
| `/review` | SME / legal review gate (human required) |
| `/backfill` | Historical restatements and audit trail reconciliation |
| `/ship` | Package filings for human-approved submission only |

Full routing: [AGENTS.md](AGENTS.md).

---

## Skills catalog

| # | Skill | Focus |
| --- | --- | --- |
| 01 | `data-ingestion-validation` | CSRD 1,100+ Omnibus data mapping |
| 02 | `ghg-emissions-calculation` | Scopes 1–3, LCA, SBTi |
| 03 | `eu-taxonomy-alignment` | NACE, TSC, DNSH |
| 04 | `double-materiality-assessment` | Impact / financial scoring |
| 05 | `sfdr-pai-computation` | 18 PAIs, Art. 6/8/9 |
| 06 | `audit-trail-reporting` | iXBRL/ESEF, DynamoDB/S3/Glacier |
| 07 | `regulatory-change-monitor` | Global deadline calendar |
| 08 | `supply-chain-due-diligence` | CSDDD, UFLPA |
| 09 | `biodiversity-tnfd-analytics` | TNFD LEAP, MSA, BII |
| 10 | `cross-border-data-transfer` | DPDP, PIPL, PDPL localization |

See [skills-index.md](skills-index.md).

---

## Project structure

```
esg-compliance-agent-skills/
├── AGENTS.md                 # Supervisor routing + lifecycle commands
├── skills/                   # 10 Agent Skills (SKILL.md each)
├── knowledge_base/           # Local JSON stubs pre-OpenSearch
├── mcp/                      # 5 SSE MCP servers + Dockerfiles
├── orchestration/            # Supervisor + worker agents
├── infrastructure/           # AWS CDK app + stack
├── docs/                     # Architecture and setup guides
├── tests/                    # Unit tests
├── scripts/                  # Validation utilities
└── .github/                  # CI workflows
```

---

## License

MIT — see [LICENSE](LICENSE).

Inspired by the engineering patterns in [compliance-agent-skills](https://github.com/vaquarkhan/compliance-agent-skills/releases).
"""

AGENTS = r"""# AGENTS.md — ESG Compliance Agent Entry Point

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
"""

SKILLS_INDEX = """# Skills Index — ESG Compliance Agent Skills

| Skill | Path | Triggers |
| --- | --- | --- |
| Data Ingestion & Validation | `skills/data-ingestion-validation/` | CSRD, ESRS, Omnibus, data mapping |
| GHG Emissions Calculation | `skills/ghg-emissions-calculation/` | Scope 1/2/3, LCA, SBTi |
| EU Taxonomy Alignment | `skills/eu-taxonomy-alignment/` | NACE, TSC, DNSH, KPIs |
| Double Materiality Assessment | `skills/double-materiality-assessment/` | Impact, financial materiality |
| SFDR PAI Computation | `skills/sfdr-pai-computation/` | PAIs, Article 6/8/9 |
| Audit Trail & Reporting | `skills/audit-trail-reporting/` | iXBRL, ESEF, immutable logs |
| Regulatory Change Monitor | `skills/regulatory-change-monitor/` | Deadlines, ESRS updates |
| Supply Chain Due Diligence | `skills/supply-chain-due-diligence/` | CSDDD, UFLPA |
| Biodiversity TNFD Analytics | `skills/biodiversity-tnfd-analytics/` | LEAP, MSA, BII |
| Cross-Border Data Transfer | `skills/cross-border-data-transfer/` | DPDP, PIPL, PDPL |
"""

CHANGELOG = """# Changelog

## [1.0.0] - 2026-06-13

### Added
- Initial ESG compliance agent ecosystem
- 10 agent skills with human-in-the-loop gates
- 5 MCP SSE servers with mock functional tool logic
- Supervisor-worker orchestration layer
- AWS CDK stack (ECS Fargate, ALB, DynamoDB, S3/Glacier, OpenSearch Serverless)
- Knowledge base JSON stubs for emission factors and taxonomy criteria
"""

CONTRIBUTING = """# Contributing

1. Fork and create a feature branch
2. Run `python scripts/validate-skills.py` and `pytest tests/ -v`
3. Follow skill frontmatter conventions in `skills/*/SKILL.md`
4. Open a PR with framework coverage notes
"""

SECURITY = """# Security Policy

Report vulnerabilities privately to the repository maintainers.

- Do not commit secrets or production filing credentials
- MCP filing tools are stubs — never point at production registries without review
- Enforce cross-border localization checks before persisting personal data
"""


def generate_knowledge_base() -> None:
    emission_factors = {
        "metadata": {
            "version": "2026.06",
            "sources": ["EPA GHG Emission Factors Hub", "DEFRA 2024", "IPCC AR6 GWP100"],
        },
        "factors": [
            {
                "id": "EPA-NATGAS-STATIONARY",
                "source": "EPA",
                "activity": "natural_gas_combustion_stationary",
                "unit": "kg CO2e / MMBtu",
                "factor": 53.06,
                "scope": "scope_1",
            },
            {
                "id": "DEFRA-ELEC-UK-2024",
                "source": "DEFRA",
                "activity": "grid_electricity_uk",
                "unit": "kg CO2e / kWh",
                "factor": 0.177,
                "scope": "scope_2_location",
            },
            {
                "id": "DEFRA-BUSINESS-TRAVEL-AIR-DOMESTIC",
                "source": "DEFRA",
                "activity": "business_travel_air_domestic",
                "unit": "kg CO2e / passenger-km",
                "factor": 0.255,
                "scope": "scope_3_cat6",
            },
            {
                "id": "EPA-DIESEL-MOBILE",
                "source": "EPA",
                "activity": "diesel_combustion_mobile",
                "unit": "kg CO2e / gallon",
                "factor": 10.21,
                "scope": "scope_1",
            },
        ],
        "gwp": {
            "standard": "IPCC AR6 GWP100",
            "values": {
                "CO2": 1.0,
                "CH4": 27.9,
                "N2O": 273.0,
                "HFC-134a": 1526.0,
                "SF6": 25200.0,
            },
        },
        "grid_factors_by_country": {
            "DE": {"unit": "kg CO2e/kWh", "factor": 0.366, "year": 2024},
            "US": {"unit": "kg CO2e/kWh", "factor": 0.386, "year": 2024},
            "IN": {"unit": "kg CO2e/kWh", "factor": 0.708, "year": 2024},
            "SG": {"unit": "kg CO2e/kWh", "factor": 0.412, "year": 2024},
        },
    }
    taxonomy = {
        "metadata": {"version": "2026.06", "framework": "EU Taxonomy Delegated Regulation"},
        "activities": [
            {
                "nace": "D35.11",
                "name": "Production of electricity from solar PV",
                "environmental_objective": "climate_mitigation",
                "tsc": {
                    "threshold": "lifecycle_ghg_savings_pct >= 73",
                    "reference": "Annex I Section 4.1",
                },
                "dnsh": ["climate_adaptation", "water", "pollution", "biodiversity", "circular_economy"],
            },
            {
                "nace": "C29.10",
                "name": "Manufacture of motor vehicles",
                "environmental_objective": "climate_mitigation",
                "tsc": {"threshold": "tailpipe_co2_g_km <= 50", "reference": "Annex I Section 3.3"},
                "dnsh": ["climate_adaptation", "water", "pollution"],
            },
        ],
        "minimum_safeguards": [
            "OECD Guidelines for Multinational Enterprises",
            "UN Guiding Principles on Business and Human Rights",
            "ILO Core Conventions",
        ],
        "objective_thresholds": {
            "climate_mitigation": {"default": "substantial_contribution_per_annex"},
            "climate_adaptation": {"default": "material_physical_risk_reduction"},
        },
    }
    write("knowledge_base/emission_factors.json", json.dumps(emission_factors, indent=2) + "\n")
    write("knowledge_base/taxonomy_criteria.json", json.dumps(taxonomy, indent=2) + "\n")


MCP_SERVER_TEMPLATE = '''"""MCP server: {name} — SSE transport via FastMCP."""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).resolve().parents[2]
KB = ROOT / "knowledge_base"

mcp = FastMCP("{name}", host=os.getenv("MCP_HOST", "0.0.0.0"), port=int(os.getenv("MCP_PORT", "{port}")))

{tool_impls}


def main() -> None:
    """Run MCP server with SSE transport (Uvicorn ASGI)."""
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
'''


def generate_mcp_shared() -> None:
    write(
        "mcp/__init__.py",
        '"""ESG compliance MCP servers."""\n',
    )
    write(
        "mcp/common/__init__.py",
        '"""Shared MCP utilities."""\n',
    )
    write(
        "mcp/common/kb_loader.py",
        '''"""Load knowledge base JSON stubs."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KB = ROOT / "knowledge_base"


@lru_cache(maxsize=8)
def load_json(name: str) -> dict:
    path = KB / name
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)
''',
    )
    write(
        "mcp/README.md",
        """# MCP Servers — ESG Compliance

Five Python MCP servers using **FastMCP** with **SSE** transport (`mcp.run(transport="sse")`).

## Servers

| Directory | Default port | Purpose |
| --- | --- | --- |
| `regulatory-db-server/` | 8001 | Framework requirements, deadlines |
| `emissions-factor-server/` | 8002 | EPA/DEFRA/IPCC factors |
| `taxonomy-criteria-server/` | 8003 | EU Taxonomy TSC/DNSH |
| `filing-submission-server/` | 8004 | CSRD/SEC filing stubs |
| `sanctions-screening-server/` | 8005 | Entity screening |

## Local run

```bash
python mcp/regulatory-db-server/server.py
```

## Docker

```bash
docker build -t esg-regulatory-mcp mcp/regulatory-db-server
docker run -p 8001:8001 esg-regulatory-mcp
```

## Cursor MCP config example

```json
{
  "mcpServers": {
    "esg-regulatory": {
      "url": "http://127.0.0.1:8001/sse"
    }
  }
}
```
""",
    )


def generate_mcp_servers() -> None:
    servers = [
        regulatory_db_server(),
        emissions_factor_server(),
        taxonomy_criteria_server(),
        filing_submission_server(),
        sanctions_screening_server(),
    ]
    for spec in servers:
        pkg = f"mcp/{spec['dir']}"
        write(f"{pkg}/__init__.py", f'"""{spec["dir"]} MCP server."""\n')
        write(f"{pkg}/server.py", spec["server_py"])
        write(f"{pkg}/tool-schemas.json", json.dumps(spec["schemas"], indent=2) + "\n")
        write(f"{pkg}/Dockerfile", spec["dockerfile"])


def regulatory_db_server() -> dict:
    impls = '''
@mcp.tool()
def get_framework_requirements(framework: str, version: str = "latest") -> dict[str, Any]:
    """Return structured requirements for a reporting framework."""
    catalog = {
        "CSRD": {"articles": ["19a", "29a"], "standards": ["ESRS E1", "ESRS S1"], "assurance": "limited_then_reasonable"},
        "SFDR": {"articles": ["6", "8", "9"], "disclosures": ["PAI", "principal_adverse_impacts"]},
        "SEC_CLIMATE": {"rules": ["10-K climate disclosure", "Scope 1/2 material emitters"]},
    }
    key = framework.upper().replace("-", "_").replace(" ", "_")
    if key not in catalog and framework.upper() not in catalog:
        return {"error": f"Unknown framework: {framework}", "supported": list(catalog.keys())}
    data = catalog.get(key) or catalog.get(framework.upper())
    return {"framework": framework, "version": version, "requirements": data, "retrieved_at": _now()}


@mcp.tool()
def get_data_point_definitions(standard: str, topic: str = "") -> dict[str, Any]:
    """Return ESRS/CSRD data point definitions (sample subset)."""
    points = [
        {"id": "E1-1", "name": "Transition plan for climate change mitigation", "datatype": "narrative"},
        {"id": "E1-6", "name": "Gross Scope 1 GHG emissions", "datatype": "monetary/energy", "unit": "tCO2e"},
        {"id": "E1-7", "name": "Gross Scope 2 GHG emissions", "datatype": "monetary/energy", "unit": "tCO2e"},
    ]
    if topic:
        points = [p for p in points if topic.lower() in p["id"].lower() or topic.lower() in p["name"].lower()]
    return {"standard": standard, "data_points": points, "count": len(points)}


@mcp.tool()
def get_deadlines(jurisdiction: str, framework: str, fiscal_year: int) -> dict[str, Any]:
    """Return filing deadlines for jurisdiction and framework."""
    deadlines = {
        ("EU", "CSRD", 2025): {"publish": "2026-06-30", "assurance": "2026-09-30"},
        ("US", "SEC_CLIMATE", 2025): {"publish": "2026-03-31"},
    }
    key = (jurisdiction.upper()[:2] if len(jurisdiction) > 2 else jurisdiction.upper(), framework.upper(), fiscal_year)
    entry = deadlines.get(key, {"publish": "TBD", "note": "Consult official registry"})
    return {"jurisdiction": jurisdiction, "framework": framework, "fiscal_year": fiscal_year, "deadlines": entry}


@mcp.tool()
def get_jurisdiction_rules(jurisdiction: str) -> dict[str, Any]:
    """Return localization and reporting rules by jurisdiction."""
    rules = {
        "EU": {"localization": "GDPR", "language": ["en", "local"], "formats": ["XHTML", "iXBRL"]},
        "IN": {"localization": "DPDP", "data_residency": "sensitive_personal_data", "consent": "explicit"},
        "CN": {"localization": "PIPL", "data_residency": "critical/important_data", "security_assessment": True},
        "SA": {"localization": "PDPL", "data_residency": "personal_data", "cross_border": "adequacy_or_consent"},
    }
    code = jurisdiction.upper()
    return {"jurisdiction": code, "rules": rules.get(code, {"note": "No stub rules; escalate to legal"})}


@mcp.tool()
def search_regulatory_text(query: str, framework: str = "", limit: int = 5) -> dict[str, Any]:
    """Search mock regulatory text snippets."""
    corpus = [
        {"framework": "CSRD", "ref": "ESRS E1.6", "text": "The undertaking shall disclose gross Scope 1 GHG emissions in tonnes of CO2eq."},
        {"framework": "EU Taxonomy", "ref": "Annex I", "text": "Substantial contribution thresholds apply per activity in the delegated acts."},
        {"framework": "SFDR", "ref": "RTS Annex I", "text": "Principal adverse impacts on sustainability factors shall be disclosed."},
    ]
    hits = [c for c in corpus if query.lower() in c["text"].lower() or (framework and framework.lower() in c["framework"].lower())]
    return {"query": query, "results": hits[:limit], "total": len(hits)}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
'''
    schemas = {
        "tools": [
            {"name": "get_framework_requirements", "parameters": {"framework": "string", "version": "string"}},
            {"name": "get_data_point_definitions", "parameters": {"standard": "string", "topic": "string"}},
            {"name": "get_deadlines", "parameters": {"jurisdiction": "string", "framework": "string", "fiscal_year": "integer"}},
            {"name": "get_jurisdiction_rules", "parameters": {"jurisdiction": "string"}},
            {"name": "search_regulatory_text", "parameters": {"query": "string", "framework": "string", "limit": "integer"}},
        ]
    }
    return _server_spec("regulatory-db-server", "8001", impls, schemas)


def emissions_factor_server() -> dict:
    impls = '''
from mcp.common.kb_loader import load_json


@mcp.tool()
def get_emission_factor(source: str, activity: str) -> dict[str, Any]:
    """Look up emission factor from knowledge base."""
    data = load_json("emission_factors.json")
    matches = [f for f in data["factors"] if f["source"].lower() == source.lower() and activity.lower() in f["activity"].lower()]
    if not matches:
        return {"error": "Factor not found", "source": source, "activity": activity}
    return {"factor": matches[0], "metadata": data["metadata"]}


@mcp.tool()
def list_factor_sources() -> dict[str, Any]:
    """List available emission factor sources."""
    data = load_json("emission_factors.json")
    sources = sorted({f["source"] for f in data["factors"]})
    return {"sources": sources, "metadata": data["metadata"]}


@mcp.tool()
def get_gwp_values(standard: str = "IPCC AR6 GWP100") -> dict[str, Any]:
    """Return GWP values from knowledge base."""
    data = load_json("emission_factors.json")
    return {"standard": data["gwp"]["standard"], "values": data["gwp"]["values"]}


@mcp.tool()
def convert_units(value: float, from_unit: str, to_unit: str, substance: str = "CO2e") -> dict[str, Any]:
    """Convert common GHG units (mock conversion table)."""
    conversions = {
        ("tCO2e", "kgCO2e"): 1000.0,
        ("kgCO2e", "tCO2e"): 0.001,
        ("MMBtu", "kWh"): 293.071,
        ("kWh", "MMBtu"): 0.003412,
    }
    key = (from_unit, to_unit)
    if key not in conversions:
        return {"error": f"Unsupported conversion: {from_unit} -> {to_unit}"}
    converted = value * conversions[key]
    return {"input": value, "from_unit": from_unit, "to_unit": to_unit, "substance": substance, "output": converted}


@mcp.tool()
def get_grid_factors_by_country(country_code: str) -> dict[str, Any]:
    """Return grid emission factors by ISO country code."""
    data = load_json("emission_factors.json")
    code = country_code.upper()
    factor = data["grid_factors_by_country"].get(code)
    if not factor:
        return {"error": f"No grid factor for {code}", "available": list(data["grid_factors_by_country"].keys())}
    return {"country_code": code, "grid_factor": factor}
'''
    schemas = {"tools": [{"name": n} for n in [
        "get_emission_factor", "list_factor_sources", "get_gwp_values", "convert_units", "get_grid_factors_by_country"
    ]]}
    return _server_spec("emissions-factor-server", "8002", impls, schemas)


def taxonomy_criteria_server() -> dict:
    impls = '''
from mcp.common.kb_loader import load_json


@mcp.tool()
def get_tsc_for_activity(nace_code: str) -> dict[str, Any]:
    """Return Technical Screening Criteria for a NACE activity."""
    data = load_json("taxonomy_criteria.json")
    matches = [a for a in data["activities"] if a["nace"] == nace_code]
    if not matches:
        return {"error": f"No TSC for NACE {nace_code}"}
    return {"activity": matches[0]}


@mcp.tool()
def get_dnsh_criteria(nace_code: str, objective: str = "") -> dict[str, Any]:
    """Return Do No Significant Harm criteria for an activity."""
    data = load_json("taxonomy_criteria.json")
    matches = [a for a in data["activities"] if a["nace"] == nace_code]
    if not matches:
        return {"error": f"No DNSH data for NACE {nace_code}"}
    activity = matches[0]
    dnsh = activity.get("dnsh", [])
    if objective:
        dnsh = [d for d in dnsh if objective.lower() in d.lower()]
    return {"nace_code": nace_code, "dnsh_criteria": dnsh}


@mcp.tool()
def check_nace_eligibility(nace_code: str, revenue_pct: float, capex_pct: float, opex_pct: float) -> dict[str, Any]:
    """Check mock taxonomy alignment KPI thresholds."""
    aligned = revenue_pct >= 0 or capex_pct >= 0  # stub: always evaluate
    return {
        "nace_code": nace_code,
        "kpis": {"revenue_pct": revenue_pct, "capex_pct": capex_pct, "opex_pct": opex_pct},
        "eligible_for_reporting": True,
        "requires_human_review": True,
        "note": "Mock logic — SME must confirm substantial contribution and DNSH",
    }


@mcp.tool()
def get_minimum_safeguards() -> dict[str, Any]:
    """Return EU Taxonomy minimum safeguards list."""
    data = load_json("taxonomy_criteria.json")
    return {"minimum_safeguards": data["minimum_safeguards"]}


@mcp.tool()
def get_objective_thresholds(objective: str) -> dict[str, Any]:
    """Return environmental objective thresholds."""
    data = load_json("taxonomy_criteria.json")
    thresholds = data["objective_thresholds"].get(objective, {"note": "See delegated act annex"})
    return {"objective": objective, "thresholds": thresholds}
'''
    schemas = {"tools": [{"name": n} for n in [
        "get_tsc_for_activity", "get_dnsh_criteria", "check_nace_eligibility", "get_minimum_safeguards", "get_objective_thresholds"
    ]]}
    return _server_spec("taxonomy-criteria-server", "8003", impls, schemas)


def filing_submission_server() -> dict:
    impls = '''
@mcp.tool()
def submit_csrd_filing(entity_id: str, package_uri: str, human_approval_token: str) -> dict[str, Any]:
    """Submit CSRD filing stub — requires human approval token."""
    if not human_approval_token or human_approval_token == "PENDING":
        return {"status": "rejected", "reason": "Human approval token required"}
    filing_id = str(uuid.uuid4())
    return {
        "status": "accepted_stub",
        "filing_id": filing_id,
        "entity_id": entity_id,
        "package_uri": package_uri,
        "registry": "ESMA ESEF (mock)",
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def submit_sec_filing(cik: str, form_type: str, package_uri: str, human_approval_token: str) -> dict[str, Any]:
    """Submit SEC filing stub — requires human approval token."""
    if not human_approval_token or human_approval_token == "PENDING":
        return {"status": "rejected", "reason": "Human approval token required"}
    return {
        "status": "accepted_stub",
        "accession_number": f"0000320193-{datetime.now(timezone.utc).strftime('%y%m%d')}-000001",
        "cik": cik,
        "form_type": form_type,
        "package_uri": package_uri,
    }


@mcp.tool()
def validate_xbrl_tagging(instance_path: str, taxonomy: str = "ESRS") -> dict[str, Any]:
    """Validate XBRL tagging (mock validation)."""
    errors = []
    if not instance_path.endswith((".xhtml", ".xml", ".zip")):
        errors.append("Invalid instance extension")
    return {
        "instance_path": instance_path,
        "taxonomy": taxonomy,
        "valid": len(errors) == 0,
        "errors": errors,
        "facts_checked": 42,
    }


@mcp.tool()
def get_filing_status(filing_id: str) -> dict[str, Any]:
    """Return mock filing status."""
    return {"filing_id": filing_id, "status": "processing", "last_updated": datetime.now(timezone.utc).isoformat()}


@mcp.tool()
def generate_esef_package(report_html: str, taxonomy_version: str = "2024") -> dict[str, Any]:
    """Generate mock ESEF package descriptor."""
    package_id = str(uuid.uuid4())
    return {
        "package_id": package_id,
        "taxonomy_version": taxonomy_version,
        "artifacts": ["report.xhtml", "calculations.xml", "labels.json"],
        "report_size_bytes": len(report_html.encode("utf-8")),
        "human_review_required": True,
    }
'''
    schemas = {"tools": [{"name": n} for n in [
        "submit_csrd_filing", "submit_sec_filing", "validate_xbrl_tagging", "get_filing_status", "generate_esef_package"
    ]]}
    return _server_spec("filing-submission-server", "8004", impls, schemas)


def sanctions_screening_server() -> dict:
    impls = '''
@mcp.tool()
def screen_entity(name: str, country: str = "", identifiers: dict[str, str] | None = None) -> dict[str, Any]:
    """Screen entity against mock sanctions lists."""
    watchlist_hits = []
    high_risk_names = {"example sanctioned corp", "blocked industries ltd"}
    if name.lower() in high_risk_names:
        watchlist_hits.append({"list": "OFAC SDN (mock)", "match_score": 0.92})
    return {
        "entity": name,
        "country": country,
        "identifiers": identifiers or {},
        "hits": watchlist_hits,
        "risk_level": "high" if watchlist_hits else "low",
        "human_review_required": bool(watchlist_hits),
    }


@mcp.tool()
def check_pep_status(name: str, role: str = "") -> dict[str, Any]:
    """Check politically exposed person status (mock)."""
    pep = "minister" in role.lower() or "senator" in role.lower()
    return {"name": name, "role": role, "is_pep": pep, "source": "mock_pep_database"}


@mcp.tool()
def get_sanctions_lists(jurisdiction: str = "GLOBAL") -> dict[str, Any]:
    """List available sanctions lists."""
    lists = {
        "GLOBAL": ["OFAC SDN", "EU Consolidated", "UN Consolidated", "UK OFSI"],
        "US": ["OFAC SDN", "BIS Entity List"],
        "EU": ["EU Consolidated"],
    }
    key = jurisdiction.upper()
    return {"jurisdiction": key, "lists": lists.get(key, lists["GLOBAL"])}


@mcp.tool()
def monitor_entity_changes(entity_id: str, since: str = "") -> dict[str, Any]:
    """Return mock entity change events for ongoing monitoring."""
    return {
        "entity_id": entity_id,
        "since": since or "2026-01-01",
        "changes": [
            {"type": "address_update", "date": "2026-03-15"},
            {"type": "director_change", "date": "2026-04-02"},
        ],
    }


@mcp.tool()
def generate_screening_report(entity_ids: list[str]) -> dict[str, Any]:
    """Generate consolidated screening report."""
    report_id = str(uuid.uuid4())
    return {
        "report_id": report_id,
        "entity_count": len(entity_ids),
        "entities": entity_ids,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {"high_risk": 0, "medium_risk": 0, "low_risk": len(entity_ids)},
    }
'''
    schemas = {"tools": [{"name": n} for n in [
        "screen_entity", "check_pep_status", "get_sanctions_lists", "monitor_entity_changes", "generate_screening_report"
    ]]}
    return _server_spec("sanctions-screening-server", "8005", impls, schemas)


def _server_spec(dir_name: str, port: str, impls: str, schemas: dict) -> dict:
    server_py = MCP_SERVER_TEMPLATE.format(name=dir_name, port=port, tool_impls=impls)
    dockerfile = f"""FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY mcp/ /app/mcp/
COPY knowledge_base/ /app/knowledge_base/
ENV PYTHONPATH=/app
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT={port}
EXPOSE {port}
CMD ["python", "mcp/{dir_name}/server.py"]
"""
    return {"dir": dir_name, "server_py": server_py, "schemas": schemas, "dockerfile": dockerfile}


SKILL_TEMPLATE = """---
name: {name}
description: {description}
---

# {title}

## Scope

{scope}

## Mandatory constraints

- **Human-in-the-loop:** All final filings, legal assessments, and assurance conclusions require explicit human reviewer sign-off.
- **No guessing:** Do not invent emission factors, taxonomy percentages, materiality scores, or regulatory citations.
- **Provenance:** Every numeric output must cite source (MCP tool response, knowledge base version, or primary document).
- **PII:** Redact personal identifiers; enforce localization via `cross-border-data-transfer` when data leaves origin jurisdiction.

## Workflow

{workflow}

## MCP tools

{mcp_tools}

## Output artifacts

{artifacts}

## Anti-patterns

- Submitting filings without `/review` approval
- Using outdated emission factors without `list_factor_sources` verification
- Declaring taxonomy alignment without DNSH assessment
"""


def generate_skills() -> None:
    skills = [
        ("data-ingestion-validation", "data-ingestion-validation",
         "Maps CSRD 1,100+ Omnibus data points to ESRS schemas with validation rules. Use for CSRD ingestion, ESRS mapping, or Omnibus reconciliation.",
         "Skill 01: CSRD Omnibus Data Ingestion & Validation",
         "Ingest enterprise ESG datasets and map to CSRD/ESRS data points including Omnibus amendments.",
         "1. Load source schema inventory\n2. Call `get_data_point_definitions` for target ESRS topics\n3. Build field-level mapping with transformation rules\n4. Validate completeness against mandatory datapoints\n5. Flag gaps for human data steward review",
         "`regulatory-db-server`: get_data_point_definitions, get_framework_requirements, search_regulatory_text",
         "- `mapping_matrix.json`\n- `validation_report.md`\n- `gap_register.csv`"),
        ("ghg-emissions-calculation", "ghg-emissions-calculation",
         "Calculates Scope 1-3 GHG inventories, LCA impacts, and SBTi trajectory tracking. Use for GHG, carbon footprint, or SBTi requests.",
         "Skill 02: GHG Emissions Calculation",
         "Compute GHG inventories aligned with GHG Protocol and IPCC AR6 GWP100.",
         "1. Bound organizational inventory\n2. Fetch factors via `get_emission_factor` / `get_grid_factors_by_country`\n3. Apply GWP via `get_gwp_values`\n4. Aggregate scopes with `convert_units` consistency\n5. Compare against SBTi pathway (human validates targets)",
         "`emissions-factor-server`: all tools",
         "- `ghg_inventory.json`\n- `factor_provenance.json`\n- `sbti_gap_analysis.md`"),
        ("eu-taxonomy-alignment", "eu-taxonomy-alignment",
         "Assesses EU Taxonomy alignment using NACE codes, TSC, and DNSH. Use for taxonomy KPIs or green revenue.",
         "Skill 03: EU Taxonomy Alignment",
         "Evaluate substantial contribution, DNSH, and minimum safeguards for eligible activities.",
         "1. Map activities to NACE\n2. Retrieve TSC via `get_tsc_for_activity`\n3. Assess DNSH via `get_dnsh_criteria`\n4. Compute KPIs with `check_nace_eligibility`\n5. Document minimum safeguards",
         "`taxonomy-criteria-server`: all tools",
         "- `taxonomy_kpi_workbook.json`\n- `dnsh_checklist.md`"),
        ("double-materiality-assessment", "double-materiality-assessment",
         "Conducts double materiality scoring for impact and financial materiality. Use for CSRD materiality or DMA workshops.",
         "Skill 04: Double Materiality Assessment",
         "Score sustainability matters on impact and financial materiality axes.",
         "1. Identify IROs (impacts, risks, opportunities)\n2. Score impact and financial dimensions (1-5 scale with evidence)\n3. Apply threshold matrix — do not auto-set material topics\n4. Human workshop validation required",
         "`regulatory-db-server`: get_framework_requirements, search_regulatory_text",
         "- `materiality_matrix.json`\n- `iro_register.md`"),
        ("sfdr-pai-computation", "sfdr-pai-computation",
         "Computes SFDR mandatory PAIs and product classification Articles 6/8/9. Use for SFDR disclosures or PAI statements.",
         "Skill 05: SFDR PAI Computation",
         "Calculate 18 mandatory principal adverse impact indicators.",
         "1. Confirm product classification (Art. 6/8/9) with legal review\n2. Gather investee data\n3. Compute PAIs with documented formulas\n4. Reconcile to RTS Annex I tables",
         "`regulatory-db-server`: get_framework_requirements; `emissions-factor-server`: get_emission_factor",
         "- `pai_statement.json`\n- `product_classification_memo.md`"),
        ("audit-trail-reporting", "audit-trail-reporting",
         "Manages iXBRL/ESEF tagging and immutable audit logs to DynamoDB/S3/Glacier. Use for ESEF packages or audit trails.",
         "Skill 06: Audit Trail & Reporting",
         "Produce tagged reports and immutable audit evidence chains.",
         "1. Generate ESEF package via `generate_esef_package`\n2. Validate tagging via `validate_xbrl_tagging`\n3. Hash artifacts (SHA-256) and log to audit store\n4. Apply Glacier lifecycle for 7+ year retention",
         "`filing-submission-server`: validate_xbrl_tagging, generate_esef_package, get_filing_status",
         "- `audit_manifest.json`\n- `ixbrl_validation_report.json`"),
        ("regulatory-change-monitor", "regulatory-change-monitor",
         "Tracks global ESG regulatory deadlines and framework updates. Use for deadline calendars or regulatory change alerts.",
         "Skill 07: Regulatory Change Monitor",
         "Maintain deadline calendar and framework change log.",
         "1. Pull deadlines via `get_deadlines`\n2. Monitor ESRS/CSRD/SFDR updates via `search_regulatory_text`\n3. Publish change log with effective dates\n4. Notify owners — no autonomous policy changes",
         "`regulatory-db-server`: get_deadlines, search_regulatory_text, get_framework_requirements",
         "- `deadline_calendar.ics`\n- `regulatory_changelog.md`"),
        ("supply-chain-due-diligence", "supply-chain-due-diligence",
         "Assesses CSDDD and UFLPA supply chain risk with entity screening. Use for due diligence or supplier onboarding.",
         "Skill 08: Supply Chain Due Diligence",
         "Screen suppliers and assess CSDDD/UFLPA composite risk.",
         "1. Collect supplier master data\n2. Screen via `screen_entity` and `check_pep_status`\n3. Monitor changes via `monitor_entity_changes`\n4. Generate `generate_screening_report` for human review",
         "`sanctions-screening-server`: all tools",
         "- `supplier_risk_register.json`\n- `screening_report.pdf` (human approved)"),
        ("biodiversity-tnfd-analytics", "biodiversity-tnfd-analytics",
         "Applies TNFD LEAP approach with MSA and BII metrics. Use for nature-related disclosures or TNFD reports.",
         "Skill 09: Biodiversity & TNFD Analytics",
         "Execute LEAP (Locate, Evaluate, Assess, Prepare) with biodiversity metrics.",
         "1. Locate interface with nature\n2. Evaluate dependencies and impacts\n3. Assess MSA/BII indicators (mock analytics OK with provenance)\n4. Prepare disclosure aligned to TNFD recommendations",
         "`emissions-factor-server`: convert_units; `regulatory-db-server`: search_regulatory_text",
         "- `tnfd_leap_assessment.json`\n- `biodiversity_metrics.csv`"),
        ("cross-border-data-transfer", "cross-border-data-transfer",
         "Enforces India DPDP, China PIPL, and Saudi PDPL data localization rules. Use before cross-border ESG data transfers.",
         "Skill 10: Cross-Border Data Transfer",
         "Validate localization, consent, and transfer mechanisms before data leaves jurisdiction.",
         "1. Classify data categories and origin jurisdiction\n2. Fetch rules via `get_jurisdiction_rules`\n3. Block transfers failing residency requirements\n4. Document legal mechanism (SCC, adequacy, consent) — human legal sign-off",
         "`regulatory-db-server`: get_jurisdiction_rules",
         "- `transfer_impact_assessment.json`\n- `localization_decision_log.md`"),
    ]
    for args in skills:
        content = SKILL_TEMPLATE.format(
            name=args[0], description=args[2], title=args[3], scope=args[4],
            workflow=args[5], mcp_tools=args[6], artifacts=args[7],
        )
        write(f"skills/{args[1]}/SKILL.md", content)


def generate_orchestration() -> None:
    write(
        "orchestration/__init__.py",
        '"""Supervisor-worker orchestration for ESG compliance agents."""\n',
    )
    write(
        "orchestration/mcp_client.py",
        '''"""Lightweight MCP SSE client for orchestration agents."""

from __future__ import annotations

import json
import os
from typing import Any

import httpx

DEFAULT_URLS = {
    "regulatory": os.getenv("MCP_REGULATORY_URL", "http://127.0.0.1:8001/sse"),
    "emissions": os.getenv("MCP_EMISSIONS_URL", "http://127.0.0.1:8002/sse"),
    "taxonomy": os.getenv("MCP_TAXONOMY_URL", "http://127.0.0.1:8003/sse"),
    "filing": os.getenv("MCP_FILING_URL", "http://127.0.0.1:8004/sse"),
    "sanctions": os.getenv("MCP_SANCTIONS_URL", "http://127.0.0.1:8005/sse"),
}


class MCPClient:
    """HTTP helper for MCP servers — uses direct REST fallback for local dev."""

    def __init__(self, base_url: str | None = None, server: str = "regulatory") -> None:
        self.base_url = base_url or DEFAULT_URLS[server]
        self.server = server

    async def call_tool(self, tool: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        """Invoke tool via local Python import fallback when SSE unavailable."""
        arguments = arguments or {}
        module_map = {
            "regulatory": "regulatory-db-server",
            "emissions": "emissions-factor-server",
            "taxonomy": "taxonomy-criteria-server",
            "filing": "filing-submission-server",
            "sanctions": "sanctions-screening-server",
        }
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(
                    self.base_url.replace("/sse", "/messages"),
                    json={"method": "tools/call", "params": {"name": tool, "arguments": arguments}},
                )
                if resp.status_code == 200:
                    return resp.json()
        except (httpx.HTTPError, OSError):
            pass
        return _invoke_local_tool(module_map[self.server], tool, arguments)


def _invoke_local_tool(server_dir: str, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
    import importlib.util
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    server_path = root / "mcp" / server_dir / "server.py"
    spec = importlib.util.spec_from_file_location(f"mcp_{server_dir.replace('-', '_')}", server_path)
    if spec is None or spec.loader is None:
        return {"error": f"Cannot load server: {server_path}"}
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn = getattr(mod, tool, None)
    if fn is None:
        return {"error": f"Tool {tool} not found in {server_dir}"}
    result = fn(**arguments)
    return {"content": result}


async def call_mcp(server: str, tool: str, **kwargs: Any) -> dict[str, Any]:
    client = MCPClient(server=server)
    return await client.call_tool(tool, kwargs)
''',
    )
    write(
        "orchestration/supervisor_agent.py",
        '''"""Supervisor agent — routes ESG tasks to specialized workers."""

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
''',
    )
    for name, skills, module in [
        ("compliance_checker_agent", ["data-ingestion-validation", "double-materiality-assessment"], "compliance"),
        ("disclosure_agent", ["eu-taxonomy-alignment", "sfdr-pai-computation", "audit-trail-reporting"], "disclosure"),
        ("calculation_agent", ["ghg-emissions-calculation", "biodiversity-tnfd-analytics"], "calculation"),
        ("monitoring_agent", ["regulatory-change-monitor", "supply-chain-due-diligence", "cross-border-data-transfer"], "monitoring"),
    ]:
        class_name = "".join(p.capitalize() for p in name.split("_"))
        write(
            f"orchestration/{name}.py",
            f'''"""Worker agent: {name.replace("_", " ")}."""

from __future__ import annotations

from typing import Any

from orchestration.mcp_client import call_mcp

SKILLS = {skills!r}


class {class_name}:
    """Handles tasks using skills: {", ".join(skills)}."""

    async def run(self, task: str) -> dict[str, Any]:
        tool_result = await self._invoke_primary_tool(task)
        return {{
            "agent": "{name}",
            "skills": SKILLS,
            "task": task,
            "tool_result": tool_result,
            "human_review_required": True,
        }}

    async def _invoke_primary_tool(self, task: str) -> dict[str, Any]:
        raise NotImplementedError
''',
        )
    # Patch each worker with concrete tool invocation
    write(
        "orchestration/compliance_checker_agent.py",
        '''"""Worker agent: compliance checker."""

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
''',
    )
    write(
        "orchestration/disclosure_agent.py",
        '''"""Worker agent: disclosure."""

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
''',
    )
    write(
        "orchestration/calculation_agent.py",
        '''"""Worker agent: calculation."""

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
''',
    )
    write(
        "orchestration/monitoring_agent.py",
        '''"""Worker agent: monitoring."""

from __future__ import annotations

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
        return {"agent": "monitoring_agent", "skills": SKILLS, "task": task, "tool_result": tool_result, "human_review_required": True}
''',
    )


def generate_infrastructure() -> None:
    write(
        "infrastructure/requirements.txt",
        "aws-cdk-lib>=2.170.0\nconstructs>=10.4.0\n",
    )
    write(
        "infrastructure/cdk.json",
        json.dumps({
            "app": "python app.py",
            "watch": {"include": ["**"], "exclude": ["README.md", "cdk*.json", "**/__pycache__", "**/*.pyc"]},
            "context": {"@aws-cdk/core:stackRelativeExports": True},
        }, indent=2) + "\n",
    )
    write("infrastructure/app.py", INFRA_APP)
    write("infrastructure/esg_compliance_stack.py", INFRA_STACK)


INFRA_APP = '''#!/usr/bin/env python3
"""AWS CDK app entry for ESG compliance MCP infrastructure."""

import aws_cdk as cdk
from esg_compliance_stack import EsgComplianceStack

app = cdk.App()

# Primary stack — replicate per region for multi-region deployment
EsgComplianceStack(
    app,
    "EsgComplianceStack-EU",
    env=cdk.Environment(account="123456789012", region="eu-west-1"),
    stack_suffix="eu-west-1",
)

app.synth()
'''

INFRA_STACK = '''"""AWS CDK stack: ECS Fargate MCP servers, ALB, DynamoDB, S3, OpenSearch Serverless.

Multi-region deployment targets (deploy separate stacks per region):
  - eu-west-1      : EU CSRD / ESEF primary
  - us-east-1      : SEC climate / SFDR US operations
  - ap-south-1     : India DPDP localization
  - ap-southeast-1 : APAC supply-chain due diligence
  - me-south-1     : Saudi PDPL / Middle East workloads
"""

from __future__ import annotations

from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_dynamodb as dynamodb,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticloadbalancingv2 as elbv2,
    aws_opensearchserverless as opensearchserverless,
    aws_s3 as s3,
)
from constructs import Construct

MCP_SERVICES = [
    {"name": "regulatory-db", "port": 8001},
    {"name": "emissions-factor", "port": 8002},
    {"name": "taxonomy-criteria", "port": 8003},
    {"name": "filing-submission", "port": 8004},
    {"name": "sanctions-screening", "port": 8005},
]


class EsgComplianceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, stack_suffix: str = "primary", **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "EsgVpc", max_azs=2, nat_gateways=1)

        cluster = ecs.Cluster(self, "McpCluster", vpc=vpc, container_insights=True)

        audit_table = dynamodb.Table(
            self,
            "AuditLogTable",
            partition_key=dynamodb.Attribute(name="pk", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="sk", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN,
            point_in_time_recovery=True,
        )

        audit_bucket = s3.Bucket(
            self,
            "AuditArchiveBucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.RETAIN,
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="GlacierDeepArchiveAfter1Year",
                    enabled=True,
                    transitions=[
                        s3.Transition(storage_class=s3.StorageClass.GLACIER, transition_after=Duration.days(90)),
                        s3.Transition(
                            storage_class=s3.StorageClass.DEEP_ARCHIVE,
                            transition_after=Duration.days(365),
                        ),
                    ],
                    expiration=Duration.days(365 * 8),
                )
            ],
        )

        collection = opensearchserverless.CfnCollection(
            self,
            "RegulatoryKnowledgeBase",
            name=f"esg-reg-kb-{stack_suffix}",
            type="VECTORSEARCH",
            description="Regulatory knowledge base for ESG MCP servers",
        )

        alb = elbv2.ApplicationLoadBalancer(
            self,
            "McpAlb",
            vpc=vpc,
            internet_facing=True,
        )
        listener = alb.add_listener("HttpListener", port=80, open=True)

        for idx, svc in enumerate(MCP_SERVICES):
            fargate = ecs_patterns.ApplicationLoadBalancedFargateService(
                self,
                f"McpService{svc['name'].replace('-', '').title()}",
                cluster=cluster,
                cpu=256,
                memory_limit_mib=512,
                desired_count=1,
                public_load_balancer=False,
                task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                    image=ecs.ContainerImage.from_registry("python:3.11-slim"),
                    container_port=svc["port"],
                    environment={
                        "MCP_PORT": str(svc["port"]),
                        "MCP_HOST": "0.0.0.0",
                        "AUDIT_TABLE": audit_table.table_name,
                        "AUDIT_BUCKET": audit_bucket.bucket_name,
                    },
                ),
            )
            target_group = elbv2.ApplicationTargetGroup(
                self,
                f"Tg{idx}",
                vpc=vpc,
                port=svc["port"],
                targets=[fargate.service],
                health_check=elbv2.HealthCheck(path="/sse", healthy_http_codes="200-499"),
            )
            listener.add_action(
                f"Route{svc['name']}",
                priority=idx + 1,
                conditions=[elbv2.ListenerCondition.path_patterns([f"/{svc['name']}/*"])],
                action=elbv2.ListenerAction.forward([target_group]),
            )
            audit_table.grant_read_write_data(fargate.task_definition.task_role)
            audit_bucket.grant_read_write(fargate.task_definition.task_role)

        from aws_cdk import CfnOutput

        CfnOutput(self, "AlbDns", value=alb.load_balancer_dns_name)
        CfnOutput(self, "AuditTableName", value=audit_table.table_name)
        CfnOutput(self, "AuditBucketName", value=audit_bucket.bucket_name)
        CfnOutput(self, "OpenSearchCollection", value=collection.attr_arn)
'''


def generate_tests() -> None:
    write(
        "tests/__init__.py",
        "",
    )
    write(
        "tests/test_knowledge_base.py",
        '''"""Knowledge base stub tests."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_emission_factors_loads():
    data = json.loads((ROOT / "knowledge_base" / "emission_factors.json").read_text())
    assert "factors" in data
    assert "gwp" in data


def test_taxonomy_criteria_loads():
    data = json.loads((ROOT / "knowledge_base" / "taxonomy_criteria.json").read_text())
    assert "activities" in data
''',
    )
    write(
        "tests/test_mcp_tools.py",
        '''"""MCP tool unit tests (local import)."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_server(server_dir: str):
    path = ROOT / "mcp" / server_dir / "server.py"
    spec = importlib.util.spec_from_file_location(server_dir, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_regulatory_framework_requirements():
    mod = _load_server("regulatory-db-server")
    result = mod.get_framework_requirements("CSRD")
    assert "requirements" in result


def test_emissions_gwp():
    mod = _load_server("emissions-factor-server")
    result = mod.get_gwp_values()
    assert "values" in result
    assert result["values"]["CO2"] == 1.0


def test_filing_requires_approval():
    mod = _load_server("filing-submission-server")
    result = mod.submit_csrd_filing("entity-1", "s3://pkg", "PENDING")
    assert result["status"] == "rejected"
''',
    )
    write(
        "tests/test_supervisor_routing.py",
        '''"""Supervisor routing tests."""

from orchestration.supervisor_agent import SupervisorAgent


def test_routes_ghg_to_calculation():
    s = SupervisorAgent()
    assert s.route("Calculate Scope 2 GHG emissions") == "calculation"


def test_routes_csrd_to_compliance():
    s = SupervisorAgent()
    assert s.route("CSRD Omnibus data mapping") == "compliance"
''',
    )


def generate_github() -> None:
    write(
        ".github/workflows/ci.yml",
        """name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: python scripts/validate-skills.py
      - run: pytest tests/ -v
      - run: ruff check .
""",
    )
    write(
        ".github/PULL_REQUEST_TEMPLATE.md",
        """## Summary

## Framework coverage

## Test plan
- [ ] `pytest tests/ -v`
- [ ] `python scripts/validate-skills.py`
""",
    )


def generate_docs() -> None:
    write(
        "docs/architecture.md",
        """# Architecture

## Components

1. **Skills** — Progressive-disclosure agent instructions in `skills/`
2. **MCP servers** — FastMCP SSE tool servers in `mcp/`
3. **Orchestration** — Supervisor-worker routing in `orchestration/`
4. **Knowledge base** — JSON stubs synced to OpenSearch Serverless in production
5. **Infrastructure** — AWS CDK stack in `infrastructure/`

## Data flow

User request → Supervisor → Worker agent → MCP tools → Knowledge base / AWS persistence
""",
    )
    write(
        "docs/getting-started.md",
        """# Getting Started

1. Run `bootstrap.sh` or `bootstrap.ps1`
2. Start MCP servers on ports 8001–8005
3. Run `python -m orchestration.supervisor_agent "your task"`
4. Follow lifecycle commands in AGENTS.md
""",
    )


if __name__ == "__main__":
    main()
