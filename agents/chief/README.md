# Chief Agent

Central orchestrator for all subagents using A2A

## Overview

This agent is built using Google's Agent Development Kit (ADK) and follows the Agent2Agent (A2A) protocol for interoperability.

**Capabilities:**
- Conversational AI

## Quick Start

### Prerequisites

- Python 3.11+
- Google Cloud Project (for deployment)
- ADK installed: `pip install google-adk`

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run locally with web UI:**
   ```bash
   adk run agent.py
   ```
   
   Then open http://localhost:8000 in your browser.

4. **Run in CLI mode:**
   ```bash
   adk run agent.py --cli
   ```

### Testing

Run the test suite:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=. --cov-report=html
```

## Project Structure

```
chief/
├── agent.py              # Main agent class
├── agent.json           # A2A Identity Card
├── config.py            # Configuration
├── requirements.txt     # Dependencies
├── adk.yaml            # Deployment config
├── tools/              # Custom tool definitions
│   ├── __init__.py
│   └── custom_tools.py
├── tests/              # Test suite
│   ├── __init__.py
│   └── test_agent.py
├── .env.example        # Example environment variables
└── README.md           # This file
```

## Deployment

### Deploy to Vertex AI Agent Engine

1. **Configure deployment:**
   Edit `adk.yaml` with your project details.

2. **Deploy:**
   ```bash
   adk deploy agent_engine \
     --config=adk.yaml \
     --region=us-central1
   ```

3. **Test deployed agent:**
   ```bash
   python test_remote_agent.py
   ```

### Deploy to Cloud Run

```bash
adk deploy cloudrun \
  --project=YOUR_PROJECT_ID \
  --region=us-central1
```

## A2A Protocol

This agent exposes A2A-compliant endpoints:

- **Discovery**: `/.well-known/agent.json`
- **Messaging**: `/a2a/v1/message`

The agent card (`agent.json`) describes capabilities and supported interfaces.

## Configuration

### Environment Variables

Create a `.env` file:

```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_REGION=us-central1
LOG_LEVEL=INFO

# Add your API keys (or use Secret Manager)
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
```

### Secret Manager (Recommended)

For production, store secrets in Google Secret Manager:

```bash
echo -n "your-api-key" | gcloud secrets create OPENAI_API_KEY --data-file=-
```

## Tools

No custom tools yet. Add tools in `tools/custom_tools.py`.

## Architecture

This agent uses:
- **ADK Framework**: Code-first agent development
- **Gemini 2.0**: Default LLM (configurable)
- **A2A Protocol**: Interagent communication
- **Vertex AI Agent Engine**: Managed deployment

## Development

### Adding New Tools

1. Create tool in `tools/custom_tools.py`:
   ```python
   from adk import tool
   
   @tool(name="my_tool")
   def my_tool(param: str) -> dict:
       """Tool description"""
       return {"result": "value"}
   ```

2. Import in `agent.py`:
   ```python
   from tools.custom_tools import my_tool
   ```

3. Add to agent's tools list

4. Write tests in `tests/test_tools.py`

### Modifying Agent Behavior

Edit `agent.py` > `handle_message()` method.

## Monitoring

View logs (after deployment):

```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=chief"
```

## Troubleshooting

### Agent not responding
- Check logs for errors
- Verify API keys are set correctly
- Ensure model quotas are available

### Deployment fails
- Verify GCP permissions
- Check `adk.yaml` configuration
- Ensure service account has required roles

## License

[Specify your license]

## Support

For issues or questions:
- ADK Documentation: https://google.github.io/adk-docs/
- ADK GitHub: https://github.com/google/adk-python
- A2A Protocol: https://a2a.how

---

**Created:** 2026-01-29  
**Framework:** Google ADK 2.1.0+  
**Protocol:** A2A v1.0
