---
name: skill-adoption
description: A meta-skill for detecting task failure, searching external repositories for pre-made agent skills, and internalizing those instructions to solve the problem.
license: MIT
metadata:
  author: Mapache Pulse
  version: 1.0.0
---

# Skill Adoption (Meta-Skill)

This skill enables the agent to act as a self-evolving system. When a task exceeds the agent's current logical framework or requires a specialized workflow, the agent will pause, search curated skill registries, and adopt the relevant `SKILL.md` instructions.

## Workflow

1. **Identify the Capability Gap:** When a task results in a "dead end," multiple failed attempts, or requires a domain-specific methodology (e.g., specialized security auditing or complex database migrations), trigger this skill.
2. **Search Registries:** Query the primary skill repositories using keywords derived from the problem. Look for `SKILL.md` files or directory names that match the required capability.
3. **Evaluate and Select:** Read the `description` and `workflow` of the found skill. Compare it against the current task requirements.
4. **Internalize (Adoption):** Load the full text of the `SKILL.md` into the active context. Acknowledge the new workflow and constraints defined in the skill.
5. **Execute and Verify:** Re-attempt the original task using the newly adopted methodology. If successful, flag the skill for permanent storage.

## Skill Registries (Knowledge Sources)

| Registry Name | Focus Area | Access Link |
| :--- | :--- | :--- |
| **Awesome AI Agent Skills** | Universal, platform-agnostic skills | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) |
| **Official Anthropic Skills** | High-quality general task workflows | [anthropics/skills](https://github.com/anthropics/skills) |
| **Awesome Agent Skills** | Comprehensive curated tool list | [skillmatic-ai/awesome-agent-skills](https://github.com/skillmatic-ai/awesome-agent-skills) |
| **GitHub Awesome Copilot** | DevOps and coding-specific skills | [github/awesome-copilot](https://github.com/github/awesome-copilot) |
| **Hugging Face Skills** | AI, ML, and data handling | [huggingface/skills](https://github.com/huggingface/skills) |
| **Skills.sh** | Global indexing registry | [https://skills.sh](https://skills.sh) |

## Proactive Skill Search (Recent History)
The following registries have been proactively swept for common difficulties. If facing issues in these domains, use these links first:
- **OAuth & API Integration:** [OAuth 2.0 Setup Skill](https://github.com/seb1n/awesome-ai-agent-skills/blob/main/api-and-integration/oauth-2-0-setup/SKILL.md)

## Usage

When encountering a problem you cannot solve:
"I am having difficulty with [Task]. I will now trigger the 'skill-adoption' meta-skill to search for a pre-made solution in my curated registries."

## Best Practices
- **Prioritize Standards:** Only adopt skills that follow the `SKILL.md` format (YAML frontmatter + Markdown workflow) to ensure compatibility.
- **Check for Regressions:** Ensure the new skill does not conflict with core system instructions or Mapache-specific logic.

## Strategy for Persistent Memory (PG Vector RAG)
While the Meta-Skill allows for "on-the-fly" adoption, relying on web searches every time is inefficient. To streamline this for the future, you should implement the PG Vector RAG as your agent's Procedural Memory.

*   **Skill Ingestion:** Whenever the agent successfully adopts a skill from the list above, it should generate a vector embedding of that `SKILL.md` file and store it in your Supabase `agent_skills` table.
*   **Local-First Search:** Before hitting the external GitHub repositories, the agent should first perform a semantic search against your local PG Vector database to see if it has "learned" or "cached" a similar skill previously.
*   **Hollowing out the Web:** Over time, your Supabase instance will become a private, high-speed mirror of the best agent skills from across the web, tailored specifically to the Mapache architecture.

This setup ensures that once the Antigravity agent solves a "problem" once by adopting a skill, it never has to "search" for that logic again—it simply retrieves it from its own memory.
