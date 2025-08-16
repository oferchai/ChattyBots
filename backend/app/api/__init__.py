"""
API package for Multi-Agent AI Chat System.

This package contains all API route modules including:
- Conversation management endpoints
- Agent information endpoints  
- WebSocket endpoints for real-time communication

Example:
    from app.api import conversations, agents, websockets
    
    app.include_router(conversations.router, prefix="/api")
    app.include_router(agents.router, prefix="/api")
    app.include_router(websockets.router, prefix="/ws")
"""

from . import conversations, agents, websockets

__all__ = [
    "conversations",
    "agents", 
    "websockets",
]
