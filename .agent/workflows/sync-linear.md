---
description: Sync current task progress to Linear issue
---

# Sync to Linear

Use this workflow to post your current progress (task.md, implementation_plan.md, or walkthrough.md) back to the associated Linear issue.

## Steps

1. **Identify the Linear issue ID**
   - Ask the user: "Which Linear issue is this work for? (e.g., LIN-123)"
   - Validate format matches pattern: `[A-Z]+-\d+`

2. **Verify issue exists**
   - Use Rube MCP: `RUBE_MULTI_EXECUTE_TOOL` with `LINEAR_GET_LINEAR_ISSUE`
   - If not found, ask user to confirm the ID

3. **Read current artifacts**
   - Check for files in the conversation's brain directory:
     - `task.md` (progress tracker)
     - `implementation_plan.md` (design doc)
     - `walkthrough.md` (proof of work)
   - Ask user which artifact(s) to sync

4. **Format comment**
   - Create markdown comment with:
     - Header: "## Antigravity Progress Update"
     - Timestamp
     - Artifact content (formatted as code blocks)
     - Link to conversation (if applicable)

5. **Post to Linear**
// turbo
   - Use `LINEAR_CREATE_LINEAR_COMMENT` with formatted body
   - Confirm success with user

6. **Update Agent Status** (optional)
   - Ask user if they want to update custom field "Agent Status"
   - Options: "Pending", "In Progress", "Completed", "Blocked", "Needs Review"
   - Use `LINEAR_RUN_QUERY_OR_MUTATION` to update custom field

## Notes
- This is a manual workflow—run it when you want to checkpoint progress to Linear
- For automated sync-back, use the `linear-artifact-sync` Composio Recipe
