"""
ADK Agent Scaffolding Script

Generates production-ready Google ADK agent projects with:
- Proper directory structure
- ADK-compliant agent.py
- A2A-compliant agent.json
- Configuration files
- Test suite
- Deployment configuration

Usage:
    python scaffold_agent.py --name "agent-name" --purpose "what it does" --tools "tool1,tool2"
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class ADKAgentScaffolder:
    """Scaffolds production-ready ADK agents"""
    
    def __init__(self, name: str, purpose: str, tools: List[str], base_dir: str = "."):
        self.name = name.lower().replace(" ", "-")
        self.class_name = "".join(word.capitalize() for word in self.name.split("-"))
        self.purpose = purpose
        self.tools = tools
        self.base_dir = Path(base_dir) / self.name
        
    def create_structure(self):
        """Create directory structure"""
        print(f"🏗️  Creating project structure for '{self.name}'...")
        
        directories = [
            self.base_dir,
            self.base_dir / "tools",
            self.base_dir / "tests",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {directory}")
    
    def generate_agent_py(self) -> str:
        """Generate main agent.py file"""
        return f'''"""
{self.class_name} Agent

Purpose: {self.purpose}
Created: {datetime.now().strftime("%Y-%m-%d")}
"""

from adk import Agent, on_message
from adk.models import Gemini
import logging

# Import custom tools
from tools.custom_tools import {", ".join(self.tools) if self.tools else "# Add your tools here"}


class {self.class_name}Agent(Agent):
    """
    {self.purpose}
    
    This agent follows Google ADK standards and A2A protocol.
    """
    
    def __init__(self):
        super().__init__(
            name="{self.name}",
            model=Gemini("gemini-2.0-flash-exp"),
            description="{self.purpose}",
            tools=[{", ".join(self.tools) if self.tools else "# Add tools here"}]
        )
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='{{\"time\":\"%(asctime)s\", \"level\":\"%(levelname)s\", \"msg\":\"%(message)s\"}}'
        )
        self.logger = logging.getLogger(__name__)
    
    @on_message
    def handle_message(self, message: str, ctx):
        """
        Handle incoming messages.
        
        Args:
            message: User message
            ctx: Context object with session, run_id, etc.
        
        Returns:
            Response string or structured data
        """
        self.logger.info(
            f"Processing message in session {{ctx.session_id}}",
            extra={{"message_length": len(message)}}
        )
        
        # Retrieve conversation history from session
        history = ctx.session.get("history", [])
        
        # Generate response using LLM
        response = self.llm.generate(
            message,
            context={{"history": history}}
        )
        
        # Update session history
        history.append({{"user": message, "agent": response.text}})
        ctx.session["history"] = history
        
        self.logger.info(
            f"Response generated",
            extra={{"response_length": len(response.text)}}
        )
        
        return response.text


# For local testing
if __name__ == "__main__":
    agent = {self.class_name}Agent()
    
    # Run with web UI at http://localhost:8000
    agent.run()
    
    # Or run in CLI mode:
    # agent.run(cli=True)
'''
    
    def generate_agent_json(self) -> Dict[str, Any]:
        """Generate A2A-compliant agent.json"""
        return {
            "id": f"{self.name}-v1",
            "version": "1.0.0",
            "name": self.class_name + " Agent",
            "description": self.purpose,
            "capabilities": self.tools if self.tools else ["conversation"],
            "endpoints": {
                "main": f"https://[DEPLOYMENT-URL]/a2a/v1/message",
                "discovery": f"https://[DEPLOYMENT-URL]/.well-known/agent.json"
            },
            "auth": {
                "type": "oauth2",
                "scope": "https://www.googleapis.com/auth/cloud-platform"
            },
            "supportedInterfaces": ["json-rpc", "http+json"],
            "skills": [
                {
                    "name": self.name,
                    "description": self.purpose
                }
            ],
            "metadata": {
                "created": datetime.now().isoformat(),
                "framework": "google-adk",
                "framework_version": "2.1.0+"
            }
        }
    
    def generate_config_py(self) -> str:
        """Generate config.py"""
        return '''"""
