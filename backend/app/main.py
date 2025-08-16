"""
Main FastAPI application for Multi-Agent AI Chat System.

This module creates and configures the FastAPI application with all necessary
middleware, error handling, and API routes.
"""
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .db import init_database
from .api import conversations, agents, websockets
from .middleware.logging import LoggingMiddleware
from .middleware.error_handler import ErrorHandlerMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    
    Handles startup and shutdown events for the FastAPI application,
    including database initialization and cleanup.
    """
    # Startup
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('./data/app.log')
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting Multi-Agent AI Chat System")
    
    # Initialize database
    init_database()
    logger.info("Database initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Multi-Agent AI Chat System")


# Create FastAPI application
app = FastAPI(
    title="Multi-Agent AI Chat System",
    description="""
    A backend API for coordinating multiple AI agents in collaborative 
    problem-solving conversations.
    
    ## Features
    
    * **Multi-Agent Conversations**: Coordinate multiple AI agents with different roles
    * **User Interaction**: Agents can ask users questions during discussions  
    * **Real-time Updates**: WebSocket support for live conversation updates
    * **Message Threading**: Organize conversations with reply threading
    * **Agent Management**: Access to configured AI agents and their capabilities
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React development
        "http://localhost:8501",  # Streamlit
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(ErrorHandlerMiddleware)

# Include API routes
app.include_router(conversations.router, prefix="/api", tags=["Conversations"])
app.include_router(agents.router, prefix="/api", tags=["Agents"])
app.include_router(websockets.router, prefix="/ws", tags=["WebSocket"])


@app.get("/", response_model=dict)
async def root():
    """
    Root endpoint providing API information.
    
    Returns:
        Basic information about the API
    """
    return {
        "name": "Multi-Agent AI Chat System",
        "version": "1.0.0",
        "description": "Backend API for coordinating AI agent conversations",
        "status": "active",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", response_model=dict)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        System health status
    """
    return {
        "status": "healthy",
        "service": "multi-agent-chat-system",
        "timestamp": "2025-08-16T11:35:00Z"
    }


@app.get("/api/status", response_model=dict)
async def system_status():
    """
    System status endpoint with detailed information.
    
    Returns:
        Detailed system status including database and agent information
    """
    from .agents import get_agent_ids
    from .db import DATABASE_URL
    
    return {
        "status": "operational",
        "database": {
            "url": DATABASE_URL.split("///")[-1] if "sqlite" in DATABASE_URL else "configured",
            "type": "sqlite" if "sqlite" in DATABASE_URL else "other"
        },
        "agents": {
            "count": len(get_agent_ids()),
            "available": get_agent_ids()
        },
        "features": [
            "multi_agent_conversations",
            "user_interaction",
            "message_threading", 
            "websocket_updates",
            "conversation_history"
        ]
    }


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "path": str(request.url.path)
        }
    )


@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    """Handle 500 errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error", 
            "message": "An unexpected error occurred"
        }
    )
