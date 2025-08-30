"""
Unit tests for the AgentManager.
"""
import pytest
from unittest.mock import AsyncMock

from app.agents.agent_manager import AgentManager
from app.agents.base import BaseAgent

@pytest.fixture
def mock_llm_service():
    """Fixture to create a mock LLM service."""
    mock = AsyncMock()
    mock.generate_response = AsyncMock(return_value="Mocked LLM response")
    return mock

def test_agent_manager_creation(mock_llm_service):
    """Test that the AgentManager can be created and creates all agents."""
    agent_manager = AgentManager(llm_service=mock_llm_service)
    assert len(agent_manager.agents) == 5
    for agent in agent_manager.agents.values():
        assert isinstance(agent, BaseAgent)

def test_get_agent(mock_llm_service):
    """Test the get_agent method of the AgentManager."""
    agent_manager = AgentManager(llm_service=mock_llm_service)
    agent = agent_manager.get_agent("project_manager")
    assert agent.agent_id == "project_manager"

    with pytest.raises(KeyError):
        agent_manager.get_agent("non_existent_agent")
