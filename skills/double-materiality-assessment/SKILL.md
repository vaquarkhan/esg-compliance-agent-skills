---
name: double-materiality-assessment
description: Conducts CSRD double materiality assessment scoring impact and financial materiality with IRO register and stakeholder integration. Use for DMA workshops, materiality matrix, or CSRD scope definition.
---

# Skill 04: Double Materiality Assessment

## Overview

Implements CSRD **impact materiality** (inside-out) and **financial materiality** (outside-in) to produce a defensible materiality matrix and ESRS topic scope.

## When to Use

- CSRD `/spec` material topic selection
- IRO (impacts, risks, opportunities) workshops
- Restating materiality after Omnibus changes

## Mandatory constraints

- **Human-in-the-loop:** Material topics require workshop sign-off — agent drafts, humans decide.
- **No guessing:** Do not auto-set "material" from LLM inference alone.
- **Provenance:** Link each IRO to ESRS topic and evidence source.

## Core process

### Step 1 — Long list ESRS topics

`get_framework_requirements("CSRD")` + sector-specific ESRS (E1–E5, S1–S4, G1, etc.)

### Step 2 — IRO identification

For each sustainability matter document:
- Impact: severity, scale, irremediability (1–5 with criteria definitions)
- Financial: magnitude, likelihood, time horizon (1–5)

### Step 3 — Threshold matrix

Apply organization thresholds (e.g., score ≥4 on either axis = candidate material). **Human workshop validates.**

### Step 4 — Stakeholder input

Document engagement method (surveys, interviews) — do not fabricate stakeholder quotes.

### Step 5 — Output

`materiality_matrix.json`, `iro_register.md` with `pending_assurance: true`

## MCP tools

`regulatory-db-server`: `get_framework_requirements`, `search_regulatory_text`

## Common rationalizations

| Excuse | Rebuttal |
| --- | --- |
| "Financial materiality only for investors." | CSRD requires **both** perspectives unless legal scope exemption applies. |
| "Copy last year's matrix." | Restatement requires **change log** if IROs or thresholds changed. |

## Red flags

- All topics marked material without scoring
- No stakeholder process documented
- Agent sets final material list without `/review`

## Verification checklist

- [ ] IRO register complete with scores and rationale
- [ ] Threshold methodology documented
- [ ] Workshop attendees and date recorded
- [ ] Human sign-off before ESRS disclosure scope locked

## SME provenance

| **Last reviewed** | 2026-06-13 |
| **Next review due** | 2026-09-13 |