Configuration for agent
"""

import os
from adk.models import Gemini

# Model Configuration
MODEL = Gemini(
    model_name="gemini-2.0-flash-exp",
    temperature=0.7,
    top_p=0.9,
    max_output_tokens=8192
)

# Agent Configuration
AGENT_NAME = "''' + self.name + '''"
AGENT_DESCRIPTION = "''' + self.purpose + '''"

# Environment
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
'''
    
    def generate_custom_tools(self) -> str:
        """Generate tools/custom_tools.py with examples"""
        tool_examples = ""
        
        for tool_name in self.tools if self.tools else ["example_tool"]:
            tool_examples += f'''

@tool(name="{tool_name}", description="Description of {tool_name}")
def {tool_name}(param1: str, param2: int = 10) -> dict:
    """
    Detailed description of what {tool_name} does.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2
    
    Returns:
        Dictionary with structured results
    """
    # TODO: Implement {tool_name}
    return {{
        "status": "success",
        "result": "Placeholder result"
    }}
'''
        
        return f'''"""
Custom tools for {self.class_name} Agent

All tools must follow ADK standards:
- Type hints on all parameters and return values
- Detailed docstrings with Args and Returns sections
- Structured return values (dict recommended)
"""

from adk import tool
from typing import Literal, Optional
import logging

logger = logging.getLogger(__name__)

{tool_examples}
'''
    
    def generate_requirements_txt(self) -> str:
        """Generate requirements.txt"""
        return '''# Core ADK
google-adk>=2.1.0

# Google Cloud
google-cloud-aiplatform>=1.38.0
google-cloud-secretmanager>=2.16.0

# Common utilities
requests>=2.31.0
python-dotenv>=1.0.0
pydantic>=2.5.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0

# Add your specific dependencies below
'''
    
    def generate_adk_yaml(self) -> str:
        """Generate adk.yaml for deployment"""
        return f'''# Vertex AI Agent Engine Deployment Configuration
name: {self.name}
runtime: python311
entrypoint: agent:app

# Scaling configuration
scaling:
  min_instances: 1
  max_instances: 10
  concurrency: 80

# Environment variables
env:
  GOOGLE_CLOUD_PROJECT: "YOUR_PROJECT_ID"
  GOOGLE_CLOUD_REGION: "us-central1"
  A2A_ENABLE: "true"
  LOG_LEVEL: "INFO"

# Secrets from Secret Manager
secrets:
  # Add your secrets here
  # - name: OPENAI_API_KEY
  #   version: latest
  # - name: ANTHROPIC_API_KEY
  #   version: latest

# Service account (recommended)
# service_account: "{self.name}-sa@YOUR_PROJECT.iam.gserviceaccount.com"
'''
    
    def generate_test_agent_py(self) -> str:
        """Generate tests/test_agent.py"""
        return f'''"""
