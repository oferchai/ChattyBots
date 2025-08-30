"""
Agent Manager for the Multi-Agent AI Chat System.

This module is responsible for creating, initializing, and managing agents.
"""
from typing import Dict, List, Type

from app.agents.base import BaseAgent
from app.agents.config import get_all_agents, AgentConfig
from app.services.llm_service import LLMService # Assuming llm_service is in app.services
from app.agents.specific_agents import (
    ProjectManagerAgent,
    TechnicalArchitectAgent,
    CreativeStrategistAgent,
    QualityAssuranceAgent,
    ResourceCoordinatorAgent,
)

AGENT_ROLE_TO_CLASS: Dict[str, Type[BaseAgent]] = {
    "Project Manager": ProjectManagerAgent,
    "Technical Architect": TechnicalArchitectAgent,
    "Creative Strategist": CreativeStrategistAgent,
    "Quality Assurance": QualityAssuranceAgent,
    "Resource Coordinator": ResourceCoordinatorAgent,
}


class AgentManager:
    """Manages the lifecycle of all agents."""

    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        self.agents: Dict[str, BaseAgent] = self._create_agents()

    def _create_agents(self) -> Dict[str, BaseAgent]:
        """Create all agents from the configuration."""
        agents: Dict[str, BaseAgent] = {}
        agent_configs = get_all_agents()
        for agent_id, config in agent_configs.items():
            agents[agent_id] = self._create_agent_from_config(agent_id, config)
        return agents

    def _create_agent_from_config(self, agent_id: str, config: AgentConfig) -> BaseAgent:
        """Creates a single agent from its configuration."""
        agent_class = AGENT_ROLE_TO_CLASS.get(config.role)
        if not agent_class:
            raise ValueError(f"Unknown agent role: {config.role}")

        return agent_class(
            agent_id=agent_id,
            name=config.name,
            role=config.role,
            personality_prompt=config.system_prompt, # Simplified for now
            system_prompt=config.system_prompt,
            llm_service=self.llm_service,
        )

    def get_agent(self, agent_id: str) -> BaseAgent:
        """Get an agent by its ID."""
        if agent_id not in self.agents:
            raise KeyError(f"Agent '{agent_id}' not found.")
        return self.agents[agent_id]

    def get_all_agents(self) -> List[BaseAgent]:
        """Get a list of all agents."""
        return list(self.agents.values())
