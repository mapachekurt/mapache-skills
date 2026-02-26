---
description: End-of-session protocol — sync Beads, push to Git, post to Linear, generate handoff
---

# Land the Plane

**MANDATORY** end-of-session protocol. The session has NOT ended until `git push` succeeds. Never say "ready to push when you are!" — YOU must push.

## Steps

1. **Set up PATH**
// turbo
   ```pwsh
   $env:PATH = "C:\Users\Kurt Anderson\AppData\Local\Programs\bd;$env:PATH"
   ```

2. **File remaining work as Beads issues**
   - Review any TODO items, known bugs, or incomplete work
   - For each: `bd create "Title" -p <priority> --json`
   - Link dependencies if applicable: `bd dep add <child> <parent>`

3. **Close completed tasks**
   - Identify all tasks completed during this session
   - `bd close <id1> <id2> --reason "Completed" --json`

4. **Sync the Beads database**
// turbo
   ```bash
   bd sync
   ```

5. **Push everything to remote — NON-NEGOTIABLE**
   ```bash
   git pull --rebase
   git push
   git status
   ```
   - If `git push` fails, resolve and retry until it succeeds
   - `git status` MUST show "up to date with origin"

6. **Clean up git state**
// turbo
   ```bash
   git stash clear
   git remote prune origin
   ```

7. **Post summary to Linear** (optional)
   - Ask: "Want me to sync this to Linear?"
   - If yes, run the `/sync-linear` workflow with the session summary

8. **Generate handoff prompt**
   - Query next ready task: `bd ready --json`
   - Provide a structured handoff:
     ```
     Continue work on bd-XXXX: [issue title].
     [Brief context about what's done and what's next.]
     ```

## Critical Rules
- The plane has NOT landed until `git push` completes successfully
- NEVER stop before `git push`
- NEVER say "ready to push when you are!" — the agent must push
- Unpushed Beads state breaks multi-agent coordination

## Notes
- This workflow is the counterpart to `/beads-status`
- It adapts Steve Yegge's "Landing the Plane" protocol from the official Beads AGENT_INSTRUCTIONS.md
