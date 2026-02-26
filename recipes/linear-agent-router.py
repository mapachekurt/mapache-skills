"""
Linear Agent Router - Composio Recipe

This recipe polls Linear for issues labeled 'agent-ready' and routes them to either
Jules (autonomous) or Antigravity (interactive) based on task complexity.

Dependencies:
- Composio LINEAR toolkit (active connection required)
- Linear custom fields: Agent Assigned, Agent Status
- Linear labels: agent-ready, jules-assigned, antigravity-assigned

Usage:
    composio-recipe execute linear-agent-router --params '{"workspace_id": "MAPAI"}'
"""

import os
import json
from typing import Dict, List, Any


def analyze_task_complexity(title: str, description: str) -> str:
    """
    Analyze issue to determine if it should go to Jules or Antigravity.
    
    Args:
        title: Issue title
        description: Issue description/body
        
    Returns:
        "Jules" or "Antigravity"
    """
    # Jules-appropriate indicators (autonomous, self-contained)
    jules_keywords = [
        "fix bug", "add test", "update dependency", "refactor function",
        "documentation", "typo", "lint", "format", "clean up"
    ]
    
    # Antigravity-appropriate indicators (needs planning, user decisions)
    antigravity_keywords = [
        "design", "architecture", "plan", "proposal", "review",
        "multi-file", "breaking change", "migration", "integration"
    ]
    
    content = f"{title} {description}".lower()
    
    # Check for complexity indicators
    jules_score = sum(1 for kw in jules_keywords if kw in content)
    antigravity_score = sum(1 for kw in antigravity_keywords if kw in content)
    
    # Multi-file or cross-module work → Antigravity
    if "across" in content or "multiple files" in content:
        return "Antigravity"
    
    # Clear acceptance criteria and bounded scope → Jules
    if "acceptance criteria" in content and jules_score > 0:
        return "Jules"
    
    # Default: if uncertain, route to Antigravity for safety
    if antigravity_score >= jules_score:
        return "Antigravity"
    
    return "Jules"


def main():
    """
    Main recipe execution logic.
    
    Environment Variables (set via Composio):
        LINEAR_WORKSPACE_ID: Linear workspace/team ID or key
        POLLING_INTERVAL_MINUTES: How often to check (default: 5)
    """
    workspace_id = os.environ.get("LINEAR_WORKSPACE_ID", "MAPAI")
    
    print(f"[LINEAR AGENT ROUTER] Polling workspace: {workspace_id}")
    
    # Step 1: Fetch issues with 'agent-ready' label
    # NOTE: This uses the Composio helper run_composio_tool which is injected
    # into the recipe execution environment
    result, error = run_composio_tool("LINEAR_LIST_LINEAR_ISSUES", {
        "first": 50,
        "filter": {
            "labels": {"name": {"eq": "agent-ready"}}
        }
    })
    
    if error:
        print(f"[ERROR] Failed to fetch Linear issues: {error}")
        return {"status": "error", "message": error}
    
    issues = result.get("data", {}).get("issues", {}).get("nodes", [])
    print(f"[INFO] Found {len(issues)} issues with 'agent-ready' label")
    
    routed_count = {"Jules": 0, "Antigravity": 0}
    
    # Step 2: Analyze and route each issue
    for issue in issues:
        issue_id = issue["id"]
        title = issue.get("title", "")
        description = issue.get("description", "")
        
        # Determine agent
        assigned_agent = analyze_task_complexity(title, description)
        routed_count[assigned_agent] += 1
        
        print(f"[ROUTING] {issue_id}: {title[:50]}... → {assigned_agent}")
        
        # Step 3: Update issue labels
        label_to_add = "jules-assigned" if assigned_agent == "Jules" else "antigravity-assigned"
        
        # Add new label
        add_result, add_error = run_composio_tool("LINEAR_ADD_LABEL_TO_ISSUE", {
            "issue_id": issue_id,
            "label_name": label_to_add
        })
        
        if add_error:
            print(f"[WARNING] Failed to add label to {issue_id}: {add_error}")
            continue
        
        # Remove 'agent-ready' label
        remove_result, remove_error = run_composio_tool("LINEAR_REMOVE_LABEL_FROM_ISSUE", {
            "issue_id": issue_id,
            "label_name": "agent-ready"
        })
        
        # Step 4: Add agent assignment label
        agent_label = f"agent:{assigned_agent.lower()}"
        agent_result, agent_error = run_composio_tool("LINEAR_ADD_LABEL_TO_ISSUE", {
            "issue_id": issue_id,
            "label_name": agent_label
        })
        
        # Step 5: Add status label: pending
        status_result, status_error = run_composio_tool("LINEAR_ADD_LABEL_TO_ISSUE", {
            "issue_id": issue_id,
            "label_name": "status:pending"
        })
        
        if agent_error or status_error:
            print(f"[WARNING] Failed to update labels for {issue_id}")
    
    # Output summary
    output = {
        "status": "success",
        "issues_processed": len(issues),
        "routed_to_jules": routed_count["Jules"],
        "routed_to_antigravity": routed_count["Antigravity"]
    }
    
    print(f"[SUMMARY] Routed {routed_count['Jules']} to Jules, {routed_count['Antigravity']} to Antigravity")
    
    return output


# Recipe entry point
output = main()
