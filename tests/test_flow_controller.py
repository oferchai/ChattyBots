"""
Unit tests for the FlowController.
"""
import pytest

from app.services.flow_controller import FlowController
from app.agents.interfaces import ConversationPhase

def test_flow_controller_initialization():
    """Test that the FlowController initializes in the INITIALIZATION phase."""
    flow_controller = FlowController()
    assert flow_controller.get_current_phase() == ConversationPhase.INITIALIZATION

def test_flow_controller_transitions():
    """Test that the FlowController correctly transitions through all phases."""
    flow_controller = FlowController()
    
    flow_controller.transition_to_next_phase()
    assert flow_controller.get_current_phase() == ConversationPhase.EXPLORATION
    
    flow_controller.transition_to_next_phase()
    assert flow_controller.get_current_phase() == ConversationPhase.DISCUSSION
    
    flow_controller.transition_to_next_phase()
    assert flow_controller.get_current_phase() == ConversationPhase.CONSENSUS
    
    flow_controller.transition_to_next_phase()
    assert flow_controller.get_current_phase() == ConversationPhase.COMPLETED
