---
name: beads-coordinator
description: Beads execution memory for mapache-solutions — session protocol, task management, cross-repo coordination via mapache-beads-hub.
---

# Beads Coordinator Skill (Mapache Workspace)

## Overview
Beads (`bd`) is a git-native task tracker that provides persistent **execution memory** for coding agents. In the mapache-solutions ecosystem, Beads coordinates work across multiple repos and agents (Jules, Codex, Antigravity).

**Architecture**: Linear = Strategy → Antigravity = Orchestration → Beads = Execution Memory → Worker Agents

## Mapache Repo Map
All repos in `mapache-solutions` org are Beads-enabled:

| Repo | Purpose |
|------|---------|
| `mapache-beads-hub` | Cross-repo hydrated task graph (Chief Agent home) |
| `mapache-app` | mapache.app — `website/` + `conversation/` (independent surfaces) |
| `mapache-solutions-web` | Traditional web app (skunkworks) |
| `mapache-agents` | ADK/A2A agent definitions |
| `mapache-infra` | DevOps, Cloud Run, Terraform |
| `mapache-lab` | Experiments (Wellgevity, FutureTech) |

## Session Protocol

### Start
```bash
bd prime            # Load context
bd ready --json     # What's unblocked?
```

### During Work
```bash
bd update <id> --claim --status in_progress   # Claim before working
bd create "New task" -p <priority>             # Discovered work
bd dep add <child> <parent>                    # Link dependencies
```

### End ("Land the Plane")
Use `/land-the-plane` workflow, which:
1. Files remaining work as Beads issues
2. Closes completed tasks
3. Runs `bd sync` + `git push`
4. Posts summary to Linear via `/sync-linear`
5. Generates handoff prompt for next session

## Dispatch Prompt Generation
When acting as the **Chief Agent**, generate dispatch prompts for external agents:

```markdown
## Dispatch for [Agent Name]
**Repo**: mapache-solutions/[repo-name]
**Branch**: feature/bd-XXXX
**Task**: bd-XXXX — [Title]
**Context**: [Brief description + any blocking info]
**Instructions**:
1. Clone/open the repo
2. Run `bd prime` then `bd show bd-XXXX`
3. Claim: `bd update bd-XXXX --claim --status in_progress`
4. Complete the work
5. Run `bd close bd-XXXX` then `bd sync` then `git push`
```

## The "Slurp" Protocol
After generating an `implementation_plan.md`, offer to decompose it:
1. Parse "Proposed Changes" sections
2. `bd create` for each component/change
3. `bd dep add` for blocking relationships
4. Markdown stays as vision; Beads graph becomes executable plan

## Anti-Patterns
- **NEVER** use `bd edit` — use `bd update` with flags
- **NEVER** end without `bd sync` + `git push`
- **NEVER** skip `bd prime` at session start
- **NEVER** work without claiming in multi-agent scenarios
