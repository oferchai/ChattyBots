"""
Unit tests for the ConsensusEngine.
"""
import pytest

from app.services.consensus_engine import ConsensusEngine
from app.agents.interfaces import Proposal, Vote

@pytest.fixture
def consensus_engine():
    """Fixture to create a ConsensusEngine."""
    return ConsensusEngine()

def test_add_proposal(consensus_engine: ConsensusEngine):
    """Test that a proposal can be added to the engine."""
    proposal = Proposal(id="prop1", title="Test Proposal", description="A test proposal.", proposed_by="agent1")
    consensus_engine.add_proposal(proposal)
    assert "prop1" in consensus_engine.proposals

def test_add_vote(consensus_engine: ConsensusEngine):
    """Test that a vote can be added for a proposal."""
    proposal = Proposal(id="prop1", title="Test Proposal", description="A test proposal.", proposed_by="agent1")
    consensus_engine.add_proposal(proposal)
    vote = Vote(proposal_id="prop1", agent_id="agent2", approve=True)
    consensus_engine.add_vote(vote)
    assert len(consensus_engine.votes["prop1"]) == 1

def test_has_consensus(consensus_engine: ConsensusEngine):
    """Test the has_consensus method."""
    proposal = Proposal(id="prop1", title="Test Proposal", description="A test proposal.", proposed_by="agent1")
    consensus_engine.add_proposal(proposal)
    
    vote1 = Vote(proposal_id="prop1", agent_id="agent2", approve=True)
    vote2 = Vote(proposal_id="prop1", agent_id="agent3", approve=True)
    
    consensus_engine.add_vote(vote1)
    assert not consensus_engine.has_consensus("prop1", agent_count=3)
    
    consensus_engine.add_vote(vote2)
    assert consensus_engine.has_consensus("prop1", agent_count=3)
