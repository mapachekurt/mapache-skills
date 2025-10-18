---
name: skill-manager
description: Automate creation, versioning, deployment, and synchronization of Claude Skills across Desktop, Code CLI, and API environments. Manages skill lifecycle from scaffolding to deployment.
---

# Skill Manager

## Purpose
Meta-skill for managing the complete lifecycle of all other Claude Skills. Ensures skills are version-controlled in Git and automatically synchronized across all Claude environments (Desktop, Code CLI, API).

## Core Capabilities
- **Create**: Scaffold new skills from templates with proper structure
- **Validate**: Check YAML frontmatter, markdown syntax, security
- **Deploy**: Sync skills to Code CLI, API, or Desktop
- **Version**: Semantic versioning and Git integration
- **Monitor**: Watch for changes and auto-sync

## Architecture Overview

### Source of Truth
- **Git Repository**: `C:\Users\Kurt Anderson\github projects\claude-skills\`
- **Branch Strategy**:
  - `main` = Production skills (stable, tested)
  - `dev` = Experimental/WIP skills
  - Feature branches = New skill development

### Deployment Targets
1. **Claude Code CLI**: `~/.claude/skills/` (symlinked to git repo)
2. **Claude API**: Via `/v1/skills` endpoint (programmatic)
3. **Claude Desktop**: Manual upload or API-based (if available)

### Standard Skill Structure
```
skill-name/
├── SKILL.md              # Required: YAML frontmatter + instructions
├── README.md             # Human documentation
├── scripts/              # Optional: Executable code
│   ├── __init__.py
│   └── helper.py
├── resources/            # Optional: Templates, data files
│   └── template.json
├── tests/                # Validation tests
│   └── test_skill.py
└── .skillmeta            # Version, author, dependencies
```

## Key Operations

### 1. Create New Skill
Scaffolds a new skill directory with proper structure and template content.

**Usage Pattern**:
"Create a new skill called 'n8n-flow-builder' that helps design n8n workflows"

**What Happens**:
1. Runs `scripts/create_skill.py` with skill name and description
2. Creates directory structure with SKILL.md template
3. Opens SKILL.md for review and editing
4. User iterates with Claude on content
5. Validates with `scripts/validate_skill.py`

### 2. Validate Skill
Checks skill for correctness and security before deployment.

**Validation Checklist**:
- ✅ YAML frontmatter is well-formed
- ✅ Required fields present (`name`, `description`)
- ✅ Markdown syntax is valid
- ✅ Script files have proper permissions
- ✅ No suspicious network calls to untrusted domains
- ✅ File access restricted to safe directories
- ✅ External dependencies documented

**Usage Pattern**:
"Validate the n8n-flow-builder skill before deploying"

### 3. Deploy Skill
Synchronizes skill to target environments.

**Deployment Options**:
- `--env code`: Deploy to Claude Code CLI (~/.claude/skills/)
- `--env api`: Deploy to Claude API via /v1/skills endpoint
- `--env all`: Deploy to all available environments

**Usage Pattern**:
"Deploy the n8n-flow-builder skill to all environments"

**What Happens**:
1. Validates skill first (auto-validation)
2. For Code CLI: Creates symlink or copies to ~/.claude/skills/
3. For API: Zips skill, POSTs to /v1/skills endpoint
4. Logs deployment status
5. Commits to Git if requested

### 4. List and Search Skills
Find skills in the repository.

**Usage Patterns**:
- "What skills do I have?"
- "Show me all skills related to GitHub"
- "List skills that haven't been deployed yet"

**Returns**:
- Skill name and version
- Description
- Deployment status
- Last modified date

### 5. Update Existing Skill
Modify and redeploy skills with version bumping.

**Usage Pattern**:
"Update the linear-orchestration skill to include new webhook format"

**What Happens**:
1. Reads current skill from git repo
2. Makes requested changes to SKILL.md or scripts
3. Shows diff for review
4. User approves changes
5. Validates updated skill
6. Deploys updated version
7. Git commit with semantic version bump (patch/minor/major)

## Helper Scripts Reference

### `scripts/create_skill.py`
Scaffolds new skills from template.

**Arguments**:
- `--name`: Skill name (kebab-case)
- `--description`: Brief description of what skill does
- `--template`: Optional template to use (default, api, workflow, etc.)

**Example**:
```bash
python scripts/create_skill.py --name "api-doc-generator" \
  --description "Generate OpenAPI specifications"
