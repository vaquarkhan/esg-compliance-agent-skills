---
name: sfdr-pai-computation
description: Computes SFDR mandatory PAIs and product classification Articles 6/8/9. Use for SFDR disclosures or PAI statements.
---

# Skill 05: SFDR PAI Computation

## Scope

Calculate 18 mandatory principal adverse impact indicators.

## Mandatory constraints

- **Human-in-the-loop:** All final filings, legal assessments, and assurance conclusions require explicit human reviewer sign-off.
- **No guessing:** Do not invent emission factors, taxonomy percentages, materiality scores, or regulatory citations.
- **Provenance:** Every numeric output must cite source (MCP tool response, knowledge base version, or primary document).
- **PII:** Redact personal identifiers; enforce localization via `cross-border-data-transfer` when data leaves origin jurisdiction.

## Workflow

1. Confirm product classification (Art. 6/8/9) with legal review
2. Gather investee data
3. Compute PAIs with documented formulas
4. Reconcile to RTS Annex I tables

## MCP tools

`regulatory-db-server`: get_framework_requirements; `emissions-factor-server`: get_emission_factor

## Output artifacts

- `pai_statement.json`
- `product_classification_memo.md`

## Anti-patterns

- Submitting filings without `/review` approval
- Using outdated emission factors without `list_factor_sources` verification
- Declaring taxonomy alignment without DNSH assessment
