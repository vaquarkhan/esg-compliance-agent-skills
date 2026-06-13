# MCP Servers — ESG Compliance

Five Python MCP servers using **FastMCP** with **SSE** transport (`mcp.run(transport="sse")`).

## Servers

| Directory | Default port | Purpose |
| --- | --- | --- |
| `regulatory-db-server/` | 8001 | Framework requirements, deadlines |
| `emissions-factor-server/` | 8002 | EPA/DEFRA/IPCC factors |
| `taxonomy-criteria-server/` | 8003 | EU Taxonomy TSC/DNSH |
| `filing-submission-server/` | 8004 | CSRD/SEC filing stubs |
| `sanctions-screening-server/` | 8005 | Entity screening |

## Local run

```bash
python mcp/regulatory-db-server/server.py
```

## Docker

```bash
docker build -t esg-regulatory-mcp mcp/regulatory-db-server
docker run -p 8001:8001 esg-regulatory-mcp
```

## Cursor MCP config example

```json
{
  "mcpServers": {
    "esg-regulatory": {
      "url": "http://127.0.0.1:8001/sse"
    }
  }
}
```
