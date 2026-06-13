---
name: ghg-emissions-calculation
description: Calculates Scope 1-3 GHG inventories using GHG Protocol and ISO 14064, location/market-based Scope 2, IPCC AR6 GWP100, and SBTi gap analysis. Use for GHG inventory, carbon footprint, Scope 3 LCA, grid factors, or SBTi trajectory requests. Do not use for EU Taxonomy KPI percentages or SFDR PAI computation without loading those skills separately.
---

# Skill 02: GHG Emissions Calculation

## Overview

This skill drives a **deterministic GHG inventory workflow** aligned with the **GHG Protocol Corporate Standard**, **ISO 14064-1**, and **IPCC AR6 GWP100**. The agent must not invent emission factors, grid intensities, or organizational boundaries. Every tonne CO2e must trace to an MCP tool response or an approved factor registry entry with version metadata.

Supports **CSRD ESRS E1**, **SEC climate**, **ISSB S2**, **SGX**, **ASRS (Australia)**, **SSBJ (Japan)**, **BRSR (India)**, **KSSB (Korea)**, **CVM Resolution 193 (Brazil)**, **UAE SCA**, and **Tadawul** reporting contexts — but **does not substitute statutory assurance**. Human reviewer sign-off is mandatory before external publication.

## When to Use

Use when:

- Building or restating **Scope 1, 2, or 3** inventories
- Applying **location-based vs market-based** Scope 2 methods
- Converting activity data with **EPA, DEFRA, or national grid factors**
- Running **SBTi gap analysis** against a validated target (human confirms target validity)
- Producing **`ghg_inventory.json`** with factor provenance for assurance

Do **not** use when:

- Task is **EU Taxonomy alignment KPIs** only → load `eu-taxonomy-alignment`
- Task is **SFDR PAI indicators** only → load `sfdr-pai-computation`
- You lack activity data or factor source — **stop** and request data steward input
- Cross-border personal data must leave India/China/Saudi without localization review → load `cross-border-data-transfer` first

## Mandatory constraints

- **Human-in-the-loop:** Inventory totals and SBTi conclusions require explicit reviewer sign-off before `/ship`.
- **No guessing:** Do not invent emission factors, grid intensities, organizational boundaries, or SBTi targets.
- **Provenance:** Every tCO2e line cites MCP tool response or KB version in `factor_provenance.json`.
- **PII / localization:** Redact identifiers; route India/China/Saudi data through Skill 10 before cross-border transfer.

## Standards and GWP

| Standard | Application |
| --- | --- |
| GHG Protocol Corporate Standard | Organizational boundary, Scope 1/2/3 categories |
| ISO 14064-1 | Optional parallel reporting structure |
| IPCC AR6 GWP100 | Default GWP set — fetch via `get_gwp_values` |
| SBTi Corporate Manual | Target gap analysis only after human confirms approved target |

**Never** mix GWP vintages (AR4/AR5/AR6) within one inventory period.

## Core Process

Execute **in order**. Do not skip provenance steps.

### Phase A — Boundaries and activity data

#### Step 1: Define inventory boundary

1. Record: reporting entity, **operational control** or **equity share** boundary, fiscal year, base year (if restatement).
2. List inclusions/exclusions with rationale (e.g., leased assets Scope 1/2 per GHG Protocol guidance).
3. Flag jurisdictions requiring localized reporting (JP Japanese filings, BR Portuguese CVM, SA Arabic CMA) — reporting language is **human/legal**; calculations remain in SI units.

#### Step 2: Ingest and validate activity data

1. Collect activity data by scope (fuel volumes, kWh, passenger-km, spend, mass).
2. Validate units and completeness — reject mixed units without `convert_units`.
3. Store raw inputs in audit manifest with SHA-256 hash (Skill 06 integration).

### Phase B — Scope 1 (direct emissions)

#### Step 3: Scope 1 calculation

**Scope 1** = direct emissions from owned/controlled sources:

- Stationary combustion (natural gas, diesel generators)
- Mobile combustion (fleet)
- Process emissions and fugitive (refrigerants — use GWP for gas species)

For each activity:

```
emissions_tCO2e = activity × emission_factor × GWP_factor (if non-CO2)
```

1. Call `list_factor_sources` — confirm KB version in `metadata`.
2. Call `get_emission_factor(source, activity)` — record `factor.id`, `source`, `unit`.
3. Call `convert_units` if activity unit ≠ factor unit.
4. Sum by gas; apply `get_gwp_values` for CH4, N2O, HFCs, SF6.

**Worked example (Scope 1 — natural gas):**

| Input | Value |
| --- | --- |
| Activity | 12,500 MMBtu natural gas (stationary) |
| Factor | EPA `EPA-NATGAS-STATIONARY`: 53.06 kg CO2e/MMBtu |
| Calculation | 12,500 × 53.06 = 663,250 kg CO2e = **663.25 tCO2e** |
| Provenance | `knowledge_base/emission_factors.json` v2026.06, MCP `get_emission_factor` |

### Phase C — Scope 2 (purchased energy)

#### Step 4: Scope 2 — location-based AND market-based

Report **both** methods when CSRD/ISSB/SEC disclosure requires dual presentation.

**Location-based:** grid average emission factor for country/region.

```
tCO2e = kWh × grid_factor_kg_per_kWh / 1000
```

1. Call `get_grid_factors_by_country(country_code)` — e.g., `IN` → 0.708 kg/kWh (2024 stub).
2. Document grid year and source limitation in `factor_provenance.json`.

