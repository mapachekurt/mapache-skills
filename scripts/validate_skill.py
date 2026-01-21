#!/usr/bin/env python3
"""
Validate Mapache Skill structure, YAML frontmatter, and security.

Usage:
    python validate_skill.py skill-name/
"""

import argparse
import sys
from pathlib import Path
import re


class SkillValidator:
    def __init__(self, skill_path: Path):
        self.skill_path = skill_path
        self.errors = []
        self.warnings = []
        
    def validate(self):
        """Run all validation checks."""
        print(f"Validating skill: {self.skill_path.name}")
        print()
        
        if not self.skill_path.exists():
            self.errors.append(f"Skill directory not found: {self.skill_path}")
            return self.report()
        
        self.check_skill_md_exists()
        self.check_yaml_frontmatter()
        
        return self.report()
    
    def check_skill_md_exists(self):
        """Check that SKILL.md file exists."""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            self.errors.append("SKILL.md file is missing")
            return False
        return True
    
    def check_yaml_frontmatter(self):
        """Validate YAML frontmatter structure."""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            return

        
        content = skill_md.read_text(encoding='utf-8')
        
        if not content.startswith('---\n'):
            self.errors.append("SKILL.md must start with YAML frontmatter (---)")
            return
        
        parts = content.split('---\n', 2)
        if len(parts) < 3:
            self.errors.append("YAML frontmatter not properly closed with ---")
            return
        
        frontmatter = parts[1]
        
        if 'name:' not in frontmatter:
            self.errors.append("YAML frontmatter missing 'name' field")
        if 'description:' not in frontmatter:
            self.errors.append("YAML frontmatter missing 'description' field")
        
        name_match = re.search(r'name:\s*(.+)', frontmatter)
        if name_match:
            name = name_match.group(1).strip()
            if not re.match(r'^[a-z0-9-]+$', name):
                self.warnings.append(
                    f"Skill name '{name}' should be kebab-case"
                )
    
    def report(self):
        """Print validation report and return success status."""
        print("=" * 60)
        
        if self.errors:
            print("ERRORS:")
            for error in self.errors:
                print(f"   * {error}")
            print()
        
        if self.warnings:
            print("WARNINGS:")
            for warning in self.warnings:
                print(f"   * {warning}")
            print()

        
        if not self.errors and not self.warnings:
            print("SUCCESS: Skill validation passed!")
            print()
        elif not self.errors:
            print("SUCCESS: Skill validation passed (with warnings)")
            print()
        else:
            print("FAILED: Skill validation failed")
            print()
        
        print("=" * 60)
        return len(self.errors) == 0


def main():
    parser = argparse.ArgumentParser(
        description='Validate Mapache Skill structure and security'
    )
    parser.add_argument(
        'skill_path',
        help='Path to skill directory'
    )
    
    args = parser.parse_args()
    skill_path = Path(args.skill_path)
    
    validator = SkillValidator(skill_path)
    success = validator.validate()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
