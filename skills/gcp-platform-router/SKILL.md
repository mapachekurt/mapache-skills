---
name: gcp-platform-router
description: Antigravity Native for steering agent development to the correct GCP platform (Cloud Run vs Vertex AI Agent Engine).
version: 1.0.0
---

# GCP Platform Router

This skill provides a standardized framework for deciding where an AI agent should be deployed on Google Cloud Platform. It uses a "Worker vs Character" heuristic to route agents to either Cloud Run (for tool-heavy, stateless workers) or Vertex AI Agent Engine (for long-lived conversational personas).

## Core Heuristic

- **Worker → Cloud Run**: Value comes from *doing work* (tools, actions, background tasks).
- **Character → Agent Engine**: Value comes from *being someone* (conversational continuity, persona, shared context).

## Decision signals

| Signal | Cloud Run | Agent Engine |
|---|---|---|
| **State** | Stateless or custom state (DB) | Built-in conversational memory |
| **Continuity** | Single-turn or ephemeral | Multi-turn, long-term threads |
| **Interaction** | API-driven / Tools | Chat-native / Human-facing |
| **Control** | Full control over runtime | Managed agent runtime |
| **Complexity** | High tool/orchestration logic | High reasoning/personality logic |

## Usage

Run the routing assistant to classify a new agent:

```bash
python skills/gcp-platform-router/scripts/route_agent.py --description "Your agent description here"
```

Refer to the resources for deeper guidance:
- [Routing Rubric](resources/agent-platform-routing.md)
- [Agent Taxonomy](resources/agent-types-by-platform.md)
