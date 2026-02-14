# Exa Grounding Skill

This skill provides a workflow for "Agent Genesis"—Creating new AI agents that are deeply grounded in specific knowledge domains.

## Features
- **Deep Research**: Uses Exa's `neural` search to find authoritative content.
- **Knowledge Synthesis**: Guides the user/agent to distill raw data into a "Knowledge Core".
- **Vector Memory**: seamlessly pushes knowledge to Supabase `pgvector` via `vecs`.

## Usage
See `SKILL.md` for detailed instructions.

## Setup
1. Install dependencies: `uv pip install -r requirements.txt`
2. Set `.env` variables: `EXA_API_KEY`, `DB_CONNECTION`.