Unit tests for {self.class_name}Agent
"""

import pytest
from agent import {self.class_name}Agent
from adk.testing import MockContext


@pytest.fixture
def agent():
    """Create agent instance for testing"""
    return {self.class_name}Agent()


@pytest.fixture
def mock_context():
    """Create mock context"""
    return MockContext(session_id="test-session-123")


def test_agent_initialization(agent):
    """Test agent initializes correctly"""
    assert agent.name == "{self.name}"
    assert agent.model is not None
    assert agent.description == "{self.purpose}"


def test_basic_message_handling(agent, mock_context):
    """Test agent handles messages"""
    response = agent.handle_message("Hello, agent!", mock_context)
    
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0


def test_session_persistence(agent, mock_context):
    """Test conversation history persists in session"""
    # First message
    agent.handle_message("Remember my name is Alice", mock_context)
    
    # Check session has history
    history = mock_context.session.get("history")
    assert history is not None
    assert len(history) > 0
    
    # Second message
    agent.handle_message("What's my name?", mock_context)
    
    # History should have grown
    updated_history = mock_context.session.get("history")
    assert len(updated_history) > len(history)


def test_tool_availability(agent):
    """Test tools are properly registered"""
    # Check agent has tools assigned
    # TODO: Add tool-specific tests when tools are implemented
    pass


# Add more tests as needed
'''
    
    def generate_readme(self) -> str:
        """Generate README.md"""
        return f'''# {self.class_name} Agent

{self.purpose}

## Overview

This agent is built using Google's Agent Development Kit (ADK) and follows the Agent2Agent (A2A) protocol for interoperability.

**Capabilities:**
{chr(10).join(f"- {tool}" for tool in self.tools) if self.tools else "- Conversational AI"}

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
{self.name}/
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
   adk deploy agent_engine \\
     --config=adk.yaml \\
     --region=us-central1
   ```

3. **Test deployed agent:**
   ```bash
   python test_remote_agent.py
   ```

### Deploy to Cloud Run

```bash
adk deploy cloudrun \\
  --project=YOUR_PROJECT_ID \\
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

{chr(10).join(f"### {tool}{chr(10)}TODO: Document {tool}" for tool in self.tools) if self.tools else "No custom tools yet. Add tools in `tools/custom_tools.py`."}

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
       \"\"\"Tool description\"\"\"
       return {{"result": "value"}}
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
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name={self.name}"
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

**Created:** {datetime.now().strftime("%Y-%m-%d")}  
**Framework:** Google ADK 2.1.0+  
**Protocol:** A2A v1.0
'''
    
    def generate_env_example(self) -> str:
        """Generate .env.example"""
        return '''# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_REGION=us-central1

# Logging
LOG_LEVEL=INFO

# API Keys (or use Secret Manager for production)
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...

# Add your environment variables here
'''
    
    def generate_init_files(self):
        """Generate __init__.py files"""
        init_content = '"""Package initialization"""'
        
        for directory in ["tools", "tests"]:
            init_file = self.base_dir / directory / "__init__.py"
            init_file.write_text(init_content, encoding="utf-8")
            print(f"✅ Created: {init_file}")
    
    def scaffold(self):
        """Execute complete scaffolding"""
        print(f"\n🚀 Scaffolding ADK Agent: {self.class_name}\n")
        
        # Create structure
        self.create_structure()
        
        # Generate files
        files = {
            "agent.py": self.generate_agent_py(),
            "agent.json": json.dumps(self.generate_agent_json(), indent=2),
            "config.py": self.generate_config_py(),
            "tools/custom_tools.py": self.generate_custom_tools(),
            "requirements.txt": self.generate_requirements_txt(),
            "adk.yaml": self.generate_adk_yaml(),
            "tests/test_agent.py": self.generate_test_agent_py(),
            "README.md": self.generate_readme(),
            ".env.example": self.generate_env_example(),
        }
        
        for filepath, content in files.items():
            full_path = self.base_dir / filepath
            full_path.write_text(content, encoding="utf-8")
            print(f"✅ Created: {full_path}")
        
        # Create __init__.py files
        self.generate_init_files()
        
        print(f"\n✨ Agent '{self.name}' successfully scaffolded!")
        print(f"\n📁 Project location: {self.base_dir.absolute()}")
        print(f"\n🎯 Next steps:")
        print(f"   1. cd {self.name}")
        print(f"   2. Edit .env.example and save as .env")
        print(f"   3. pip install -r requirements.txt")
        print(f"   4. Implement tools in tools/custom_tools.py")
        print(f"   5. adk run agent.py")
        print(f"\n📖 See README.md for full documentation")


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a production-ready Google ADK agent"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Agent name (e.g., 'weather-bot')"
    )
    parser.add_argument(
        "--purpose",
        required=True,
        help="Agent purpose (e.g., 'Provides weather information')"
    )
    parser.add_argument(
        "--tools",
        default="",
        help="Comma-separated list of tool names (e.g., 'search_web,analyze_data')"
    )
    parser.add_argument(
        "--dir",
        default=".",
        help="Base directory for project (default: current directory)"
    )
    
    args = parser.parse_args()
    
    tools = [t.strip() for t in args.tools.split(",") if t.strip()]
    
    scaffolder = ADKAgentScaffolder(
        name=args.name,
        purpose=args.purpose,
        tools=tools,
        base_dir=args.dir
    )
    
    scaffolder.scaffold()


if __name__ == "__main__":
    main()
