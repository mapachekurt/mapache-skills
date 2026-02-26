# Resource: Snapshot + Refs Mechanic

The "Snapshot + Refs" system is the core architectural innovation of the `agent-browser` tool. It is designed to bridge the gap between heavy, unstructured web data and the limited context window of LLMs.

## How it works

### 1. The Snapshot
A snapshot is a semantic representation of the DOM. Unlike raw HTML, it:
- Filters out non-interactive elements (by default or with `-i`).
- Normalizes roles and labels for high-level reasoning.
- Captures bounding boxes for spatial awareness.

### 2. The Reference (Ref)
Every interactive element is assigned a temporary identifier (e.g., `@e1`). This ref acts as a handle for the agent.
- **Syntactic Sugar**: Instead of passing `document.querySelector('button[type="submit"]')`, the agent simply passes `@e1`.
- **Efficiency**: Reduces input tokens significantly.

### 3. State Management
Refs are **volatile**. They are tied to a specific snapshot ID. 
- **Invalidation**: If the page navigates, reloads, or undergoes a significant client-side DOM update, the current refs are invalidated.
- **Recovery**: The agent must run `agent-browser snapshot -i` again to re-sync its worldview and get fresh refs.

## Reasoning Patterns for Agents

### Pattern A: Exploratory
1. `open <url>`
2. `snapshot -i` -> Observe available refs.
3. `get text <ref>` -> Inspect specific content.

### Pattern B: Procedural
1. `fill <ref_a> <data>`
2. `fill <ref_b> <data>`
3. `click <ref_c>`
4. `wait --load networkidle`
5. `snapshot -i` -> Verify new state.

## Troubleshooting
- **Ref Mismatch**: If a `click @e1` fails, it's likely the DOM changed. Always take a fresh snapshot if actions fail.
- **Shadow DOM**: The snapshotter automatically flattens accessible shadow roots to ensure full transparency to the agent.
