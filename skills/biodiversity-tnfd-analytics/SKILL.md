---
name: biodiversity-tnfd-analytics
description: Applies TNFD LEAP approach with MSA, BII, and nature-related dependency metrics for CSRD ESRS E4 and ISSB biodiversity disclosures. Use for TNFD report, LEAP assessment, or nature KPI requests.
---

# Skill 09: Biodiversity & TNFD Analytics

## Overview

Executes **TNFD LEAP** (Locate, Evaluate, Assess, Prepare) with biodiversity indicators (MSA, BII proxies) linked to ESRS E4 and ISSB S2 nature-related risks.

## When to Use

- TNFD-aligned disclosure draft
- ESRS E4 biodiversity material topic
- Nature-related financial risk assessment

Pair with Skill 02 for climate-nature interlinkages.

## Mandatory constraints

- **Human-in-the-loop:** Ecologist/SME validates location-specific impacts.
- **No guessing:** MSA/BII values require cited models or primary surveys — mock analytics must be labeled.
- **Provenance:** GEOS coordinates, dataset version, model name in `biodiversity_metrics.csv`.

## Core process

### Step 1 — Locate (L)

Map operational sites to biomes, protected areas, water stress (WRI Aqueduct), key biodiversity areas.

### Step 2 — Evaluate (E)

Dependencies & impacts on ecosystem services per TNFD guidance.

### Step 3 — Assess (A)

Quantify where data exists:
- Mean Species Abundance (MSA) loss proxies
- Biodiversity Intactness Index (BII) regional values
Document uncertainty bands.

### Step 4 — Prepare (P)

Disclosure aligned to TNFD recommendations + ESRS E4 datapoints.

`search_regulatory_text("TNFD LEAP", framework="TNFD")` for requirement crosswalk.

### Step 5 — Output

`tnfd_leap_assessment.json`, `biodiversity_metrics.csv`

## MCP tools

`regulatory-db-server`: `search_regulatory_text`  
`emissions-factor-server`: `convert_units` (land area, water volume harmonization)

## Common rationalizations

| Excuse | Rebuttal |
| --- | --- |
| "Use global average MSA." | Site-specific **Locate** step requires geospatial specificity. |
| "TNFD is voluntary so skip." | May be **material** under CSRD ESRS E4 — materiality from Skill 04 governs. |

## Red flags

- Precision implied without survey/model citation
- Nature metrics disconnected from financial risk narrative

## Verification checklist

- [ ] LEAP four phases documented
- [ ] Metrics include source + uncertainty
- [ ] SME ecologist review recorded
- [ ] Cross-reference ESRS E4 datapoints

## SME provenance

| **Source** | TNFD Recommendations v1.0 |
| **Last reviewed** | 2026-06-13 |
| **Next review due** | 2026-09-13 |
