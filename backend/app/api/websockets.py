"""
WebSocket API endpoints for Multi-Agent AI Chat System.

This module provides WebSocket endpoints for real-time communication
during conversations, including live message updates and status changes.
"""
import json
import logging
import uuid
from typing import Dict, List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..models import Conversation


logger = logging.getLogger(__name__)
router = APIRouter()


class ConnectionManager:
    """
    WebSocket connection manager.
    
    Manages active WebSocket connections for real-time communication
    during conversations, supporting broadcasting messages to specific
    conversation participants.
    """
    
    def __init__(self):
        # Dictionary: conversation_id -> List of WebSocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, conversation_id: str) -> None:
        """
        Accept a new WebSocket connection for a conversation.
        
        Args:
            websocket: WebSocket connection
            conversation_id: Unique conversation identifier
        """
        await websocket.accept()
        
        if conversation_id not in self.active_connections:
            self.active_connections[conversation_id] = []
        
        self.active_connections[conversation_id].append(websocket)
        logger.info(f"WebSocket connected to conversation {conversation_id}")
        
        # Send welcome message
        await websocket.send_text(json.dumps({
            "type": "connection_established",
            "conversation_id": conversation_id,
            "message": "Connected to conversation"
        }))
    
    def disconnect(self, websocket: WebSocket, conversation_id: str) -> None:
        """
        Remove a WebSocket connection.
        
        Args:
            websocket: WebSocket connection to remove
            conversation_id: Conversation the connection was associated with
        """
        if conversation_id in self.active_connections:
            if websocket in self.active_connections[conversation_id]:
                self.active_connections[conversation_id].remove(websocket)
                logger.info(f"WebSocket disconnected from conversation {conversation_id}")
            
            # Clean up empty conversation lists
            if not self.active_connections[conversation_id]:
                del self.active_connections[conversation_id]
    
    async def send_personal_message(self, message: dict, websocket: WebSocket) -> None:
        """
        Send a message to a specific WebSocket connection.
        
        Args:
            message: Message data to send
            websocket: Target WebSocket connection
        """
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
    
    async def broadcast_to_conversation(self, message: dict, conversation_id: str) -> None:
        """
        Broadcast a message to all connections in a conversation.
        
        Args:
            message: Message data to broadcast
            conversation_id: Target conversation ID
        """
        if conversation_id not in self.active_connections:
            return
        
        # Create list copy to avoid modification during iteration
        connections = self.active_connections[conversation_id].copy()
        
        for websocket in connections:
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting to conversation {conversation_id}: {e}")
                # Remove failed connection
                self.disconnect(websocket, conversation_id)
    
    def get_connection_count(self, conversation_id: str) -> int:
        """Get number of active connections for a conversation."""
        return len(self.active_connections.get(conversation_id, []))


# Global connection manager instance
manager = ConnectionManager()


@router.websocket("/conversations/{conversation_id}")
async def websocket_conversation(websocket: WebSocket, conversation_id: str):
    """
    WebSocket endpoint for real-time conversation updates.
    
    Args:
        websocket: WebSocket connection
        conversation_id: Unique conversation identifier
        
    Provides real-time updates for:
    - New messages in the conversation
    - Conversation status changes
    - Agent typing indicators
    - System notifications
    """
    # Validate conversation exists
    db = SessionLocal()
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == uuid.UUID(conversation_id)
        ).first()
        
        if not conversation:
            await websocket.close(code=4004, reason="Conversation not found")
            return
            
    except ValueError:
        await websocket.close(code=4000, reason="Invalid conversation ID format")
        return
    except Exception as e:
        logger.error(f"Error validating conversation: {e}")
        await websocket.close(code=4003, reason="Server error")
        return
    finally:
        db.close()
    
    # Accept connection
    await manager.connect(websocket, conversation_id)
    
    try:
        while True:
            # Wait for messages from client
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                await handle_websocket_message(message, conversation_id, websocket)
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON format"
                }))
            except Exception as e:
                logger.error(f"Error handling WebSocket message: {e}")
                await websocket.send_text(json.dumps({
                    "type": "error", 
                    "message": "Error processing message"
                }))
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, conversation_id)
        logger.info(f"Client disconnected from conversation {conversation_id}")


async def handle_websocket_message(message: dict, conversation_id: str, websocket: WebSocket) -> None:
    """
    Handle incoming WebSocket messages.
    
    Args:
        message: Parsed message data from client
        conversation_id: Associated conversation ID
        websocket: Source WebSocket connection
    """
    message_type = message.get("type", "unknown")
    
    if message_type == "ping":
        # Heartbeat/ping message
        await websocket.send_text(json.dumps({
            "type": "pong",
            "timestamp": message.get("timestamp")
        }))
    
    elif message_type == "subscribe_to_updates":
        # Client wants to receive all conversation updates
        await websocket.send_text(json.dumps({
            "type": "subscription_confirmed",
            "conversation_id": conversation_id,
            "updates": ["messages", "status_changes", "agent_activity"]
        }))
    
    elif message_type == "get_status":
        # Client requests current conversation status
        db = SessionLocal()
        try:
            conversation = db.query(Conversation).filter(
                Conversation.id == uuid.UUID(conversation_id)
            ).first()
            
            if conversation:
                await websocket.send_text(json.dumps({
                    "type": "status_update",
                    "conversation_id": conversation_id,
                    "status": conversation.status.value,
                    "message_count": conversation.message_count,
                    "is_waiting_for_user": conversation.is_waiting_for_user
                }))
        finally:
            db.close()
    
    else:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": f"Unknown message type: {message_type}"
        }))


# Utility functions for broadcasting from other parts of the application
async def broadcast_new_message(conversation_id: str, message_data: dict) -> None:
    """
    Broadcast a new message to all connections in a conversation.
    
    Args:
        conversation_id: Target conversation ID
        message_data: Message information to broadcast
    """
    await manager.broadcast_to_conversation({
        "type": "new_message",
        "conversation_id": conversation_id,
        "data": message_data
    }, conversation_id)


async def broadcast_status_change(conversation_id: str, new_status: str, additional_data: dict = None) -> None:
    """
    Broadcast a conversation status change to all connections.
    
    Args:
        conversation_id: Target conversation ID
        new_status: New conversation status
        additional_data: Additional status information
    """
    message = {
        "type": "status_change",
        "conversation_id": conversation_id,
        "new_status": new_status
    }
    
    if additional_data:
        message.update(additional_data)
    
    await manager.broadcast_to_conversation(message, conversation_id)


async def broadcast_agent_activity(conversation_id: str, agent_id: str, activity: str) -> None:
    """
    Broadcast agent activity (like typing) to all connections.
    
    Args:
        conversation_id: Target conversation ID
        agent_id: Agent performing the activity
        activity: Type of activity (typing, thinking, etc.)
    """
    await manager.broadcast_to_conversation({
        "type": "agent_activity",
        "conversation_id": conversation_id,
        "agent_id": agent_id,
        "activity": activity
    }, conversation_id)
