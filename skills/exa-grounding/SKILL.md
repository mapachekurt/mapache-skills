---
name: exa-grounding
description: Use this skill to ground a new AI agent in a specific domain. It performs deep research via Exa, synthesizes a System Prompt, and optionally populates a Supabase Vector DB.
---

# Exa Grounding: The Agent Genesis Skill

## Goal
To bootstrap a new AI agent with "Deep Knowledge" of a specific topic, ensuring it is grounded in authoritative sources before it writes a single line of code.

## Workflow Overview
This is a **Hybrid Workflow** combining Agent Capabilities (Search/Synthesis) and Local Scripts (Vector Ops).

1.  **Phase 0: Define Success (The Standard)**
    - Before gathering knowledge, you MUST define *how* the agent will be tested.
    - Use Exa to find "tough interview questions" or "certification scenarios".
    - Create a `verification_suite.md` or `.py` that the agent *must* pass.

2.  **Phase 1: Deep Research (Agent-Driven)**
    - The Agent (You) uses the `EXA_SEARCH` tool (via Rube) to find authoritative documentation.
    - You read the content and save the raw findings to `knowledge_core_raw.md`.

3.  **Phase 2: Synthesis (Agent-Driven)**
    - You process `knowledge_core_raw.md` to remove noise/marketing.
    - You create a "Golden Reference" artifact named `knowledge_core_clean.md`.

4.  **Phase 3: Vector Genesis (Script-Driven)**
    - You run `scripts/ground_agent.py` to chunk and upsert `knowledge_core_clean.md` to Supabase.
    - *Verification*: Run the `verification_suite` against the new agent. If it fails, return to Phase 1.

5.  **Phase 4: Prompt Generation (Agent-Driven)**
    - You draft the System Prompt based on the clean knowledge core.

## Configuration
- **Script**: `scripts/ground_agent.py`
- **Environment** (`.env`):
    - `DB_CONNECTION`: Postgres connection string for Supabase Vector.
    - `EXA_API_KEY`: Required for `generate_evals.py` script (if used).

## Instructions

### Step 0: Design Evals
"Find 5 difficult scenarios for [Topic]."
-> Output: `verification_suite.md`.

### Step 1: Execute Research
"I will now search for [Topic] using Rube."
-> Run `EXA_SEARCH` tool.
-> Save findings to artifact.

### Step 2: Synthesize
"I will distill these findings into a Knowledge Core."
-> Read findings.
-> Write `knowledge_core_clean.md`.

### Step 3: Vector Upsert
Run the script to push the *Clean* knowledge to the DB.

```bash
uv run python scripts/ground_agent.py --file "knowledge_core_clean.md" --action vector --collection "agent_knowledge"
```

### Step 4: Draft Prompt
Create the system prompt:
> "You are an expert in [TOPIC]..."
