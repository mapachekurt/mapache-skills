# GCP Agent Taxonomy

Concrete examples of agent archetypes and their recommended deployment targets.

## 🚀 Cloud Run Agents (Workers)
*Agents whose value comes from doing work.*

- **Linear Agent**: Creates issues, updates statuses, triages backlogs.
- **GitHub Agent**: Opens PRs, reviews diffs, merges branches.
- **Supabase / DB Agent**: Queries, migrations, cleanup jobs.
- **n8n Agent**: Generates or validates workflows.
- **MCP Router Agent**: Routes calls to the right MCP server.
- **Browser Agent**: Runs UI teardown, E2E tests, scraping.
- **Monitoring Agent**: Watches logs, usage, failures.
- **Cost Agent**: Computes ROI, credit usage, burn.
- **Agent Dispatcher**: Coordinates other agents.
- **Policy / Guardrail Agent**: Enforces rules across systems.

## 🧠 Vertex AI Agent Engine Agents (Characters)
*Agents whose value comes from being someone.*

- **Company AI Assistant**: "Knows" the business context over months.
- **Project Manager Agent (Human-Facing)**: Remembers goals, frustrations, tradeoffs.
- **Founder Copilot**: Long-term strategic conversational partner.
- **Strategy Advisor Agent**: Thinks, reflects, explains high-level strategy.
- **Architecture Review Agent**: Builds a shared mental model of system design.
- **Personal AI Twin**: Conversational mirror of a user.
- **Onboarding Guide Agent**: Guides new users through long-running setups.

## 🏗️ Hybrid Agents
*Persona front-end + Worker back-ends.*

- **Autonomous CEO**: Agent Engine persona (intent) + Cloud Run workers (execution).
- **Project Lead**: Agent Engine for user interaction + Cloud Run for tool sync/issue creation.
- **Knowledge Synthesis Agent**: Agent Engine for chat + Cloud Run for heavy scraping/processing.
