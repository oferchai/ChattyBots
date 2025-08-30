"""
Unit tests for the ConversationManager.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock

from app.services.conversation_manager import ConversationManager
from app.models.conversation import Conversation
from app.agents.agent_manager import AgentManager

@pytest.fixture
def mock_agent_manager():
    """Fixture to create a mock AgentManager."""
    mock = MagicMock(spec=AgentManager)
    mock.get_all_agents = MagicMock(return_value=[])
    return mock

@pytest.fixture
def mock_conversation():
    """Fixture to create a mock Conversation."""
    mock = MagicMock(spec=Conversation)
    mock.id = "conv1"
    mock.goal_description = "Test goal"
    return mock

@pytest.mark.asyncio
async def test_conversation_manager_creation(mock_agent_manager, mock_conversation):
    """Test that the ConversationManager can be created."""
    manager = ConversationManager(agent_manager=mock_agent_manager, conversation=mock_conversation)
    assert manager.agent_manager == mock_agent_manager
    assert manager.conversation == mock_conversation

@pytest.mark.asyncio
async def test_start(mock_agent_manager, mock_conversation):
    """Test the start method of the ConversationManager."""
    manager = ConversationManager(agent_manager=mock_agent_manager, conversation=mock_conversation)
    manager.run_conversation_loop = AsyncMock()
    
    await manager.start()
    
    assert len(manager.conversation_history) == 1
    assert manager.conversation_history[0].sender == "system"
    manager.run_conversation_loop.assert_called_once()
