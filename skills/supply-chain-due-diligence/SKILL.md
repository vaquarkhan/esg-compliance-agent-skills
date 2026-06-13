---
name: supply-chain-due-diligence
description: Assesses CSDDD and UFLPA supply chain risk with entity screening. Use for due diligence or supplier onboarding.
---

# Skill 08: Supply Chain Due Diligence

## Scope

Screen suppliers and assess CSDDD/UFLPA composite risk.

## Mandatory constraints

- **Human-in-the-loop:** All final filings, legal assessments, and assurance conclusions require explicit human reviewer sign-off.
- **No guessing:** Do not invent emission factors, taxonomy percentages, materiality scores, or regulatory citations.
- **Provenance:** Every numeric output must cite source (MCP tool response, knowledge base version, or primary document).
- **PII:** Redact personal identifiers; enforce localization via `cross-border-data-transfer` when data leaves origin jurisdiction.

## Workflow

1. Collect supplier master data
2. Screen via `screen_entity` and `check_pep_status`
3. Monitor changes via `monitor_entity_changes`
4. Generate `generate_screening_report` for human review

## MCP tools

`sanctions-screening-server`: all tools

## Output artifacts

- `supplier_risk_register.json`
- `screening_report.pdf` (human approved)

## Anti-patterns

- Submitting filings without `/review` approval
- Using outdated emission factors without `list_factor_sources` verification
- Declaring taxonomy alignment without DNSH assessment
