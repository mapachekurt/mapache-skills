"""
Linear Artifact Sync-Back - Composio Recipe

This recipe monitors Git commits for Linear issue references and syncs
artifacts (walkthroughs, implementation plans) back to Linear as comments.

Dependencies:
- Composio LINEAR toolkit
- Git repo with commit patterns like "Fixes LIN-123" or "Closes LIN-456"
- Linear custom fields: Agent Status, Artifacts

Usage:
    composio-recipe execute linear-artifact-sync --params '{"repo_path": "/path/to/repo"}'
"""

import os
import re
import subprocess
from typing import Dict, List, Tuple, Optional


def get_recent_commits(repo_path: str, since_minutes: int = 60) -> List[Dict[str, str]]:
    """
    Get recent commits from the Git repository.
    
    Args:
        repo_path: Path to Git repository
        since_minutes: How far back to look for commits
        
    Returns:
        List of commit dictionaries with {hash, message, author, timestamp}
    """
    cmd = [
        "git", "-C", repo_path, "log",
        f"--since={since_minutes} minutes ago",
        "--pretty=format:%H|%s|%an|%at"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        commits = []
        
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("|")
            if len(parts) == 4:
                commits.append({
                    "hash": parts[0],
                    "message": parts[1],
                    "author": parts[2],
                    "timestamp": parts[3]
                })
        
        return commits
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to get commits: {e}")
        return []


def extract_linear_issue_id(commit_message: str) -> Optional[str]:
    """
    Extract Linear issue ID from commit message.
    
    Patterns supported:
    - Fixes LIN-123
    - Closes LIN-456
    - Resolves MAPAI-789
    
    Args:
        commit_message: Git commit message
        
    Returns:
        Linear issue ID or None
    """
    patterns = [
        r"(?:Fixes|Closes|Resolves)\s+([A-Z]+-\d+)",
        r"\[([A-Z]+-\d+)\]",
        r"#([A-Z]+-\d+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, commit_message, re.IGNORECASE)
        if match:
            return match.group(1).upper()
    
    return None


def find_artifact_files(repo_path: str, commit_hash: str) -> Dict[str, str]:
    """
    Find artifact files (walkthrough.md, implementation_plan.md) in a commit.
    
    Args:
        repo_path: Path to Git repository
        commit_hash: Git commit hash
        
    Returns:
        Dictionary mapping artifact type to file content
    """
    artifacts = {}
    artifact_files = ["walkthrough.md", "implementation_plan.md", "task.md"]
    
    for filename in artifact_files:
        cmd = ["git", "-C", repo_path, "show", f"{commit_hash}:{filename}"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode == 0:
                artifacts[filename] = result.stdout
        except Exception:
            continue
    
    return artifacts


def main():
    """
    Main recipe execution logic.
    
    Environment Variables:
        GIT_REPO_PATH: Path to Git repository
        ARTIFACT_DIRECTORY: Directory containing .gemini artifacts (optional)
        GOOGLE_DRIVE_FOLDER_ID: For large artifact uploads (optional)
    """
    repo_path = os.environ.get("GIT_REPO_PATH", ".")
    artifacts_dir = os.environ.get("ARTIFACT_DIRECTORY", "")
    
    print(f"[ARTIFACT SYNC] Monitoring repo: {repo_path}")
    
    # Step 1: Get recent commits
    commits = get_recent_commits(repo_path, since_minutes=60)
    print(f"[INFO] Found {len(commits)} recent commits")
    
    synced_count = 0
    
    # Step 2: Process each commit
    for commit in commits:
        commit_hash = commit["hash"]
        commit_message = commit["message"]
        
        # Extract Linear issue ID
        issue_id = extract_linear_issue_id(commit_message)
        if not issue_id:
            continue
        
        print(f"[PROCESSING] Commit {commit_hash[:7]} → {issue_id}")
        
        # Step 3: Fetch the Linear issue
        result, error = run_composio_tool("LINEAR_GET_LINEAR_ISSUE", {
            "issue_id": issue_id
        })
        
        if error:
            print(f"[WARNING] Issue {issue_id} not found: {error}")
            continue
        
        issue = result.get("data", {}).get("issue", {})
        if not issue:
            continue
        
        # Step 4: Find artifacts in commit
        artifacts = find_artifact_files(repo_path, commit_hash)
        
        # Step 5: Create comment with commit summary
        comment_body = f"## Agent Work Completed\n\n"
        comment_body += f"**Commit**: `{commit_hash[:7]}`\n"
        comment_body += f"**Author**: {commit['author']}\n"
        comment_body += f"**Message**: {commit_message}\n\n"
        
        if artifacts:
            comment_body += f"### Artifacts\n\n"
            
            for artifact_name, content in artifacts.items():
                # Truncate large artifacts
                if len(content) > 5000:
                    comment_body += f"**{artifact_name}** (truncated - see full version in repo)\n\n"
                    comment_body += f"```markdown\n{content[:5000]}\n... (truncated)\n```\n\n"
                else:
                    comment_body += f"**{artifact_name}**\n\n{content}\n\n"
        
        # Post comment
        comment_result, comment_error = run_composio_tool("LINEAR_CREATE_LINEAR_COMMENT", {
            "issue_id": issue_id,
            "body": comment_body
        })
        
        if comment_error:
            print(f"[WARNING] Failed to create comment for {issue_id}: {comment_error}")
            continue
        
        # Step 6: Update Agent Status to "Completed"
        mutation = f"""
        mutation {{
          issueUpdate(
            id: "{issue_id}",
            input: {{
              customFields: {{
                "Agent Status": "Completed"
              }}
            }}
          ) {{
            success
          }}
        }}
        """
        
        status_result, status_error = run_composio_tool("LINEAR_RUN_QUERY_OR_MUTATION", {
            "query_or_mutation": mutation
        })
        
        if status_error:
            print(f"[WARNING] Failed to update status for {issue_id}: {status_error}")
        
        synced_count += 1
        print(f"[SUCCESS] Synced artifacts for {issue_id}")
    
    # Output summary
    output = {
        "status": "success",
        "commits_processed": len(commits),
        "issues_synced": synced_count
    }
    
    print(f"[SUMMARY] Synced {synced_count} issues from {len(commits)} commits")
    
    return output


# Recipe entry point
output = main()
