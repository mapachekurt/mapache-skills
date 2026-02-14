---
name: skill-wizard
description: Interactive wizard for creating grounded Antigravity skills.
---

# Skill: Skill Wizard

## Overview
Meta-skill for creating new Antigravity skills grounded in real documentation. Mirrors the [Context7 Skill Wizard](https://upstash.com/blog/context7-skill-wizard) flow. Use this to turn library docs into concise, constraint-focused AI instructions.

## When to Use

## The 5-Step Wizard Process

### Step 1: Describe the Expertise
Ask the user: **"What domain or technology should this skill cover?"**

Focus on *expertise*, not tasks. You are teaching the AI how to think about a domain, not asking it to do one specific thing.

**Example prompts:**
- "An expert in Beads agentic task management"
- "A Next.js 15 App Router specialist"
- "A Supabase Edge Functions developer"

### Step 2: Select Documentation Sources
Identify and read the **primary documentation sources** for the target domain. These can be:
- Official docs (URLs read via `read_url_content`)
- DeepWiki pages for open-source repos
- Local files or READMEs in the workspace
- Existing Knowledge Items (KIs) in Antigravity

**Critical**: The skill MUST be grounded in real, current documentation. Never generate patterns from memory alone. Always cite which docs you used.

### Step 3: Answer Clarifying Questions
Before generating the skill, ask the user 3-5 targeted questions to narrow scope:
- Which version / patterns do they use?
- Any specific sub-features to focus on?
- What are the most common mistakes they encounter?
- Integration context (e.g., "used with TypeScript? Deployed on Vercel?")

Provide recommended defaults for each question so the user can just press Enter.

### Step 4: Generate and Review
Generate the `SKILL.md` file following the standard Antigravity skill format:

```markdown
---
name: <skill-name>
description: <one-line description>
---

# Skill: <Title>

## Overview
<2-3 sentence description of what this skill teaches the AI>

## Core Concepts
<Key mental models, architecture patterns, and design principles>

## Best Practices
<Constraint-focused instructions: DO this, NEVER do that>

## Common Patterns
<Code snippets and usage examples grounded in real docs>

## Anti-Patterns
<What to avoid, with explanations of WHY>

## Key Commands / API Reference
<Quick-reference table of the most important commands or APIs>
```

Present the generated skill to the user for review. Offer:
1. **Edit in place** — make specific changes.
2. **Request changes** — describe what to adjust; regenerate.
3. **Approve** — install the skill.

### Step 5: Install
Write the final `SKILL.md` to the Antigravity skills directory:
```
C:\Users\<username>\.gemini\antigravity\skills\<skill-name>\SKILL.md
```

Confirm installation by listing the skills directory.

## Quality Checklist
Before finalizing any skill, verify:
- [ ] Grounded in real documentation (cite sources)
- [ ] Concise — no tutorials, only constraints and patterns
- [ ] Version-specific — references current API / patterns
- [ ] Has Anti-Patterns section — teaches what NOT to do
- [ ] Has command/API quick-reference table
- [ ] Follows the standard YAML frontmatter format

## Notes
- If an existing skill already covers part of the domain (e.g., `beads-coordinator`), the new skill should be **complementary**, not duplicative. Reference the existing skill and explain the relationship.
- Skills should be updated when libraries release major versions. Re-run the wizard with updated docs.
