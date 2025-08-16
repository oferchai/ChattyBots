"""
Agent configuration and management for Multi-Agent AI Chat System.

This module provides access to static agent configurations and utilities
for working with AI agents in conversations.

Example:
    from app.agents import get_agent_config, AGENTS
    
    pm_config = get_agent_config("project_manager")
    print(pm_config.name)  # "Alex PM"
"""

from .config import (
    AgentConfig,
    AGENTS,
    get_agent_config,
    get_all_agents,
    get_agent_ids,
    is_valid_agent_id,
)

__all__ = [
    "AgentConfig",
    "AGENTS",
    "get_agent_config", 
    "get_all_agents",
    "get_agent_ids",
    "is_valid_agent_id",
]
