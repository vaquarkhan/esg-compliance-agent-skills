---
name: cross-border-data-transfer
description: Enforces India DPDP, China PIPL, and Saudi PDPL data localization rules. Use before cross-border ESG data transfers.
---

# Skill 10: Cross-Border Data Transfer

## Scope

Validate localization, consent, and transfer mechanisms before data leaves jurisdiction.

## Mandatory constraints

- **Human-in-the-loop:** All final filings, legal assessments, and assurance conclusions require explicit human reviewer sign-off.
- **No guessing:** Do not invent emission factors, taxonomy percentages, materiality scores, or regulatory citations.
- **Provenance:** Every numeric output must cite source (MCP tool response, knowledge base version, or primary document).
- **PII:** Redact personal identifiers; enforce localization via `cross-border-data-transfer` when data leaves origin jurisdiction.

## Workflow

1. Classify data categories and origin jurisdiction
2. Fetch rules via `get_jurisdiction_rules`
3. Block transfers failing residency requirements
4. Document legal mechanism (SCC, adequacy, consent) — human legal sign-off

## MCP tools

`regulatory-db-server`: get_jurisdiction_rules

## Output artifacts

- `transfer_impact_assessment.json`
- `localization_decision_log.md`

## Anti-patterns

- Submitting filings without `/review` approval
- Using outdated emission factors without `list_factor_sources` verification
- Declaring taxonomy alignment without DNSH assessment
