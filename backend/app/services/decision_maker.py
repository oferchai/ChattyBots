"""
Decision Maker for the Multi-Agent AI Chat System.

This module is responsible for compiling the final decision.
"""
from typing import List

from app.agents.interfaces import Proposal, Vote

class DecisionMaker:
    """Compiles the final decision of a conversation."""

    def compile_decision(self, proposal: Proposal, votes: List[Vote]) -> str:
        """Compiles the final decision based on the proposal and votes."""
        approved_votes = [vote for vote in votes if vote.approve]
        decision = f"Proposal '{proposal.title}' has been approved with {len(approved_votes)} votes.\n"
        decision += f"Description: {proposal.description}\n"
        decision += "\nVoting Summary:\n"
        for vote in votes:
            decision += f"- {vote.agent_id}: {'Approve' if vote.approve else 'Reject'}\n"
            if vote.reasoning:
                decision += f"  Reasoning: {vote.reasoning}\n"
        return decision