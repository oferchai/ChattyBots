"""
Pydantic schemas for Multi-Agent AI Chat System API.

This module defines request and response schemas for API endpoints,
providing data validation and documentation for the FastAPI application.
"""
import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .models import ConversationStatus, MessageType, SenderType


# Base schemas
class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    class Config:
        from_attributes = True
        use_enum_values = True


# Agent schemas
class AgentInfo(BaseSchema):
    """Agent information schema."""
    
    id: str = Field(..., description="Agent unique identifier")
    name: str = Field(..., description="Human-readable agent name")
    role: str = Field(..., description="Agent's role in conversations")
    personality_traits: List[str] = Field(..., description="Agent personality characteristics")
    expertise_areas: List[str] = Field(..., description="Areas of expertise")


class AgentList(BaseSchema):
    """Schema for listing all available agents."""
    
    agents: List[AgentInfo]
    count: int = Field(..., description="Total number of available agents")


# Message schemas  
class MessageCreate(BaseSchema):
    """Schema for creating a new message."""
    
    sender_type: SenderType = Field(..., description="Whether sender is agent or user")
    sender_id: str = Field(..., description="Agent ID or 'user'")
    content: str = Field(..., min_length=1, max_length=10000, description="Message content")
    message_type: MessageType = Field(..., description="Type of message")
    parent_message_id: Optional[uuid.UUID] = Field(None, description="Parent message for threading")
    requires_user_response: bool = Field(False, description="Whether message requires user response")


class MessageResponse(BaseSchema):
    """Schema for message response."""
    
    id: uuid.UUID
    conversation_id: uuid.UUID
    sender_type: SenderType
    sender_id: str
    content: str
    message_type: MessageType
    parent_message_id: Optional[uuid.UUID] = None
    requires_user_response: bool
    created_at: datetime
    
    # Additional computed fields
    agent_name: str = Field(..., description="Human-readable sender name")
    is_from_agent: bool = Field(..., description="Whether message is from an agent")
    is_from_user: bool = Field(..., description="Whether message is from a user")
    is_question_for_user: bool = Field(..., description="Whether this requires user response")


class MessageList(BaseSchema):
    """Schema for listing messages."""
    
    messages: List[MessageResponse]
    count: int = Field(..., description="Total number of messages")
    conversation_id: uuid.UUID = Field(..., description="Parent conversation ID")


# Conversation schemas
class ConversationCreate(BaseSchema):
    """Schema for creating a new conversation."""
    
    goal_description: str = Field(
        ..., 
        min_length=10, 
        max_length=2000,
        description="Description of the goal or problem to solve"
    )


class ConversationUpdate(BaseSchema):
    """Schema for updating a conversation."""
    
    status: Optional[ConversationStatus] = Field(None, description="Conversation status")
    final_summary: Optional[str] = Field(None, description="Final summary when completed")


class ConversationResponse(BaseSchema):
    """Schema for conversation response."""
    
    id: uuid.UUID
    goal_description: str
    status: ConversationStatus
    final_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Additional computed fields
    message_count: int = Field(..., description="Number of messages in conversation")
    is_waiting_for_user: bool = Field(..., description="Whether conversation is paused for user input")


class ConversationDetail(ConversationResponse):
    """Schema for detailed conversation response including messages."""
    
    messages: List[MessageResponse] = Field(..., description="All messages in the conversation")


class ConversationList(BaseSchema):
    """Schema for listing conversations."""
    
    conversations: List[ConversationResponse] 
    count: int = Field(..., description="Total number of conversations")


# System schemas
class SystemStatus(BaseSchema):
    """Schema for system status response."""
    
    status: str = Field(..., description="Overall system status")
    database: dict = Field(..., description="Database information")
    agents: dict = Field(..., description="Agent information")
    features: List[str] = Field(..., description="Available system features")


class HealthCheck(BaseSchema):
    """Schema for health check response."""
    
    status: str = Field(..., description="Health status")
    service: str = Field(..., description="Service name")
    timestamp: str = Field(..., description="Current timestamp")


# WebSocket schemas
class WebSocketMessage(BaseSchema):
    """Schema for WebSocket messages."""
    
    type: str = Field(..., description="Message type")
    conversation_id: uuid.UUID = Field(..., description="Related conversation ID")
    data: dict = Field(..., description="Message payload")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Message timestamp")


# Error schemas
class ErrorResponse(BaseSchema):
    """Schema for error responses."""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    type: str = Field(..., description="Error category")
    path: Optional[str] = Field(None, description="Request path where error occurred")
