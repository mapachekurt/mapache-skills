---
name: mindsdb
description: Federated AI query engine — build SQL-based agents, knowledge bases with hybrid search, and connect 200+ data sources behind a unified SQL interface.
---

# MindsDB

## When to use this skill
Use this skill when the user asks to:
- Build AI agents that query databases or knowledge bases using natural language.
- Create and manage vector knowledge bases with semantic or hybrid search.
- Connect multiple data sources (Postgres, MySQL, MongoDB, S3, etc.) behind a unified SQL API.
- Deploy MindsDB locally or in the cloud.

## Core Concepts

MindsDB follows a **Connect → Unify → Respond** philosophy:
1. **Connect** — Link 200+ data sources via `CREATE DATABASE`.
2. **Unify** — Organize data with knowledge bases, views, and jobs.
3. **Respond** — Query AI agents that combine LLMs with your data.

> **Key Insight**: Everything in MindsDB is SQL. Agents, knowledge bases, and data sources are all queried with SQL-like syntax.

## 1. AI Agents

Agents combine an LLM with data sources (tables and knowledge bases) to answer natural-language questions.

### Create an Agent

```sql
CREATE AGENT my_agent
USING
  model = {
    "provider": "openai",
    "model_name": "gpt-4o",
    "api_key": "sk-..."
  },
  data = {
    "knowledge_bases": ["mindsdb.sales_kb", "mindsdb.orders_kb"],
    "tables": ["postgres_conn.customers", "mysql_conn.products"]
  },
  prompt_template='
    mindsdb.sales_kb stores sales analytics data
    mindsdb.orders_kb stores order data
    postgres_conn.customers stores customer records
    mysql_conn.products stores product catalog
  ',
  timeout=10;
```

**Parameters:**
| Parameter | Required | Description |
|---|---|---|
| `model` | Yes | LLM config: `provider`, `model_name`, `api_key`, optional `base_url` and `api_version` |
| `data` | No | `knowledge_bases` and/or `tables` lists for the agent to query |
| `prompt_template` | No | Natural-language description of what each data source contains |
| `timeout` | No | Max response time in seconds |

**Supported Providers:** `openai`, `google`, `azure_openai`, `anthropic`

### Query an Agent

```sql
SELECT answer
FROM my_agent
WHERE question = 'What is the average number of orders per customer?';
```

Override model at query time:

```sql
SELECT answer
FROM my_agent
WHERE question = 'Summarize top products'
USING model = {
  "provider": "google",
  "model_name": "gemini-2.5-flash",
  "api_key": "ABc123"
};
```

### Modify / Delete

```sql
-- Update data sources or model
ALTER AGENT my_agent
USING data = {
  "knowledge_bases": ["mindsdb.sales_kb"],
  "tables": ["mysql_db.car_sales", "mysql_db.car_info"]
};

-- Remove agent
DROP AGENT my_agent;
```

### Wildcard Data Binding

Use `*` to give the agent access to all tables or KBs in a connection:

```sql
CREATE AGENT my_agent
USING
  model = { ... },
  data = {
    "knowledge_bases": ["project_name.*"],
    "tables": ["datasource_conn_name.*"]
  };
```

## 2. Knowledge Bases

Knowledge bases store embeddings for semantic search and optional hybrid search (BM25 + vector).

### Create a Knowledge Base

```sql
CREATE KNOWLEDGE_BASE my_kb
USING
  embedding_model = {
    "provider": "openai",
    "model_name": "text-embedding-3-large",
    "api_key": "sk-..."
  },
  reranking_model = {
    "provider": "openai",
    "model_name": "gpt-4o",
    "api_key": "sk-..."
  },
  metadata_columns = ['product'],
  content_columns = ['notes'],
  id_column = 'order_id';
```

**Parameters:**
| Parameter | Required | Description |
|---|---|---|
| `embedding_model` | Yes | Provider + model for vector embeddings (`openai`, `azure_openai`) |
| `reranking_model` | No | LLM for hybrid search re-ranking (enables BM25 + vector) |
| `storage` | No | External vector store table (e.g., `my_vector_store.storage_table`) |
| `metadata_columns` | No | Columns stored as filterable metadata |
| `content_columns` | No | Columns whose text gets embedded |
| `id_column` | No | Unique identifier column |

### Ingest Data

```sql
INSERT INTO my_kb
SELECT order_id, product, notes
FROM sample_data.orders;
```

### Semantic Search

```sql
SELECT * FROM my_kb
WHERE content = 'color preference';
```

### Filter by Relevance

```sql
SELECT * FROM my_kb
WHERE content = 'color'
AND relevance >= 0.25;
```

### Manage Knowledge Bases

```sql
SHOW KNOWLEDGE_BASES;
DESCRIBE KNOWLEDGE_BASE my_kb;
DROP KNOWLEDGE_BASE my_kb;
```

## 3. Data Integrations

Connect external databases with `CREATE DATABASE`:

```sql
CREATE DATABASE my_postgres
WITH ENGINE = "postgres",
PARAMETERS = {
  "user": "demo_user",
  "password": "demo_password",
  "host": "samples.mindsdb.com",
  "port": "5432",
  "database": "my_database"
};
```

