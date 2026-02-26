---
name: adk-master-architect
description: Complete system for designing, building, deploying, and maintaining Google ADK agents with A2A protocol support.
version: 1.1.0
dependencies:
  - adk-foundations
sources:
  - name: ADK Comprehensive Knowledge Base
    path: ../adk-foundations/resources/comprehensive_knowledge_base.md
    type: internal
  - name: ADK Official Docs
    url: https://google.github.io/adk-docs/
    type: official
---

# ADK Master Architect

**Purpose:** Authoritative skill for creating, validating, deploying, and maintaining Google ADK agents.

> [!IMPORTANT]
> **Static Knowledge Migration**: Global architectural standards, A2A protocols, and project structures have been moved to the project-level `AGENTS.md` file for passive context. Refer to `AGENTS.md` for core mandates.

## Capabilities
- **Create & Scaffold**: Generate production-ready ADK project structures.
- **Test & Validate**: Generate test suites and validate A2A compliance.
- **Deployment**: Automate deployments to Vertex AI Agent Engine.
- **Maintenance**: Update and refactor existing agents.

## Tool Operations
This skill leverages the following embedded scripts:
- `scaffold_agent.py`: Scaffolds project structure.
- `validate_agent.py`: Validates compliance.
- `deploy_agent.py`: Automates deployment.
- `generate_tools.py`: Generates tool templates.

## Usage Scenarios
- "Scaffold a new agent named [name]"
- "Add [capability] to [agent]"
- "Deploy [agent] to Vertex AI"

## Review Checklist
- [ ] Project follows the structure defined in `AGENTS.md`.
- [ ] Agent class inherits from the correct ADK base classes.
- [ ] Tools have proper type hints and structured returns.
- [ ] No hardcoded secrets.
