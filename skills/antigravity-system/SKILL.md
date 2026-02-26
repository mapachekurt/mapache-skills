---
name: antigravity-system
description: The specific architectural and configuration knowledge of this Antigravity environment. Use this skill to understand file paths, artifact conventions, and toolchain requirements.
---

# Antigravity System Knowledge

## When to use this skill
- When an agent needs to **find configuration files** (e.g., "Where is mcp_config.json?").
- When an agent needs to **understand artifact structure** (e.g., "Where do I save the plan?").
- When an agent encounters **toolchain errors** (e.g., "Python script not found", "MCP connection failed").
- When an agent is **newly instantiated** and needs to ground itself in the environment.

## Critical Configuration

### 1. Master Configuration
- **File**: `mcp_config.json`
- **Path**: `C:\Users\Kurt Anderson\.gemini\antigravity\mcp_config.json`
- **Purpose**: Defines all MCP servers (Cloud Run, Rube, NotebookLM, Beads, Pencil).
- **Modification Rule**: ALWAYS use `uv tool run` for Python-based MCPs to avoid "simulated" script errors. Restart Antigravity after changes.

### 2. Extensions & Tools
- **Extensions**: `C:\Users\Kurt Anderson\.antigravity\extensions`
- **Python Tools**: `C:\Users\Kurt Anderson\.uv\tools` (Managed by `uv`).
- **Global Workflows**: `C:\Users\Kurt Anderson\.gemini\antigravity\global_workflows`

## Artifact System ("The Brain")

### 1. Location
- **Root**: `C:\Users\Kurt Anderson\.gemini\antigravity\brain\<conversation-id>`
- **Convention**: All persistent artifacts MUST be saved here.

### 2. Standard Artifacts
- **task.md**: The proactive checklist. Updated via `task_boundary` and `write_to_file`.
- **implementation_plan.md**: The technical design doc. Created in PLANNING mode.
- **walkthrough.md**: The proof-of-work doc. Created in VERIFICATION mode.

## Guidelines & Architecture (Official)

### 1. The Antigravity Ecosystem
- **Skills ("Brains")**: Ephemeral, lightweight task definitions (like this file). Driven by LLM intent matching.
    - *Scope*: Workspace (`<root>/.agent/skills`) or Global (`~/.gemini/antigravity/skills`).
- **MCPs ("Hands")**: Persistent, heavy-duty tool connections (e.g., PostgreSQL, GitHub). Managed via `mcp_config.json`.
- **Rules ("Guardrails")**: Passive, always-on constraints (e.g., `GEMINI.md`).
- **Workflows ("Macros")**: User-triggered sequences for repeatable tasks.

### 2. Skill Structure Standard
All skills should follow this directory structure:
```text
my-skill/
├── SKILL.md         # Definition & Instructions (Frontmatter + Body)
├── scripts/         # Executable logic (Python/Bash/Node)
├── references/      # Static knowledge & templates
└── assets/          # Images/Logos
```

### 3. Toolchain Guidelines

#### Python (`uv`)
- **Rule**: This environment uses `uv` for Python management.
- **Install**: `pip install uv` (if missing).
- **Run**: `uv tool run <tool-name>` or `uv pip install <package>`.

#### Browser (`agent-browser`)
- **Rule**: Use `agent-browser` (via `skills/agent-browser`) for authenticated sessions.
- **Auth**: Authenticate via `nlm login` (NotebookLM) or similar CLI tools in the user's terminal, NOT inside the agent's headless browser if possible.

## EXPERT KNOWLEDGE & HIDDEN FEATURES

### 1. The "Vibe Coding" Protocol
To maximize efficiency, split responsibilities:
- **Nano Banana Pro**: Use for *Layout & Visuals* (CSS/Structure).
- **Gemini 3 Pro**: Use for *Logic & Architecture* (Typescript/React/Node).
- **Workflow**: 
  1. Prompt Nano Banana for the visual shell. 
  2. Prompt Gemini to "wire it up" with logic.

### 2. Hidden Slash Commands
Antigravity supports undocumented slash commands for power users:
- **/codebase**: Force-reindex the codebase context.
- **/component [name]**: Scaffold a full React component (index, types, test, story).
- **/refactor**: Triggers the "Smart Refactor" agent on the active file.
- **/debug**: Enters "Evidence-Based Debugging" mode (auto-injects logs).
- **/security**: Scans the current file for secrets/API keys.

### 3. Advanced Configuration (`settings.json`)
Unlock beta features by adding these to your VSCode `settings.json`:
```json
{
  "antigravity.experimental.enabled": true,
  "antigravity.agent.beta": true,        // Unlocks Voice & Multi-Agent
  "antigravity.context.smart": true,     // Semantic Context Loading
  "antigravity.ui.showConfidence": true, // Show AI confidence scores
  "antigravity.generation.parallel": true // Faster, multi-file edits
}
```

### 4. Power User Workflows
- **Multi-File Refactor**: Enter Agent Mode (Cmd+Shift+A) -> "Rename X to Y everywhere" -> Review in Manager View.
- **Instant Docs**: Select function -> Cmd+I -> "/docs".
- **Quick Fix**: Select Error -> Cmd+K -> "fix".

## Knowledge System ("KIs")
- **Location**: `C:\Users\Kurt Anderson\.gemini\antigravity\knowledge`
- **Purpose**: Long-term memory and distilled insights.

## Troubleshooting

### "Simulated" vs Real
- **Symptom**: "NotebookLM returned simulated data."
- **Cause**: `mcp_config.json` points to `playground/.../mcp_notebooklm.py`.
- **Fix**: Update config to use `uv tool run notebooklm-mcp`.

### "Path Not Found"
- **Cause**: Using relative paths or assuming Linux paths on Windows.
- **Fix**: ALWAYS use absolute paths starting with `C:\Users\Kurt Anderson\...`.

### Security Warning
- **API Keys**: NEVER paste raw API keys in chat or comments. Markdown rendering can be exploited. Use `.env` files.

## Core Concepts (Architecture)
- **Agent-First IDE**: Antigravity is not just an editor; it's a runtime for "Context-Aware Agents".
- **Multi-Model Intelligence**: 
    - *Gemini 3 Pro*: The "Architect" (Logic, Reasoning, Code).
    - *Nano Banana*: The "Artist" (Visuals, Layouts, Assets).
- **Artifacts**: The "Bridge" between Human and Agent (Plans, Walkthroughs). NEVER skip creating them for complex tasks.

## Best Practices (Official)
### ✅ DO
- **Atomic Commits**: Keep changes small and verifiable.
- **Context Boundaries**: Use `/codebase` or `/folder` to scope the agent's attention.
- **Review Artifacts**: Use the "Comment" feature on artifacts to guide the agent asynchronously.

### ❌ DON'T
- **Overload Context**: Don't dump entire repos into the chat. Use targeted context.
- **Ignore Plans**: Always review `implementation_plan.md` before approving execution.

