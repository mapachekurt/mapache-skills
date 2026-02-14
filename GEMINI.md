# Google Antigravity Global Rules

These rules define the coding and documentation standards for this environment. They are "Always On" by default unless otherwise specified.

## 1. Documentation Standards
- **JSDoc Requirement**: All functions and classes must be documented using JSDoc (or equivalent for other languages). Include descriptions, `@param` tags, and `@returns` tags. [Ref: Video 02:21]
- **"Why," Not Just "What"**: Comments should focus on explaining the reasoning behind tricky logic or design decisions. Avoid redundant comments that simply restate what the code is doing. [Ref: Video 02:21]

## 2. Rule Activation Modes (Strategic Selection)
- **Always On**: Apply these core standards (commenting, linting, etc.) to every single interaction.
- **Manual Trigger**: Use the `@` symbol to invoke specific, situational rules (e.g., `@performance-audit`).
- **Context-Aware**: Provide natural language descriptions for situational rules, allowing the model to decide when to apply them based on task context.

### Debug Mode (Evidence-Based)
When a bug is encountered:
1. Formulate a hypothesis.
2. Add logging statements to gather evidence.
3. Create a multi-phase plan to resolve the issue based on logs.

### Agent & MCP TDD ("Eval-Driven Genesis")
- **Mandate**: No new agent OR MCP server is created without a `verification_suite.md`.
- **Phase 0 (Agents)**: Use `exa-grounding` to find "Expert Scenarios" (exams, edge cases).
- **Phase 0 (MCPs)**: Define the JSON Schema and expected output for every tool *before* writing implementation code.
- **The Loop**: 
    1. **Red**: Run scenarios/tools against vanilla model/stub (Expect Failure).
    2. **Green**: Ground agent (Vector DB) or Implement Tool (API Logic).
    3. **Refactor**: If verification fails, add targeted grounding or fix tool logic.

- **Glob Scoping**: Use file patterns to target specific directories or extensions:
    - `src/**/*.js`: Apply only to Javascript source files.
    - `tests/**/*`: Apply only to test files.

## 3. UI/Visual Consistency (Pencil/CloudRun)
- **Aesthetics First**: Use curated color palettes (HSL), modern typography (Google Fonts), and glassmorphism where applicable.
- **Micro-animations**: Integrate subtle hover effects and transitions to make interfaces feel alive.
- **Dynamic Response**: Ensure all designs are fully responsive and premium in feel.

## 4. Beads Execution Memory
- **Session Protocol**: Always run `bd prime` at session start in any Beads-enabled repo (contains `.beads/` directory).
- **Never Orphan Work**: Always "Land the Plane" (`/land-the-plane`) before ending a session — `bd sync` + `git push` is non-negotiable.
- **Artifact Bridge**: When generating an `implementation_plan.md`, offer to "slurp" its tasks into Beads for persistent tracking.
- **Anti-Patterns**: Never use `bd edit` (interactive editor). Never skip claiming a task in multi-agent repos.
