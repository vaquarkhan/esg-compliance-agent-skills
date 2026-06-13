---
name: audit-trail-reporting
description: Manages iXBRL/ESEF tagging, SEC Inline XBRL, immutable audit logs on DynamoDB/S3/Glacier, and jurisdiction-specific report packaging. Use for ESEF packages, XBRL validation, or 7+ year retention.
---

# Skill 06: Audit Trail & Reporting

## Overview

Produces **immutable audit evidence** and **digital tagging** for CSRD/ESEF, SEC climate, and APAC ISSB-aligned filings. Hot logs in DynamoDB, analytics in S3, long-term retention in Glacier Deep Archive (see CDK stack).

## When to Use

- Building ESEF/iXBRL packages
- SHA-256 manifest for assurance
- SEC Inline XBRL climate disclosure tagging

## Mandatory constraints

- **Human-in-the-loop:** `submit_*` MCP tools require approval token; agent prepares only.
- **No guessing:** XBRL tags must map to published taxonomy elements.
- **Provenance:** Every artifact in `audit_manifest.json` with hash, timestamp, author.

## Core process

### Step 1 — Generate report package

`generate_esef_package(report_html, taxonomy_version="2024")` — review artifact list.

### Step 2 — Validate tagging

`validate_xbrl_tagging(instance_path, taxonomy="ESRS")` — fix all errors before `/validate`.

### Step 3 — Audit manifest

```json
{
  "artifacts": [
    {"path": "report.xhtml", "sha256": "...", "stored": "s3://audit/..."}
  ],
  "dynamodb_audit_pk": "entity#FY2025",
  "retention_years": 7
}
```

### Step 4 — Filing status tracking

`get_filing_status(filing_id)` after human-submitted filing.

### Step 5 — Jurisdiction packaging

| Region | Format | Language note |
| --- | --- | --- |
| EU | ESEF/iXBRL | ESRS taxonomy |
| US SEC | Inline XBRL | US GAAP + climate tags |
| JP | ISSB/SSBJ | Japanese filing copy human-prepared |
| BR | CVM | Portuguese human-prepared |

## MCP tools

`filing-submission-server`: `validate_xbrl_tagging`, `generate_esef_package`, `get_filing_status`, `submit_*` (human gate only)

## Common rationalizations

| Excuse | Rebuttal |
| --- | --- |
| "PDF is enough for CSRD." | **ESEF machine-readable** format required for EU listed issuers. |
| "Skip hash manifest for drafts." | Drafts still need lineage for `/backfill` restatements. |

## Red flags

- submit_* called without human_approval_token
- XBRL validation errors ignored
- Audit logs without retention policy

## Verification checklist

- [ ] XBRL validation pass recorded
- [ ] audit_manifest.json complete
- [ ] Glacier lifecycle documented (CDK)
- [ ] Human filing submission separate from agent

## SME provenance

| **Last reviewed** | 2026-06-13 |
| **Next review due** | 2026-09-13 |
