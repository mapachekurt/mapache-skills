#!/usr/bin/env python3
"""
Deploy Mapache Skills to target environments.

Usage:
    python deploy_skill.py skill-name/ --env code
    python deploy_skill.py skill-name/ --env all
"""

import argparse
import sys
import shutil
import subprocess
from pathlib import Path


class SkillDeployer:
    def __init__(self, skill_path: Path, repo_root: Path = None):
        self.skill_path = skill_path
        self.skill_name = skill_path.name
        
        if repo_root is None:
            # Assume repo root is parent of scripts/
            self.repo_root = Path(__file__).parent.parent
        else:
            self.repo_root = repo_root
    
    def deploy_to_code_cli(self):
        """Deploy skill to Claude Code CLI (~/.claude/skills/)."""
        print(f"Deploying {self.skill_name} to Claude Code CLI...")
        
        # Target directory for Claude Code
        home = Path.home()
        claude_skills_dir = home / ".claude" / "skills"
        
        # Create .claude/skills directory if it doesn't exist
        claude_skills_dir.mkdir(parents=True, exist_ok=True)
        
        target = claude_skills_dir / self.skill_name
        
        # Check if already exists
        if target.exists():
            print(f"   Warning: Skill already exists at {target}")
            print(f"   Removing old version...")
            if target.is_symlink():
                target.unlink()
            else:
                shutil.rmtree(target)
        
        # Try to create symlink first (preferred)
        try:
            target.symlink_to(self.skill_path.resolve())
            print(f"   Created symlink: {target} -> {self.skill_path}")
            print(f"   Successfully deployed to Code CLI")
            return True
        except OSError as e:
            # If symlink fails (Windows permissions), copy instead
            print(f"   Symlink failed ({e}), copying files instead...")
            shutil.copytree(self.skill_path, target)
            print(f"   Copied to: {target}")
            print(f"   Successfully deployed to Code CLI")
            return True
    
    def deploy_to_api(self):
        """Deploy skill to Claude API via /v1/skills endpoint."""
        print(f"Deploying {self.skill_name} to Claude API...")
        print(f"   API deployment not yet implemented")
        print(f"   Manual upload required via Claude Console")
        print(f"   Visit: https://console.anthropic.com")
        return False
    
    def deploy(self, environments):
        """Deploy to specified environments."""
        results = {}
        
        if 'code' in environments or 'all' in environments:
            results['code'] = self.deploy_to_code_cli()
        
        if 'api' in environments or 'all' in environments:
            results['api'] = self.deploy_to_api()

        
        return all(results.values()) if results else False


def main():
    parser = argparse.ArgumentParser(
        description='Deploy Mapache Skill to target environments'
    )
    parser.add_argument(
        'skill_path',
        help='Path to skill directory'
    )
    parser.add_argument(
        '--env',
        choices=['code', 'api', 'all'],
        default='code',
        help='Target environment (default: code)'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        default=True,
        help='Validate skill before deploying (default: true)'
    )
    
    args = parser.parse_args()
    skill_path = Path(args.skill_path)
    
    if not skill_path.exists():
        print(f"Error: Skill directory not found: {skill_path}")
        sys.exit(1)
    
    # Validate first if requested
    if args.validate:
        print("Running validation first...\n")
        result = subprocess.run(
            [sys.executable, Path(__file__).parent / "validate_skill.py", str(skill_path)],
            capture_output=False
        )
        if result.returncode != 0:
            print("\nValidation failed. Fix errors before deploying.")
            sys.exit(1)
        print()

    
    # Deploy
    deployer = SkillDeployer(skill_path)
    environments = [args.env]
    
    print("=" * 60)
    success = deployer.deploy(environments)
    print("=" * 60)
    
    if success:
        print("\nDeployment complete!")
    else:
        print("\nDeployment completed with warnings")
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
