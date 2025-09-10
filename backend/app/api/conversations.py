"""
Conversation API endpoints for Multi-Agent AI Chat System.

This module provides REST API endpoints for managing conversations,
including creating, reading, updating, and managing conversation messages.
"""
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Conversation, ConversationStatus, Message, MessageType, SenderType
from ..schemas import (
    ConversationCreate,
    ConversationResponse,
    ConversationDetail,
    ConversationList,
    ConversationUpdate,
    MessageCreate,
    MessageResponse,
    MessageList,
)


router = APIRouter()


@router.post("/conversations", response_model=ConversationResponse, status_code=201)
async def create_conversation(
    conversation_data: ConversationCreate,
    db: Session = Depends(get_db)
) -> ConversationResponse:
    """
    Create a new conversation.
    
    Args:
        conversation_data: Conversation creation data
        db: Database session
        
    Returns:
        Created conversation information
    """
    # Create new conversation
    conversation = Conversation(
        goal_description=conversation_data.goal_description,
        status=ConversationStatus.ACTIVE
    )
    
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return ConversationResponse(
        id=conversation.id,
        goal_description=conversation.goal_description,
        status=conversation.status,
        final_summary=conversation.final_summary,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        message_count=conversation.message_count,
        is_waiting_for_user=conversation.is_waiting_for_user
    )


