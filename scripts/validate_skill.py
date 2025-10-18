#!/usr/bin/env python3
"""
Validate Claude Skill structure, YAML frontmatter, and security.

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
        print(f"🔍 Validating skill: {self.skill_path.name}")
        print()
        
        # Check directory exists
        if not self.skill_path.exists():
            self.errors.append(f"Skill directory not found: {self.skill_path}")
            return self.report()
        
        # Run validation checks
        self.check_skill_md_exists()
        self.check_yaml_frontmatter()
        self.check_markdown_structure()
        self.check_scripts()
        self.check_security()
        
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
        
        # Check for frontmatter delimiters
        if not content.startswith('---\n'):
            self.errors.append("SKILL.md must start with YAML frontmatter (---)")
            return
        
        # Extract frontmatter
        parts = content.split('---\n', 2)
        if len(parts) < 3:
            self.errors.append("YAML frontmatter not properly closed with ---")
            return
        
        frontmatter = parts[1]
        
        # Check required fields
        if 'name:' not in frontmatter:
            self.errors.append("YAML frontmatter missing 'name' field")
        if 'description:' not in frontmatter:
            self.errors.append("YAML frontmatter missing 'description' field")
        
        # Check name format (should be kebab-case)
        name_match = re.search(r'name:\s*(.+)', frontmatter)
        if name_match:
            name = name_match.group(1).strip()
            if not re.match(r'^[a-z0-9-]+$', name):
                self.warnings.append(
                    f"Skill name '{name}' should be kebab-case (lowercase, hyphens)"
                )

                if not first_line.startswith('#!'):
                    self.warnings.append(
                        f"Script {script.name} missing shebang line"
                    )
    
    def check_security(self):
        """Basic security checks for scripts."""
        scripts_dir = self.skill_path / "scripts"
        if not scripts_dir.exists():
            return
        
        script_files = list(scripts_dir.glob('*.py')) + list(scripts_dir.glob('*.js'))
        
        # Suspicious patterns to flag
        suspicious_patterns = [
            (r'requests\.get\(["\']http[s]?://(?!.*(?:github\.com|anthropic\.com))', 
             'Untrusted network call'),
            (r'subprocess\.call.*\bsudo\b', 'Sudo command detected'),
            (r'os\.system.*\brm\s+-rf\b', 'Dangerous file deletion'),
            (r'eval\(', 'Use of eval() detected'),
            (r'exec\(', 'Use of exec() detected'),
        ]
        
        for script in script_files:
            content = script.read_text(encoding='utf-8')
            for pattern, message in suspicious_patterns:
                if re.search(pattern, content):
                    self.warnings.append(
                        f"Security: {script.name} - {message}"
                    )
    
    def report(self):
        """Print validation report and return success status."""
        print("=" * 60)
        
        if self.errors:
            print("❌ ERRORS:")
            for error in self.errors:
                print(f"   • {error}")
            print()
        
        if self.warnings:
            print("⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"   • {warning}")
            print()

        if not self.errors and not self.warnings:
            print("✅ Skill validation passed!")
            print()
        elif not self.errors:
            print("✅ Skill validation passed (with warnings)")
            print()
        else:
            print("❌ Skill validation failed")
            print()
        
        print("=" * 60)
        return len(self.errors) == 0


def main():
    parser = argparse.ArgumentParser(
        description='Validate Claude Skill structure and security'
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
