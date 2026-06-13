---
name: data-ingestion-validation
description: Maps CSRD 1,100+ Omnibus data points to ESRS schemas, validates ERP/IoT/third-party feeds, and flags gaps for human stewards. Use for CSRD ingestion, ESRS mapping, Omnibus reconciliation, or data lake lineage.
---

# Skill 01: CSRD Omnibus Data Ingestion & Validation

## Overview

Integrates ERP, IoT, HR, finance, and third-party ESG feeds into a **single auditable mapping** against CSRD/ESRS datapoints (including Omnibus amendments). Produces lineage-ready artifacts — not final disclosures.

## When to Use

- Building `mapping_matrix.json` for ESRS E/S/G topics
- Validating completeness vs mandatory datapoints
- Preparing AWS Sustainability Data Fabric-style centralization (S3/OpenSearch targets)

Do **not** use for GHG calculations alone → `ghg-emissions-calculation`.

## Mandatory constraints

- **Human-in-the-loop:** Data stewards sign off gap register before `/build` disclosures.
- **No guessing:** Do not invent ESRS IDs or map fields without source column provenance.
- **Provenance:** Each mapping row: `source_system`, `source_field`, `transform`, `esrs_id`, `hash`.
- **PII:** Redact before mapping; route cross-border feeds through Skill 10.

## Core process

### Step 1 — Source inventory

Catalog systems: ERP (SAP/Oracle), utility APIs, travel, fleet IoT, supplier surveys. Record refresh cadence and owner.

### Step 2 — ESRS datapoint pull

1. `get_framework_requirements("CSRD")`
2. `get_data_point_definitions(standard="ESRS E1", topic="E1")` (repeat per material topic from Skill 04)
3. `search_regulatory_text` for Omnibus delta keywords

### Step 3 — Field mapping

Build `mapping_matrix.json`:

```json
{
  "esrs_id": "E1-6",
  "source_system": "erp_gl",
  "source_field": "fuel_consumption_mmbtu",
  "transform": "unit_convert_to_MMBtu",
  "mandatory": true
}
```

### Step 4 — Validation rules

- Completeness: % mandatory datapoints with mapped source
- Type/units vs ESRS datatype
- Anomaly flags (null spikes, negative energy)

### Step 5 — Gap register

Unmapped mandatory points → `gap_register.csv` with owner, ETA, blocking `/validate`.

## MCP tools

`regulatory-db-server`: `get_data_point_definitions`, `get_framework_requirements`, `search_regulatory_text`

## Output artifacts

- `mapping_matrix.json`, `validation_report.md`, `gap_register.csv`, `lineage_manifest.json` (SHA-256 per source extract)

## Common rationalizations

| Excuse | Rebuttal |
| --- | --- |
| "Sample 10 datapoints is enough." | CSRD requires **material topic coverage** — sample mapping ≠ compliance mapping. |
| "We can map later during audit." | Gap register must exist **before** `/build`; late mapping breaks audit trail. |

## Red flags

- Mapping without source field names
- PII in mapping matrix unredacted
- Omnibus amendments ignored

## Verification checklist

- [ ] All **material** ESRS topics have datapoint definitions fetched
- [ ] Every mapped row has source + transform + hash
- [ ] Gap register reviewed by data steward
- [ ] `/review` before disclosure publication

## SME provenance

| **Last reviewed** | 2026-06-13 |
| **Next review due** | 2026-09-13 |
| **Assurance status** | Pending external sign-off |
