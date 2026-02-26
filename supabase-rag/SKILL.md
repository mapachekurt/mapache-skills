# Supabase Domain-Driven RAG Skill

Expert skill for managing Supabase database architecture and RAG ingestions following domain-driven design principles.

## Architecture Standards

- **Schemas**:
  - `public`: SaaS core logic.
  - `composio`: App ecosystem / marketplace.
  - `intelligence`: RAG data, internal technical docs.
- **Naming**: `snake_case` only. No schema-name prefixes in table names.
- **Documentation**: All DB entities must have `COMMENT ON` statements.

## RAG Ingestion Protocol

1. **Model**: Use Gemini `text-embedding-004` (768 dimensions).
2. **Table Schema**:
   ```sql
   CREATE TABLE intelligence.your_table (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       content TEXT NOT NULL,
       embedding VECTOR(768),
       metadata JSONB,
       created_at TIMESTAMPTZ DEFAULT NOW()
   );
   ```
3. **Secrets**: Use Google Secret Manager for all API keys.

## Scripts & Tools

- Use `SUPABASE_BETA_RUN_SQL_QUERY` for all DDL and batch insertions.
- Use `firecrawl` for technical documentation scraping.
