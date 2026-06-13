"""MCP tool catalog exposed to the LLM planner for dynamic tool selection."""

from __future__ import annotations

from typing import Any

# server key → list of callable tools (mirrors mcp/*/server.py)
MCP_TOOL_CATALOG: dict[str, list[dict[str, Any]]] = {
    "regulatory": [
        {"tool": "get_framework_requirements", "args": ["framework", "version?"]},
        {"tool": "get_data_point_definitions", "args": ["standard", "topic?"]},
        {"tool": "get_deadlines", "args": ["jurisdiction", "framework", "fiscal_year"]},
        {"tool": "get_jurisdiction_rules", "args": ["jurisdiction"]},
        {"tool": "search_regulatory_text", "args": ["query", "framework?", "limit?"]},
    ],
    "emissions": [
        {"tool": "get_emission_factor", "args": ["source", "activity"]},
        {"tool": "list_factor_sources", "args": []},
        {"tool": "get_gwp_values", "args": ["standard?"]},
        {"tool": "convert_units", "args": ["value", "from_unit", "to_unit", "substance?"]},
        {"tool": "get_grid_factors_by_country", "args": ["country_code"]},
    ],
    "taxonomy": [
        {"tool": "get_tsc_for_activity", "args": ["nace_code"]},
        {"tool": "get_dnsh_criteria", "args": ["nace_code", "objective?"]},
        {"tool": "check_nace_eligibility", "args": ["nace_code", "revenue_pct", "capex_pct", "opex_pct"]},
        {"tool": "get_minimum_safeguards", "args": []},
        {"tool": "get_objective_thresholds", "args": ["objective"]},
    ],
    "filing": [
        {"tool": "validate_xbrl_tagging", "args": ["instance_path", "taxonomy?"]},
        {"tool": "generate_esef_package", "args": ["report_html", "taxonomy_version?"]},
        {"tool": "get_filing_status", "args": ["filing_id"]},
    ],
    "sanctions": [
        {"tool": "screen_entity", "args": ["name", "country?", "identifiers?"]},
        {"tool": "check_pep_status", "args": ["name", "role?"]},
        {"tool": "get_sanctions_lists", "args": ["jurisdiction?"]},
        {"tool": "generate_screening_report", "args": ["entity_ids"]},
    ],
}

WORKER_SKILLS: dict[str, list[str]] = {
    "compliance": ["data-ingestion-validation", "double-materiality-assessment"],
    "disclosure": ["eu-taxonomy-alignment", "sfdr-pai-computation", "audit-trail-reporting"],
    "calculation": ["ghg-emissions-calculation", "biodiversity-tnfd-analytics"],
    "monitoring": ["regulatory-change-monitor", "supply-chain-due-diligence", "cross-border-data-transfer"],
}