@router.get("/conversations", response_model=ConversationList)
async def list_conversations(
    skip: int = Query(0, ge=0, description="Number of conversations to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of conversations to return"),
    status: Optional[ConversationStatus] = Query(None, description="Filter by conversation status"),
    db: Session = Depends(get_db)
) -> ConversationList:
    """
    List conversations with optional filtering and pagination.
    
    Args:
        skip: Number of conversations to skip
        limit: Maximum number of conversations to return
        status: Filter by conversation status
        db: Database session
        
    Returns:
        List of conversations
    """
    # Build query
    query = db.query(Conversation)
    
    if status:
        query = query.filter(Conversation.status == status)
    
    # Get total count
    total_count = query.count()
    
    # Apply pagination and ordering
    conversations = query.order_by(Conversation.updated_at.desc()).offset(skip).limit(limit).all()
    
    # Convert to response format
    conversation_responses = [
        ConversationResponse(
            id=conv.id,
            goal_description=conv.goal_description,
            status=conv.status,
            final_summary=conv.final_summary,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            message_count=conv.message_count,
            is_waiting_for_user=conv.is_waiting_for_user
        )
        for conv in conversations
    ]
    
    return ConversationList(
        conversations=conversation_responses,
        count=total_count
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(
    conversation_id: uuid.UUID,
    include_messages: bool = Query(True, description="Whether to include messages"),
    db: Session = Depends(get_db)
) -> ConversationDetail:
    """
    Get detailed information about a specific conversation.
    
    Args:
        conversation_id: Unique conversation identifier
        include_messages: Whether to include conversation messages
        db: Database session
        
    Returns:
        Detailed conversation information
        
    Raises:
        HTTPException: If conversation is not found
    """
    # Find conversation
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Convert messages to response format
    message_responses = []
    if include_messages:
        for msg in conversation.messages:
            message_responses.append(MessageResponse(
                id=msg.id,
                conversation_id=msg.conversation_id,
                sender_type=msg.sender_type,
                sender_id=msg.sender_id,
                content=msg.content,
                message_type=msg.message_type,
                parent_message_id=msg.parent_message_id,
                requires_user_response=msg.requires_user_response,
                created_at=msg.created_at,
                agent_name=msg.agent_name,
                is_from_agent=msg.is_from_agent,
                is_from_user=msg.is_from_user,
                is_question_for_user=msg.is_question_for_user
            ))
    
    return ConversationDetail(
        id=conversation.id,
        goal_description=conversation.goal_description,
        status=conversation.status,
        final_summary=conversation.final_summary,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        message_count=conversation.message_count,
        is_waiting_for_user=conversation.is_waiting_for_user,
        messages=message_responses
    )


@router.put("/conversations/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: uuid.UUID,
    update_data: ConversationUpdate,
    db: Session = Depends(get_db)
) -> ConversationResponse:
    """
    Update conversation status or summary.
    
    Args:
        conversation_id: Unique conversation identifier
        update_data: Conversation update data
        db: Database session
        
    Returns:
        Updated conversation information
        
    Raises:
        HTTPException: If conversation is not found
    """
    # Find conversation
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Update fields
    if update_data.status is not None:
        conversation.status = update_data.status
    
    if update_data.final_summary is not None:
        conversation.final_summary = update_data.final_summary
    
    db.commit()
    db.refresh(conversation)
    
    return ConversationResponse(
        id=conversation.id,
        goal_description=conversation.goal_description,
        status=conversation.status,
        final_summary=conversation.final_summary,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        message_count=conversation.message_count,
        is_waiting_for_user=conversation.is_waiting_for_user
    )


@router.delete("/conversations/{conversation_id}", status_code=204)
async def delete_conversation(
    conversation_id: uuid.UUID,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a conversation and all its messages.
    
    Args:
        conversation_id: Unique conversation identifier
        db: Database session
        
    Raises:
        HTTPException: If conversation is not found
    """
    # Find conversation
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Delete conversation (cascade will delete messages)
    db.delete(conversation)
    db.commit()


@router.post("/conversations/{conversation_id}/start", response_model=ConversationResponse)
async def start_conversation_discussion(
    conversation_id: uuid.UUID,
    db: Session = Depends(get_db)
) -> ConversationResponse:
    """
    Start the multi-agent discussion for a given conversation.
    
    Args:
        conversation_id: Unique conversation identifier
        db: Database session
        
    Returns:
        Updated conversation information
        
    Raises:
        HTTPException: If conversation is not found
    """
    # Verify conversation exists
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Initialize LLMServiceFactory and AgentManager
    # Assuming settings are accessible globally or via dependency injection
    from backend.config import get_settings
    from app.services.llm_service import LLMServiceFactory
    from app.agents.agent_manager import AgentManager
    from app.services.conversation_manager import ConversationManager as ServiceConversationManager
    
    settings = get_settings()
    llm_service_factory = LLMServiceFactory(config=settings.llm.model_dump())
    agent_manager = AgentManager(llm_service=llm_service_factory)
    
    # Create a service-level ConversationManager and start the discussion
    service_conversation_manager = ServiceConversationManager(
        agent_manager=agent_manager,
        conversation=conversation
    )
    await service_conversation_manager.start()
    
    # Refresh conversation status after discussion
    db.refresh(conversation)
    
    return ConversationResponse(
        id=conversation.id,
        goal_description=conversation.goal_description,
        status=conversation.status,
        final_summary=conversation.final_summary,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        message_count=conversation.message_count,
        is_waiting_for_user=conversation.is_waiting_for_user
    )


@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse, status_code=201)
async def create_message(
    conversation_id: uuid.UUID,
    message_data: MessageCreate,
    db: Session = Depends(get_db)
) -> MessageResponse:
    """
    Create a new message in a conversation.
    
    Args:
        conversation_id: Unique conversation identifier
        message_data: Message creation data
        db: Database session
        
    Returns:
        Created message information
        
    Raises:
        HTTPException: If conversation is not found or validation fails
    """
    # Verify conversation exists
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Validate parent message if specified
    if message_data.parent_message_id:
        parent_message = db.query(Message).filter(
            Message.id == message_data.parent_message_id,
            Message.conversation_id == conversation_id
        ).first()
        
        if not parent_message:
            raise HTTPException(status_code=400, detail="Parent message not found in this conversation")
    
    # Create new message
    message = Message(
        conversation_id=conversation_id,
        sender_type=message_data.sender_type,
        sender_id=message_data.sender_id,
        content=message_data.content,
        message_type=message_data.message_type,
        parent_message_id=message_data.parent_message_id,
        requires_user_response=message_data.requires_user_response
    )
    
    db.add(message)
    
    # Update conversation status based on message type
    if message_data.message_type == MessageType.QUESTION_TO_USER and message_data.requires_user_response:
        conversation.pause_for_user_input()
    elif message_data.message_type == MessageType.USER_RESPONSE and conversation.status == ConversationStatus.PAUSED:
        conversation.resume()
    
    db.commit()
    db.refresh(message)
    
    return MessageResponse(
        id=message.id,
        conversation_id=message.conversation_id,
        sender_type=message.sender_type,
        sender_id=message.sender_id,
        content=message.content,
        message_type=message.message_type,
        parent_message_id=message.parent_message_id,
        requires_user_response=message.requires_user_response,
        created_at=message.created_at,
        agent_name=message.agent_name,
        is_from_agent=message.is_from_agent,
        is_from_user=message.is_from_user,
        is_question_for_user=message.is_question_for_user
    )


@router.get("/conversations/{conversation_id}/messages", response_model=MessageList)
async def get_conversation_messages(
    conversation_id: uuid.UUID,
    skip: int = Query(0, ge=0, description="Number of messages to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of messages to return"),
    message_type: Optional[MessageType] = Query(None, description="Filter by message type"),
    sender_type: Optional[SenderType] = Query(None, description="Filter by sender type"),
    db: Session = Depends(get_db)
) -> MessageList:
    """
    Get messages from a conversation with optional filtering and pagination.
    
    Args:
        conversation_id: Unique conversation identifier
        skip: Number of messages to skip
        limit: Maximum number of messages to return
        message_type: Filter by message type
        sender_type: Filter by sender type
        db: Database session
        
    Returns:
        List of conversation messages
        
    Raises:
        HTTPException: If conversation is not found
    """
    # Verify conversation exists
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Build query
    query = db.query(Message).filter(Message.conversation_id == conversation_id)
    
    if message_type:
        query = query.filter(Message.message_type == message_type)
    
    if sender_type:
        query = query.filter(Message.sender_type == sender_type)
    
    # Get total count
    total_count = query.count()
    
    # Apply pagination and ordering
    messages = query.order_by(Message.created_at.asc()).offset(skip).limit(limit).all()
    
    # Convert to response format
    message_responses = [
        MessageResponse(
            id=msg.id,
            conversation_id=msg.conversation_id,
            sender_type=msg.sender_type,
            sender_id=msg.sender_id,
            content=msg.content,
            message_type=msg.message_type,
            parent_message_id=msg.parent_message_id,
            requires_user_response=msg.requires_user_response,
            created_at=msg.created_at,
            agent_name=msg.agent_name,
            is_from_agent=msg.is_from_agent,
            is_from_user=msg.is_from_user,
            is_question_for_user=msg.is_question_for_user
        )
        for msg in messages
    ]
    
    return MessageList(
        messages=message_responses,
        count=total_count,
        conversation_id=conversation_id
    )


@router.get("/conversations/{conversation_id}/messages/pending", response_model=MessageList)
async def get_pending_user_messages(
    conversation_id: uuid.UUID,
    db: Session = Depends(get_db)
) -> MessageList:
    """
    Get messages that require user response.
    
    Args:
        conversation_id: Unique conversation identifier
        db: Database session
        
    Returns:
        List of messages requiring user response
        
    Raises:
        HTTPException: If conversation is not found
    """
    # Verify conversation exists
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Get pending messages
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id,
        Message.requires_user_response == True
    ).order_by(Message.created_at.asc()).all()
    
    # Convert to response format
    message_responses = [
        MessageResponse(
            id=msg.id,
            conversation_id=msg.conversation_id,
            sender_type=msg.sender_type,
            sender_id=msg.sender_id,
            content=msg.content,
            message_type=msg.message_type,
            parent_message_id=msg.parent_message_id,
            requires_user_response=msg.requires_user_response,
            created_at=msg.created_at,
            agent_name=msg.agent_name,
            is_from_agent=msg.is_from_agent,
            is_from_user=msg.is_from_user,
            is_question_for_user=msg.is_question_for_user
        )
        for msg in messages
    ]
    
    return MessageList(
        messages=message_responses,
        count=len(message_responses),
        conversation_id=conversation_id
    )
