"""
Agents API endpoints for Multi-Agent AI Chat System.

This module provides REST API endpoints for accessing information
about available AI agents and their configurations.
"""
from fastapi import APIRouter, HTTPException

from ..agents import get_agent_config, get_all_agents, get_agent_ids, is_valid_agent_id
from ..schemas import AgentInfo, AgentList


router = APIRouter()


@router.get("/agents", response_model=AgentList)
async def list_agents() -> AgentList:
    """
    List all available AI agents.
    
    Returns:
        List of all configured agents with their information
    """
    all_agents = get_all_agents()
    
    agent_infos = [
        AgentInfo(
            id=agent_id,
            name=config.name,
            role=config.role,
            personality_traits=config.personality_traits,
            expertise_areas=config.expertise_areas
        )
        for agent_id, config in all_agents.items()
    ]
    
    return AgentList(
        agents=agent_infos,
        count=len(agent_infos)
    )


@router.get("/agents/{agent_id}", response_model=AgentInfo)
async def get_agent_details(agent_id: str) -> AgentInfo:
    """
    Get detailed information about a specific agent.
    
    Args:
        agent_id: Unique identifier for the agent
        
    Returns:
        Detailed agent information including personality and expertise
        
    Raises:
        HTTPException: If agent is not found
    """
    if not is_valid_agent_id(agent_id):
        available_agents = get_agent_ids()
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{agent_id}' not found. Available agents: {available_agents}"
        )
    
    config = get_agent_config(agent_id)
    
    return AgentInfo(
        id=agent_id,
        name=config.name,
        role=config.role,
        personality_traits=config.personality_traits,
        expertise_areas=config.expertise_areas
    )
