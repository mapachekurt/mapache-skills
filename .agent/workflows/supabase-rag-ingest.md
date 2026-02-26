---
description: Scrape and ingest technical documentation into Supabase RAG system
---

1. **Scrape**: Use `firecrawl` to crawl the target documentation URL.
2. **Provision**: Create $TABLE_NAME in the `intelligence` schema with `vector(768)` support.
3. **Vectorize**: Generate embeddings using Gemini `text-embedding-004`.
4. **Ingest**: Batch insert content, metadata, and embeddings into Supabase.
5. **Memorialize**: Update the `SUPABASE_STANDARDS.md` if any new patterns are established.
