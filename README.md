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
├── skill-manager/           # Meta-skill for managing all other skills
│   └── SKILL.md
└── scripts/                 # Helper scripts for skill lifecycle
    ├── create_skill.py      # Scaffold new skills
    ├── validate_skill.py    # Validate skill structure
    └── deploy_skill.py      # Deploy to environments
```

## Quick Start

### For Claude Desktop
Upload skills via Settings > Capabilities > Upload skill

### For Claude Code CLI
```bash
# Symlink this repo to Claude Code skills directory
ln -s "C:\Users\Kurt Anderson\github projects\mapache-skills" ~/.claude/skills
```

### For Claude API
Use the `/v1/skills` endpoint to upload programmatically
