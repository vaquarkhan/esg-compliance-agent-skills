# ESG SME review cadence and reference provenance

Checklists in `references/` are **operational aids**, not legal opinions or assurance conclusions.

## Sustainability assurance gate

ESG filings require **external sustainability assurance** (e.g., ISAE 3000 / AA1000). This repository never auto-grants assurance.

Every filing-bound artifact must carry:

| Field | Default | When signed |
| --- | --- | --- |
| `assurance_status` | `pending_sustainability_assurance_sign_off` | `sustainability_assurance_signed_off` |
| `sustainability_assuror_sign_off` | `null` | Assuror name + credential |
| `signed_at` | `null` | ISO-8601 timestamp |
| `human_review_required` | `true` | `false` only after signed assurance |

Schema: [knowledge_base/attestation_schema.json](../knowledge_base/attestation_schema.json).  
Helper: `orchestration/attestation.py`.

Reference checklists must include an **Assurance status** row in their Provenance table, defaulting to pending.

## Review cadence

| Asset type | Minimum review | Trigger for out-of-cycle review |
| --- | --- | --- |
| CSRD / ESRS checklists | **Quarterly** | ESRS Omnibus, EFRAG IG updates |
| EU Taxonomy TSC/DNSH | **Quarterly** | Delegated act amendments |
| SFDR PAIs / RTS | **Semi-annual** | ESMA Q&A, RTS revisions |
| SEC climate rules | **Semi-annual** | SEC rule amendments |
| TNFD / biodiversity | **Semi-annual** | TNFD recommendation updates |
| Cross-border (DPDP, PIPL, PDPL) | **Quarterly** | New localization guidance |

## Required checklist sections

Every `references/*checklist*.md` must include:

1. **Authoritative sources** — link to ESRS, delegated acts, GHG Protocol, etc.
2. **Provenance** table with Last reviewed / Next review due / Reviewer / **Assurance status**

## CI enforcement

```bash
python scripts/validate-sme-provenance.py
make validate-sme
```

See [reviews/TEMPLATE.md](../reviews/TEMPLATE.md) for review records.
