"""
Unit tests for the DecisionMaker.
"""
import pytest

from app.services.decision_maker import DecisionMaker
from app.agents.interfaces import Proposal, Vote

@pytest.fixture
def decision_maker():
    """Fixture to create a DecisionMaker."""
    return DecisionMaker()

def test_compile_decision(decision_maker: DecisionMaker):
    """Test the compile_decision method."""
    proposal = Proposal(id="prop1", title="Test Proposal", description="A test proposal.", proposed_by="agent1")
    votes = [
        Vote(proposal_id="prop1", agent_id="agent2", approve=True),
        Vote(proposal_id="prop1", agent_id="agent3", approve=False, reasoning="Not good enough."),
    ]
    
    decision = decision_maker.compile_decision(proposal, votes)
    
    assert "Proposal 'Test Proposal' has been approved with 1 votes." in decision
    assert "Description: A test proposal." in decision
    assert "- agent2: Approve" in decision
    assert "- agent3: Reject" in decision
    assert "Reasoning: Not good enough." in decision
