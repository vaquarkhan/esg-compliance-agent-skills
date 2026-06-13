---
name: ghg-emissions-calculation
description: Calculates Scope 1-3 GHG inventories, LCA impacts, and SBTi trajectory tracking. Use for GHG, carbon footprint, or SBTi requests.
---

# Skill 02: GHG Emissions Calculation

## Scope

Compute GHG inventories aligned with GHG Protocol and IPCC AR6 GWP100.

## Mandatory constraints

- **Human-in-the-loop:** All final filings, legal assessments, and assurance conclusions require explicit human reviewer sign-off.
- **No guessing:** Do not invent emission factors, taxonomy percentages, materiality scores, or regulatory citations.
- **Provenance:** Every numeric output must cite source (MCP tool response, knowledge base version, or primary document).
- **PII:** Redact personal identifiers; enforce localization via `cross-border-data-transfer` when data leaves origin jurisdiction.

## Workflow

1. Bound organizational inventory
2. Fetch factors via `get_emission_factor` / `get_grid_factors_by_country`
3. Apply GWP via `get_gwp_values`
4. Aggregate scopes with `convert_units` consistency
5. Compare against SBTi pathway (human validates targets)

## MCP tools

`emissions-factor-server`: all tools

## Output artifacts

- `ghg_inventory.json`
- `factor_provenance.json`
- `sbti_gap_analysis.md`

## Anti-patterns

- Submitting filings without `/review` approval
- Using outdated emission factors without `list_factor_sources` verification
- Declaring taxonomy alignment without DNSH assessment
