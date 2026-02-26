---
name: agent-browser
description: Headless browser automation CLI for AI agents with context-efficient text output and ref-based deterministic element selection. Developed by Vercel Labs.
version: 1.0.0
nosync: false
---

# Agent Browser Skill

`agent-browser` (https://agent-browser.dev/) is a browser automation CLI specifically designed for AI agents. Rather than dumping a massive HTML DOM that consumes thousands of tokens, it outputs a highly compact text-based accessibility tree where each interactable element is assigned a discrete reference (e.g., `@e1`, `@e2`). This deterministic ref-based system allows language models to confidently interact with web pages using minimal context window overhead.

Under the hood, it features a client-daemon architecture: a fast native Rust CLI for instant command parsing that communicates with a Node.js daemon managing a Playwright browser instance, persisting sessions between commands.

## Core Capabilities

- **Agent-First Output**: Compact text output (often ~200-400 tokens) designed for context efficiency compared to full HTML DOMs (~3000-5000 tokens).
- **Ref-Based Interaction**: The `snapshot` command generates an accessibility tree with unique refs for elements, enabling deterministic interaction (e.g., `agent-browser click @e2`).
- **Speed & Architecture**: Native Rust binaries for the CLI with a persistent Node.js/Playwright daemon running in the background.
- **Session Management**: Supports multiple isolated browser instances with separate authentication states.
- **Cross-Platform**: Available on macOS, Linux, and Windows via npm or Homebrew.

## CLI Usage

Install globally via npm:
```bash
npm install -g agent-browser
```

### Basic Workflow Example
1. Open a URL and get a snapshot (filtering for interactive elements):
```bash
agent-browser open example.com
agent-browser snapshot -i
```
*Output looks like:*
```
- heading "Example Domain" [ref=e1]
- link "More information..." [ref=e2]
```

2. Interact using refs:
```bash
agent-browser click @e2
agent-browser screenshot page.png
agent-browser close
```

### Common Commands
- **Navigation**:
  - `agent-browser open <url>`
  - `agent-browser back` / `forward` / `reload`
  - `agent-browser close`
- **Interaction**:
  - `agent-browser click <sel>`, `agent-browser dblclick <sel>`
  - `agent-browser fill <sel> <text>`, `agent-browser type <sel> <text>`
  - `agent-browser hover <sel>`
  - `agent-browser scroll <dir> [px]`, `agent-browser scrollintoview <sel>`
- **Keyboard**:
  - `agent-browser press <key>` (e.g. Enter, Tab, Control+a)
  - `agent-browser keyboard type <text>`, `agent-browser keydown <key>`
- **Visuals**:
  - `agent-browser screenshot [path]` (`--full` for full page)
  - `agent-browser screenshot --annotate`
  - `agent-browser pdf <path>`
- **Data/Extraction**:
  - `agent-browser snapshot [-i]`
  - `agent-browser get text <sel>`, `agent-browser get html <sel>`, `agent-browser get url`
- **State Check**:
  - `agent-browser is visible <sel>`
- **Waiting**:
  - `agent-browser wait --load <state>` (e.g. `load`, `domcontentloaded`, `networkidle`)
  - `agent-browser wait --url <pattern>`

## Best Practices

- **Use Snapshot First**: Always use `agent-browser snapshot -i` to build spatial awareness of the page BEFORE attempting interactions.
- **Recycle Refs**: Refs are valid only until the next navigation or significant DOM change. Always take a fresh snapshot after an action that updates the UI.
- **Prefer Refs Over CSS**: Target elements via their generated `@eX` refs. Refs are significantly less brittle than CSS selectors and guarantee deterministic AI execution.
- **Wait for Network**: Use `wait --load networkidle` for heavy SPAs to ensure elements are present and interactive before taking a snapshot.
- **Token Efficiency**: Rely on `snapshot` output instead of `get html` when feeding page structures to LLMs to drastically save context tokens.
