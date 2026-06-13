---
name: regulatory-change-monitor
description: Tracks global ESG regulatory deadlines, ESRS/Omnibus/SFDR updates, and APAC LATAM MENA mandatory dates from jurisdiction stubs. Use for deadline calendars, regulatory changelog, or compliance horizon scanning.
---

# Skill 07: Regulatory Change Monitor

## Overview

Maintains **deadline calendar** and **regulatory changelog** across EU, US, APAC, LATAM, and MENA using MCP + `knowledge_base/jurisdiction_reporting.json`.

## When to Use

- Building `deadline_calendar.ics`
- Horizon scanning for CSRD Omnibus, SEC climate, SGX, ASRS, BRSR, CVM 193, UAE SCA, Tadawul
- Triggering `/backfill` when rules change

## Mandatory constraints

- **Human-in-the-loop:** Agent publishes **draft** changelog; compliance officer approves.
- **No guessing:** Verify dates against official gazettes — stubs are starting points only.
- **Provenance:** Cite source URL + effective date per entry.

## Core process

### Step 1 — Pull deadlines

`get_deadlines(jurisdiction, framework, fiscal_year)` for each in-scope entity.

### Step 2 — Jurisdiction overlay

Load `jurisdiction_reporting.json` for APAC/LATAM/MENA mandatory phases (e.g., BRSR assurance rollout, Tadawul 2025/2027).

### Step 3 — Monitor text changes

`search_regulatory_text(query, framework)` — diff against prior changelog version.

### Step 4 — Impact assessment

Map changes to affected skills (01–10) and open `/plan` tasks.

### Step 5 — Publish

`regulatory_changelog.md` + `deadline_calendar.ics` with `review_status: draft`

## Key dates (stubs — verify officially)

| Jurisdiction | Milestone |
| --- | --- |
| SG SGX | ISSB FY2025 large-cap → FY2027 all |
| AU ASRS | Group 1 Jan 2025 → Group 3 Jul 2027 |
| IN BRSR | Assurance phase-down to top 1000 by FY2027 |
| BR CVM 193 | FY2026 reports due 2027 |
| AE SCA | FY2024 ADX/DFM mandatory |
| SA Tadawul | Large-cap 2025 → all 2027 |

See [docs/global-regulatory-landscape.md](../docs/global-regulatory-landscape.md).

## MCP tools

`regulatory-db-server`: `get_deadlines`, `search_regulatory_text`, `get_framework_requirements`, `get_jurisdiction_rules`

## Common rationalizations

| Excuse | Rebuttal |
| --- | --- |
| "Stubs are current law." | KB version must be **verified** with official sources before filing deadlines relied upon. |

## Red flags

- Auto-updating corporate policy from agent changelog without legal review
- Missing localization triggers (DPDP/PIPL/PDPL) when new region added

## Verification checklist

- [ ] Each deadline cites source
- [ ] KB `jurisdiction_reporting.json` version noted
- [ ] Compliance officer `/review` on published calendar

## SME provenance

| **Last reviewed** | 2026-06-13 |
| **Next review due** | 2026-06-27 (quarterly) |
