"""
Flow Controller for the Multi-Agent AI Chat System.

This module manages the different phases of a conversation.
"""
from app.agents.interfaces import ConversationPhase

class FlowController:
    """Manages the flow and phase of a conversation."""

    def __init__(self):
        self.current_phase = ConversationPhase.INITIALIZATION

    def get_current_phase(self) -> ConversationPhase:
        """Returns the current phase of the conversation."""
        return self.current_phase

    def transition_to_next_phase(self):
        """Transitions the conversation to the next phase."""
        if self.current_phase == ConversationPhase.INITIALIZATION:
            self.current_phase = ConversationPhase.EXPLORATION
        elif self.current_phase == ConversationPhase.EXPLORATION:
            self.current_phase = ConversationPhase.DISCUSSION
        elif self.current_phase == ConversationPhase.DISCUSSION:
            self.current_phase = ConversationPhase.CONSENSUS
        elif self.current_phase == ConversationPhase.CONSENSUS:
            self.current_phase = ConversationPhase.COMPLETED