```

### `scripts/validate_skill.py`
Validates skill structure and security.

**Checks**:
- YAML frontmatter syntax
- Required field presence
- Markdown lint
- Script security scan
- Dependency audit

**Example**:
```bash
python scripts/validate_skill.py skill-name/
```

### `scripts/deploy_skill.py`
Deploys skills to target environments.

**Arguments**:
- `skill_path`: Path to skill directory
- `--env`: Target environment (code|api|all)
- `--validate`: Run validation first (default: true)
- `--commit`: Commit to git after deploy (default: false)

**Example**:
```bash
python scripts/deploy_skill.py n8n-flow-builder/ --env all --commit
```

## Security Considerations

### Validation Rules
Skills must pass all security checks before deployment:

1. **Network Access**: Scripts cannot call arbitrary URLs
   - Whitelist approved domains in skill config
   - Block suspicious patterns

2. **File Access**: Scripts restricted to safe directories
   - Skill directory itself
   - `/mnt/user-data/` (Claude execution environment)
   - Explicitly approved paths only

3. **Dependency Audit**: External libraries documented
   - All imports declared in `.skillmeta`
   - Known vulnerabilities flagged
   - Version pinning required

4. **Code Review**: Human review for high-risk operations
   - Network calls
   - File system modifications
   - Environment variable access

### Approval Workflow
- **Auto-deploy**: Skills that pass validation on `main` branch
- **Manual review**: New skills or those with network/file access beyond standard patterns

## Integration with Your Workflow

### Bootstrap Process
When starting a new session:
1. Claude Desktop loads `skill-manager` skill (this one)
2. Check git repo for latest skill updates
3. Auto-sync to Code CLI if changes detected
4. Report which skills are active and their versions

### Continuous Sync Options

**Option A: File Watcher (Recommended)**
Background daemon watches git repo for changes:
```python
# scripts/skill_sync_daemon.py
# Watches for SKILL.md changes
# Auto-validates and deploys to Code CLI
# Logs all operations
```

**Option B: n8n Automation (Optional)**
GitHub webhook triggers n8n workflow on push to `main`:
1. Validates all changed skills
2. Runs tests
3. Deploys to Code CLI (file sync)
4. Deploys to API (HTTP POST)
5. Posts deployment report to Slack
6. Creates Linear ticket if failures detected

**Option C: Manual Sync (Simplest)**
Run deployment manually when skills change:
```bash
python scripts/deploy_skill.py --env all
```

## Workflow Examples

### Example 1: Create and Deploy New Skill
```
User: "Create a new skill for n8n workflow authoring"

Claude (using skill-manager):
1. ✅ Runs create_skill.py with name "n8n-flow-builder"
2. ✅ Generates SKILL.md with template structure
3. 📝 Opens for user review: "Here's the template. What should I include?"
4. 🔄 User iterates: "Add section on webhook patterns"
5. 🔍 Validates with validate_skill.py
6. ✅ User approves: "Looks good, deploy it"
7. 🚀 Runs deploy_skill.py --env all
8. 📦 Commits to git: "feat: add n8n-flow-builder skill v1.0.0"
9. 🔗 Pushes to GitHub
10. ✅ Reports: "Deployed to Code CLI and ready for API upload"
```

### Example 2: Update Existing Skill
```
User: "Update linear-orchestration to include new status field format"

Claude (using skill-manager):
1. 📖 Reads linear-orchestration/SKILL.md from git
2. ✏️ Makes changes to include new status field
3. 👀 Shows diff: "Here's what I'm changing..."
4. ✅ User approves
5. 🔍 Validates changes
6. 🚀 Deploys updated version
7. 📦 Git commit: "feat(linear): add new status field format"
8. 🏷️ Bumps version: v1.2.0 → v1.3.0
```

### Example 3: Search and Discover
```
User: "What skills do I have related to GitHub?"

Claude: Searches repository and returns:
- **github-coordinator** (v1.2.0) - Manage branches, PRs, CI/CD
  Last updated: 2025-10-15
  Status: Deployed to Code CLI ✅
  
- **github-actions-builder** (v0.5.0) - Create GH Actions workflows
  Last updated: 2025-10-10
  Status: Local only, not deployed ⚠️
```

## Setup Instructions

### Initial Setup
1. Ensure git repository exists at expected path
2. Initialize git if not already done:
   ```bash
   cd "C:\Users\Kurt Anderson\github projects\claude-skills"
   git init
   git add .
   git commit -m "Initial commit: skill-manager"
   ```

3. Set up Code CLI symlink (run once):
   ```bash
   ln -s "C:\Users\Kurt Anderson\github projects\claude-skills" ~/.claude/skills
   ```

4. Install Python dependencies (if using scripts):
   ```bash
   pip install pyyaml click watchdog
   ```

### Warp Integration
Since Warp terminal owns system-level tasks:
- Run deployment scripts
- Manage git operations (commit, push, pull)
- Set up and maintain symlinks
- Execute file watchers as background services

## Best Practices

### Skill Naming Convention
- Use kebab-case: `n8n-flow-builder`, `linear-orchestration`
- Be descriptive but concise
- Prefix with domain if part of suite: `github-coordinator`, `github-actions-builder`

### Version Numbering (Semantic Versioning)
- **Major (X.0.0)**: Breaking changes to skill interface
- **Minor (0.X.0)**: New features, backward compatible
- **Patch (0.0.X)**: Bug fixes, documentation updates

### Commit Message Format
```
type(scope): brief description

Examples:
feat(linear): add webhook callback format
fix(n8n): correct node connection validation
docs(skill-manager): update deployment instructions
```

### Testing Before Deploy
1. Validate skill structure
2. Test in isolated Claude session
3. Verify all referenced files exist
4. Check script executables work
5. Review security implications

## Troubleshooting

### Common Issues

**Issue**: Skill not loading in Claude Code CLI
**Solution**: Check symlink is correct, restart Claude Code

**Issue**: Validation fails on YAML frontmatter
**Solution**: Check frontmatter has three dashes on separate lines, proper YAML syntax

**Issue**: Script can't be executed
**Solution**: Verify script has execute permissions, check shebang line

**Issue**: Deployment to API fails
**Solution**: Check API key is set, skill size under 8MB limit, max 8 skills per request

## Next Steps

Once skill-manager is working:
1. Create your first domain skill (n8n-flow-builder recommended)
2. Set up automation (file watcher or n8n workflow)
3. Establish review process for new skills
4. Document your skill library in main README
5. Share useful skills with team (if applicable)

## Notes

- This skill is self-referential (meta) - it manages itself too
- Start simple: manual deployment first, automation later
- Skills are portable: work with any LLM that can read files
- Git is your safety net: always commit before major changes
- Desktop Commander can be buggy: GitHub MCP is more reliable for repo operations

## Resources

- [Anthropic Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Skills GitHub Repository](https://github.com/anthropics/skills)
- [Skills Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/skills)
