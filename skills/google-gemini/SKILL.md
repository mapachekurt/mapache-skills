---
name: google-gemini
description: Access the latest Gemini models and grounding capabilities. Enables real-time information retrieval via Google Search and deep context via NotebookLM to prevent hallucinations and provide up-to-date answers.
---

# Google Gemini Grounding

## When to use this skill
Use this skill when the user asks for:
- Information about current events, latest library versions, or recent API changes.
- "Grounding" their agent or responses in real-world data.
- Guidance on using the "latest" Gemini models (e.g., Gemini 1.5 Pro, Gemini 3 Pro).
- Research that requires avoiding hallucinations by verifying facts.

## Core Capabilities

### 1. Live Grounding (Google Search)
**Tool**: `search_web`
**Usage**:
- ALWAYS use `search_web` when the user asks about recent events (post-knowledge cutoff) or specific technical documentation that changes frequently.
- **Pattern**:
  1. Identify the core entity or question.
  2. Formulate a specific search query.
  3. READ the search results.
  4. Synthesize the answer with citations (URLs).

**Example**:
> User: "What is the latest version of Next.js?"
> Agent: Call `search_web(query="latest Next.js version release notes")` -> "The latest version is 14.2..."

### 2. Custom Data Grounding (NotebookLM)
**Tool**: `mcp_notebooklm_query_gem_grounded` / `mcp_notebooklm_search_notebook_contents`
**Usage**:
- Use for **Deep Context Retrieval** (Project History, Meeting Transcripts, Large PDF Specs, Competitor Analysis).
- **CRITICAL GUARDRAIL**: Do **NOT** use NotebookLM for:
    - **Active Coding Rules**: Use `GEMINI.md` instead.
    - **Task Management**: Use `task.md` instead.
    - **Operational Skills**: Use Antigravity `skills/` instead.
- **Pattern**:
  1. Check if a relevant NotebookLM source is available (or ask user).
  2. Query the Gem for *background info* or *reference material*.
  3. Apply Antigravity Rules (`GEMINI.md`) to *implement* that material.

### 3. Model Usage Guidelines
- **Default to Latest**: Always assume the user wants the most capable model available (e.g., Gemini 1.5 Pro or newer).
- **Multimodal**: If the user provides images, use the natively multimodal capabilities of Gemini rather than separate OCR tools if possible.
- **Context**: Leverage the long context window of Gemini 1.5+ by reading full files when necessary (up to reasonable limits), rather than small snippets, to improve reasoning.

## Instructions for the Agent
1. **Check Freshness**: If a user asks a technical question, ask yourself: "Could this have changed recently?" If yes, SEARCH.
2. **Cite Sources**: When using `search_web` or `notebooklm`, explicitly link the source in the markdown response.
3. **Verify Deprecations**: If suggesting code, quickly search for "library_name deprecated features" to ensure you aren't suggesting legacy patterns.

## Setup (NotebookLM MCP)
To use the NotebookLM features, the `notebooklm-mcp-cli` must be installed and authenticated on the host machine.

1.  **Install `uv`** (if not present):
    ```bash
    pip install uv
    ```
2.  **Install the CLI**:
    ```bash
    uv tool install notebooklm-mcp-cli
    ```
3.  **Authenticate**:
    ```bash
    nlm login
    ```
    *Follow the browser flow to authorize access.*
4.  **Configure Antigravity (`mcp_config.json`)**:
    Use `uv tool run` to ensure the correct executable is found:
    ```json
    "notebooklm": {
      "command": "uv",
      "args": ["tool", "run", "notebooklm-mcp"]
    }
    ```

## Troubleshooting
- **MCP Error "Method not found"**: The server might be running the old "simulated" script. Restart Antigravity/MCP server to load the new config.
- **`nlm query` fails**: Use `nlm prompt` or `nlm list notebooks` instead. The CLI syntax can vary.
- **Authentication**: If `nlm login` hangs or fails to open a browser, try running it from a standard terminal (outside the agent) to interact with the auth flow.

## Verification
Run this command to test the connection:
```bash
nlm list notebooks
```
If it lists your notebooks, the setup is complete.
