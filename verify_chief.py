"""
Verification script for Chief Orchestrator
"""

from agents.chief.agent import ChiefAgent
import logging

# Set up logging for output
logging.basicConfig(level=logging.INFO)

def verify_orchestration():
    print("\n--- Starting Chief Orchestration Verification ---\n")
    
    # 1. Initialize Chief
    print("Step 1: Initializing Chief Agent...")
    chief = ChiefAgent()
    
    # 2. Check Discovery
    print(f"\nStep 2: Checking discovered agents...")
    for agent_id in chief.registry:
        print(f"  [+] Found: {agent_id}")
    
    if "search-bot-v1" not in chief.registry:
        print("  [-] ERROR: search-bot-v1 not found in registry!")
    
    # 3. Simulate User Request
    print("\nStep 3: Simulating user request ('Who is the CEO of Google?')...")
    # We'll call handle_message directly (mocking the ADK run loop)
    # mock_ctx can be None for this basic test
    response = chief.handle_message("Who is the CEO of Google?", None)
    
    print("\n--- Final Response from Chief ---")
    print(response)
    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    verify_orchestration()
