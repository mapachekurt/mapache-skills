#!/usr/bin/env python3
"""
Scaffold new Mapache Skills from templates.

Usage:
    python create_skill.py --name "my-skill" --description "What it does"
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

SKILL_TEMPLATE = """---
name: {name}
description: {description}
---

# {title}

## Purpose
[Describe what this skill does and when Claude should use it]

## Usage Patterns
[Examples of how users will invoke this skill]

## Key Instructions
[Step-by-step guidance for Claude]

## Examples
[Show concrete examples of this skill in action]

## Notes
- Created: {created_date}
- Author: Kurt Anderson
- Version: 1.0.0
"""

README_TEMPLATE = """# {title}

## Description
{description}

## Installation
This skill is part of the mapache-skills repository.

For Claude Code CLI:
```bash
ln -s "C:\\Users\\Kurt Anderson\\github projects\\mapache-skills" ~/.claude/skills
```

## Usage
See SKILL.md for detailed instructions.

## Version History
- v1.0.0 - Initial release
"""

SKILLMETA_TEMPLATE = """{
  "version": "1.0.0",
  "author": "Kurt Anderson",
  "created": "{created_date}",
  "dependencies": [],
  "tags": []
}
"""


def create_skill(name: str, description: str, base_path: str = None):
    """Create a new skill directory with template files."""
    if base_path is None:
        base_path = Path(__file__).parent.parent
    else:
        base_path = Path(base_path)
    
    # Convert name to kebab-case if needed
    skill_name = name.lower().replace(' ', '-').replace('_', '-')
    skill_dir = base_path / skill_name
    
    # Check if skill already exists
    if skill_dir.exists():
        print(f"❌ Error: Skill '{skill_name}' already exists at {skill_dir}")
        return False
    
    # Create directory structure
    skill_dir.mkdir(parents=True)
    (skill_dir / "scripts").mkdir(exist_ok=True)
    (skill_dir / "resources").mkdir(exist_ok=True)

    (skill_dir / "tests").mkdir(exist_ok=True)
    
    # Generate title (Title Case)
    title = ' '.join(word.capitalize() for word in skill_name.split('-'))
    
    # Get current date
    created_date = datetime.now().strftime('%Y-%m-%d')
    
    # Create SKILL.md
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(SKILL_TEMPLATE.format(
        name=skill_name,
        description=description,
        title=title,
        created_date=created_date
    ))
    
    # Create README.md
    readme = skill_dir / "README.md"
    readme.write_text(README_TEMPLATE.format(
        title=title,
        description=description
    ))
    
    # Create .skillmeta
    skillmeta = skill_dir / ".skillmeta"
    skillmeta.write_text(SKILLMETA_TEMPLATE.format(
        created_date=created_date
    ))
    
    print(f"✅ Successfully created skill: {skill_name}")
    print(f"📁 Location: {skill_dir}")
    print(f"\nNext steps:")
    print(f"1. Edit {skill_dir}/SKILL.md to add your instructions")
    print(f"2. Validate: python scripts/validate_skill.py {skill_name}/")
    print(f"3. Deploy: python scripts/deploy_skill.py {skill_name}/ --env code")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Create a new Mapache Skill from template'
    )
    parser.add_argument(
        '--name',
        required=True,
        help='Name of the skill (will be converted to kebab-case)'
    )
    parser.add_argument(
        '--description',
        required=True,
        help='Brief description of what the skill does'
    )
    parser.add_argument(
        '--path',
        default=None,
        help='Base path for skills repository (default: parent of scripts/)'
    )
    
    args = parser.parse_args()
    
    success = create_skill(args.name, args.description, args.path)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
