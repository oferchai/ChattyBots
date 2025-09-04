"""
Unit tests for database models in Multi-Agent AI Chat System.
"""
import pytest
import uuid
from backend.config import reload_settings

from app.agents import get_agent_config, get_agent_ids
from app.db import DatabaseSession, init_database, reset_database
from app.models import (
    Conversation, 
    ConversationStatus, 
    Message, 
    MessageType, 
    SenderType
)

@pytest.fixture(scope="function")
def setup_database(monkeypatch):
    """Fixture to initialize and clean up the database for model tests."""
    monkeypatch.setenv('DATABASE_URL', 'sqlite:///:memory:')
    reload_settings()
    reset_database()
    yield
    # Clean up after test
    reload_settings()

def test_agent_configuration():
    """Test static agent configuration."""
    # Test getting all agent IDs
    agent_ids = get_agent_ids()
    assert len(agent_ids) > 0
    assert "project_manager" in agent_ids
    
    # Test individual agent configs
    for agent_id in agent_ids:
        config = get_agent_config(agent_id)
        assert config.name is not None
        assert config.role is not None
        assert len(config.personality_traits) > 0
        assert len(config.expertise_areas) > 0

@pytest.fixture(scope="function")
def conversation_with_messages_fixture(setup_database):
    """Fixture to create a conversation with messages for testing."""
    with DatabaseSession() as db:
        # Create a test conversation
        conversation = Conversation(
            goal_description="Design a mobile banking app for millennials",
            status=ConversationStatus.ACTIVE
        )
        db.add(conversation)
        db.flush()  # Get the ID without committing
        
        # Create initial user message
        user_message = Message(
            conversation_id=conversation.id,
            sender_type=SenderType.USER,
            sender_id="user",
            content="I need help designing a mobile banking app that appeals to millennials",
            message_type=MessageType.USER_RESPONSE
        )
        db.add(user_message)
        
        # Create agent discussion messages
        pm_message = Message(
            conversation_id=conversation.id,
            sender_type=SenderType.AGENT,
            sender_id="project_manager",
            content="Great! Let me understand the requirements better. What specific features are most important to your target users?",
            message_type=MessageType.QUESTION_TO_USER,
            requires_user_response=True,
            parent_message_id=user_message.id
        )
        db.add(pm_message)
        
        tech_message = Message(
            conversation_id=conversation.id,
            sender_type=SenderType.AGENT,
            sender_id="technical_architect",
            content="From a technical perspective, we should consider React Native for cross-platform development",
            message_type=MessageType.DISCUSSION
        )
        db.add(tech_message)
        
        creative_message = Message(
            conversation_id=conversation.id,
            sender_type=SenderType.AGENT,
            sender_id="creative_strategist",
            content="What if we gamified the banking experience with spending challenges and savings goals?",
            message_type=MessageType.DISCUSSION
        )
        db.add(creative_message)
        
        # Commit all changes
        db.commit()
        
        # Refresh to get relationships
        db.refresh(conversation)
        
        yield conversation

def test_database_models(conversation_with_messages_fixture):
    """Test database models and relationships."""
    conversation = conversation_with_messages_fixture
    
    assert conversation.id is not None
    assert conversation.status == ConversationStatus.ACTIVE
    assert conversation.is_waiting_for_user is False
    
    assert conversation.message_count == 4
    assert len(conversation.messages) == 4
    
    # Test message properties
    for msg in conversation.messages:
        assert msg.agent_name is not None
        assert msg.content is not None
        assert msg.message_type is not None
        assert isinstance(msg.is_from_agent, bool)
    
    # Test conversation state changes
    conversation.pause_for_user_input()
    assert conversation.is_waiting_for_user is True
    
    conversation.resume()
    assert conversation.status == ConversationStatus.ACTIVE
    
    conversation.complete("Team agreed on React Native app with gamification features")
    assert conversation.status == ConversationStatus.COMPLETED
    assert conversation.final_summary == "Team agreed on React Native app with gamification features"

def test_message_threading(conversation_with_messages_fixture):
    """Test message threading functionality."""
    conversation = conversation_with_messages_fixture
    
    with DatabaseSession() as db:
        # Find the PM question message
        pm_question = db.query(Message).filter(
            Message.conversation_id == conversation.id,
            Message.sender_id == "project_manager",
            Message.message_type == MessageType.QUESTION_TO_USER
        ).first()
        assert pm_question is not None
        
        # Create user response
        user_response = Message(
            conversation_id=conversation.id,
            sender_type=SenderType.USER,
            sender_id="user",
            content="The most important features are: easy money transfers, spending analytics, and budget alerts",
            message_type=MessageType.USER_RESPONSE,
            parent_message_id=pm_question.id
        )
        db.add(user_response)
        db.commit()
        
        # Mark question as answered
        pm_question.mark_as_answered()
        db.commit()
        
        # Test threading
        db.refresh(pm_question)
        assert pm_question.requires_user_response is False
        assert len(pm_question.replies) == 1
        
        for reply in pm_question.replies:
            assert reply.agent_name == "User"
            assert reply.content == "The most important features are: easy money transfers, spending analytics, and budget alerts"
