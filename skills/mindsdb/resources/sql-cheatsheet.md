# MindsDB SQL Cheatsheet

## Agents

```sql
-- Create
CREATE AGENT my_agent
USING
  model = { "provider": "openai", "model_name": "gpt-4o", "api_key": "sk-..." },
  data = {
    "knowledge_bases": ["mindsdb.my_kb"],
    "tables": ["pg_conn.my_table"]
  },
  prompt_template='Describe what each data source contains',
  timeout=10;

-- Query
SELECT answer FROM my_agent WHERE question = 'Your question here';

-- Query with model override
SELECT answer FROM my_agent
WHERE question = 'Your question'
USING model = { "provider": "google", "model_name": "gemini-2.5-flash", "api_key": "..." };

-- Update
ALTER AGENT my_agent
USING data = { "tables": ["pg_conn.new_table"] };

-- Delete
DROP AGENT my_agent;

-- List
SHOW AGENTS;
SHOW AGENTS WHERE name = 'my_agent';
```

## Knowledge Bases

```sql
-- Create
CREATE KNOWLEDGE_BASE my_kb
USING
  embedding_model = { "provider": "openai", "model_name": "text-embedding-3-large", "api_key": "sk-..." },
  reranking_model = { "provider": "openai", "model_name": "gpt-4o", "api_key": "sk-..." },
  metadata_columns = ['category'],
  content_columns = ['description'],
  id_column = 'item_id';

-- Create in a project
CREATE PROJECT my_project;
CREATE KNOWLEDGE_BASE my_project.my_kb USING ...;

-- Ingest data
INSERT INTO my_kb SELECT item_id, category, description FROM source_db.items;

-- Semantic search
SELECT * FROM my_kb WHERE content = 'search query';

-- Filtered search
SELECT * FROM my_kb WHERE content = 'search query' AND relevance >= 0.25;

-- Describe
DESCRIBE KNOWLEDGE_BASE my_kb;

-- List
SHOW KNOWLEDGE_BASES;

-- Delete
DROP KNOWLEDGE_BASE my_kb;
```

## Data Connections

```sql
-- Connect PostgreSQL
CREATE DATABASE pg_conn
WITH ENGINE = "postgres",
PARAMETERS = {
  "user": "user", "password": "pass",
  "host": "hostname", "port": "5432",
  "database": "dbname"
};

-- Connect MySQL
CREATE DATABASE mysql_conn
WITH ENGINE = "mysql",
PARAMETERS = {
  "user": "user", "password": "pass",
  "host": "hostname", "port": "3306",
  "database": "dbname"
};

-- Upload file
CREATE FILE my_data FROM '/path/to/file.csv';

-- List connections
SHOW DATABASES;

-- Drop connection
DROP DATABASE pg_conn;
```

## Views & Jobs

```sql
-- Create view
CREATE VIEW my_view AS (
  SELECT * FROM pg_conn.my_table WHERE status = 'active'
);

-- Create scheduled job
CREATE JOB my_job AS (
  INSERT INTO my_kb SELECT * FROM pg_conn.new_data
) EVERY hour;

-- List / Drop
SHOW JOBS;
DROP JOB my_job;
```

## Projects

```sql
CREATE PROJECT my_project;
SHOW PROJECTS;
DROP PROJECT my_project;
```
