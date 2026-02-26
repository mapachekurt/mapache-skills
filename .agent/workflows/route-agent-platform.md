---
description: Interactive workflow for routing an agent to the correct GCP platform
---

# Route Agent Platform Workflow

This workflow helps you decide whether to deploy your agent to Google Cloud Run, Vertex AI Agent Engine, or a Hybrid model.

## Step 1: Gather Agent Description

To give you an accurate recommendation, please describe your agent. 

**Questions:**
1. What is the agent's primary purpose?
2. Is it a "character" (persona-driven) or a "worker" (tool-driven)?
3. Does it need long-term conversational continuity (remembering chat history across sessions)?
4. Does it perform heavy tool orchestration or MCP routing?
5. Do you need full control over the runtime environment?

## Step 2: Run Routing Analysis

Based on your input, I will run the routing assistant:

// turbo
```bash
python skills/gcp-platform-router/scripts/route_agent.py --description "[YOUR_AGENT_DESCRIPTION]"
```

## Step 3: Review Recommendation

I will present the recommended `deployment_target` along with:
- **Confidence level**
- **Reasons** for the placement
- **Implementation notes**
- **Anti-patterns** to avoid

## Step 4: Next Steps

Once the placement is confirmed, you can proceed with:
- `/create-adk-agent` (using the recommended target)
- `gcp-deploy` (for deployment guidance)

## Resources

- [Routing Rubric](file:///c:/Users/Kurt%20Anderson/github%20projects/mapache-skills/mapache-skills/skills/gcp-platform-router/resources/agent-platform-routing.md)
- [Agent Taxonomy](file:///c:/Users/Kurt%20Anderson/github%20projects/mapache-skills/mapache-skills/skills/gcp-platform-router/resources/agent-types-by-platform.md)
