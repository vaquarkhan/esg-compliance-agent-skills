---
name: regulatory-change-monitor
description: Tracks global ESG regulatory deadlines and framework updates. Use for deadline calendars or regulatory change alerts.
---

# Skill 07: Regulatory Change Monitor

## Scope

Maintain deadline calendar and framework change log.

## Mandatory constraints

- **Human-in-the-loop:** All final filings, legal assessments, and assurance conclusions require explicit human reviewer sign-off.
- **No guessing:** Do not invent emission factors, taxonomy percentages, materiality scores, or regulatory citations.
- **Provenance:** Every numeric output must cite source (MCP tool response, knowledge base version, or primary document).
- **PII:** Redact personal identifiers; enforce localization via `cross-border-data-transfer` when data leaves origin jurisdiction.

## Workflow

1. Pull deadlines via `get_deadlines`
2. Monitor ESRS/CSRD/SFDR updates via `search_regulatory_text`
3. Publish change log with effective dates
4. Notify owners — no autonomous policy changes

## MCP tools

`regulatory-db-server`: get_deadlines, search_regulatory_text, get_framework_requirements

## Output artifacts

- `deadline_calendar.ics`
- `regulatory_changelog.md`

## Anti-patterns

- Submitting filings without `/review` approval
- Using outdated emission factors without `list_factor_sources` verification
- Declaring taxonomy alignment without DNSH assessment
