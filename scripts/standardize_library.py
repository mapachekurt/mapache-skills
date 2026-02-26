#!/usr/bin/env python3
"""
Standardize the Mapache Skill library.
Enforces YAML frontmatter and standard directory structures.
"""

import os
import re
from pathlib import Path

def standardize_skill(skill_dir: Path):
    """Standardize a single skill directory."""
    print(f"Standardizing: {skill_dir.name}")
    
    # 1. Ensure SKILL.md exists
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"  ⚠️  SKILL.md missing in {skill_dir.name}, skipping.")
        return

    # 2. Check/Add YAML Frontmatter
    content = skill_md.read_text(encoding='utf-8')
    if not content.startswith('---'):
        print(f"  ➕ Adding missing YAML frontmatter to {skill_dir.name}")
        name = skill_dir.name
        description = f"Specialized skill for {name.replace('-', ' ')}."
        header = f"---\nname: {name}\ndescription: {description}\nlicense: MIT\n---\n\n"
        skill_md.write_text(header + content, encoding='utf-8')
    else:
        # Check if description or name is missing in existing frontmatter
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            if 'name:' not in frontmatter:
                 print(f"  🩹 Fixing missing 'name' in frontmatter for {skill_dir.name}")
                 new_content = content.replace('---\n', f"---\nname: {skill_dir.name}\n", 1)
                 skill_md.write_text(new_content, encoding='utf-8')

    # 3. Ensure standard directories exist
    for sub in ["scripts", "resources", "references", "assets", "examples", "tests"]:
        (skill_dir / sub).mkdir(exist_ok=True)
        # Add a .gitkeep to ensure empty dirs are tracked if needed, 
        # though usually we only want them if they have content.
        # But for standardization, let's just make them.

    # 4. Proactive: Move README.md to references if it looks like external docs
    # (Optional: Only if user wants, but for now let's just ensure folders are there)

def main():
    repo_root = Path(__file__).parent.parent
    skills_dir = repo_root / "skills"
    
    if not skills_dir.exists():
        print(f"❌ Skills directory not found at {skills_dir}")
        return

    for item in skills_dir.iterdir():
        if item.is_dir():
            standardize_skill(item)

    print("\n✅ Library standardization complete!")

if __name__ == "__main__":
    main()
