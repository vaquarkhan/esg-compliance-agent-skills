# ESG SME review cadence and reference provenance

Checklists in `references/` are **operational aids**, not legal opinions or assurance conclusions.

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
2. **Provenance** table with Last reviewed / Next review due / Reviewer

## CI enforcement

```bash
python scripts/validate-sme-provenance.py
make validate-sme
```

See [reviews/TEMPLATE.md](../reviews/TEMPLATE.md) for review records.
