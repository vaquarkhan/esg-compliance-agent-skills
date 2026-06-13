# Copilot instructions

Read [AGENTS.md](../AGENTS.md) before ESG compliance tasks.

- Use lifecycle: `/spec`, `/plan`, `/build`, `/validate`, `/review`, `/backfill`, `/ship`
- Never guess emission factors, taxonomy eligibility, or legal conclusions
- Human-in-the-loop for `submit_*` MCP filing tools
- Redact PII via `redaction.py` before reasoning
- Load one primary skill per thread from `skills/`

MCP servers (SSE): ports 8001–8005. See [mcp/README.md](../mcp/README.md).
