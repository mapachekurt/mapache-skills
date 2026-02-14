#!/usr/bin/env python3
"""
Check for updates and documentation changes in the vercel-labs/add-skill repository.
"""

import subprocess
import re
import sys
import json
from pathlib import Path

UPSTREAM_URL = "https://github.com/vercel-labs/add-skill"
NPM_PACKAGE = "add-skill"

def get_current_npm_version():
    try:
        result = subprocess.run(["npx", NPM_PACKAGE, "--version"], capture_output=True, text=True, shell=True)
        return result.stdout.strip()
    except:
        return None

def check_upstream():
    print(f"🔍 Checking upstream for {UPSTREAM_URL} updates...")
    
    # 1. Check NPM version
    current_version = get_current_npm_version()
    print(f"📦 Local/Cached version: {current_version or 'Not found'}")
    
    # In a real script, we might fetch the latest from npm registry API
    # For now, we'll inform the user how to force an update
    print(f"💡 Tip: Run 'npx {NPM_PACKAGE}@latest --version' to force use the latest tool.")

    # 2. Inform about manual tracking
    print(f"\n📢 Manual Tracking Instructions:")
    print(f"   * Repository: {UPSTREAM_URL}")
    print(f"   * Recommendation: 'Watch' the repo for 'Releases' to get notified of new agents or features.")
    print(f"   * Check 'Creating Skills' section in README if your skills stop working.")

if __name__ == "__main__":
    check_upstream()
