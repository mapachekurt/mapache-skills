"""
SearchBot Agent

Purpose: Performs web searches and returns summaries
Created: 2026-01-29
"""

try:
    from google.adk import Agent, on_message
    from google.adk.models import Gemini
except ImportError:
    from adk import Agent, on_message
    from adk.models import Gemini
import logging

# Import custom tools
from tools.custom_tools import web_search


class SearchBotAgent(Agent):
    """
    Performs web searches and returns summaries
    
    This agent follows Google ADK standards and A2A protocol.
    """
    
    def __init__(self):
        super().__init__(
            name="search-bot",
            model=Gemini("gemini-2.0-flash-exp"),
            description="Performs web searches and returns summaries",
            tools=[web_search]
        )
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='{"time":"%(asctime)s", "level":"%(levelname)s", "msg":"%(message)s"}'
        )
        self.logger = logging.getLogger(__name__)
    
    @on_message
    def handle_message(self, message: str, ctx):
        """
        Handle incoming messages.
        
        Args:
            message: User message
            ctx: Context object with session, run_id, etc.
        
        Returns:
            Response string or structured data
        """
        self.logger.info(
            f"Processing message in session {ctx.session_id}",
            extra={"message_length": len(message)}
        )
        
        # Retrieve conversation history from session
        history = ctx.session.get("history", [])
        
        # Generate response using LLM
        response = self.llm.generate(
            message,
            context={"history": history}
        )
        
        # Update session history
        history.append({"user": message, "agent": response.text})
        ctx.session["history"] = history
        
        self.logger.info(
            f"Response generated",
            extra={"response_length": len(response.text)}
        )
        
        return response.text


# For local testing
if __name__ == "__main__":
    agent = SearchBotAgent()
    
    # Run with web UI at http://localhost:8000
    agent.run()
    
    # Or run in CLI mode:
    # agent.run(cli=True)
