---
name: audit-trail-reporting
description: Manages iXBRL/ESEF tagging and immutable audit logs to DynamoDB/S3/Glacier. Use for ESEF packages or audit trails.
---

# Skill 06: Audit Trail & Reporting

## Scope

Produce tagged reports and immutable audit evidence chains.

## Mandatory constraints

- **Human-in-the-loop:** All final filings, legal assessments, and assurance conclusions require explicit human reviewer sign-off.
- **No guessing:** Do not invent emission factors, taxonomy percentages, materiality scores, or regulatory citations.
- **Provenance:** Every numeric output must cite source (MCP tool response, knowledge base version, or primary document).
- **PII:** Redact personal identifiers; enforce localization via `cross-border-data-transfer` when data leaves origin jurisdiction.

## Workflow

1. Generate ESEF package via `generate_esef_package`
2. Validate tagging via `validate_xbrl_tagging`
3. Hash artifacts (SHA-256) and log to audit store
4. Apply Glacier lifecycle for 7+ year retention

## MCP tools

`filing-submission-server`: validate_xbrl_tagging, generate_esef_package, get_filing_status

## Output artifacts

- `audit_manifest.json`
- `ixbrl_validation_report.json`

## Anti-patterns

- Submitting filings without `/review` approval
- Using outdated emission factors without `list_factor_sources` verification
- Declaring taxonomy alignment without DNSH assessment
