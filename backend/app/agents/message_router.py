"""
Message Router for the Multi-Agent AI Chat System.

This module is responsible for routing messages between agents and other
components of the system.
"""
from typing import List

from app.agents.interfaces import Message
from app.models.conversation import Conversation # Assuming conversation model exists

class MessageRouter:
    """Routes messages to the appropriate destination."""

    def __init__(self, conversation_manager: 'ConversationManager'):
        self.conversation_manager = conversation_manager

    async def route_message(self, message: Message, conversation: Conversation):
        """Routes a message to the appropriate agent or service."""
        # This is a simplified implementation. A real implementation would have
        # more complex routing logic based on the message type, conversation
        # state, and other factors.

        if message.sender == 'user':
            # If the message is from the user, it might be a response to a question
            # from an agent, or it could be a new instruction.
            # For now, we'll just broadcast it to all agents.
            await self.broadcast_to_agents(message, conversation)
        else:
            # If the message is from an agent, it might be a response to another
            # agent, a question to the user, or a proposal.
            # For now, we'll just broadcast it to all other agents.
            await self.broadcast_to_other_agents(message, conversation)

    async def broadcast_to_agents(self, message: Message, conversation: Conversation):
        """Broadcasts a message to all agents in a conversation."""
        agents = self.conversation_manager.get_agents_in_conversation(conversation.id)
        for agent in agents:
            await agent.process_message(message)

    async def broadcast_to_other_agents(self, message: Message, conversation: Conversation):
        """Broadcasts a message to all agents in a conversation except the sender."""
        agents = self.conversation_manager.get_agents_in_conversation(conversation.id)
        for agent in agents:
            if agent.agent_id != message.sender:
                await agent.process_message(message)
