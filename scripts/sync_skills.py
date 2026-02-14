#!/usr/bin/env python3
"""
Sync local Mapache Skills to all detected coding agents globally.
Respects 'nosync: true' in SKILL.md YAML frontmatter.
"""

import os
import sys
import subprocess
import yaml
import re
from pathlib import Path

def get_nosync_skills(skills_dir: Path):
    """Scan skills for 'nosync: true' in frontmatter."""
    nosync_skills = []
    
    for skill_path in skills_dir.iterdir():
        if not skill_path.is_dir():
            continue
            
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            continue
            
        try:
            content = skill_md.read_text(encoding='utf-8')
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    if frontmatter and frontmatter.get('nosync') is True:
                        nosync_skills.append(skill_path.name)
        except Exception as e:
            print(f"⚠️ Warning: Could not parse frontmatter for {skill_path.name}: {e}")
            
    return nosync_skills

def sync_skills():
    repo_root = Path(__file__).parent.parent
    skills_dir = repo_root / "skills"
    
    print("🔄 Starting Mapache Skill Sync...")
    
    nosync = get_nosync_skills(skills_dir)
    if nosync:
        print(f"⏭️ Skipping exempted skills: {', '.join(nosync)}")
    
    # Base command
    cmd = ["npx", "-y", "add-skill", ".", "-g", "-y"]
    
    # If we have specific skills to sync (excluding nosync ones)
    all_skills = [p.name for p in skills_dir.iterdir() if p.is_dir() and (p / "SKILL.md").exists()]
    to_sync = [s for s in all_skills if s not in nosync]
    
    if not to_sync:
        print("ℹ️ No syncable skills found.")
        return
        
    for skill in to_sync:
        print(f"📦 Syncing {skill}...")
        subprocess.run(["npx", "-y", "add-skill", ".", "-g", "-y", "-s", skill], cwd=repo_root, shell=True)

    print("\n✅ Sync complete!")

if __name__ == "__main__":
    sync_skills()
