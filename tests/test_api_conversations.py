"""
Unit/integration tests for the Conversation API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock
import uuid
from datetime import datetime

from app.main import app
from app.db import get_db
from app.models import Conversation, ConversationStatus, Message, MessageType, SenderType
from app.services.llm_service import LLMServiceFactory
from app.agents.agent_manager import AgentManager
from app.services.conversation_manager import ConversationManager as ServiceConversationManager
from app.api.websockets import ConnectionManager

# Fixtures for mocking dependencies
@pytest.fixture
def mock_db_session():
    """Mock database session."""
    return MagicMock()

@pytest.fixture
def mock_llm_service_factory():
    """Mock LLMServiceFactory."""
    mock = MagicMock(spec=LLMServiceFactory)
    mock.create_llm_service.return_value = AsyncMock()
    return mock

@pytest.fixture
def mock_agent_manager():
    """Mock AgentManager."""
    return MagicMock(spec=AgentManager)

@pytest.fixture
def mock_connection_manager():
    """Mock ConnectionManager."""
    return MagicMock(spec=ConnectionManager)

@pytest.fixture(autouse=True)
def override_dependencies(mock_db_session, mock_llm_service_factory, mock_agent_manager, mock_connection_manager):
    """Override FastAPI dependencies with mocks."""
    app.dependency_overrides[get_db] = lambda: mock_db_session
    app.dependency_overrides[LLMServiceFactory] = lambda: mock_llm_service_factory
    app.dependency_overrides[AgentManager] = lambda: mock_agent_manager
    app.dependency_overrides[ConnectionManager] = lambda: mock_connection_manager
    yield
    app.dependency_overrides.clear()

# Test client
@pytest.fixture(scope="module")
def client():
    """Test client for FastAPI app."""
    with TestClient(app) as c:
        yield c

# --- Conversation Management Tests ---

def test_create_conversation(client, mock_db_session):
    """Test POST /api/conversations."""
    conversation_data = {"goal_description": "Design a new mobile app"}
    mock_conversation = MagicMock(spec=Conversation, id=uuid.uuid4(), goal_description="Design a new mobile app", status=ConversationStatus.ACTIVE, message_count=0, is_waiting_for_user=False, created_at=datetime.now(), updated_at=datetime.now())
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_conversation

    response = client.post("/api/conversations", json=conversation_data)
    assert response.status_code == 201
    assert response.json()["goal_description"] == "Design a new mobile app"
    assert response.json()["status"] == "active"

def test_list_conversations(client, mock_db_session):
    """Test GET /api/conversations."""
    mock_conversation = MagicMock(spec=Conversation, id=uuid.uuid4(), goal_description="Test", status=ConversationStatus.ACTIVE, message_count=0, is_waiting_for_user=False, created_at=datetime.now(), updated_at=datetime.now(), final_summary=None)
    mock_db_session.query.return_value.count.return_value = 1
    mock_db_session.query.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = [mock_conversation]

    response = client.get("/api/conversations")
    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert response.json()["conversations"][0]["goal_description"] == "Test"

def test_get_conversation(client, mock_db_session):
    """Test GET /api/conversations/{id}."""
    conv_id = uuid.uuid4()
    mock_conversation = MagicMock(spec=Conversation, id=conv_id, goal_description="Test", status=ConversationStatus.ACTIVE, message_count=0, is_waiting_for_user=False, messages=[], created_at=datetime.now(), updated_at=datetime.now(), final_summary=None)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_conversation

    response = client.get(f"/api/conversations/{conv_id}")
    assert response.status_code == 200
    assert response.json()["id"] == str(conv_id)
    assert response.json()["goal_description"] == "Test"

def test_update_conversation(client, mock_db_session):
    """Test PUT /api/conversations/{id}."""
    conv_id = uuid.uuid4()
    mock_conversation = MagicMock(spec=Conversation, id=conv_id, goal_description="Test", status=ConversationStatus.ACTIVE, message_count=0, is_waiting_for_user=False, created_at=datetime.now(), updated_at=datetime.now(), final_summary=None)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_conversation

    update_data = {"status": "paused", "final_summary": "Updated summary"}
    response = client.put(f"/api/conversations/{conv_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["status"] == "paused"
    assert response.json()["final_summary"] == "Updated summary"

def test_delete_conversation(client, mock_db_session):
    """Test DELETE /api/conversations/{id}."""
    conv_id = uuid.uuid4()
    mock_conversation = MagicMock(spec=Conversation, id=conv_id)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_conversation

    response = client.delete(f"/api/conversations/{conv_id}")
    assert response.status_code == 204
    mock_db_session.delete.assert_called_once_with(mock_conversation)
    mock_db_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_start_conversation_discussion(client, mock_db_session, mock_llm_service_factory, mock_agent_manager, mock_connection_manager):
    """Test POST /api/conversations/{id}/start."""
    conv_id = uuid.uuid4()
    mock_conversation = MagicMock(spec=Conversation, id=conv_id, goal_description="Test goal", status=ConversationStatus.ACTIVE, message_count=0, is_waiting_for_user=False, created_at=datetime.now(), updated_at=datetime.now())
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_conversation

    # Mock the service-level ConversationManager's start method
    with patch('app.services.conversation_manager.ServiceConversationManager.start', new_callable=AsyncMock) as mock_service_conv_manager_start:
        response = client.post(f"/api/conversations/{conv_id}/start")
        assert response.status_code == 200
        assert response.json()["id"] == str(conv_id)
        mock_service_conv_manager_start.assert_called_once()

# --- Message Operations Tests ---

def test_create_message(client, mock_db_session):
    """Test POST /api/conversations/{id}/messages."""
    conv_id = uuid.uuid4()
    mock_conversation = MagicMock(spec=Conversation, id=conv_id, status=ConversationStatus.ACTIVE, created_at=datetime.now(), updated_at=datetime.now(), message_count=0, is_waiting_for_user=False)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_conversation

    message_data = {
        "sender_type": "user",
        "sender_id": "user",
        "content": "Hello",
        "message_type": "user_response",
        "requires_user_response": False
    }
    mock_message = MagicMock(spec=Message, id=uuid.uuid4(), conversation_id=conv_id, created_at=datetime.now(), agent_name="User", is_from_agent=False, is_from_user=True, is_question_for_user=False, **message_data)
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_message

    response = client.post(f"/api/conversations/{conv_id}/messages", json=message_data)
    assert response.status_code == 201
    assert response.json()["content"] == "Hello"

def test_get_conversation_messages(client, mock_db_session):
    """Test GET /api/conversations/{id}/messages."""
    conv_id = uuid.uuid4()
    mock_conversation = MagicMock(spec=Conversation, id=conv_id, created_at=datetime.now(), updated_at=datetime.now(), status=ConversationStatus.ACTIVE, final_summary=None)
    mock_message = MagicMock(spec=Message, id=uuid.uuid4(), conversation_id=conv_id, content="Test message", sender_id="user", sender_type=SenderType.USER, message_type=MessageType.DISCUSSION, requires_user_response=False, agent_name="User", is_from_agent=False, is_from_user=True, is_question_for_user=False, created_at=datetime.now(), parent_message_id=None)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_conversation
    mock_db_session.query.return_value.filter.return_value.count.return_value = 1
    mock_db_session.query.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = [mock_message]

    response = client.get(f"/api/conversations/{conv_id}/messages")
    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert response.json()["messages"][0]["content"] == "Test message"

def test_get_pending_user_messages(client, mock_db_session):
    """Test GET /api/conversations/{id}/messages/pending."""
    conv_id = uuid.uuid4()
    mock_conversation = MagicMock(spec=Conversation, id=conv_id, created_at=datetime.now(), updated_at=datetime.now(), status=ConversationStatus.ACTIVE, final_summary=None)
    mock_message = MagicMock(spec=Message, id=uuid.uuid4(), conversation_id=conv_id, content="Pending message", sender_id="agent", sender_type=SenderType.AGENT, message_type=MessageType.QUESTION_TO_USER, requires_user_response=True, agent_name="Project Manager", is_from_agent=True, is_from_user=False, is_question_for_user=True, created_at=datetime.now(), parent_message_id=None)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_conversation
    mock_db_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = [mock_message]

    response = client.get(f"/api/conversations/{conv_id}/messages/pending")
    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert response.json()["messages"][0]["content"] == "Pending message"
