---
name: data-ingestion-validation
description: Maps CSRD 1,100+ Omnibus data points to ESRS schemas with validation rules. Use for CSRD ingestion, ESRS mapping, or Omnibus reconciliation.
---

# Skill 01: CSRD Omnibus Data Ingestion & Validation

## Scope

Ingest enterprise ESG datasets and map to CSRD/ESRS data points including Omnibus amendments.

## Mandatory constraints

- **Human-in-the-loop:** All final filings, legal assessments, and assurance conclusions require explicit human reviewer sign-off.
- **No guessing:** Do not invent emission factors, taxonomy percentages, materiality scores, or regulatory citations.
- **Provenance:** Every numeric output must cite source (MCP tool response, knowledge base version, or primary document).
- **PII:** Redact personal identifiers; enforce localization via `cross-border-data-transfer` when data leaves origin jurisdiction.

## Workflow

1. Load source schema inventory
2. Call `get_data_point_definitions` for target ESRS topics
3. Build field-level mapping with transformation rules
4. Validate completeness against mandatory datapoints
5. Flag gaps for human data steward review

## MCP tools

`regulatory-db-server`: get_data_point_definitions, get_framework_requirements, search_regulatory_text

## Output artifacts

- `mapping_matrix.json`
- `validation_report.md`
- `gap_register.csv`

## Anti-patterns

- Submitting filings without `/review` approval
- Using outdated emission factors without `list_factor_sources` verification
- Declaring taxonomy alignment without DNSH assessment
