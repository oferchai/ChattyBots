"""
Consensus Engine for the Multi-Agent AI Chat System.

This module handles voting and consensus building.
"""
from typing import List, Dict

from app.agents.interfaces import Proposal, Vote

class ConsensusEngine:
    """Manages the consensus-building process."""

    def __init__(self):
        self.proposals: Dict[str, Proposal] = {}
        self.votes: Dict[str, List[Vote]] = {}

    def add_proposal(self, proposal: Proposal):
        """Adds a new proposal to the consensus engine."""
        self.proposals[proposal.id] = proposal
        self.votes[proposal.id] = []

    def add_vote(self, vote: Vote):
        """Adds a vote for a proposal."""
        if vote.proposal_id not in self.proposals:
            raise ValueError(f"Proposal with id {vote.proposal_id} not found.")
        self.votes[vote.proposal_id].append(vote)

    def has_consensus(self, proposal_id: str, agent_count: int) -> bool:
        """Checks if a proposal has reached consensus."""
        if proposal_id not in self.votes:
            return False

        # Simple majority consensus for now
        return len(self.votes[proposal_id]) >= (agent_count // 2) + 1