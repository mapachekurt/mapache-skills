---
name: n8n-flow-builder
description: Expert guidance for node configuration, error handling, and deployment of n8n workflows.
version: 1.1.0
---

# n8n Flow Builder

**Purpose:** Action-oriented guidance for creating, configuring, and deploying n8n workflows.

> [!NOTE]
> **Passive Context**: Environment context (dev/staging/prod) and high-level flow design patterns have been moved to the project-level `AGENTS.md` file.

## Node Configuration Guide

### 1. HTTP Request Node
- **Auth**: Use n8n credential system.
- **Resilience**: Enable "Continue on Fail" for non-critical calls. Configure retries.
- **Dynamic Headers**: Use expressions for dynamic authorization.

### 2. Code/Function Node
- **Logic**: Keep focused and handle null/undefined values.
- **Format**: Return consistent JSON structures.

### 3. Logic Nodes (IF/Merge/Set)
- **Branching**: Handle both true/false paths in IF nodes.
- **Merging**: Use "Merge" for combining data streams by key.
- **State**: Use "Set" to store intermediate results for debugging.

## Error Handling Standards
- **Try-Catch**: Use "Continue on Fail" + IF node to catch errors.
- **Global Error Flows**: Configure at the workflow level to notify Slack/email.

## Deployment Workflow
1. **Export**: Save workflow JSON from local n8n.
2. **Staging**: Import to Railway Staging and run acceptance tests.
3. **Prod**: Deploy to Railway Prod and monitor initial runs.

## Tool Operations
- Use `n8n` MCP for programmatic listing, export, and deployment of workflows.
