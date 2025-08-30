"""
Data interfaces for the Multi-Agent AI Chat System.

This module defines the Pydantic models used for communication and data
exchange between agents, the conversation manager, and other services.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
import uuid

class ConversationPhase(str, Enum):
    """Represents the different phases of a conversation."""
    INITIALIZATION = "initialization"
    EXPLORATION = "exploration"
    DISCUSSION = "discussion"
    CONSENSUS = "consensus"
    COMPLETED = "completed"


class Message(BaseModel):
    """Represents a single message in a conversation."""
    content: str
    sender: str # agent_id or 'user'

class Response(BaseModel):
    """Represents a response from an agent."""
    content: str

class ConversationContext(BaseModel):
    """Holds the context of the conversation for an agent."""
    conversation_history: List[Message]
    current_goal: str

class Proposal(BaseModel):
    """Represents a proposed solution or idea."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    proposed_by: str # agent_id

class Vote(BaseModel):
    """Represents an agent's vote on a proposal."""
    proposal_id: str
    agent_id: str
    approve: bool
    reasoning: Optional[str] = None

class AgentState(BaseModel):
    """Represents the current state of an agent."""
    agent_id: str
    is_active: bool
    current_task: Optional[str] = None
