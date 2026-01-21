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
