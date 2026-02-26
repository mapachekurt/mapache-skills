# Google Gemini Grounding Skill

This skill provides a manual implementation of the capabilities expected from the `@google/gemini` package, specifically focused on **Grounding** and **Model Currency**.

## Features
- **Live Web Grounding**: Leveraging Antigravity's `search_web` tool to pull real-time data.
- **Custom Knowledge Grounding**: Integrating with NotebookLM via MCP.
- **Latest Model Patterns**: Instructions to prefer modern Gemini 1.5+ patterns (long context, multimodal).

## Installation
This skill is installed in `mapache-skills/skills/google-gemini`.

## Usage
The agent will automatically utilize this skill when you ask for:
- "Ground this answer..."
- "Check the latest docs..."
- "Use Gemini 1.5 features..."

## Relationship to `@google/gemini`
This skill mimics the behavior described in "Gemini's Latest SKILL Update" by orchestrating the underlying tools (Search, NotebookLM) directly within the Antigravity framework.
