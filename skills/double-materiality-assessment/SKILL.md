---
name: double-materiality-assessment
description: Conducts double materiality scoring for impact and financial materiality. Use for CSRD materiality or DMA workshops.
---

# Skill 04: Double Materiality Assessment

## Scope

Score sustainability matters on impact and financial materiality axes.

## Mandatory constraints

- **Human-in-the-loop:** All final filings, legal assessments, and assurance conclusions require explicit human reviewer sign-off.
- **No guessing:** Do not invent emission factors, taxonomy percentages, materiality scores, or regulatory citations.
- **Provenance:** Every numeric output must cite source (MCP tool response, knowledge base version, or primary document).
- **PII:** Redact personal identifiers; enforce localization via `cross-border-data-transfer` when data leaves origin jurisdiction.

## Workflow

1. Identify IROs (impacts, risks, opportunities)
2. Score impact and financial dimensions (1-5 scale with evidence)
3. Apply threshold matrix — do not auto-set material topics
4. Human workshop validation required

## MCP tools

`regulatory-db-server`: get_framework_requirements, search_regulatory_text

## Output artifacts

- `materiality_matrix.json`
- `iro_register.md`

## Anti-patterns

- Submitting filings without `/review` approval
- Using outdated emission factors without `list_factor_sources` verification
- Declaring taxonomy alignment without DNSH assessment
