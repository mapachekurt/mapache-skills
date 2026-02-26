# Complete ADK & A2A Knowledge Base for Antigravity
**Version:** 2.0  
**Last Updated:** 2026-01-28  
**Purpose:** Comprehensive reference for building Google ADK agents with A2A protocol support

---

## 📚 Table of Contents
1. [Official Sources](#official-sources)
2. [Google ADK Core Framework](#google-adk-core-framework)
3. [Agent2Agent (A2A) Protocol](#agent2agent-a2a-protocol)
4. [Vertex AI Agent Engine Deployment](#vertex-ai-agent-engine-deployment)
5. [Code Patterns & Examples](#code-patterns--examples)
6. [Best Practices & Patterns](#best-practices--patterns)
7. [Multi-Agent Systems](#multi-agent-systems)
8. [Tools & Integrations](#tools--integrations)
9. [Testing & Evaluation](#testing--evaluation)
10. [Video Tutorials](#video-tutorials)

---

## Official Sources

### Primary Documentation
- **ADK Official Docs**: https://google.github.io/adk-docs/
- **ADK Python GitHub**: https://github.com/google/adk-python
- **ADK Samples GitHub**: https://github.com/google/adk-samples
- **ADK Community Tools**: https://github.com/google/adk-python-community
- **A2A Protocol Spec**: https://a2a.how
- **A2A GitHub Spec**: https://github.com/Linux Foundation/A2A (under Linux Foundation)
- **A2A Protocol Info**: https://agent2agent.info
- **Vertex AI Agent Engine**: https://cloud.google.com/vertex-ai/docs/agent-engine

### Language-Specific SDKs
- **Python**: https://github.com/google/adk-python
- **TypeScript/JavaScript**: https://github.com/google/adk-js (also adk-web)
- **Go**: https://github.com/google/adk-go
- **Java**: https://github.com/google/adk-java

### Learning Resources
- **YouTube Introduction**: "Introducing Agent Development Kit" - https://www.youtube.com/watch?v=zgrOwow_uTQ
- **Getting Started (Python)**: https://google.github.io/adk-docs/get-started/python/
- **Multi-Agent Systems**: https://google.github.io/adk-docs/agents/multi-agents/
- **Tools Documentation**: https://google.github.io/adk-docs/tools/
- **Deployment Guide**: https://google.github.io/adk-docs/deploy/
- **Safety & Security**: https://google.github.io/adk-docs/safety/

### Community & Tutorials
- **Medium - Mastering Google ADK Series** (April 2025+)
- **DEV.to - ADK Deployment Guides**
- **Google Codelabs - ADK Crash Course** (December 2025)
- **YouTube Crash Courses** - "Learn Google's New AI Framework" (January 2026)

---

## Google ADK Core Framework

### What is ADK?
Agent Development Kit (ADK) is an **open-source, code-first Python framework** for building, evaluating, and deploying sophisticated AI agents with flexibility and control. It makes agent development feel like traditional software development.

**Key Principles:**
- **Model-Agnostic**: Works with Gemini, GPT, Claude, and any LLM
- **Deployment-Agnostic**: Deploy anywhere (local, Cloud Run, Vertex AI Agent Engine)
- **Interoperable**: Compatible with other frameworks and supports A2A protocol
- **Code-First**: Define agents as Python classes with type hints

### Installation

```bash
# Stable Release (Recommended)
pip install google-adk

# Development Version (latest features)
pip install git+https://github.com/google/adk-python.git@main
```

**Release Cadence**: Bi-weekly stable releases

### Core Architecture

#### 1. Agent Types

##### LLM Agents (`Agent`, `LlmAgent`)
```python
from adk import Agent
from adk.models import Gemini

class MyAgent(Agent):
    def __init__(self):
        super().__init__(
            name="my-agent",
            model=Gemini("gemini-2.0-flash-exp"),
            description="Agent that uses LLM for reasoning"
        )
```

**Use When:**
- Dynamic decision-making required
- Natural language understanding needed
- Flexible tool selection
- Adaptive behavior based on context

##### Workflow Agents (Deterministic)
```python
from adk import SequentialAgent, ParallelAgent, LoopAgent

# Sequential: Steps happen in order
research_pipeline = SequentialAgent(
    name="research",
    agents=[search_agent, analyze_agent, write_agent]
)

# Parallel: Steps happen simultaneously
fan_out = ParallelAgent(
    name="parallel",
    agents=[agent_a, agent_b, agent_c]
)

# Loop: Repeat until condition
retry_agent = LoopAgent(
    name="retry",
    agent=worker_agent,
    max_iterations=5
)
```

**Use When:**
- Predictable workflow required
- No need for LLM-based routing
- Cost optimization (no LLM calls for orchestration)

##### Custom Agents
```python
from adk import BaseAgent

class CustomAgent(BaseAgent):
    def execute(self, input_data, ctx):
        # Your custom logic
        return {"result": "custom output"}
```

#### 2. The Context Object (`ctx`)

**Critical Concept**: Every agent function receives a `ctx` parameter.

```python
from adk import Agent, on_message

class StatefulAgent(Agent):
    @on_message
    def handle(self, message: str, ctx):
        # Access session state
        user_prefs = ctx.session.get("preferences", {})
        
        # Get unique run ID
        run_id = ctx.run_id
        
        # Session ID (persists across turns)
        session_id = ctx.session_id
        
        # Update state
        ctx.session["last_query"] = message
        
        return f"Processed in session {session_id}"
```

**Context Properties:**
- `ctx.session`: Mutable dict that persists across turns
- `ctx.run_id`: Unique ID for this specific invocation
- `ctx.session_id`: Persistent ID across conversation
- `ctx.user_id`: Optional user identifier

#### 3. Event-Driven Architecture

ADK uses **event streams** instead of simple request/response.

```python
from adk import Agent, on_message

class StreamingAgent(Agent):
    @on_message
    async def handle(self, message: str, ctx):
        # Yield intermediate results
        yield {"type": "thinking", "content": "Processing..."}
        
        result = await self.process(message)
        
        yield {"type": "result", "content": result}
```

#### 4. Tools (Functions Agents Can Call)

```python
from adk import tool

@tool(name="search_web", description="Search the internet")
def search_web(query: str) -> str:
    """
    Args:
        query: The search query
    Returns:
        Search results as text
    """
    # Implementation
    return search_results

# Add tool to agent
class SearchAgent(Agent):
    def __init__(self):
        super().__init__(
            name="searcher",
            model=Gemini("gemini-2.0-flash-exp"),
            tools=[search_web]
        )
```

**Tool Sources:**
- **Custom Functions**: Python functions with `@tool` decorator
- **Pre-built Tools**: Google Search, Code Execution, etc.
- **OpenAPI Specs**: Auto-generate tools from API specs
- **MCP Tools**: Model Context Protocol integrations
- **Agents as Tools**: Use other agents as callable tools

### Project Structure (Standard)

```
my-agent/
├── agent.py              # Main agent definition
├── agent.json           # A2A Identity Card
├── config.py            # Configuration (model, params)
├── tools/               # Tool definitions
│   ├── __init__.py
│   └── custom_tool.py
├── requirements.txt     # Dependencies (must include google-adk)
├── tests/              # Unit tests
│   └── test_agent.py
├── Dockerfile          # Optional (ADK can generate)
└── adk.yaml           # Deployment configuration
```

### Recent Features (2025-2026)

1. **Custom Service Registration**: Generic way to register custom services in FastAPI server
2. **Rewind**: Ability to rewind a session to before a previous invocation
3. **AgentEngineSandboxCodeExecutor**: Execute agent-generated code in sandboxed environment
4. **Tool Confirmation (HITL)**: Human-in-the-loop for tool execution
5. **Agent Config**: Build agents without code using configuration

---

## Agent2Agent (A2A) Protocol

### What is A2A?

The **Agent2Agent (A2A) Protocol** is an **open standard** (Linux Foundation) for enabling communication and interoperability between independent AI agent systems regardless of framework, language, or vendor.

**Key Principles:**
- **Interoperability**: Cross-framework, cross-vendor agent communication
- **Security & Trust**: OAuth2, API key, or custom auth
- **Extensibility**: Build on HTTP, JSON-RPC 2.0, Server-Sent Events

**Industry Support**: Google, AWS, Microsoft, Salesforce, SAP, ServiceNow, Cisco

### Core A2A Objects

#### 1. AgentCard (`agent.json`)

**REQUIRED**: Every A2A agent must publish metadata at `/.well-known/agent.json`

```json
{
  "id": "my-service-agent",
  "version": "1.0.0",
  "name": "Inventory Manager",
  "description": "Checks stock levels and reserves items",
  "capabilities": [
    "inventory_check",
    "reservation",
    "streaming"
  ],
  "endpoints": {
    "main": "https://my-agent.example.com/a2a/v1/message",
    "discovery": "https://my-agent.example.com/.well-known/agent.json"
  },
  "auth": {
    "type": "oauth2",
    "scope": "https://www.googleapis.com/auth/cloud-platform"
  },
  "supportedInterfaces": ["json-rpc", "http+json"],
  "skills": [
    {
      "name": "inventory_management",
      "description": "Manage product inventory"
    }
  ]
}
```

**Required Fields:**
- `id`: Unique identifier
- `version`: Semantic version
- `name`: Human-readable name
- `endpoints.discovery`: URL to this file
- `endpoints.main`: Primary communication endpoint

#### 2. Task

The **unit of action** in A2A.

```json
{
  "id": "task-uuid-1234",
  "status": "Working",
  "artifacts": [],
  "history": [
    {
      "role": "USER",
      "parts": [
        {"text": "Check stock for SKU-99"}
      ]
    }
  ]
}
```

**Task Lifecycle:**
- `Submitted`: Task received
- `Working`: Agent processing
- `Completed`: Task finished
- `Failed`: Error occurred
- `Cancelled`: User/system cancelled

#### 3. Message

A single unit of communication.

```json
{
  "role": "AGENT",
  "parts": [
    {"text": "Stock for SKU-99: 42 units available"},
    {
      "data": {
        "sku": "SKU-99",
        "quantity": 42,
        "warehouse": "US-WEST-1"
      }
    }
  ]
}
```

**Roles:** `USER` or `AGENT`

#### 4. Part (Content Types)

```json
// Text
{"text": "Hello world"}

// File reference
{
  "file": {
    "uri": "gs://bucket/file.pdf",
    "mimeType": "application/pdf"
  }
}

// Structured data
{
  "data": {
    "key": "value",
    "nested": {"field": 123}
  }
}
```

#### 5. Artifact

The **formal output** of a task.

```json
{
  "artifactId": "artifact-uuid-5678",
  "parts": [
    {"text": "Report generated"},
    {
      "file": {
        "uri": "gs://bucket/report.pdf"
      }
    }
  ]
}
```

### A2A Interaction Flow

```
┌─────────────┐                    ┌─────────────┐
│ Client      │                    │ Server      │
│ Agent       │                    │ Agent       │
└──────┬──────┘                    └──────┬──────┘
       │                                  │
       │ 1. Discovery (GET agent.json)    │
       │─────────────────────────────────>│
       │<─────────────────────────────────│
       │   {"capabilities": [...]}         │
       │                                  │
       │ 2. Validate Capabilities         │
       │                                  │
       │ 3. Submit Task                   │
       │ POST /a2a/v1/message             │
       │─────────────────────────────────>│
       │   {"task_id": "...",             │
       │    "payload": {...}}             │
       │                                  │
       │ 4. Processing...                 │
       │                                  │
       │ 5. Return Artifacts              │
       │<─────────────────────────────────│
       │   {"artifacts": [...]}           │
       │                                  │
```

### Implementing A2A in ADK

```python
from adk import Agent
from adk.a2a import A2AServer

class InventoryAgent(Agent):
    def __init__(self):
        super().__init__(
            name="inventory-agent",
            model=Gemini("gemini-2.0-flash-exp"),
            description="Manages inventory"
        )
    
    # Agent logic here

# Create A2A server
server = A2AServer(
    agent=InventoryAgent(),
    agent_card={
        "id": "inventory-v1",
        "capabilities": ["inventory_check", "reservation"],
        # ... full agent card
    }
)

# Serves agent.json at /.well-known/agent.json
# Serves messaging endpoint at /a2a/v1/message
```

---

## Vertex AI Agent Engine Deployment

### What is Agent Engine?

**Vertex AI Agent Engine** is a fully managed, serverless runtime for deploying ADK agents at scale.

**Benefits:**
- **Managed Infrastructure**: No container/VM management
- **Auto-scaling**: Handles traffic spikes automatically
- **Integrated Monitoring**: Cloud Logging, Cloud Trace
- **Persistent State**: Built-in session management
- **Security**: IAM integration, Secret Manager
- **A2A Ready**: Automatic endpoint provisioning

### Deployment Methods

#### Method 1: CLI Deployment (Recommended)

```bash
# Install ADK with deployment tools
pip install google-adk[deploy]

# Deploy
adk deploy agent_engine \
  --project="my-gcp-project-id" \
  --region="us-central1" \
  --display-name="My Production Agent" \
  --agent-dir="./my-agent" \
  --service-account="agent-sa@my-project.iam.gserviceaccount.com"
```

#### Method 2: Using `adk.yaml` (Best Practice)

Create `adk.yaml`:
```yaml
name: my-agent
runtime: python311
entrypoint: agent:app

scaling:
  min_instances: 1
  max_instances: 10

env:
  GOOGLE_CLOUD_PROJECT: "my-project-id"
  A2A_ENABLE: "true"

secrets:
  - name: OPENAI_API_KEY
    version: latest
```

Deploy:
```bash
adk deploy agent_engine --config=adk.yaml --region=us-central1
```

#### Method 3: Python SDK

```python
from google.cloud import aiplatform
from adk.deployment import deploy_to_agent_engine

# Initialize Vertex AI
aiplatform.init(
    project="my-project-id",
    location="us-central1"
)

# Deploy
engine = deploy_to_agent_engine(
    agent_path="./my-agent",
    display_name="Production Agent",
    description="Deployed via SDK"
)

print(f"Agent URL: {engine.resource_name}")
```

### Deployment Checklist

**Before Deployment:**
1. ✅ `requirements.txt` includes `google-adk>=2.1.0`
2. ✅ `agent.json` present (for A2A)
3. ✅ Service account has required IAM roles:
   - `roles/aiplatform.user`
   - `roles/run.invoker`
   - `roles/secretmanager.secretAccessor` (if using secrets)
4. ✅ Secrets stored in Secret Manager (never hardcode)
5. ✅ Environment variables configured
6. ✅ A2A endpoints configured (if needed)

**Post-Deployment:**
1. Test with `test_remote_agent.py`
2. Monitor Cloud Logging
3. Set up alerting
4. Configure auto-scaling parameters

### Background Deployment Process

When you run `adk deploy`, the system:
1. Generates `.pkl` files (serialized agents)
2. Creates `requirements.txt` (if missing)
3. Builds `dependencies.tar` (Python packages)
4. Containerizes the agent
5. Pushes to Artifact Registry
6. Deploys to Agent Engine
7. Provisions A2A endpoints (if enabled)

### Accessing Deployed Agents

**Via REST API:**
```bash
curl -X POST \
  https://REGION-aiplatform.googleapis.com/v1/projects/PROJECT/locations/REGION/agentEngines/AGENT_ID:execute \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "What is the weather?",
    "session_id": "user-123-session"
  }'
```

**Via Python SDK:**
```python
from google.cloud import aiplatform

client = aiplatform.gapic.AgentServiceClient()

response = client.execute_agent(
    name="projects/PROJECT/locations/REGION/agentEngines/AGENT_ID",
    input="What is the weather?",
    session_id="user-123-session"
)
```

---

## Code Patterns & Examples

### Pattern 1: Basic LLM Agent

```python
from adk import Agent, on_message
from adk.models import Gemini
import logging

class BasicAgent(Agent):
    """Simple conversational agent"""
    
    def __init__(self):
        super().__init__(
            name="basic-agent",
            model=Gemini("gemini-2.0-flash-exp"),
            description="A basic conversational agent"
        )
    
    @on_message
    def handle_message(self, message: str, ctx):
        logging.info(f"Received: {message} in session {ctx.session_id}")
        
        # Generate response
        response = self.llm.generate(message)
        
        return response.text

# Run locally
if __name__ == "__main__":
    agent = BasicAgent()
    agent.run()  # Starts web UI at http://localhost:8000
```

### Pattern 2: Agent with Custom Tools

```python
from adk import Agent, tool
from adk.models import Gemini
import requests

@tool(name="get_weather", description="Get current weather for a city")
def get_weather(city: str, units: str = "metric") -> dict:
    """
    Fetch weather data from API.
    
    Args:
        city: City name (e.g., "London")
        units: Temperature units ("metric" or "imperial")
    
    Returns:
        Weather data dictionary
    """
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"https://api.weather.com/v1/current?city={city}&units={units}"
    response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
    return response.json()

@tool(name="convert_currency")
def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert currency"""
    # Implementation
    return converted_amount

class WeatherAgent(Agent):
    def __init__(self):
        super().__init__(
            name="weather-agent",
            model=Gemini("gemini-2.0-flash-exp"),
            tools=[get_weather, convert_currency],
            description="Agent that provides weather and currency info"
        )
```

### Pattern 3: Multi-Agent System

```python
from adk import Agent, SequentialAgent, ParallelAgent
from adk.models import Gemini

# Specialized agents
class ResearchAgent(Agent):
    def __init__(self):
        super().__init__(
            name="researcher",
            model=Gemini("gemini-2.0-flash-exp"),
            tools=[web_search, read_document],
            description="Conducts research"
        )

class AnalysisAgent(Agent):
    def __init__(self):
        super().__init__(
            name="analyst",
            model=Gemini("gemini-2.0-flash-exp"),
            tools=[analyze_data, generate_insights],
            description="Analyzes research findings"
        )

class WriterAgent(Agent):
    def __init__(self):
        super().__init__(
            name="writer",
            model=Gemini("gemini-2.0-flash-exp"),
            description="Writes reports"
        )

# Orchestrate with Sequential workflow
research_pipeline = SequentialAgent(
    name="research-pipeline",
    agents=[
        ResearchAgent(),
        AnalysisAgent(),
        WriterAgent()
    ],
    description="Complete research workflow"
)

# Or parallel for fan-out
parallel_research = ParallelAgent(
    name="parallel-research",
    agents=[
        ResearchAgent(name="researcher-1"),
        ResearchAgent(name="researcher-2"),
        ResearchAgent(name="researcher-3")
    ],
    description="Parallel research execution"
)
```

### Pattern 4: Stateful Agent with Memory

```python
from adk import Agent, on_message
from adk.models import Gemini

class StatefulAgent(Agent):
    def __init__(self):
        super().__init__(
            name="stateful-agent",
            model=Gemini("gemini-2.0-flash-exp"),
            description="Maintains conversation context"
        )
    
    @on_message
    def handle_message(self, message: str, ctx):
        # Retrieve conversation history
        history = ctx.session.get("history", [])
        user_preferences = ctx.session.get("preferences", {})
        
        # Add current message to history
        history.append({"role": "user", "content": message})
        
        # Generate contextual response
        response = self.llm.generate(
            message,
            context={"history": history, "preferences": user_preferences}
        )
        
        # Update history
        history.append({"role": "assistant", "content": response.text})
        ctx.session["history"] = history
        
        # Learn preferences
        if "prefer" in message.lower():
            # Extract and store preference
            ctx.session["preferences"] = self.extract_preference(message)
        
        return response.text
```

### Pattern 5: A2A-Enabled Agent

```python
from adk import Agent, tool
from adk.a2a import A2AServer, AgentCard
from adk.models import Gemini

@tool(name="process_order")
def process_order(order_id: str, action: str) -> dict:
    """Process order actions"""
    # Implementation
    return {"status": "success", "order_id": order_id}

class OrderAgent(Agent):
    def __init__(self):
        super().__init__(
            name="order-agent",
            model=Gemini("gemini-2.0-flash-exp"),
            tools=[process_order],
            description="Handles order processing"
        )

# Create A2A server
agent_card = AgentCard(
    id="order-agent-v1",
    version="1.0.0",
    name="Order Processing Agent",
    description="Processes and manages customer orders",
    capabilities=["order_creation", "order_tracking", "order_modification"],
    endpoints={
        "main": "https://my-agent.example.com/a2a/v1/message",
        "discovery": "https://my-agent.example.com/.well-known/agent.json"
    },
    auth={
        "type": "oauth2",
        "scope": "https://www.googleapis.com/auth/cloud-platform"
    }
)

server = A2AServer(
    agent=OrderAgent(),
    agent_card=agent_card,
    port=8080
)

if __name__ == "__main__":
    server.run()
```

---

## Best Practices & Patterns

### 1. Error Handling

```python
from adk import Agent, on_message
from adk.exceptions import ToolExecutionError, ModelError

class RobustAgent(Agent):
    @on_message
    def handle_message(self, message: str, ctx):
        try:
            response = self.llm.generate(message)
            return response.text
        
        except ToolExecutionError as e:
            logging.error(f"Tool failed: {e}")
            return "I encountered an error with that tool. Let me try another approach."
        
        except ModelError as e:
            logging.error(f"Model error: {e}")
            return "I'm having trouble processing that right now. Please try again."
        
        except Exception as e:
            logging.exception(f"Unexpected error: {e}")
            return "An unexpected error occurred."
```

### 2. Secret Management

**DO NOT** hardcode secrets:
```python
# ❌ WRONG
api_key = "sk-abc123..."  # Never do this!
```

**DO** use Secret Manager:
```python
# ✅ CORRECT
from google.cloud import secretmanager
import os

def get_secret(secret_name: str) -> str:
    """Retrieve secret from Secret Manager"""
    client = secretmanager.SecretManagerServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    
    return response.payload.data.decode("UTF-8")

# Use in agent
api_key = get_secret("openai-api-key")
```

### 3. Logging & Observability

```python
import logging
from adk import Agent, on_message

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s", "level":"%(levelname)s", "msg":"%(message)s"}'
)

class ObservableAgent(Agent):
    @on_message
    def handle_message(self, message: str, ctx):
        # Log with context
        logging.info(
            "Processing message",
            extra={
                "session_id": ctx.session_id,
                "run_id": ctx.run_id,
                "message_length": len(message)
            }
        )
        
        # Your logic
        response = self.process(message)
        
        logging.info(
            "Response generated",
            extra={
                "session_id": ctx.session_id,
                "response_length": len(response)
            }
        )
        
        return response
```

### 4. Testing Patterns

```python
import pytest
from adk import Agent
from adk.testing import MockContext, MockLLM

def test_agent_basic_response():
    """Test basic agent functionality"""
    agent = MyAgent()
    ctx = MockContext(session_id="test-123")
    
    response = agent.handle_message("Hello", ctx)
    
    assert response is not None
    assert len(response) > 0

def test_agent_with_tools():
    """Test agent tool invocation"""
    agent = MyAgent()
    ctx = MockContext()
    
    # Mock tool responses
    with patch('my_agent.tools.search_web', return_value="mock results"):
        response = agent.handle_message("Search for Python", ctx)
        assert "mock results" in response

def test_agent_state_persistence():
    """Test session state"""
    agent = MyAgent()
    ctx = MockContext(session_id="test-456")
    
    # First message
    agent.handle_message("Remember I like blue", ctx)
    
    # Check state
    assert ctx.session.get("color_preference") == "blue"
```

### 5. Performance Optimization

```python
from adk import Agent
from functools import lru_cache

class OptimizedAgent(Agent):
    
    @lru_cache(maxsize=100)
    def expensive_computation(self, input_data: str) -> str:
        """Cache expensive operations"""
        # ...
        return result
    
    def handle_message(self, message: str, ctx):
        # Batch API calls when possible
        results = self.batch_process([message, other_messages])
        
        # Stream responses for long outputs
        for chunk in self.generate_streaming(message):
            yield chunk
```

---

## Multi-Agent Systems

### Architecture Patterns

#### Pattern 1: Sequential Pipeline
```python
from adk import SequentialAgent

# Data processing pipeline
pipeline = SequentialAgent(
    name="data-pipeline",
    agents=[
        ExtractAgent(),      # Pulls data from source
        TransformAgent(),    # Cleans and transforms
        AnalyzeAgent(),      # Runs analysis
        ReportAgent()        # Generates report
    ]
)
```

#### Pattern 2: Hierarchical (Manager-Worker)
```python
from adk import Agent, transfer

class ManagerAgent(Agent):
    """Coordinates work across specialists"""
    
    def __init__(self):
        self.workers = {
            "finance": FinanceAgent(),
            "legal": LegalAgent(),
            "hr": HRAgent()
        }
        super().__init__(
            name="manager",
            model=Gemini("gemini-2.0-flash-exp"),
            description="Delegates to specialists"
        )
    
    @on_message
    def handle_message(self, message: str, ctx):
        # Determine which specialist to use
        specialist = self.determine_specialist(message)
        
        # Transfer to specialist
        return transfer(self.workers[specialist], message, ctx)
```

#### Pattern 3: Collaborative (Peer-to-Peer)
```python
# Agents that work together as equals
collaborative_team = ParallelAgent(
    name="research-team",
    agents=[
        ResearchAgent(focus="academic"),
        ResearchAgent(focus="industry"),
        ResearchAgent(focus="news")
    ],
    aggregation_strategy="consensus"  # Combine results
)
```

### Inter-Agent Communication

```python
from adk import Agent, send_message_to_agent

class CollaborativeAgent(Agent):
    @on_message
    def handle_message(self, message: str, ctx):
        # Query another agent
        research_result = send_message_to_agent(
            agent_id="research-agent-v1",
            message="Find information about X",
            ctx=ctx
        )
        
        # Use result in this agent's work
        analysis = self.analyze(research_result)
        
        return analysis
```

---

## Tools & Integrations

### Pre-Built Tools (Google Ecosystem)

```python
from adk.tools import (
    GoogleSearch,
    CodeExecution,
    VertexAISearch,
    BigQueryTool
)

agent = Agent(
    name="data-agent",
    tools=[
        GoogleSearch(),
        CodeExecution(language="python"),
        BigQueryTool(project_id="my-project"),
        VertexAISearch(datastore_id="my-datastore")
    ]
)
```

### OpenAPI Integration

```python
from adk.tools import OpenAPITool

# Auto-generate tools from OpenAPI spec
github_tool = OpenAPITool(
    spec_url="https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json",
    operations=["get /repos/{owner}/{repo}", "post /repos/{owner}/{repo}/issues"]
)

agent = Agent(
    name="github-agent",
    tools=[github_tool]
)
```

### MCP (Model Context Protocol) Integration

```python
from adk.tools import MCPTool

# Use MCP servers as tools
linear_tool = MCPTool(
    server_url="https://mcp.linear.app",
    capabilities=["issues", "projects"]
)

agent = Agent(
    name="project-manager",
    tools=[linear_tool]
)
```

---

## Testing & Evaluation

### Unit Testing

```python
import pytest
from adk import Agent
from adk.testing import MockContext

@pytest.fixture
def agent():
    return MyAgent()

@pytest.fixture
def mock_context():
    return MockContext(session_id="test-session")

def test_basic_functionality(agent, mock_context):
    response = agent.handle_message("Hello", mock_context)
    assert response is not None

def test_tool_invocation(agent, mock_context):
    response = agent.handle_message("Search for Python", mock_context)
    # Verify tool was called
    assert mock_context.tool_calls_made > 0
```

### Evaluation Framework

```python
from adk.evaluation import Evaluator, Metric

# Define test cases
test_cases = [
    {
        "input": "What is 2+2?",
        "expected_output": "4",
        "expected_tools": []
    },
    {
        "input": "Search for Python tutorials",
        "expected_tools": ["google_search"]
    }
]

# Create evaluator
evaluator = Evaluator(
    agent=MyAgent(),
    metrics=[
        Metric.accuracy(),
        Metric.tool_usage(),
        Metric.response_time()
    ]
)

# Run evaluation
results = evaluator.evaluate(test_cases)

print(f"Accuracy: {results.accuracy}")
print(f"Avg Response Time: {results.avg_response_time}ms")
```

---

## Video Tutorials

### Official Google Videos
1. **"Introducing Agent Development Kit"**
   - URL: https://www.youtube.com/watch?v=zgrOwow_uTQ
   - Overview of ADK framework and philosophy

2. **"Getting started with Agent Development Kit"**
   - Covers: Agent definition, Runner, Services
   - Includes: YouTube Shorts agent demo

3. **"Introduction to Vertex AI Agent Engine"**
   - Managed deployment walkthrough
   - Shows containerization and scaling

### Community Tutorials

4. **"Google ADK Tutorial – Quick Demo"**
   - Installation, first agent, quick demo

5. **"Google Cloud Agent Development Kit Tutorial | Build Your First ADK Agent"**
   - Beginner-friendly introduction

6. **"Google Agent Development Kit (ADK): Complete Tutorial for Building AI Agents"**
   - Comprehensive multi-agent systems
   - Memory, safety, cross-model support

7. **"Build Your First AI Agent Team with ADK"**
   - Multi-agent Weather Bot system
   - Delegation patterns

8. **"ADK Course #3 - Build a Sequential Workflow Agent"**
   - Sequential multi-agent for webpage generation
   - Project structure best practices

---

## Critical Implementation Notes

### ADK-Specific Requirements

1. **ALWAYS inherit from `adk.Agent`**
   - Never use bare LangChain or CrewAI
   - Wrap external frameworks in ADK Tools if needed

2. **ALWAYS create `agent.json` for A2A compliance**
   - Required in project root
   - Must be served at `/.well-known/agent.json`

3. **ALWAYS use type hints**
   - ADK auto-generates tool schemas from type hints
   - Use Pydantic models for complex inputs

4. **State Management**
   - Agents should be stateless between turns
   - Use `ctx.session` for persistent state
   - Never rely on instance variables for state

5. **Model Selection**
   ```python
   from adk.models import Gemini, OpenAI, Anthropic
   
   # Gemini (recommended)
   model = Gemini("gemini-2.0-flash-exp")
   
   # OpenAI
   model = OpenAI("gpt-4")
   
   # Anthropic
   model = Anthropic("claude-3-5-sonnet-20241022")
   ```

### Common Pitfalls to Avoid

❌ **Don't**: Hardcode API keys
✅ **Do**: Use Secret Manager

❌ **Don't**: Store state in instance variables
✅ **Do**: Use `ctx.session`

❌ **Don't**: Skip error handling
✅ **Do**: Wrap in try/except with fallbacks

❌ **Don't**: Deploy without testing locally
✅ **Do**: Use `agent.run()` for local development

❌ **Don't**: Ignore tool schemas
✅ **Do**: Provide detailed type hints and descriptions

---

## Quick Reference Commands

```bash
# Installation
pip install google-adk

# Run locally (with web UI)
adk run agent.py

# Run locally (CLI mode)
adk run agent.py --cli

# Deploy to Vertex AI Agent Engine
adk deploy agent_engine --project=PROJECT --region=REGION

# Test deployed agent
python test_remote_agent.py

# View logs
gcloud logging read "resource.type=cloud_run_revision"

# Generate project structure
adk init my-agent --template=basic

# Evaluate agent
adk evaluate agent.py --test-cases=tests.json
```

---

## Version Compatibility

- **ADK Python**: `>= 2.1.0`
- **Python Version**: `>= 3.11`
- **Gemini Models**: `gemini-2.0-flash-exp`, `gemini-1.5-pro`, `gemini-1.5-flash`
- **A2A Protocol**: `v1.0`
- **Vertex AI SDK**: `>= 1.38.0`

---

## Additional Resources

### GitHub Discussions
- Feature requests: https://github.com/google/adk-python/discussions
- Community Q&A: https://github.com/google/adk-samples/discussions

### Issue Tracking
- Report bugs: https://github.com/google/adk-python/issues
- Sample issues: https://github.com/google/adk-samples/issues

### Community
- ADK Community Tools: https://github.com/google/adk-python-community
- Sample Implementations: https://github.com/d3xvn/adk-samples
- More Examples: https://github.com/Neutrollized/adk-examples

---

**Document Maintained By**: Antigravity ADK Foundations Skill  
**Last Knowledge Update**: January 28, 2026  
**Next Review**: February 2026 (following ADK release cycle)
