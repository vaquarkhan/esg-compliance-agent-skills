---
name: supply-chain-due-diligence
description: Assesses CSDDD and UFLPA supply chain risk with entity screening, PEP checks, and composite supplier risk registers. Use for supplier onboarding, due diligence, or sanctions-adjacent ESG screening.
---

# Skill 08: Supply Chain Due Diligence

## Overview

Combines **CSDDD** human-rights/environmental due diligence workflow with **UFLPA** forced-labor risk screening via sanctions MCP tools.

## When to Use

- Supplier onboarding / annual refresh
- CSDDD value chain assessment
- UFLPA entity list cross-check (US supply chains)

## Mandatory constraints

- **Human-in-the-loop:** Screening hits require analyst review — never auto-clear suppliers.
- **No guessing:** Risk scores are **indicative** from mock MCP; production uses live lists.
- **PII:** Supplier contacts redacted in agent logs; localize per Skill 10.

## Core process

### Step 1 — Supplier master data

Collect: legal name, country, NACE, tier, spend, products.

### Step 2 — Entity screening

`screen_entity(name, country, identifiers)` — escalate `risk_level: high`

### Step 3 — PEP / governance

`check_pep_status(name, role)` for senior supplier leadership where relevant.

### Step 4 — Ongoing monitoring

`monitor_entity_changes(entity_id, since)` on annual cycle.

### Step 5 — Consolidated report

`generate_screening_report(entity_ids)` → human-approved PDF.

Emit `supplier_risk_register.json` with CSDDD action plans (prevent, mitigate, remedy).

## MCP tools

`sanctions-screening-server`: all five tools

## Common rationalizations

| Excuse | Rebuttal |
| --- | --- |
| "Low MCP risk clears supplier." | Mock screening ≠ cleared — **human analyst** required. |
| "Tier 1 only is enough for CSDDD." | CSDDD expects **value chain** depth proportional to severity. |

## Red flags

- Auto-approval on watchlist hit
- Supplier PII in unencrypted cross-border storage

## Verification checklist

- [ ] All tier-1+ suppliers screened
- [ ] Hits assigned analyst owner
- [ ] CSDDD remediation plan for high-risk suppliers
- [ ] `/review` before procurement policy change

## SME provenance

| **Last reviewed** | 2026-06-13 |
| **Next review due** | 2026-09-13 |
