"""
ADK Agent Validator

Validates Google ADK agents for:
- ADK pattern compliance
- A2A protocol compliance
- Project structure correctness
- Code quality checks
- Deployment readiness

Usage:
    python validate_agent.py --dir path/to/agent
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Any
import re


class ValidationResult:
    """Stores validation results"""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.passed: List[str] = []
    
    def add_error(self, message: str):
        """Add an error"""
        self.errors.append(f"❌ ERROR: {message}")
    
    def add_warning(self, message: str):
        """Add a warning"""
        self.warnings.append(f"⚠️  WARNING: {message}")
    
    def add_pass(self, message: str):
        """Add a passed check"""
        self.passed.append(f"✅ PASS: {message}")
    
    def is_valid(self) -> bool:
        """Check if validation passed (no errors)"""
        return len(self.errors) == 0
    
    def print_report(self):
        """Print validation report"""
        print("\n" + "="*60)
        print("ADK AGENT VALIDATION REPORT")
        print("="*60)
        
        if self.passed:
            print("\n✅ PASSED CHECKS:")
            for check in self.passed:
                print(f"  {check}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if self.errors:
            print("\n❌ ERRORS:")
            for error in self.errors:
                print(f"  {error}")
        
        print("\n" + "="*60)
        if self.is_valid():
            print("✨ VALIDATION PASSED - Agent is compliant!")
        else:
            print(f"❌ VALIDATION FAILED - {len(self.errors)} error(s) found")
        print("="*60 + "\n")


class ADKAgentValidator:
    """Validates ADK agent compliance"""
    
    REQUIRED_FILES = [
        "agent.py",
        "agent.json",
        "requirements.txt"
    ]
    
    RECOMMENDED_FILES = [
        "config.py",
        "adk.yaml",
        "README.md",
        ".env.example",
        "tests/test_agent.py"
    ]
    
    def __init__(self, agent_dir: Path):
        self.agent_dir = Path(agent_dir)
        self.result = ValidationResult()
    
    def validate(self) -> ValidationResult:
        """Run all validations"""
        print(f"\n🔍 Validating ADK agent at: {self.agent_dir}")
        
        # Check directory exists
        if not self.agent_dir.exists():
            self.result.add_error(f"Agent directory not found: {self.agent_dir}")
            return self.result
        
        # Run validation checks
        self.validate_file_structure()
        self.validate_agent_py()
        self.validate_agent_json()
        self.validate_requirements()
        self.validate_tools()
        self.validate_tests()
        
        return self.result
    
    def validate_file_structure(self):
        """Validate project file structure"""
        print("\n📁 Checking file structure...")
        
        # Check required files
        for filename in self.REQUIRED_FILES:
            filepath = self.agent_dir / filename
            if filepath.exists():
                self.result.add_pass(f"Required file present: {filename}")
            else:
                self.result.add_error(f"Missing required file: {filename}")
        
        # Check recommended files
        for filename in self.RECOMMENDED_FILES:
            filepath = self.agent_dir / filename
            if filepath.exists():
                self.result.add_pass(f"Recommended file present: {filename}")
            else:
                self.result.add_warning(f"Missing recommended file: {filename}")
    
    def validate_agent_py(self):
        """Validate main agent.py file"""
        print("\n🐍 Checking agent.py...")
        
        agent_file = self.agent_dir / "agent.py"
        if not agent_file.exists():
            return  # Already reported as error
        
        content = agent_file.read_text()
        
        # Check imports
        required_imports = [
            (r"from adk import Agent", "Must import Agent from adk"),
            (r"from adk\.models import", "Must import model from adk.models"),
        ]
        
        for pattern, message in required_imports:
            if re.search(pattern, content):
                self.result.add_pass(f"Import check: {message}")
            else:
                self.result.add_error(message)
        
        # Check class definition
        if re.search(r"class \w+Agent\(Agent\):", content):
            self.result.add_pass("Agent class inherits from adk.Agent")
        elif re.search(r"class \w+\(Agent\):", content):
            self.result.add_pass("Agent class inherits from adk.Agent")
        else:
            self.result.add_error("Agent class must inherit from adk.Agent")
        
        # Check @on_message decorator
        if "@on_message" in content:
            self.result.add_pass("Using @on_message decorator")
        else:
            self.result.add_warning("No @on_message decorator found")
        
        # Check for ctx parameter
        if re.search(r"def \w+\([^)]*ctx[^)]*\):", content):
            self.result.add_pass("Message handlers use ctx parameter")
        else:
            self.result.add_warning("Message handlers should use ctx parameter")
        
        # Anti-patterns: Check for stateful instance variables
        if re.search(r"self\.\w+\s*=\s*\[\]", content) or re.search(r"self\.\w+\s*=\s*\{\}", content):
            self.result.add_warning(
                "Potential stateful instance variable detected. "
                "Use ctx.session for state management instead."
            )
        
        # Check for hardcoded secrets
        secret_patterns = [
            (r'["\']sk-[a-zA-Z0-9]{20,}["\']', "Potential OpenAI API key"),
            (r'["\']sk-ant-[a-zA-Z0-9]{20,}["\']', "Potential Anthropic API key"),
            (r'api_key\s*=\s*["\'][^"\']+["\']', "Potential hardcoded API key"),
        ]
        
        for pattern, message in secret_patterns:
            if re.search(pattern, content):
                self.result.add_error(f"SECURITY: {message} appears to be hardcoded")
    
    def validate_agent_json(self):
        """Validate A2A agent.json file"""
        print("\n📋 Checking agent.json (A2A compliance)...")
        
        json_file = self.agent_dir / "agent.json"
        if not json_file.exists():
            return  # Already reported as error
        
        try:
            data = json.loads(json_file.read_text())
        except json.JSONDecodeError as e:
            self.result.add_error(f"Invalid JSON in agent.json: {e}")
            return
        
        # Check required A2A fields
        required_fields = {
            "id": str,
            "version": str,
            "name": str,
            "description": str,
            "capabilities": list,
            "endpoints": dict
        }
        
        for field, expected_type in required_fields.items():
            if field in data:
                if isinstance(data[field], expected_type):
                    self.result.add_pass(f"A2A field '{field}' present and correct type")
                else:
                    self.result.add_error(
                        f"A2A field '{field}' has wrong type "
                        f"(expected {expected_type.__name__}, got {type(data[field]).__name__})"
                    )
            else:
                self.result.add_error(f"Missing required A2A field: {field}")
        
        # Check endpoints structure
        if "endpoints" in data and isinstance(data["endpoints"], dict):
            required_endpoints = ["main", "discovery"]
            for endpoint in required_endpoints:
                if endpoint in data["endpoints"]:
                    self.result.add_pass(f"A2A endpoint '{endpoint}' defined")
                else:
                    self.result.add_error(f"Missing required A2A endpoint: {endpoint}")
        
        # Check version format (semver)
        if "version" in data:
            if re.match(r"^\d+\.\d+\.\d+", data["version"]):
                self.result.add_pass("Version follows semantic versioning")
            else:
                self.result.add_warning("Version should follow semantic versioning (X.Y.Z)")
    
    def validate_requirements(self):
        """Validate requirements.txt"""
        print("\n📦 Checking requirements.txt...")
        
        req_file = self.agent_dir / "requirements.txt"
        if not req_file.exists():
            return
        
        content = req_file.read_text()
        
        # Check for google-adk
        if re.search(r"google-adk", content):
            # Check version constraint
            if re.search(r"google-adk>=2\.", content):
                self.result.add_pass("google-adk with version constraint present")
            elif re.search(r"google-adk==", content):
                self.result.add_warning("Consider using >= instead of == for google-adk version")
            else:
                self.result.add_warning("google-adk should specify minimum version (>=2.1.0)")
        else:
            self.result.add_error("requirements.txt must include google-adk")
        
        # Check for common dependencies
        recommended_deps = [
            ("google-cloud-aiplatform", "Vertex AI integration"),
            ("google-cloud-secretmanager", "Secret management"),
        ]
        
        for dep, purpose in recommended_deps:
            if dep in content:
                self.result.add_pass(f"Recommended dependency present: {dep} ({purpose})")
            else:
                self.result.add_warning(f"Consider adding {dep} for {purpose}")
    
    def validate_tools(self):
        """Validate tool definitions"""
        print("\n🔧 Checking tools...")
        
        tools_dir = self.agent_dir / "tools"
        if not tools_dir.exists():
            self.result.add_warning("No tools/ directory found")
            return
        
        # Find Python files in tools/
        tool_files = list(tools_dir.glob("*.py"))
        tool_files = [f for f in tool_files if f.name != "__init__.py"]
        
        if not tool_files:
            self.result.add_warning("No tool files found in tools/ directory")
            return
        
        for tool_file in tool_files:
            content = tool_file.read_text()
            
            # Check for @tool decorator
            if "@tool" in content:
                self.result.add_pass(f"Tool file uses @tool decorator: {tool_file.name}")
            else:
                self.result.add_warning(f"Tool file should use @tool decorator: {tool_file.name}")
            
            # Check for type hints
            if re.search(r"def \w+\([^)]*:\s*\w+", content):
                self.result.add_pass(f"Tool file uses type hints: {tool_file.name}")
            else:
                self.result.add_warning(f"Tool functions should use type hints: {tool_file.name}")
    
    def validate_tests(self):
        """Validate test suite"""
        print("\n🧪 Checking tests...")
        
        tests_dir = self.agent_dir / "tests"
        if not tests_dir.exists():
            self.result.add_warning("No tests/ directory found")
            return
        
        test_files = list(tests_dir.glob("test_*.py"))
        
        if not test_files:
            self.result.add_warning("No test files found (should have test_*.py)")
            return
        
        self.result.add_pass(f"Found {len(test_files)} test file(s)")
        
        # Check test imports
        for test_file in test_files:
            content = test_file.read_text()
            
            if "import pytest" in content:
                self.result.add_pass(f"Test file uses pytest: {test_file.name}")
            else:
                self.result.add_warning(f"Test file should use pytest: {test_file.name}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate ADK agent compliance"
    )
    parser.add_argument(
        "--dir",
        required=True,
        help="Path to agent directory"
    )
    
    args = parser.parse_args()
    
    validator = ADKAgentValidator(agent_dir=args.dir)
    result = validator.validate()
    
    result.print_report()
    
    # Return appropriate exit code
    sys.exit(0 if result.is_valid() else 1)


if __name__ == "__main__":
    main()