**Popular Engines:** `postgres`, `mysql`, `mariadb`, `mongodb`, `snowflake`, `bigquery`, `redshift`, `s3`, `clickhouse`, `elasticsearch`, `dynamodb`, `sqlite`

Upload files directly:

```sql
CREATE FILE my_data FROM '/path/to/data.csv';
```

## 4. Installation

| Method | Command / Link |
|---|---|
| **Docker Desktop** (recommended) | [docs.mindsdb.com/setup/self-hosted/docker-desktop](https://docs.mindsdb.com/setup/self-hosted/docker-desktop) |
| **Docker** | `docker run --name mindsdb -p 47334:47334 -p 47335:47335 mindsdb/mindsdb` |
| **PyPI** | `pip install mindsdb` |
| **AWS Marketplace** | [docs.mindsdb.com/setup/cloud/aws-marketplace](https://docs.mindsdb.com/setup/cloud/aws-marketplace) |

## 5. Agent-to-Agent (A2A) Protocol

MindsDB supports [Google's A2A protocol](https://google.github.io/A2A/) — an open standard for agent-to-agent communication built on JSON-RPC 2.0 over HTTP(S). This is **complementary to MCP**: MCP handles agent-to-tool communication, while A2A handles agent-to-agent communication.

> **Key Distinction**:
> - **MCP** = Agent ↔ Tool (e.g., "query this database")
> - **A2A** = Agent ↔ Agent (e.g., "delegate this analysis to a specialist agent")

### How It Works

Every MindsDB agent automatically becomes an A2A-compatible agent when the server is running:

1. **Discovery** — Other agents find your agent via its **Agent Card** at `/.well-known/agent.json`
2. **Task Management** — Agents can send tasks, check status, and receive results
3. **Artifact Exchange** — Agents share structured results (tables, files, reports) during collaboration
4. **Streaming** — Supports real-time streaming responses between agents

### Agent Card

Each MindsDB agent exposes an Agent Card — a JSON document describing its capabilities:

```
GET http://localhost:47334/.well-known/agent.json
```

The Agent Card includes:
| Field | Description |
|---|---|
| `name` | Agent name (from `CREATE AGENT`) |
| `description` | What the agent does |
| `url` | Service endpoint URL |
| `capabilities` | Streaming, push notifications, state history |
| `skills` | List of specific capabilities the agent can perform |
| `authentication` | Required auth schemes |

### Architecture (Unified Server)

As of September 2025, MindsDB runs **HTTP, MCP, and A2A on a single server process**:

```
Port 47334 → HTTP REST API + A2A endpoint
Port 47335 → MCP SSE endpoint
```

This means any agent you create with `CREATE AGENT` is automatically accessible via:
- **SQL** (`SELECT FROM agent`)
- **MCP** (via the `query` tool)
- **A2A** (via the Agent Card and JSON-RPC)
- **Chat UI** (via the MindsDB web interface)

### Multi-Agent Collaboration Example

A typical MindsDB A2A setup uses specialized agents:

```sql
-- SQL Agent: queries structured databases
CREATE AGENT sql_agent
USING
  model = { "provider": "openai", "model_name": "gpt-4o", "api_key": "sk-..." },
  data = { "tables": ["postgres_conn.*"] },
  prompt_template='You are a SQL specialist. Query databases to answer questions.';

-- Knowledge Agent: searches unstructured documents
CREATE AGENT knowledge_agent
USING
  model = { "provider": "openai", "model_name": "gpt-4o", "api_key": "sk-..." },
  data = { "knowledge_bases": ["mindsdb.docs_kb"] },
  prompt_template='You are a knowledge specialist. Search documents to answer questions.';

-- A chat agent can then coordinate between these via A2A
```

External A2A clients discover these agents at `http://localhost:47334/.well-known/agent.json` and send tasks via JSON-RPC 2.0.

## Instructions for the Agent

1. **Always use SQL syntax** — MindsDB's interface is SQL. Don't suggest REST API calls when SQL commands exist.
2. **Describe data in prompt_template** — When creating agents, always include a `prompt_template` that tells the LLM what each connected data source contains.
3. **Prefer knowledge bases for unstructured data** — Documents, notes, and text go into knowledge bases. Structured tables stay as database connections.
4. **Use hybrid search for accuracy** — When creating knowledge bases for production use, include a `reranking_model` to enable BM25 + vector hybrid search.
5. **Use A2A for multi-agent architectures** — When building systems with specialized agents, leverage A2A for inter-agent communication rather than chaining SQL queries.
6. **Check the SQL cheatsheet** — See [resources/sql-cheatsheet.md](resources/sql-cheatsheet.md) for a quick reference of all commands.

## References

- [Official Docs](https://docs.mindsdb.com)
- [Agent Syntax](https://docs.mindsdb.com/mindsdb_sql/agents/agent_syntax)
- [Knowledge Base Docs](https://docs.mindsdb.com/mindsdb_sql/knowledge_bases/overview)
- [Data Integrations](https://docs.mindsdb.com/integrations/data-overview)
- [A2A Protocol](https://google.github.io/A2A/)
- [GitHub](https://github.com/mindsdb/mindsdb)
