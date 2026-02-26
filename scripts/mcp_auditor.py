import json
import os
import sys

# Path to the mcp_config.json
MCP_CONFIG_PATH = r"C:\Users\Kurt Anderson\.gemini\antigravity\mcp_config.json"

def audit_mcp_servers():
    if not os.path.exists(MCP_CONFIG_PATH):
        print(f"Error: {MCP_CONFIG_PATH} not found.")
        return

    with open(MCP_CONFIG_PATH, 'r') as f:
        config = json.load(f)

    servers = config.get("mcpServers", {})
    independent_servers = [name for name in servers if name not in ["rube", "pencil", "beads"]] # Pencil/Beads are internal/special

    print(f"Found {len(independent_servers)} independent MCP servers: {', '.join(independent_servers)}")
    
    # In a real scenario, this would call the Rube search tools.
    # For now, we output the list of targets for Antigravity to process.
    return independent_servers

if __name__ == "__main__":
    audit_mcp_servers()
