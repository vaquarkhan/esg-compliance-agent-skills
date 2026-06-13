---
name: eu-taxonomy-alignment
description: Evaluates EU Taxonomy alignment via NACE codes, Technical Screening Criteria, DNSH, minimum safeguards, and turnover/CapEx/OpEx KPIs. Use for taxonomy KPIs, green revenue, or eligible activity assessment.
---

# Skill 03: EU Taxonomy Alignment

## Overview

Deterministic workflow for **substantial contribution**, **Do No Significant Harm (DNSH)**, **minimum safeguards**, and **Article 8 KPIs** (turnover, CapEx, OpEx %) per EU Taxonomy Delegated Acts.

## When to Use

- Taxonomy-aligned revenue/CapEx/OpEx disclosure
- NACE activity eligibility assessment
- DNSH checklist before claiming "aligned"

Not for SFDR PAIs alone → `sfdr-pai-computation`.

## Mandatory constraints

- **Human-in-the-loop:** Legal/SME confirms substantial contribution + DNSH before publishing KPIs.
- **No guessing:** Never invent taxonomy %; use MCP + documented activity economics.
- **Provenance:** Cite NACE, Annex reference, TSC threshold per activity row.

## Core process

### Step 1 — Activity → NACE mapping

Map each economic activity to **NACE Rev. 2.1** code with revenue/CapEx/OpEx splits.

### Step 2 — Substantial contribution (TSC)

1. `get_tsc_for_activity(nace_code)` — record threshold (e.g., lifecycle GHG savings %)
2. Compare activity performance vs TSC — document evidence (LCA, energy performance)

### Step 3 — DNSH (all six objectives)

1. `get_dnsh_criteria(nace_code, objective)` for climate, water, pollution, biodiversity, circular economy, adaptation
2. Complete checklist — **all objectives** before alignment claim

### Step 4 — Minimum safeguards

`get_minimum_safeguards()` — OECD, UNGP, ILO alignment attestation (human HR/legal input)

### Step 5 — KPI calculation

`check_nace_eligibility(nace, revenue_pct, capex_pct, opex_pct)` — **mock returns require human review**; replace with audited figures.

Emit `taxonomy_kpi_workbook.json`:

```json
{
  "aligned_turnover_pct": null,
  "eligible_not_aligned_pct": null,
  "non_eligible_pct": null,
  "human_review_required": true
}
```

## MCP tools

`taxonomy-criteria-server`: all five tools

## Common rationalizations

| Excuse | Rebuttal |
| --- | --- |
| "TSC pass means fully aligned." | **DNSH + minimum safeguards** are mandatory — TSC alone is insufficient. |
| "Use group average NACE." | KPIs require **activity-level** NACE and economic figures. |

## Red flags

- DNSH skipped for "climate-only" companies
- KPI percentages without CapEx/OpEx breakdown
- Mock MCP eligibility treated as final

## Verification checklist

- [ ] TSC documented per NACE with Annex reference
- [ ] DNSH complete for all six objectives
- [ ] Minimum safeguards attested
- [ ] KPI workbook human-signed

## SME provenance

| **Source** | EU Taxonomy Delegated Regulation |
| **Last reviewed** | 2026-06-13 |
| **Next review due** | 2026-09-13 |
