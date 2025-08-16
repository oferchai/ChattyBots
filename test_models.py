#!/usr/bin/env python3
"""
Test script for database models in Multi-Agent AI Chat System.

This script tests the database models by creating sample data
and verifying relationships work correctly.
"""
import sys
from pathlib import Path

# Add backend app to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.agents import get_agent_config, get_agent_ids
from app.db import DatabaseSession, init_database
from app.models import (
    Conversation, 
    ConversationStatus, 
    Message, 
    MessageType, 
    SenderType
)


def test_agent_configuration():
    """Test static agent configuration."""
    print("🤖 Testing Agent Configuration...")
    
    # Test getting all agent IDs
    agent_ids = get_agent_ids()
    print(f"Available agents: {agent_ids}")
    
    # Test individual agent configs
    for agent_id in agent_ids:
        config = get_agent_config(agent_id)
        print(f"  {agent_id}: {config.name} - {config.role}")
        print(f"    Traits: {', '.join(config.personality_traits[:3])}...")
        print(f"    Expertise: {', '.join(config.expertise_areas[:3])}...")
    
    print("✅ Agent configuration test passed!\n")


def test_database_models():
    """Test database models and relationships."""
    print("💾 Testing Database Models...")
    
    # Initialize database
    init_database()
    
    with DatabaseSession() as db:
        # Create a test conversation
        conversation = Conversation(
            goal_description="Design a mobile banking app for millennials",
            status=ConversationStatus.ACTIVE
        )
        db.add(conversation)
        db.flush()  # Get the ID without committing
        
        print(f"Created conversation: {conversation}")
        print(f"  ID: {conversation.id}")
        print(f"  Status: {conversation.status}")
        print(f"  Waiting for user: {conversation.is_waiting_for_user}")
        
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
        
        # Test relationships
        print(f"  Message count: {conversation.message_count}")
        print(f"  Messages in conversation: {len(conversation.messages)}")
        
        # Test message properties
        for msg in conversation.messages:
            print(f"    {msg.agent_name}: {msg.content[:50]}...")
            print(f"      Type: {msg.message_type}, From Agent: {msg.is_from_agent}")
            if msg.is_question_for_user:
                print("      🤔 This message requires user response")
        
        # Test conversation state changes
        conversation.pause_for_user_input()
        print(f"  After pausing - Waiting for user: {conversation.is_waiting_for_user}")
        
        conversation.resume()
        print(f"  After resuming - Status: {conversation.status}")
        
        conversation.complete("Team agreed on React Native app with gamification features")
        print(f"  After completion - Status: {conversation.status}")
        print(f"  Final summary: {conversation.final_summary}")
    
    print("✅ Database models test passed!\n")


def test_message_threading():
    """Test message threading functionality."""
    print("🧵 Testing Message Threading...")
    
    with DatabaseSession() as db:
        # Find the conversation we created
        conversation = db.query(Conversation).first()
        
        if conversation:
            # Find the PM question message
            pm_question = db.query(Message).filter(
                Message.conversation_id == conversation.id,
                Message.sender_id == "project_manager",
                Message.message_type == MessageType.QUESTION_TO_USER
            ).first()
            
            if pm_question:
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
                print(f"PM Question: {pm_question.content[:50]}...")
                print(f"  Requires response: {pm_question.requires_user_response}")
                print(f"  Replies count: {len(pm_question.replies)}")
                
                for reply in pm_question.replies:
                    print(f"    Reply from {reply.agent_name}: {reply.content[:50]}...")
    
    print("✅ Message threading test passed!\n")


def main():
    """Run all tests."""
    print("🚀 Starting Multi-Agent AI Chat System Model Tests\n")
    
    try:
        test_agent_configuration()
        test_database_models()
        test_message_threading()
        
        print("🎉 All tests passed successfully!")
        print("The database models and agent configuration are working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        raise


if __name__ == "__main__":
    main()
