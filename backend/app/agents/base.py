"""
Abstract base class for all AI agents in the Multi-Agent AI Chat System.

This module defines the common interface that all agents must implement.
"""
from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.llm_service import LLMService

from app.agents.interfaces import (
    Message,
    Response,
    ConversationContext,
    Proposal,
    Vote,
    AgentState,
)

class BaseAgent(ABC):
    """Abstract base class for all agents."""

    def __init__(
        self,
        agent_id: str,
        name: str,
        role: str,
        personality_prompt: str,
        system_prompt: str,
        llm_service: "LLMService",
    ):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.personality_prompt = personality_prompt
        self.system_prompt = system_prompt
        self.llm_service = llm_service

    @abstractmethod
    async def process_message(self, message: Message) -> Response:
        """Process an incoming message and return a response."""
        pass

    @abstractmethod
    async def generate_response(self, context: ConversationContext) -> str:
        """Generate a response based on the conversation context."""
        pass

    @abstractmethod
    async def vote_on_proposal(self, proposal: Proposal) -> Vote:
        """Vote on a given proposal."""
        pass

    @abstractmethod
    def validate_response(self, response: str) -> bool:
        """Validate the agent's own response before sending."""
        pass

    @abstractmethod
    def get_agent_state(self) -> AgentState:
        """Get the current state of the agent."""
        pass
