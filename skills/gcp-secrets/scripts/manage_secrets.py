import os
import sys
import json
import argparse
import subprocess
from typing import List, Optional, Dict, Any

def find_gcloud() -> str:
    """Locates the gcloud executable on Windows."""
    common_paths = [
        os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"),
        os.path.join(os.environ.get("ProgramFiles(x86)", ""), r"Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"),
        "gcloud.cmd",
        "gcloud"
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path
    return "gcloud"

GCLOUD_PATH = find_gcloud()

def run_command(command: List[str]) -> subprocess.CompletedProcess:
    """Runs a shell command and returns the result."""
    # Replace the command with the absolute path
    if command[0] == "gcloud":
        command[0] = GCLOUD_PATH
        
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            shell=True if os.name == 'nt' else False
        )
        return result
    except Exception as e:
        print(f"❌ Execution error: {e}")
        sys.exit(1)

def get_secret(name: str, version: str = "latest") -> Optional[str]:
    """Retrieves a secret value from GSM."""
    cmd = ["gcloud", "secrets", "versions", "access", version, f"--secret={name}"]
    result = run_command(cmd)
    
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        print(f"❌ Error retrieving secret '{name}': {result.stderr.strip()}")
        return None

def set_secret(name: str, value: str):
    """Creates or updates a secret in GSM."""
    # Check if secret exists
    check_cmd = ["gcloud", "secrets", "describe", name]
    check_result = run_command(check_cmd)
    
    if check_result.returncode != 0:
        print(f"🏗️ Creating secret '{name}'...")
        create_cmd = ["gcloud", "secrets", "create", name, "--replication-policy=automatic"]
        create_result = run_command(create_cmd)
        if create_result.returncode != 0:
            print(f"❌ Failed to create secret: {create_result.stderr.strip()}")
            return

    # Add new version
    print(f"🔐 Adding new version to secret '{name}'...")
    add_cmd = ["gcloud", "secrets", "versions", "add", name, f"--data-file=-"]
    
    try:
        process = subprocess.Popen(
            add_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=value)
        
        if process.returncode == 0:
            print(f"✅ Secret '{name}' updated successfully.")
        else:
            print(f"❌ Failed to update secret: {stderr.strip()}")
    except Exception as e:
        print(f"❌ Process error: {e}")

def list_secrets() -> List[str]:
    """Lists names of all secrets in the project."""
    cmd = ["gcloud", "secrets", "list", "--format=json(name)"]
    result = run_command(cmd)
    
    if result.returncode == 0:
        try:
            secrets_data = json.loads(result.stdout)
            # Secret names look like projects/PROJECT_ID/secrets/NAME
            return [s['name'].split('/')[-1] for s in secrets_data]
        except Exception as e:
            print(f"❌ JSON parse error: {e}")
            return []
    else:
        print(f"❌ Error listing secrets: {result.stderr.strip()}")
        return []

def main():
    parser = argparse.ArgumentParser(description="GCP Secret Manager CLI for Antigravity")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Get command
    get_parser = subparsers.add_parser("get", help="Retrieve a secret")
    get_parser.add_argument("--name", required=True, help="Secret name")
    get_parser.add_argument("--version", default="latest", help="Secret version (default: latest)")

    # Set command
    set_parser = subparsers.add_parser("set", help="Store a secret")
    set_parser.add_argument("--name", required=True, help="Secret name")
    set_parser.add_argument("--value", help="Secret value (if omitted, will prompt)")

    # List command
    subparsers.add_parser("list", help="List all secrets")

    args = parser.parse_args()

    if args.command == "get":
        value = get_secret(args.name, args.version)
        if value:
            # We print the value only if explicitly requested. 
            # In a real tool, it might be better to write to a file or stdout.
            print(value)
    
    elif args.command == "set":
        value = args.value
        if not value:
            import getpass
            value = getpass.getpass(f"Enter value for secret '{args.name}': ")
        set_secret(args.name, value)
    
    elif args.command == "list":
        secrets = list_secrets()
        if secrets:
            print("\n".join(secrets))
        else:
            print("No secrets found or error occurred.")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
