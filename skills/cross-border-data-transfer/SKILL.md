---
name: cross-border-data-transfer
description: Enforces India DPDP, China PIPL, and Saudi PDPL data localization and transfer rules before ESG data leaves jurisdiction. Use for cross-border transfers, data residency architecture, or APAC MENA compliance.
---

# Skill 10: Cross-Border Data Transfer

## Overview

**Blocking gate** before persisting or transmitting ESG data containing personal identifiers across borders. Required for India BRSR pipelines, China operations, Saudi Tadawul reporting, and any multi-region CDK deployment.

## When to Use

- Before S3/OpenSearch replication cross-region
- Supplier surveys with worker PII
- HR diversity data (including India BRSR caste/MSE fields)

Always run **before** Skills 01, 08 when data crosses borders.

## Mandatory constraints

- **Human-in-the-loop:** Legal DPO sign-off for transfer mechanism (SCC, adequacy, consent).
- **No guessing:** Localization rules from MCP + legal — stubs are not legal opinions.
- **Block by default:** If transfer fails assessment, **do not persist** outside origin region.

## Core process

### Step 1 — Classify data

Categories: personal, sensitive personal, critical/important (China), public ESG metrics (non-PII).

Redact via `redaction.py` before classification review.

### Step 2 — Origin & destination

Record source jurisdiction and target AWS region (eu-west-1, ap-south-1, me-south-1, etc.).

### Step 3 — Rules lookup

`get_jurisdiction_rules("IN"|"CN"|"SA"|"EU"|"US")`

Cross-check `knowledge_base/jurisdiction_reporting.json` localization fields.

### Step 4 — Transfer mechanism

Document: adequacy, SCCs, binding corporate rules, explicit consent, or **domestic processing only**.

### Step 5 — Decision log

`transfer_impact_assessment.json`:

```json
{
  "decision": "block|allow_with_safeguards",
  "mechanism": "domestic_only",
  "dpo_sign_off": false,
  "human_review_required": true
}
```

## Region constraints (summary)

| Law | Requirement |
| --- | --- |
| India DPDP 2023 | Sensitive personal data — localization + consent |
| China PIPL | Critical/important data — security assessment, local storage |
| Saudi PDPL | Personal data — domestic processing unless adequacy/consent |

## MCP tools

`regulatory-db-server`: `get_jurisdiction_rules`

## Common rationalizations

| Excuse | Rebuttal |
| --- | --- |
| "ESG data isn't personal." | BRSR social, supplier, HR feeds **often contain PII**. |
| "Replicate all regions for DR." | DR must respect **localization** — use in-region replicas only. |

## Red flags

- Cross-region S3 sync without TIA
- Agent approves transfer without DPO sign-off field

## Verification checklist

- [ ] Data classified
- [ ] Rules fetched and cited
- [ ] Decision log complete
- [ ] DPO `/review` before enable replication

## SME provenance

| **Last reviewed** | 2026-06-13 |
| **Next review due** | 2026-06-27 |
