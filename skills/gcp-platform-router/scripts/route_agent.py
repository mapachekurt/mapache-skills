import os
import sys
import json
import argparse
from typing import Dict, Any

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("❌ Error: google-genai not installed. Run 'pip install google-genai'.")
    sys.exit(1)

def get_api_key(provided_key: Optional[str] = None) -> str:
    """Retrieves the API key from environment, args, or GSM."""
    if provided_key:
        return provided_key
    
    key = os.environ.get("GOOGLE_API_KEY")
    if key:
        return key

    # Try fetching from gcp-secrets skill
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        manage_secrets_path = os.path.join(current_dir, "../../gcp-secrets/scripts/manage_secrets.py")
        if os.path.exists(manage_secrets_path):
            from google.cloud import secretmanager # Optional check
            # For simplicity, we just run the script as a subprocess
            import subprocess
            result = subprocess.run(
                [sys.executable, manage_secrets_path, "get", "--name", "GOOGLE_API_KEY"],
                capture_output=True,
                text=True,
                shell=True if os.name == 'nt' else False
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
    except Exception:
        pass

    return ""

def route_agent(description: str, api_key: str) -> Dict[str, Any]:
    """
    Classifies an agent description into cloud_run, agent_engine, or hybrid.
    """
    client = genai.Client(api_key=api_key)
    
    system_instruction = """
    You are the 'GCP Agent Placement Router' for Antigravity. 
    Your job is to decide whether an agent should be deployed to Google Cloud Run, Vertex AI Agent Engine, or a Hybrid model.

    Decision Framework:
    1. Worker -> Cloud Run: Value comes from doing work (tools, actions, background tasks, orchestration, MCP routing).
    2. Character -> Agent Engine: Value comes from being someone (conversational continuity, persona, shared context, long-lived chat).
    3. Hybrid: A persona (Agent Engine) that intent-dispatches to workers (Cloud Run).

    Rules:
    - MCP Routers, Tool Agents, Background Workers, and Orchestrators MUST go to Cloud Run.
    - Long-lived personal assistants or company context bots SHOULD go to Agent Engine.
    - High-level 'CEO' agents with complex execution SHOULD be Hybrid.

    Return JSON strictly in this format:
    {
      "deployment_target": "cloud_run | agent_engine | hybrid",
      "confidence": "high | medium | low",
      "reasons": ["reason 1", "reason 2"],
      "implementation_notes": ["note 1", "note 2"],
      "anti_patterns": ["anti-pattern 1"]
    }
    """

    prompt = f"Agent Description: {description}\n\nRoute this agent according to the framework."

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
            ),
            contents=prompt,
        )
        
        return json.loads(response.text)
    except Exception as e:
        return {
            "error": str(e),
            "deployment_target": "unknown",
            "confidence": "low",
            "reasons": ["Error during LLM classification"],
            "implementation_notes": [],
            "anti_patterns": []
        }

def main():
    parser = argparse.ArgumentParser(description="Route an agent to the correct GCP platform.")
    parser.add_argument("--description", required=True, help="Description of the agent to route.")
    parser.add_argument("--api-key", help="Google API Key (overrides GOOGLE_API_KEY env var).")
    args = parser.parse_args()

    api_key = get_api_key(args.api_key)
    if not api_key:
        print("❌ Error: Google API Key not found. Provide --api-key, set GOOGLE_API_KEY, or store in GSM.")
        sys.exit(1)

    result = route_agent(args.description, api_key)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
