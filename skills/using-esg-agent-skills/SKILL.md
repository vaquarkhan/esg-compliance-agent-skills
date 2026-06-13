---
name: using-esg-agent-skills
description: Routes ESG compliance tasks to the correct skill, lifecycle command, MCP server, and worker agent. Use when scope is unclear, onboarding a new engagement, or choosing between CSRD, Taxonomy, SFDR, GHG, TNFD, or cross-border workflows.
---

# Using ESG Agent Skills

## Overview

Meta-skill for **progressive disclosure**. Load this skill first when the user's framework, jurisdiction, or deliverable is ambiguous. Then load **exactly one** primary domain skill per thread.

## When to Use

- First message in an ESG engagement
- User asks "where do I start?" for CSRD, taxonomy, GHG, etc.
- Task spans multiple frameworks — decompose before loading multiple skills

## Mandatory constraints

- **Human-in-the-loop:** `/ship` and all filing MCP tools require human approval token.
- **No guessing:** Never invent ESRS IDs, emission factors, taxonomy %, or legal conclusions.
- **One primary skill per thread** unless supervisor explicitly decomposes.

## Skill routing table

| User signal | Primary skill | Worker | MCP |
| --- | --- | --- | --- |
| CSRD, Omnibus, ESRS mapping | `data-ingestion-validation` | compliance_checker | regulatory-db |
| Scope 1/2/3, SBTi, carbon | `ghg-emissions-calculation` | calculation | emissions-factor |
| NACE, TSC, DNSH, green revenue | `eu-taxonomy-alignment` | disclosure | taxonomy-criteria |
| Materiality, IRO, DMA | `double-materiality-assessment` | compliance_checker | regulatory-db |
| SFDR, PAI, Article 6/8/9 | `sfdr-pai-computation` | disclosure | regulatory-db |
| iXBRL, ESEF, audit log | `audit-trail-reporting` | disclosure | filing-submission |
| Deadlines, regulatory change | `regulatory-change-monitor` | monitoring | regulatory-db |
| CSDDD, UFLPA, suppliers | `supply-chain-due-diligence` | monitoring | sanctions-screening |
| TNFD, LEAP, biodiversity | `biodiversity-tnfd-analytics` | calculation | regulatory-db |
| DPDP, PIPL, PDPL, transfer | `cross-border-data-transfer` | monitoring | regulatory-db |

## Lifecycle commands

`/spec` → `/plan` → `/build` → `/validate` → `/review` → `/ship`

See `.claude/commands/` and [AGENTS.md](../AGENTS.md).

## Common rationalizations

| Excuse | Rebuttal |
| --- | --- |
| "Load all 10 skills at once." | Progressive disclosure — one primary skill; use supervisor to decompose. |
| "Skip /spec and start calculating." | `/spec` produces `scope.json` — required for auditable `/build`. |
| "MCP mock data is fine for filing." | Mock tools enforce human gate; never treat stub output as filed disclosure. |

## Verification checklist

- [ ] Primary skill identified and named in response
- [ ] Lifecycle step stated (`/spec`, `/build`, etc.)
- [ ] Human review gate mentioned if output is disclosure-grade
- [ ] Cross-border data flagged for Skill 10 when APAC/MENA/India/China involved

## SME provenance

| Field | Value |
| --- | --- |
| **Last reviewed** | 2026-06-13 |
| **Reviewer** | Repository maintainer |
| **Next review due** | 2026-09-13 |
