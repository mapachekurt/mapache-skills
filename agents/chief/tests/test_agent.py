"""
Unit tests for ChiefAgent
"""

import pytest
from agent import ChiefAgent
from adk.testing import MockContext


@pytest.fixture
def agent():
    """Create agent instance for testing"""
    return ChiefAgent()


@pytest.fixture
def mock_context():
    """Create mock context"""
    return MockContext(session_id="test-session-123")


def test_agent_initialization(agent):
    """Test agent initializes correctly"""
    assert agent.name == "chief"
    assert agent.model is not None
    assert agent.description == "Central orchestrator for all subagents using A2A"


def test_basic_message_handling(agent, mock_context):
    """Test agent handles messages"""
    response = agent.handle_message("Hello, agent!", mock_context)
    
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0


def test_session_persistence(agent, mock_context):
    """Test conversation history persists in session"""
    # First message
    agent.handle_message("Remember my name is Alice", mock_context)
    
    # Check session has history
    history = mock_context.session.get("history")
    assert history is not None
    assert len(history) > 0
    
    # Second message
    agent.handle_message("What's my name?", mock_context)
    
    # History should have grown
    updated_history = mock_context.session.get("history")
    assert len(updated_history) > len(history)


def test_tool_availability(agent):
    """Test tools are properly registered"""
    # Check agent has tools assigned
    # TODO: Add tool-specific tests when tools are implemented
    pass


# Add more tests as needed