**Market-based:** use supplier-specific factors, RECs, or residual mix where available.

- If no contractual instrument evidence → **do not** claim market-based reduction; use residual mix or disclose "not available."
- Human reviewer must attest REC/PPA documentation before market-based figures ship.

**Worked example (Scope 2 — location-based, India operations):**

| Input | Value |
| --- | --- |
| Activity | 4,200,000 kWh purchased electricity |
| Grid factor | IN 0.708 kg CO2e/kWh (2024) |
| Calculation | 4,200,000 × 0.708 / 1000 = **2,973.6 tCO2e** |

### Phase D — Scope 3 (value chain)

#### Step 5: Scope 3 categories

Prioritize material categories (GHG Protocol 15 categories). Acceptable approaches:

| Approach | When to use |
| --- | --- |
| Supplier-specific | Primary data from tier-1 suppliers |
| Hybrid | Primary + secondary for gaps |
| Average-data | Industry averages (DEFRA spend/category factors) |
| Spend-based | Economic input-output when activity data unavailable |

1. Map each category to factor source — **never** use spend-based for material categories when primary data exists.
2. For business travel (Cat 6): `get_emission_factor("DEFRA", "business_travel_air_domestic")`.
3. Document uncertainty and data quality tier (1–5) per category.

### Phase E — Aggregation and SBTi

#### Step 6: Aggregate inventory

1. Sum Scope 1 + Scope 2 (both methods) + Scope 3 by category.
2. Emit `ghg_inventory.json`:

```json
{
  "reporting_period": "FY2025",
  "boundary": "operational_control",
  "scopes": {
    "scope_1_tCO2e": 663.25,
    "scope_2_location_tCO2e": 2973.6,
    "scope_2_market_tCO2e": null,
    "scope_3_tCO2e": {}
  },
  "gwp_standard": "IPCC AR6 GWP100",
  "kb_version": "2026.06"
}
```

#### Step 7: SBTi gap analysis (human gate)

1. Obtain **validated SBTi target** from human reviewer — do not scrape or guess targets.
2. Compute: `gap = projected_emissions - target_trajectory_year`.
3. Emit `sbti_gap_analysis.md` with explicit "pending sustainability assurance sign-off" footer.

## MCP tools

| Tool | Purpose |
| --- | --- |
| `list_factor_sources` | Verify KB freshness before calculations |
| `get_emission_factor` | Activity-level factors (EPA, DEFRA) |
| `get_grid_factors_by_country` | Scope 2 location-based |
| `get_gwp_values` | IPCC AR6 GWP100 |
| `convert_units` | Unit harmonization |

Server: `emissions-factor-server` (port 8002).

## Output artifacts

- `ghg_inventory.json` — scoped totals and category breakdown
- `factor_provenance.json` — every factor ID, source, version, MCP call timestamp
- `sbti_gap_analysis.md` — only after human supplies validated target
- `activity_data_manifest.json` — hashed raw inputs (optional, recommended)

Runnable reference: [examples/ghg-inventory/](../../examples/ghg-inventory/).

## Common rationalizations

| Excuse | Required rebuttal |
| --- | --- |
| "Industry average is close enough for Scope 3." | Material categories require **best available data hierarchy** per GHG Protocol. Averages are last resort — document why primary data was unavailable. |
| "We can use last year's grid factor." | Grid factors change annually. Call `get_grid_factors_by_country` and record **year**; restate if factor year ≠ reporting year without disclosure. |
| "Market-based Scope 2 equals zero because we bought RECs." | REC/PPA **documentation** is mandatory. Without human-attested instruments, market-based method is **not available** — do not report zero. |
| "CH4/N2O can use CO2 factors." | Non-CO2 gases require **`get_gwp_values`** — mixing without GWP is a calculation error. |
| "SBTi target of 50% by 2030 is industry standard." | SBTi targets are **company-specific and validated**. Never invent targets. |
| "APAC report can use EU DEFRA factors." | Use **jurisdiction-appropriate** factors or disclose proxy methodology and uncertainty. |

## Red flags

Stop and escalate if:

- Emission factor returned `error` from MCP but inventory continues
- Scope 3 > 70% of total with >50% spend-based and no uncertainty disclosure
- GWP standard ≠ IPCC AR6 without explicit policy exception approved by human
- Inventory totals published without `factor_provenance.json`
- Personal data in activity files crosses border without Skill 10 review

## Verification checklist

Do not mark complete until:

- [ ] `list_factor_sources` called; KB version recorded
- [ ] Every line item has factor ID + source in `factor_provenance.json`
- [ ] Scope 2 includes location-based; market-based only with human-attested instruments
- [ ] GWP from `get_gwp_values` applied to all non-CO2 gases
- [ ] Units harmonized via `convert_units` where needed
- [ ] Scope 3 categories documented with data quality tier
- [ ] SBTi section marked "pending assurance" unless human signed target
- [ ] `/review` human approval before `/ship` or external filing
- [ ] Cross-border activity data routed through localization rules if applicable

## SME provenance

| Field | Value |
| --- | --- |
| **Source document** | GHG Protocol Corporate Standard; ISO 14064-1; IPCC AR6 |
| **Last reviewed** | 2026-06-13 |
| **Reviewer** | Repository maintainer |
| **Next review due** | 2026-09-13 |
| **Assurance status** | Pending external sustainability assurance sign-off |
