"""
Unit tests for the AI agents.
"""
import pytest
from unittest.mock import AsyncMock

from app.agents.config import get_agent_config
from app.agents.specific_agents import (
    ProjectManagerAgent,
    TechnicalArchitectAgent,
    CreativeStrategistAgent,
    QualityAssuranceAgent,
    ResourceCoordinatorAgent,
)
from app.agents.interfaces import ConversationContext, Message

@pytest.fixture
def mock_llm_service():
    """Fixture to create a mock LLM service."""
    mock = AsyncMock()
    mock.generate_response = AsyncMock(return_value="Mocked LLM response")
    return mock

@pytest.mark.asyncio
async def test_project_manager_agent_creation(mock_llm_service):
    """Test that the ProjectManagerAgent can be created."""
    config = get_agent_config("project_manager")
    agent = ProjectManagerAgent(
        agent_id="project_manager",
        name=config.name,
        role=config.role,
        personality_prompt=config.system_prompt,
        system_prompt=config.system_prompt,
        llm_service=mock_llm_service,
    )
    assert agent.agent_id == "project_manager"

@pytest.mark.asyncio
async def test_project_manager_agent_generate_response(mock_llm_service):
    """Test the generate_response method of the ProjectManagerAgent."""
    config = get_agent_config("project_manager")
    agent = ProjectManagerAgent(
        agent_id="project_manager",
        name=config.name,
        role=config.role,
        personality_prompt=config.system_prompt,
        system_prompt=config.system_prompt,
        llm_service=mock_llm_service,
    )
    context = ConversationContext(
        conversation_history=[Message(sender="user", content="Hello")],
        current_goal="Test goal",
    )
    response = await agent.generate_response(context)
    assert response == "Mocked LLM response"
    mock_llm_service.generate_response.assert_called_once()
