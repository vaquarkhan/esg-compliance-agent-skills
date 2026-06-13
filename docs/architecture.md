# Architecture

## Components

1. **Skills** — Progressive-disclosure agent instructions in `skills/`
2. **MCP servers** — FastMCP SSE tool servers in `mcp/`
3. **Orchestration** — Supervisor-worker routing in `orchestration/`
4. **Knowledge base** — JSON stubs synced to OpenSearch Serverless in production
5. **Infrastructure** — AWS CDK stack in `infrastructure/`

## Data flow

User request → Supervisor → Worker agent → MCP tools → Knowledge base / AWS persistence
