# Getting Started

1. Run `bootstrap.sh` or `bootstrap.ps1`
2. Start MCP servers on ports 8001–8005 (optional — local import fallback works for tests)
3. Pick an orchestration tier:
   - **Deterministic** (default): `python -m orchestration.supervisor_agent "your task"`
   - **LLM planner**: `ESG_ORCHESTRATION_MODE=planner python -m orchestration.supervisor_agent "your task"`
   - **Full agent**: `python agent.py "your task"`
4. Follow lifecycle commands in AGENTS.md — all filing-bound outputs default to `pending_sustainability_assurance_sign_off`

See [docs/architecture.md](architecture.md) for what each tier does and does not do.
