# A2UI (Agent to UI) Protocol Specification (v0.8 Summary)

## Core Philosophy
A2UI decouples the agent's logic from the specific UI implementation, allowing for platform-agnostic, streaming interfaces.

## Key Concepts

### 1. JSONL Stream
All communication is a stream of JSON objects, allowing for progressive rendering.

### 2. Surfaces
Managing multiple UI regions (e.g., Sidebar, Main Content, Toast).
- `surfaceUpdate`: Message to update a specific UI region.

### 3. Component Model
- `catalogNegotiation`: Determining which components the client supports.
- `component`: A generic object representing a UI element.

### 4. Data Binding
- `dataModelUpdate`: Decouples the data from the component structure.
- `BoundValue`: Objects that link UI properties to the underlying data model.

## UI Composition
Uses an **Adjacency List Model** for tree construction, enabling efficient partial updates to deep hierarchies.
