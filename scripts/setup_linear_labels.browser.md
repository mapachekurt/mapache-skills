# Browser Automation: Linear Label Setup

**Purpose**: Automate creation of Linear labels for agent orchestration system using browser automation.

**Tools**: Gemini Browser Use (Chrome) or Browserbase MCP

## Labels to Create

```json
[
  {"name": "agent:unassigned", "color": "#9E9E9E", "description": "No agent assigned"},
  {"name": "agent:jules", "color": "#2196F3", "description": "Assigned to Jules (autonomous)"},
  {"name": "agent:antigravity", "color": "#9C27B0", "description": "Assigned to Antigravity (interactive)"},
  {"name": "status:pending", "color": "#FF9800", "description": "Waiting to start"},
  {"name": "status:in-progress", "color": "#FFC107", "description": "Currently being worked on"},
  {"name": "status:completed", "color": "#4CAF50", "description": "Work finished"},
  {"name": "status:blocked", "color": "#F44336", "description": "Blocked on dependency"},
  {"name": "status:needs-review", "color": "#009688", "description": "Ready for review"},
  {"name": "agent-ready", "color": "#4CAF50", "description": "Ready for router to assign"}
]
```

## Browser Automation Steps

### Using Gemini Browser Use

1. **Navigate to Linear Labels**
   - URL: `https://linear.app/settings/labels`
   - Wait for page load

2. **For Each Label** (loop through JSON above):
   - Click button with text "New label" or "Create label"
   - Wait for modal/form to appear
   - Type label name in input field (usually has placeholder "Label name")
   - Click color picker, enter hex code
   - (Optional) Enter description if field available
   - Click "Create" or "Save"
   - Wait for confirmation/page update

3. **Verification**
   - After all labels created, scroll through label list
   - Verify all 9 labels exist with correct colors

### Using Browserbase MCP (if configured)

Similar steps but executed via MCP tool calls through Rube.

## Fallback: API Approach

If browser automation fails, Linear's GraphQL API *does* support label creation:

```graphql
mutation CreateLabel {
  issueLabelCreate(input: {
    name: "agent:jules"
    color: "#2196F3"
    description: "Assigned to Jules (autonomous)"
  }) {
    success
    issueLabel {
      id
      name
    }
  }
}
```

Use `LINEAR_RUN_QUERY_OR_MUTATION` via Rube MCP for each label.
