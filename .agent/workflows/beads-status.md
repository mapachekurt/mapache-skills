---
description: Generate a cross-repo "State of the Union" using Beads and Linear
---

# Beads Status Report

Generate a unified status report across all mapache-solutions repos by querying the Beads graph and cross-referencing with Linear.

## Steps

1. **Set up PATH**
// turbo
   ```pwsh
   $env:PATH = "C:\Users\Kurt Anderson\AppData\Local\Programs\bd;$env:PATH"
   ```

2. **Sync the current repo's Beads state**
// turbo
   ```bash
   bd sync
   ```

3. **Query the full task graph**
// turbo
   ```bash
   bd list --all --json
   ```

4. **Get ready (unblocked) tasks**
// turbo
   ```bash
   bd ready --json
   ```

5. **Get blocked tasks**
// turbo
   ```bash
   bd list --status blocked --json
   ```

6. **Cross-reference with Linear** (optional)
   - Ask the user: "Which Linear project should I cross-reference? (or skip)"
   - If provided, use Rube MCP: `LINEAR_SEARCH_LINEAR_ISSUES` to find matching issues
   - Compare Beads task statuses with Linear issue statuses

7. **Generate status artifact**
   - Create a markdown "State of the Union" summary containing:
     - **Ready**: Tasks that are unblocked and available for agents
     - **In Progress**: Tasks currently claimed by an agent
     - **Blocked**: Tasks waiting on dependencies
     - **Completed**: Tasks closed since last report
     - **Risk Items**: Any tasks that have been in_progress too long or have no assignee
   - Save as an Antigravity artifact in the brain directory

8. **Present to user**
   - Display the summary and ask if they want to:
     - Dispatch tasks to agents (generate dispatch prompts)
     - Post the report to Linear
     - Adjust priorities or dependencies

## Notes
- For full cross-repo visibility, run this from the `mapache-beads-hub` repo
- This workflow pairs with `/land-the-plane` as the bookend protocol
