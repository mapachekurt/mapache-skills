"""
Chief Agent - Orchestrator

The central agent that orchestrates tasks across subagents.
"""

try:
    from google.adk import Agent, on_message
    from google.adk.models import Gemini
except ImportError:
    from adk import Agent, on_message
    from adk.models import Gemini
import logging
import os

try:
    from .discovery import AgentDiscovery
    from .a2a_client import A2AClient
except ImportError:
    from discovery import AgentDiscovery
    from a2a_client import A2AClient

class ChiefAgent(Agent):
    """
    Chief Orchestrator Agent
    
    This agent coordinates subagents based on their A2A profiles.
    """
    
    def __init__(self):
        super().__init__(
            name="chief",
            model=Gemini("gemini-1.5-flash"), # Using flash for orchestration speed
            description="Central orchestrator for all subagents using A2A"
        )
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='{"time":"%(asctime)s", "level":"%(levelname)s", "msg":"%(message)s"}'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize discovery and client
        # For testing, we point to the parent 'agents' directory
        self.discovery = AgentDiscovery(search_path="..")
        self.registry = self.discovery.scan()
        self.a2a_client = A2AClient(self.registry)
        
        # Add delegation tool
        self.add_tool(self.delegate_to_agent)
        
        self.logger.info(f"Chief initialized with {len(self.registry)} subagents.")

    def delegate_to_agent(self, agent_id: str, request: str) -> str:
        """
        Delegates a specific task or request to a specialized subagent.
        
        Args:
            agent_id: The ID of the subagent (e.g., 'search-bot-v1')
            request: The task or question for the subagent
            
        Returns:
            The subagent's response
        """
        self.logger.info(f"Delegating requested '{request[:30]}...' to {agent_id}")
        return self.a2a_client.send_message(agent_id, request)

    def get_system_instructions(self) -> str:
        """Inject subagent capabilities into system instructions"""
        caps = self.discovery.get_capabilities_summary()
        return f"""You are 'chief', a high-level orchestrator agent.
Your job is to help users by coordinating specialized subagents.

AVAILABLE SUBAGENTS:
{caps}

GUIDELINES:
1. When a user asks a question, determine which subagent is best suited to help.
2. ALWAYS use the 'delegate_to_agent' tool if a subagent can handle the request.
3. If no subagent matches, try to help the user directly using your own knowledge.
4. Summarize subagent responses for the user, but keep technical details intact.
5. If multiple agents are needed, explain the plan to the user.
"""

    @on_message
    def handle_message(self, message: str, ctx):
        """
        Handle user requests by delegating to subagents.
        """
        self.logger.info(f"Chief received message: {message[:100]}")
        
        # Refresh registry occasionally or on demand
        # self.registry = self.discovery.scan() 
        
        # Update system instructions with current subagent capabilities
        # Note: In ADK, system instructions are often passed during LLM initialization
        # or as part of the prompt in custom implementations.
        
        # For this prototype, we'll manually construct the prompt
        prompt = f"{self.get_system_instructions()}\n\nUser: {message}"
        
        # Generate response using LLM
        # In a real ADK agent, the LLM would decide to use the 'delegate' tool
        # For simplicity in this initial implementation, we'll let the LLM generate
        # its plan, and we'll implement a simple tool for delegation.
        
        response = self.model.generate(prompt)
        return response.text

    # We can also define a Tool for delegation that the LLM can call
    # But for now, we'll keep the handler simple.

if __name__ == "__main__":
    agent = ChiefAgent()
    agent.run()
