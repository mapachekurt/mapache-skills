import os
import argparse
import sys
from typing import List, Dict

# Try to import required libraries, guide user if missing
try:
    from exa_py import Exa
    import vecs
    from dotenv import load_dotenv
    # Assuming standard OpenAI for embeddings unless otherwise specified
    # In a real scenario, we might use a lighter model or Antigravity's internal tools if available via bridge
    # For now, we'll assume the user has OPENAI_API_KEY or we skip embedding generation in this script
    # and just output text for the agent to embed properly.
    # Actually, standardizing on sentence-transformers for local embedding would be better/cheaper
    # but `vecs` often integrates with OpenAI or other providers.
    # Let's assume standard OpenAI for simplicity of this script, or fall back to just text output.
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Please run: uv pip install exa-py vecs python-dotenv openai")
    sys.exit(1)

load_dotenv()

def search_exa(topic: str, api_key: str) -> str:
    """Performs a deep neural search on Exa."""
    print(f"🔍 Searching Exa for: '{topic}'...")
    exa = Exa(api_key)
    
    # "Neural" search with autoprompt is best for broad concept grounding
    result = exa.search_and_contents(
        topic,
        type="neural",
        use_autoprompt=True,
        num_results=5,
        text=True
    )
    
    knowledge_core = f"# Knowledge Core: {topic}\n\n"
    
    for res in result.results:
        print(f"  - Found: {res.title}")
        knowledge_core += f"## Source: {res.title}\n"
        knowledge_core += f"**URL**: {res.url}\n\n"
        knowledge_core += f"{res.text[:5000]}... [truncated]\n\n" # Truncate to avoid massive context overhead
        
    return knowledge_core

def upsert_vectors(file_path: str, collection_name: str, supabase_url: str, supabase_key: str):
    """Chunks and upserts knowledge to Supabase."""
    print(f"💾 Upserting {file_path} to Supabase collection '{collection_name}'...")
    
    # Connect to Supabase Vector
    # Note: vecs connects via Postgres connection string, not URL/Key directly usually.
    # We construct the connection string from standard Supabase params if possible
    # DB_CONNECTION = "postgresql://postgres.project:password@aws-0-region.pooler.supabase.com:6543/postgres"
    db_connection = os.getenv("DB_CONNECTION")
    if not db_connection:
         print("❌ Error: DB_CONNECTION environment variable required for Supabase Vector.")
         sys.exit(1)

    vx = vecs.create_client(db_connection)
    docs = vx.get_or_create_collection(name=collection_name, dimension=1536) # Standard OpenAI dimension

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Naive chunking by double newline (paragraphs)
    # In production, use a proper text splitter (RecursiveCharacterTextSplitter)
    chunks = content.split("\n\n")
    
    vectors = []
    # NOTE: This script assumes you have a way to generate embeddings. 
    # For this simplified version, we will placeholder the embedding generation
    # or rely on the `vecs` adapter if configured (vecs handles orchestration if you pass an adapter).
    # Since we didn't set up an adapter, we'll just warn the user.
    
    print("⚠️  Warning: Embedding generation requires a configured adapter in this script.")
    print("⚠️  For now, just verifying connection and content read.")
    print(f"ℹ️  Read {len(chunks)} chunks from knowledge core.")
    
    # Real implementation would loop chunks, call OpenAI/Gemini embedding API, and upsert.
    # docs.upsert(records=[(id, vec, meta), ...])
    
    print("✅ Connection relevant. Knowledge Core ready for embedding.")

def main():
    parser = argparse.ArgumentParser(description="Exa Grounding Agent Script")
    parser.add_argument("--action", choices=["search", "vector"], required=True)
    parser.add_argument("--topic", help="Topic to research")
    parser.add_argument("--file", help="File to upsert")
    parser.add_argument("--collection", default="agent_knowledge", help="Vector collection name")
    
    args = parser.parse_args()
    
    exa_key = os.getenv("EXA_API_KEY")
    
    if args.action == "search":
        if not args.topic:
            print("Error: --topic required for search")
            sys.exit(1)
        if not exa_key:
            print("Error: EXA_API_KEY not set")
            sys.exit(1)
            
        content = search_exa(args.topic, exa_key)
        
        output_file = "knowledge_core.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ Knowledge synthesis saved to {output_file}")
        
    elif args.action == "vector":
        if not args.file:
             print("Error: --file required for vector upsert")
             sys.exit(1)
        
        upsert_vectors(args.file, args.collection, "", "")

if __name__ == "__main__":
    main()
