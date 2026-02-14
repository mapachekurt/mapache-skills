#!/usr/bin/env python3
"""
Automatically bump version in .skillmeta and SKILL.md.
"""

import sys
import json
import re
import argparse
from pathlib import Path

def bump_version(current: str, type: str):
    major, minor, patch = map(int, current.split('.'))
    if type == 'major':
        return f"{major + 1}.0.0"
    elif type == 'minor':
        return f"{major}.{minor + 1}.0"
    else:
        return f"{major}.{minor}.{patch + 1}"

def update_skill(skill_dir: Path, bump_type: str):
    skillmeta_path = skill_dir / ".skillmeta"
    skill_md_path = skill_dir / "SKILL.md"
    
    if not skillmeta_path.exists():
        print(f"❌ Error: .skillmeta not found in {skill_dir}")
        return False
        
    # Update .skillmeta
    with open(skillmeta_path, 'r') as f:
        meta = json.load(f)
    
    old_version = meta.get('version', '1.0.0')
    new_version = bump_version(old_version, bump_type)
    meta['version'] = new_version
    
    with open(skillmeta_path, 'w') as f:
        json.dump(meta, f, indent=2)
        
    # Update SKILL.md if version is present there
    if skill_md_path.exists():
        content = skill_md_path.read_text(encoding='utf-8')
        # Look for - Version: X.Y.Z
        new_content = re.sub(r'(- Version:\s*)\d+\.\d+\.\d+', rf'\g<1>{new_version}', content)
        if new_content != content:
            skill_md_path.write_text(new_content, encoding='utf-8')
            
    print(f"✅ Bumped {skill_dir.name}: {old_version} -> {new_version}")
    return True

def main():
    parser = argparse.ArgumentParser(description='Bump skill version')
    parser.add_argument('skill_name', help='Name of the skill directory')
    parser.add_argument('--bump', choices=['patch', 'minor', 'major'], default='patch')
    
    args = parser.parse_args()
    repo_root = Path(__file__).parent.parent
    skill_dir = repo_root / "skills" / args.skill_name
    
    if not skill_dir.exists():
        print(f"❌ Error: Skill directory not found: {skill_dir}")
        sys.exit(1)
        
    update_skill(skill_dir, args.bump)

if __name__ == "__main__":
    main()
