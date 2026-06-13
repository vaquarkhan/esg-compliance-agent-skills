# CSRD E1 Data Mapping Example

## Deterministic routing (default)

```bash
python -m orchestration.supervisor_agent "Map CSRD ESRS E1 data points for FY2025"
```

Expected: `compliance_checker_agent` via regex routing. Output includes `assurance_status: pending_sustainability_assurance_sign_off`.

## LLM planner mode

```bash
ESG_ORCHESTRATION_MODE=planner python -m orchestration.supervisor_agent "Map CSRD ESRS E1 and validate iXBRL tagging"
```

Expected: multi-step plan with dynamic MCP tool calls.

## Standalone mapping artifact

```bash
python examples/csrd-e1-mapping/run_mapping.py
```

Writes `mapping_matrix.json` with attestation envelope.

Human sustainability assuror sign-off required before disclosure publication.
