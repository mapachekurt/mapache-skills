# AGENTS.md - Multi-Agent Architecture & Standards

This file contains the "Passive Context" for the Antigravity agent. It should be treated as high-priority project knowledge that is "always on." Logic and executable actions remain in `skills/`.

## 🏗️ Google ADK Architecture
Antigravity agents must follow these Google Agent Developer Kit (ADK) standards:

- **Inheritance**: ALWAYS inherit from `adk.Agent`, `SequentialAgent`, `ParallelAgent`, or `LoopAgent`.
- **Message Handlers**: Use the `@on_message` decorator and include `ctx` as a parameter.
- **State Management**: Use `ctx.session` for persistence. **NEVER** use instance variables (`self.var`) for state.
- **Type Hints**: Mandatory for all tool functions and parameters.
- **Secrets**: Use Google Secret Manager via the `/manage-secrets` workflow. No hardcoded keys.

## 🤝 A2A & A2UI Protocols
- **A2A (Agent2Agent)**: Use structured message envelopes. Serves `agent.json` at `/.well-known/agent.json`.
- **A2UI (Agent2UI)**: Use Markdown for responses. Leverage "Artifacts" for complex deliverables. Use progress indicators (task view) for multi-step tasks.

## 🎯 GCP Platform Routing
- **Worker → Cloud Run**: Value comes from *doing work* (tools, actions, background tasks).
- **Character → Agent Engine**: Value comes from *being someone* (conversational continuity, persona).
- **Hybrid**: Persona (Agent Engine) + Worker (Cloud Run).
- **Policy**: Never put MCP routing or agent orchestration inside Agent Engine.
- **Full Rubric**: [GCP Agent Placement Rubric](file:///c:/Users/Kurt%20Anderson/github%20projects/mapache-skills/mapache-skills/skills/gcp-platform-router/resources/agent-platform-routing.md).

## 📁 Repository Standards
- **Structure**:
    - `skills/`: Action-oriented scripts and skill-specific instructions.
    - `lab/`: WIP and experimental modules.
    - `scripts/`: Helper utilities for lifecycle management.
    - `tools/`: Generic utilities.
- **Rules**: Refer to `GEMINI.md` for coding and documentation standards.

## 🔄 n8n Deployment Patterns
- **Environments**: 
    - `Dev`: Local Docker (`http://localhost:5678`).
    - `Staging`: Railway (integration testing).
    - `Prod`: Railway (production automation).
- **Patterns**: Use webhook-triggered or scheduled flows with consistent error handling (Log + Notify).

## 📊 Skill Quality (Feedback Standards)
- **Priority-Based**: Critical issues (Security, Performance) first.
- **Conciseness**: Actionable and focused.
- **Tone**: Positive reinforcement + professional collaboration.

## 🔗 Linear Integration (Agent Orchestration)

**Context**: Linear is the single source of truth for project knowledge. Both Jules (autonomous) and Antigravity (interactive) sync work through Linear.

### Before Starting Work
1. Use `LINEAR_GET_LINEAR_ISSUE` to read the issue and comments
2. Check for prior agent work (Jules' commits, artifacts in comments)
3. Update custom field `Agent Status` to `In Progress`

### During Work
- Reference the Linear issue in commit messages: `Fixes LIN-123` or `Closes LIN-456`
- Use `/sync-linear` workflow to post progress updates manually

### After Completion
1. Post walkthrough/implementation plan as a Linear comment
2. Update `Agent Status` custom field to `Completed`
3. Set `Artifacts` URL to link to Google Drive (if artifact >5KB)

### Custom Fields Reference
- **Agent Assigned**: `Unassigned`, `Jules`, `Antigravity`
- **Agent Status**: `Pending`, `In Progress`, `Completed`, `Blocked`, `Needs Review`
- **Artifacts**: URL to implementation plan or walkthrough

## 🧵 Beads Integration (Execution Memory)

**Context**: Beads is the execution memory layer. Linear = Strategy (What/Why), Beads = Tactics (How/When), Antigravity = Orchestration (Who/Where).

### Session Start
1. Set PATH: `$env:PATH = "C:\Users\Kurt Anderson\AppData\Local\Programs\bd;$env:PATH"`
2. Run `bd prime` to load current task context
3. Run `bd ready` to see unblocked tasks

### During Work
- Claim tasks before starting: `bd update <id> --claim --status in_progress`
- Create sub-tasks for discovered work: `bd create "Title" -p <priority>`
- Link dependencies: `bd dep add <child> <parent>`
- Never use `bd edit` — use `bd update` with flags

### Session End ("Land the Plane")
1. Close finished tasks: `bd close <ids> --reason "Completed"`
2. File issues for remaining work: `bd create`
3. Sync database: `bd sync`
4. Push to remote: `git push` (NON-NEGOTIABLE)
5. Generate handoff prompt for next session

### Cross-Repo Coordination
- The `mapache-beads-hub` repo hydrates tasks from all mapache-solutions repos
- Use `/beads-status` workflow for unified view
- Use `/land-the-plane` workflow for session cleanup

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
