# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-06-13

### Summary

- CI: Ruff lint/format, mypy, pip-audit, Bandit, detect-secrets, CodeQL, pytest coverage gate (≥80% on `agent.py` + `redaction.py`)
- Locked dependencies via `requirements-lock.txt` (pip-tools)
- Dependabot, pre-commit hooks, CODEOWNERS, issue/PR templates
- Docs: architecture, redaction limitations, SME review cadence, plugin publishing, coverage roadmap
- Examples: CSRD E1 mapping with scope validator
- IDE plugins: VS Code (.vsix) and JetBrains (.zip) scaffold
- 10 ESG skills, 5 MCP SSE servers, Supervisor-Worker orchestration, AWS CDK stack

### Install plugins locally

**VS Code:** Extensions → ⋯ → Install from VSIX → select `esg-compliance-agent-skills-1.0.0.vsix`

**JetBrains:** Settings → Plugins → ⚙ → Install Plugin from Disk → select `ESG Compliance Agent Skills-1.0.0.zip`

### Marketplace publish

See [docs/plugin-publishing.md](docs/plugin-publishing.md) for manual VS Code Marketplace and JetBrains Marketplace steps.
