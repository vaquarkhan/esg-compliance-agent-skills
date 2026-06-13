# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- **Full lifecycle E2E pipeline** — `scripts/e2e_pipeline.py` and `scripts/lifecycle/{spec,plan,build,validate,review,ship}.py`
- **Attestation validation** — `scripts/validate-attestation.py` + CI enforcement
- **LLM planner orchestration** — `orchestration/planner_agent.py` (`ESG_ORCHESTRATION_MODE=planner`)
- **Domain attestation envelope** — `orchestration/attestation.py`, `knowledge_base/attestation_schema.json`
- **Pure MCP logic modules** — `mcp/common/emissions_logic.py`, `mcp/common/filing_logic.py` (no FastMCP import for examples/E2E)

### Changed

- GHG and CSRD examples use knowledge-base logic directly (no MCP server boot required)
- Default supervisor explicitly labeled deterministic; workers carry pending assurance
- Makefile: `make e2e`, `make test-all`; CI runs full lifecycle + attestation checks
- Lifecycle slash commands wired to runnable scripts with assurance gates

## [1.0.0] - 2026-06-13

### Summary

- CI: Ruff lint/format, mypy, pip-audit, Bandit, detect-secrets, CodeQL, pytest coverage gate (≥80% on `agent.py` + `redaction.py`)
- Locked dependencies via `requirements-lock.txt` (pip-tools)
- Dependabot, pre-commit hooks, CODEOWNERS, issue/PR templates
- Docs: architecture, redaction limitations, SME review cadence, plugin publishing, coverage roadmap
- Examples: CSRD E1 mapping with scope validator
- IDE plugins: VS Code (.vsix) and JetBrains (.zip) scaffold
- 10 ESG skills, 5 MCP SSE servers, three-tier orchestration (deterministic / planner / agent), AWS CDK stack

### Install plugins locally

**VS Code:** Extensions → ⋯ → Install from VSIX → select `esg-compliance-agent-skills-1.0.0.vsix`

**JetBrains:** Settings → Plugins → ⚙ → Install Plugin from Disk → select `ESG Compliance Agent Skills-1.0.0.zip`

### Marketplace publish

See [docs/plugin-publishing.md](docs/plugin-publishing.md) for manual VS Code Marketplace and JetBrains Marketplace steps.
