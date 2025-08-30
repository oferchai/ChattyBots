"""
Conversation Manager for the Multi-Agent AI Chat System.

This module is the core orchestrator for conversations.
"""
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.agents.agent_manager import AgentManager
from app.agents.interfaces import Message, ConversationContext, ConversationPhase
from app.models.conversation import Conversation # Assuming conversation model exists
from app.services.flow_controller import FlowController
from app.services.consensus_engine import ConsensusEngine
from app.services.decision_maker import DecisionMaker

class ConversationManager:
    """Manages the lifecycle of a single conversation."""

    def __init__(self, agent_manager: "AgentManager", conversation: Conversation):
        self.agent_manager = agent_manager
        self.conversation = conversation
        self.flow_controller = FlowController()
        self.consensus_engine = ConsensusEngine()
        self.decision_maker = DecisionMaker()
        self.conversation_history: List[Message] = []

    async def start(self):
        """Starts the conversation."""
        # Initial message to the agents
        initial_message = Message(sender="system", content=f"New conversation started with goal: {self.conversation.goal_description}")
        self.conversation_history.append(initial_message)
        await self.run_conversation_loop()

    async def run_conversation_loop(self):
        """The main loop that drives the conversation."""
        while self.flow_controller.get_current_phase() != ConversationPhase.COMPLETED:
            current_phase = self.flow_controller.get_current_phase()
            print(f"Conversation {self.conversation.id} is in phase: {current_phase}")

            if current_phase == ConversationPhase.INITIALIZATION:
                # In the initialization phase, each agent gets to ask a clarifying question.
                await self.initialization_phase()
                self.flow_controller.transition_to_next_phase()

            elif current_phase == ConversationPhase.EXPLORATION:
                # In the exploration phase, agents generate ideas.
                await self.exploration_phase()
                self.flow_controller.transition_to_next_phase()

            elif current_phase == ConversationPhase.DISCUSSION:
                # In the discussion phase, agents discuss the ideas.
                await self.discussion_phase()
                self.flow_controller.transition_to_next_phase()

            elif current_phase == ConversationPhase.CONSENSUS:
                # In the consensus phase, agents vote on proposals.
                await self.consensus_phase()
                self.flow_controller.transition_to_next_phase()

    async def initialization_phase(self):
        """The initialization phase of the conversation."""
        for agent in self.agent_manager.get_all_agents():
            context = ConversationContext(
                conversation_history=self.conversation_history,
                current_goal=self.conversation.goal_description,
            )
            response = await agent.generate_response(context)
            message = Message(sender=agent.agent_id, content=response)
            self.conversation_history.append(message)

    async def exploration_phase(self):
        """The exploration phase of the conversation."""
        # Placeholder for exploration phase logic
        pass

    async def discussion_phase(self):
        """The discussion phase of the conversation."""
        # Placeholder for discussion phase logic
        pass

    async def consensus_phase(self):
        """The consensus phase of the conversation."""
        # Placeholder for consensus phase logic
        pass