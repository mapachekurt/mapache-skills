---
name: beads
description: Architectural reference for Beads (bd) persistent execution memory.
---

# Skill: Beads Architecture

## Overview
Beads (`bd`) is a git-native, dependency-aware issue tracker for AI agents. It provides a persistent, queryable DAG stored in `.beads/`.

**Complementary Note**: `beads` (this skill) focuses on **internals/architecture**. Use `beads-coordinator` for **operational commands**.

**Sources**: [Overview](https://deepwiki.com/steveyegge/beads/1-overview), [Architecture](https://deepwiki.com/steveyegge/beads/1.2-architecture-overview).

## Core Architecture

### 1. Layers & Modes
- **Presentation**: CLI (Go/Cobra) and MCP Server (FastMCP/Python).
- **Storage**: Unified `storage.Storage` interface. Backends: SQLite (default), Dolt, or Memory.
- **Modes**: Selected automatically in `PersistentPreRun`:
    - **Direct**: In-process access to SQLite.
    - **Daemon**: RPC via Unix socket. Required for multi-agent concurrency.

### 2. Data Flow
- **Write Path**: `store.CreateIssue()` → `dirty=1` → `FlushManager` → `writeIssuesToJSONL()` → `git commit`.
- **Import Path**: `git pull` → `fsnotify` → `loadIssuesFromJSONL()` → `importWithCollisionDetection()`.
- **Sync**: Pull-first strategy; 3-way merge between base, local, and remote states.
- **Incremental Export**: Uses SHA256 content hashes in `export_hashes` table to only write issues where `dirty=1`.

### 3. Git Integration
- **Hooks**: Delegates to `bd hook {name}` (pre-commit, post-merge, pre-push, post-checkout).
- **Merge Driver**: Registered for `issues.jsonl`. Performs field-level resolution (LWW for scalars, union for arrays).
- **Sync Branch**: Uses isolated worktree (`beads-sync`) to avoid polluting main branch with auto-sync commits.

## Agent Integration
- **MCP**: Best for Claude/Antigravity. Tools: `create_issue`, `update_issue`, `list_issues`, `search_issues`, `show_issue`.
- **`bd prime`**: Generates context-dense summaries (~1-2k tokens) for session start.

## Database Schema (SQLite)
| Table | Key Fields | Purpose |
|-------|------------|---------|
| `issues` | `status`, `priority`, `type` | Core entity data |
| `dependencies` | `issue_id`, `depends_on` | DAG relationships |
| `labels` / `comments` | `issue_id` | Metadata & discussion |
| `export_hashes` | `content_hash` | Incremental export tracking |
| `events` | `actor`, `timestamp` | Audit log |

## Constraints & Anti-Patterns
- **No Direct Edits**: Never modify `issues.jsonl` manually; use `bd` CLI.
- **Sync First**: Always `bd sync` before `git push`.
- **Daemon Consistency**: Ensure version parity between CLI client and running daemon.
- **Agent Work**: Never use `bd edit` (interactive); use `bd update` with flags.

## Reference
- **Config Precedence**: CLI Flags > Repo Config (`.beads/`) > Global Config (`~/.config/`) > Defaults.
- **Command Groups**: Issues (CRUD), Views (Queries), Deps (DAG), Sync (Git), Setup (Init/Config).
