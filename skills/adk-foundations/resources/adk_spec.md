# Google Agent Development Kit (ADK) Overview

## Agent Categories

1. **LLM Agents (`LlmAgent`, `Agent`)**:
   - Use LLMs for reasoning, planning, and tool selection.
   - Ideal for language-centric, flexible tasks.

2. **Workflow Agents (`SequentialAgent`, `ParallelAgent`, `LoopAgent`)**:
   - Deterministic control flow.
   - No LLM used for flow control itself.
   - Ideal for predictable, structured processes.

3. **Custom Agents**:
   - Extend `BaseAgent` for unique logic or integrations.

## Multi-Agent Systems
Orchestrate complexity by composing specialized agents into broad architectures.
- Use **Workflow Agents** for the pipeline.
- Use **LLM Agents** for the decision-making steps.
- Use **Task Update Delivery** (A2A) to track progress.
