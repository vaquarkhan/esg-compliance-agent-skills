---
name: biodiversity-tnfd-analytics
description: Applies TNFD LEAP approach with MSA and BII metrics. Use for nature-related disclosures or TNFD reports.
---

# Skill 09: Biodiversity & TNFD Analytics

## Scope

Execute LEAP (Locate, Evaluate, Assess, Prepare) with biodiversity metrics.

## Mandatory constraints

- **Human-in-the-loop:** All final filings, legal assessments, and assurance conclusions require explicit human reviewer sign-off.
- **No guessing:** Do not invent emission factors, taxonomy percentages, materiality scores, or regulatory citations.
- **Provenance:** Every numeric output must cite source (MCP tool response, knowledge base version, or primary document).
- **PII:** Redact personal identifiers; enforce localization via `cross-border-data-transfer` when data leaves origin jurisdiction.

## Workflow

1. Locate interface with nature
2. Evaluate dependencies and impacts
3. Assess MSA/BII indicators (mock analytics OK with provenance)
4. Prepare disclosure aligned to TNFD recommendations

## MCP tools

`emissions-factor-server`: convert_units; `regulatory-db-server`: search_regulatory_text

## Output artifacts

- `tnfd_leap_assessment.json`
- `biodiversity_metrics.csv`

## Anti-patterns

- Submitting filings without `/review` approval
- Using outdated emission factors without `list_factor_sources` verification
- Declaring taxonomy alignment without DNSH assessment
