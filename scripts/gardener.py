#!/usr/bin/env python3
"""
Gardener: The Evergreen Skill Engine (Lightweight Edition).
Scans skills for 'sources', handles discovery via Exa AI snippets.
"""

import os
import sys
import yaml
import json
import subprocess
from pathlib import Path
from datetime import datetime

class Gardener:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.skills_dir = root_dir / "skills"
        self.manifest_name = "manifest.json"
        self.sync_script = root_dir / "scripts" / "knowledge_sync.py"

    def scan_skills(self):
        print(f"🌱 Gardening in {self.skills_dir}...")
        for skill_path in self.skills_dir.iterdir():
            if not skill_path.is_dir():
                continue
            
            skill_md = skill_path / "SKILL.md"
            if not skill_md.exists():
                continue
            
            self.process_skill(skill_path, skill_md)

    def process_skill(self, skill_path: Path, skill_md: Path):
        content = skill_md.read_text(encoding='utf-8')
        if not content.startswith('---'):
            return

        try:
            parts = content.split('---', 2)
            if len(parts) < 3:
                return
            
            frontmatter = yaml.safe_load(parts[1])
            sources = frontmatter.get('sources', [])
            
            if not sources:
                return

            print(f"🌻 Found {len(sources)} sources for '{skill_path.name}'")
            self.sync_sources(skill_path, sources)
            
        except Exception as e:
            print(f"❌ Error processing {skill_path.name}: {e}")

    def sync_sources(self, skill_path: Path, sources: list):
        resources_dir = skill_path / "resources"
        resources_dir.mkdir(exist_ok=True)
        
        manifest_path = resources_dir / self.manifest_name
        manifest = self.load_manifest(manifest_path)
        
        for source in sources:
            name = source.get('name')
            url = source.get('url')
            
            print(f"  🔄 Syncing {name}...")
            
            # Use Knowledge Sync script
            try:
                # Simulated discovery content - in a real recipe, this would come from Exa
                discovery_content = f"Latest GROUNDED knowledge from {url} regarding {name} standards."
                
                subprocess.run([
                    sys.executable, str(self.sync_script), 
                    "--name", name, 
                    "--url", url, 
                    "--content", discovery_content
                ], check=True)
                
                manifest['sources'][name] = {
                    "url": url,
                    "last_sync": datetime.now().isoformat(),
                    "status": "synced"
                }
            except Exception as e:
                print(f"  ⚠️ Sync failed for {name}: {e}")

        self.save_manifest(manifest_path, manifest)

    def load_manifest(self, path: Path):
        if path.exists():
            return json.loads(path.read_text())
        return {"sources": {}, "last_full_scan": None, "engine": "lightweight"}

    def save_manifest(self, path: Path, manifest: dict):
        manifest['last_full_scan'] = datetime.now().isoformat()
        path.write_text(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    repo_root = Path(__file__).parent.parent
    gardener = Gardener(repo_root)
    gardener.scan_skills()
