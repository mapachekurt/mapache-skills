# Mapache Skills Repository

## Overview
This repository contains custom Mapache Skills that enhance capabilities across Desktop, Code CLI, and API environments.

Skills are portable, composable instruction packages that work with any LLM that supports:
- File system access
- Markdown reading
- Code execution

## Repository Structure

```
mapache-skills/
├── README.md
├── .gitignore
├── skills/                  # Core skill packages
│   ├── skill-manager/       # Meta-skill for managing all other skills
│   ├── n8n-flow-builder/
│   └── ...
├── scripts/                 # Helper scripts for skill lifecycle
│   ├── create_skill.py
│   ├── validate_skill.py
│   └── deploy_skill.py
├── lab/                     # Experimental and WIP projects
└── tools/                   # Utility scripts and external tools
```

## Quick Start

### For Claude Desktop
Upload skills via Settings > Capabilities > Upload skill

### For Claude Code CLI
```bash
# Symlink this repo to Claude Code skills directory
ln -s "C:\Users\Kurt Anderson\github projects\mapache-skills\skills" ~/.claude/skills
```

### For Claude API
Use the `/v1/skills` endpoint to upload programmatically

## Automation & Sync

This repository supports automated skill updates for coding agents like Antigravity, Claude Code, and Gemini CLI using `vercel-labs/add-skill`.

### 1. Manual Sync
Sync all non-exempt local skills to all installed agents:
```bash
python scripts/sync_skills.py
```

### 2. Automatic Updates (Background)
To keep your agents updated in real-time whenever you modify a skill:
1. Open PowerShell as Administrator.
2. Run the setup script:
   ```powershell
   .\scripts\setup_watcher.ps1
   ```
This registers a Windows background task that monitors the `skills/` directory.

### 3. Automatic Versioning
Bump a skill's version before deployment:
```bash
python scripts/version_skill.py <skill-name> --bump [patch|minor|major]
```

### 4. Skill Exemptions
To prevent a specific skill from being automatically synced (e.g., WIP or private skills), add this to its `SKILL.md` frontmatter:
```yaml
---
name: my-skill
description: ...
nosync: true
---
```

### 5. Upstream Maintenance
Check for tool updates and improvements from the upstream repository:
```bash
python scripts/check_upstream.py
```
