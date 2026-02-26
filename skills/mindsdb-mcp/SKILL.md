---
name: mindsdb-mcp
description: Run MindsDB as an MCP and A2A server to give AI agents federated access to 200+ data sources via SQL queries. Covers Docker setup, authentication, A2A Agent Cards, and Antigravity integration.
---

# MindsDB MCP & A2A Server

## When to use this skill
Use this skill when the user asks to:
- Connect MindsDB as an MCP server to Cursor, OpenAI, Anthropic, or Antigravity.
- Give AI agents federated SQL access to multiple databases through a single MCP endpoint.
- Set up MindsDB's MCP server locally with Docker.
- Enable agent-to-agent (A2A) communication between MindsDB agents and external A2A clients.
- Discover MindsDB agent capabilities via A2A Agent Cards.

## How It Works

MindsDB acts as a **unified data gateway** via MCP:
1. Client connects to the MindsDB MCP server.
2. A query is issued from the client.
3. MindsDB routes the query to the appropriate federated data sources.
4. Results are unified and returned to the client.

## Setup

### Prerequisites
- Docker or Docker Desktop installed
- Data sources you want to query (optional — can add later)

### 1. Start MCP Server (No Auth)

Best for local development and Cursor:

```bash
docker run --name mindsdb_container \
  -p 47334:47334 \
  -p 47335:47335 \
  mindsdb/mindsdb
```

### 2. Start MCP Server (With Auth)

Required for OpenAI and Anthropic integrations:

```bash
docker run --name mindsdb_container \
  -p 47334:47334 \
  -p 47335:47335 \
  -e MINDSDB_USERNAME=admin \
  -e MINDSDB_PASSWORD=password123 \
  mindsdb/mindsdb
```

### 3. Get Auth Token

```bash
curl -X POST \
  -d '{"username":"admin","password":"password123"}' \
  -H "Content-Type: application/json" \
  http://localhost:47334/api/login
```

This returns a token for use in MCP client configuration.

### 4. Verify Server Status

```bash
curl http://127.0.0.1:47334/mcp/status
```

A successful response means the MCP environment is ready.

## MCP Tools

MindsDB exposes two MCP tools:

| Tool | Description |
|---|---|
| `list_databases` | Lists all connected data sources and their tables |
| `query` | Executes SQL queries against MindsDB (agents, KBs, databases) |

## Antigravity Integration

Add MindsDB to your `mcp_config.json`:

```json
{
  "mindsdb": {
    "url": "http://127.0.0.1:47335/mcp",
    "transport": "streamable-http"
  }
}
```

For authenticated connections, include the token in headers:

```json
{
  "mindsdb": {
    "url": "http://127.0.0.1:47335/mcp",
    "transport": "streamable-http",
    "headers": {
      "Authorization": "Bearer <token_from_login>"
    }
  }
}
```

> **Note**: Port `47334` = HTTP/REST API + A2A endpoint. Port `47335` = MCP SSE endpoint. All three protocols (HTTP, MCP, A2A) run in a **single server process**.

## Client Connection Guides

| Client | Auth Required | Docs |
|---|---|---|
| **Cursor** | No | [docs.mindsdb.com/mcp/cursor_usage](https://docs.mindsdb.com/mcp/cursor_usage) |
| **OpenAI** | Yes | [docs.mindsdb.com/mcp/openai](https://docs.mindsdb.com/mcp/openai) |
| **Anthropic** | Yes | [docs.mindsdb.com/mcp/anthropic](https://docs.mindsdb.com/mcp/anthropic) |

## Connecting Data Sources

Once the MCP server is running, connect data sources via the MindsDB SQL editor (at `http://localhost:47334`) or through the `query` MCP tool:

```sql
CREATE DATABASE sales_data
WITH ENGINE = "postgres",
PARAMETERS = {
  "user": "demo_user",
  "password": "demo_password",
  "host": "samples.mindsdb.com",
  "port": "5432",
  "database": "sales_manager_data"
};
```

## A2A Protocol

MindsDB also supports [Google's A2A protocol](https://google.github.io/A2A/) for **agent-to-agent communication** — complementary to MCP (which handles agent-to-tool communication).

| Protocol | Purpose | Port | Transport |
|---|---|---|---|
| **MCP** | Agent ↔ Tool | 47335 | SSE / Streamable HTTP |
| **A2A** | Agent ↔ Agent | 47334 | JSON-RPC 2.0 over HTTP(S) |

### Agent Card Discovery

Every MindsDB agent created with `CREATE AGENT` automatically exposes an **Agent Card** — a JSON document describing its capabilities:

```
GET http://localhost:47334/.well-known/agent.json
```

External A2A clients use this endpoint to:
1. **Discover** available agents and their skills
2. **Send tasks** via JSON-RPC 2.0
3. **Receive results** including streaming responses and structured artifacts

### A2A Client Configuration

A2A clients connect to the same Docker container — no additional setup needed:

```
A2A Endpoint:  http://localhost:47334
Agent Card:    http://localhost:47334/.well-known/agent.json
Auth:          Same token-based auth as HTTP/MCP
```

> For detailed A2A concepts (Agent Cards, multi-agent collaboration patterns, specialized agent design), see the core [mindsdb skill](../mindsdb/SKILL.md#5-agent-to-agent-a2a-protocol).

## Instructions for the Agent

1. **Always verify the server is running** before attempting MCP queries — check `http://127.0.0.1:47334/mcp/status`.
2. **Use no-auth for local dev** — only enable auth when connecting to external clients (OpenAI, Anthropic).
3. **Port mapping matters** — `47334` = HTTP API + A2A, `47335` = MCP endpoint. Don't mix them up.
4. **MCP for tools, A2A for agents** — Use MCP when an AI tool needs to query data. Use A2A when agents need to collaborate with each other.
5. **Combine with the `mindsdb` skill** — Use the core MindsDB skill for SQL syntax reference when writing queries through the MCP `query` tool.

## Troubleshooting

- **Container won't start**: Check if ports 47334/47335 are already in use: `docker ps` or `netstat -tlnp`.
- **MCP status returns error**: The container may still be initializing. Wait 30-60 seconds and retry.
- **Auth token expired**: Re-run the login curl command to get a fresh token.
- **"Connection refused" from AI client**: Ensure the Docker container is running and the correct port is being used.
- **A2A Agent Card not found**: Ensure at least one agent exists (`CREATE AGENT`) and the server is fully initialized.

## References

- [MCP Overview](https://docs.mindsdb.com/mcp/overview)
- [MCP Usage & Tools](https://docs.mindsdb.com/model-context-protocol/usage)
- [A2A Protocol Spec](https://google.github.io/A2A/)
- [Docker Setup](https://docs.mindsdb.com/setup/self-hosted/docker)
- [GitHub](https://github.com/mindsdb/mindsdb)
