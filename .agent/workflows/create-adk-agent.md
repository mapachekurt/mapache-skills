---
description: Interactive workflow to create a new Google ADK agent with A2A support
---

# Create ADK Agent Workflow

This workflow guides you through creating a production-ready Google ADK agent with full A2A protocol support.

## Step 1: Gather Requirements

First, I'll ask you a few questions to understand what kind of agent you want to build:

**Questions:**
1. What should the agent be named? (e.g., "weather-bot", "research-assistant")
2. What is the agent's primary purpose? (1-2 sentences)
3. What tools/capabilities should it have? (e.g., web search, data analysis, file processing)
4. Will this agent need to communicate with other agents? (A2A integration)
5. Where will it be deployed? (local, Vertex AI Agent Engine, Cloud Run)

## Step 1.5: Platform Routing

Based on your answers, I'll help you decide the best GCP deployment target (Cloud Run vs Vertex AI Agent Engine).

// turbo
```bash
python skills/gcp-platform-router/scripts/route_agent.py --description "[AGENT_PURPOSE] with tools [TOOLS]"
```

I'll present the recommendation and we'll confirm the `deployment_target` before proceeding.

## Step 1.6: Secrets Management

If your agent requires API keys, ensure they are stored in Google Secret Manager.

// turbo
```bash
python skills/gcp-secrets/scripts/manage_secrets.py list
```

If a required key (e.g., `GOOGLE_API_KEY`) is missing, run `/manage-secrets` to add it.

## Step 2: Review Architecture

// turbo
## Step 3: Generate Project Structure

```bash
python skills/adk-master-architect/scripts/scaffold_agent.py \
  --name "[AGENT_NAME]" \
  --purpose "[AGENT_PURPOSE]" \
  --tools "[TOOL1,TOOL2,...]" \
  --dir "."
```

## Step 4: Review Generated Files

I'll show you the key files that were generated:
- `agent.py` - Main agent implementation
- `agent.json` - A2A identity card
- `config.py` - Configuration
- `tools/custom_tools.py` - Tool definitions
- `adk.yaml` - Deployment configuration

## Step 5: Customize Implementation

I'll help you:
1. Implement custom tools in `tools/custom_tools.py`
2. Configure the agent behavior in `agent.py`
3. Set up environment variables
4. Configure deployment settings

## Step 6: Validate

// turbo
```bash
python skills/adk-master-architect/scripts/validate_agent.py --dir "[AGENT_NAME]"
```

## Step 7: Test Locally

// turbo
```bash
cd [AGENT_NAME]
pip install -r requirements.txt
adk run agent.py
```

This will start the agent with a web UI at http://localhost:8000

## Step 8: Deploy (Optional)

If you're ready to deploy:

```bash
cd [AGENT_NAME]
adk deploy agent_engine --config=adk.yaml --region=us-central1
```

## Next Steps

After creation:
- Implement tool logic in `tools/custom_tools.py`
- Add tests in `tests/test_agent.py`
- Update README.md with specific details
- Configure secrets in Google Secret Manager
- Set up monitoring and logging

## Resources

- ADK Documentation: https://google.github.io/adk-docs/
- A2A Protocol Spec: https://a2a.how
- Knowledge Base: `skills/adk-foundations/resources/comprehensive_knowledge_base.md`
