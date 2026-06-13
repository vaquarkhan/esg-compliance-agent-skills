# Skills Index — ESG Compliance Agent Skills

**11 skills total:** 1 meta + **10 domain skills** (100% coverage of the ESG agent module set).

| ID | Skill | Path | Worker | Triggers |
| --- | --- | --- | --- | --- |
| — | Using ESG Agent Skills | `skills/using-esg-agent-skills/` | supervisor | Routing, onboarding, lifecycle |
| 01 | Data Ingestion & Validation | `skills/data-ingestion-validation/` | compliance_checker | CSRD, ESRS, Omnibus, data mapping |
| 02 | GHG Emissions Calculation | `skills/ghg-emissions-calculation/` | calculation | Scope 1/2/3, LCA, SBTi |
| 03 | EU Taxonomy Alignment | `skills/eu-taxonomy-alignment/` | disclosure | NACE, TSC, DNSH, KPIs |
| 04 | Double Materiality Assessment | `skills/double-materiality-assessment/` | compliance_checker | Impact, financial materiality |
| 05 | SFDR PAI Computation | `skills/sfdr-pai-computation/` | disclosure | PAIs, Article 6/8/9 |
| 06 | Audit Trail & Reporting | `skills/audit-trail-reporting/` | disclosure | iXBRL, ESEF, audit logs |
| 07 | Regulatory Change Monitor | `skills/regulatory-change-monitor/` | monitoring | Deadlines, APAC/LATAM/MENA |
| 08 | Supply Chain Due Diligence | `skills/supply-chain-due-diligence/` | monitoring | CSDDD, UFLPA |
| 09 | Biodiversity TNFD Analytics | `skills/biodiversity-tnfd-analytics/` | calculation | LEAP, MSA, BII |
| 10 | Cross-Border Data Transfer | `skills/cross-border-data-transfer/` | monitoring | DPDP, PIPL, PDPL |

Machine-readable manifest: [registry/skills.json](registry/skills.json).

## Presets

| Preset | Path |
| --- | --- |
| CSRD / ESRS | `presets/csrd-esrs/PRESET.md` |
| SFDR / Taxonomy | `presets/sfdr-taxonomy/PRESET.md` |

## Starter packs

| Pack | Path |
| --- | --- |
| CSRD ESRS starter | `starter-packs/csrd-esrs-starter.yaml` |

## Runnable examples

| Example | Path |
| --- | --- |
| GHG inventory | `examples/ghg-inventory/` |
| CSRD E1 mapping | `examples/csrd-e1-mapping/` |

Load skills progressively — one primary domain skill per thread. Start with `using-esg-agent-skills` when unclear. See [AGENTS.md](AGENTS.md).
