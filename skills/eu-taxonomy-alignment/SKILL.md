---
name: eu-taxonomy-alignment
description: Assesses EU Taxonomy alignment using NACE codes, TSC, and DNSH. Use for taxonomy KPIs or green revenue.
---

# Skill 03: EU Taxonomy Alignment

## Scope

Evaluate substantial contribution, DNSH, and minimum safeguards for eligible activities.

## Mandatory constraints

- **Human-in-the-loop:** All final filings, legal assessments, and assurance conclusions require explicit human reviewer sign-off.
- **No guessing:** Do not invent emission factors, taxonomy percentages, materiality scores, or regulatory citations.
- **Provenance:** Every numeric output must cite source (MCP tool response, knowledge base version, or primary document).
- **PII:** Redact personal identifiers; enforce localization via `cross-border-data-transfer` when data leaves origin jurisdiction.

## Workflow

1. Map activities to NACE
2. Retrieve TSC via `get_tsc_for_activity`
3. Assess DNSH via `get_dnsh_criteria`
4. Compute KPIs with `check_nace_eligibility`
5. Document minimum safeguards

## MCP tools

`taxonomy-criteria-server`: all tools

## Output artifacts

- `taxonomy_kpi_workbook.json`
- `dnsh_checklist.md`

## Anti-patterns

- Submitting filings without `/review` approval
- Using outdated emission factors without `list_factor_sources` verification
- Declaring taxonomy alignment without DNSH assessment
