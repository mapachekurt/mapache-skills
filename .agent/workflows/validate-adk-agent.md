---
description: Validate an existing ADK agent for compliance with ADK and A2A standards
---

# Validate ADK Agent Workflow

This workflow validates an existing ADK agent for compliance with Google ADK standards and A2A protocol requirements.

## Step 1: Specify Agent Directory

What is the path to your agent directory?

Example: `./my-agent` or `/full/path/to/agent`

// turbo
## Step 2: Run Validation

```bash
python skills/adk-master-architect/scripts/validate_agent.py --dir "[AGENT_DIR]"
```

## Step 3: Review Results

The validator will check:

### ✅ Required Files
- `agent.py` - Main agent implementation
- `agent.json` - A2A identity card
- `requirements.txt` - Python dependencies

### ✅ ADK Compliance
- Proper inheritance from `adk.Agent`
- Use of `@on_message` decorator
- Context (`ctx`) parameter usage
- No stateful instance variables
- No hardcoded secrets

### ✅ A2A Protocol Compliance
- Valid JSON schema in `agent.json`
- Required fields: id, version, name, description, capabilities, endpoints
- Proper endpoint configuration
- Semantic versioning

### ✅ Code Quality
- Type hints on tool functions
- Proper tool decorator usage
- Test file presence
- Documentation

## Step 4: Fix Issues

Based on validation errors and warnings, I'll help you fix:

### Common Errors

**Error: "Agent class must inherit from adk.Agent"**
```python
# ❌ Wrong
from langchain import SomeAgent
class MyAgent(SomeAgent):
    pass

# ✅ Correct
from adk import Agent
class MyAgent(Agent):
    pass
```

**Error: "Missing required A2A field: endpoints"**
```json
{
  "id": "my-agent",
  "endpoints": {
    "main": "https://[URL]/a2a/v1/message",
    "discovery": "https://[URL]/.well-known/agent.json"
  }
}
```

**Error: "SECURITY: Potential hardcoded API key"**
```python
# ❌ Wrong
api_key = "sk-abc123..."

# ✅ Correct
from google.cloud import secretmanager
api_key = get_secret("api-key-name")
```

## Step 5: Re-validate

After making fixes, run validation again to ensure compliance:

// turbo
```bash
python skills/adk-master-architect/scripts/validate_agent.py --dir "[AGENT_DIR]"
```

## Step 6: Next Steps

Once validation passes:
1. Run local tests: `cd [AGENT_DIR] && pytest tests/`
2. Test locally: `adk run agent.py`
3. Consider deployment: `/deploy-vertex-agent`

## Resources

- Validation Script: `skills/adk-master-architect/scripts/validate_agent.py`
- Knowledge Base: `skills/adk-foundations/resources/comprehensive_knowledge_base.md`
- ADK Standards: `skills/adk-foundations/SKILL.md`
