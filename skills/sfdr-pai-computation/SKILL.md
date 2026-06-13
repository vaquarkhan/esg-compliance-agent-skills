---
name: sfdr-pai-computation
description: Computes SFDR mandatory and optional PAIs, Article 6/8/9 product classification, and taxonomy alignment percentages for financial products. Use for PAI statements, RTS Annex I, or fund classification.
---

# Skill 05: SFDR PAI Computation

## Overview

Calculates **18 mandatory Principal Adverse Impact indicators** (and optional) per SFDR RTS Annex I, with product-level **Article 6 / 8 / 9** classification workflow.

## When to Use

- Entity-level or product-level PAI statement
- Fund classification review (light green vs dark green)
- Taxonomy alignment % at product level (with Skill 03)

## Mandatory constraints

- **Human-in-the-loop:** Legal/compliance confirms Art. 6/8/9 classification before marketing.
- **No guessing:** PAI numerators/denominators need investee data or documented estimates methodology.
- **Provenance:** Cite RTS indicator ID, data source, estimation method per indicator.

## Core process

### Step 1 — Product classification

Confirm with legal: Art. 6 (no sustainability focus), Art. 8 (promotes E/S characteristics), Art. 9 (sustainable objective). Document in `product_classification_memo.md`.

### Step 2 — PAI data collection

Gather investee-level data for mandatory indicators (GHG emissions, fossil exposure, biodiversity, social, governance, etc.). Use `get_emission_factor` where activity data exists.

### Step 3 — Calculate 18 mandatory PAIs

For each indicator record: formula, numerator, denominator, unit, coverage % of AUM.

Reference RTS Annex I table — do not paraphrase indicator definitions.

### Step 4 — Optional indicators & taxonomy %

Include optional PAIs if advertised. Product taxonomy alignment % requires Skill 03 outputs.

### Step 5 — Emit `pai_statement.json`

Mark `human_review_required: true`, `assurance_status: pending`.

## MCP tools

`regulatory-db-server`: `get_framework_requirements("SFDR")`  
`emissions-factor-server`: `get_emission_factor` (PAI 1–3 GHG-related)

## Common rationalizations

| Excuse | Rebuttal |
| --- | --- |
| "Estimate all PAIs with sector averages." | RTS expects **best available data** — document why investee data unavailable. |
| "Article 8 and 9 are marketing labels." | Misclassification is **regulatory risk** — legal sign-off required. |

## Red flags

- PAI statement without coverage ratio disclosure
- GHG PAIs inconsistent with Skill 02 inventory without reconciliation note

## Verification checklist

- [ ] All 18 mandatory PAIs addressed or explicitly N/A with reason
- [ ] Product classification memo signed
- [ ] RTS indicator IDs cited
- [ ] `/review` before publication

## SME provenance

| **Source** | SFDR RTS Annex I |
| **Last reviewed** | 2026-06-13 |
| **Next review due** | 2026-09-13 |
