"""
Main FastAPI application for Multi-Agent AI Chat System.

This module creates and configures the FastAPI application with all necessary
middleware, error handling, and API routes using the comprehensive configuration system.
"""
import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from backend.config import get_settings
from .db import init_database
from .api import conversations, agents, websockets
from .middleware.logging import LoggingMiddleware
from .middleware.error_handler import ErrorHandlerMiddleware
from .services.llm_service import LLMServiceFactory

# Get application settings
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    
    Handles startup and shutdown events for the FastAPI application,
    including database initialization and cleanup using new configuration system.
    """
    # Configure logging based on settings
    logging.basicConfig(
        level=getattr(logging, settings.logging.level.value),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' if not settings.logging.json_format
        else None,  # JSON formatting would be handled by a JSON formatter
        handlers=[
            logging.StreamHandler() if settings.logging.console_output else logging.NullHandler(),
            logging.FileHandler(settings.logging.file_path) if settings.logging.file_path else logging.NullHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Starting {settings.app_name} v{settings.version}")
    logger.info(f"Environment: {settings.environment.value}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"LLM Provider: {settings.llm.provider.value}")
    
    # Validate production readiness if needed
    if settings.is_production:
        issues = settings.validate_production_readiness()
        if issues:
            logger.warning(f"Production configuration issues: {'; '.join(issues)}")
    
    try:
        # Initialize database
        init_database()
        logger.info("Database initialized successfully")
        yield
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
    finally:
        # Shutdown
        logger.info(f"Shutting down {settings.app_name}")


# Create FastAPI application with new configuration
app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.version,
    debug=settings.debug,
    lifespan=lifespan,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
    openapi_url="/openapi.json" if not settings.is_production else None,
)

# Add CORS middleware with new configuration
app.add_middleware(
    CORSMiddleware,
    **settings.get_cors_config()
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
        "name": settings.app_name,
        "version": settings.version,
        "description": settings.description,
        "environment": settings.environment.value,
        "status": "active",
        "docs": "/docs" if not settings.is_production else "disabled",
        "redoc": "/redoc" if not settings.is_production else "disabled"
    }


@app.get("/health", response_model=dict)
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        System health status with timestamp
    """
    try:
        return {
            "status": "healthy",
            "service": "multi-agent-chat-system",
            "version": settings.version,
            "environment": settings.environment.value,
            "timestamp": time.time(),
            "database": "connected",
            "llm_provider": settings.llm.provider.value
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


@app.get("/api/config", response_model=dict)
async def get_config_info():
    """
    Get public configuration information.
    
    Returns:
        Non-sensitive configuration details
    """
    return {
        "app_name": settings.app_name,
        "version": settings.version,
        "environment": settings.environment.value,
        "debug": settings.debug and not settings.is_production,
        "llm_provider": settings.llm.provider.value,
        "max_conversation_rounds": settings.agents.max_conversation_rounds,
        "consensus_threshold": settings.agents.consensus_threshold,
        "features": {
            "websockets": True,
            "agent_conversations": True,
            "message_threading": True,
        }
    }


@app.get("/api/status", response_model=dict)
async def system_status():
    """
    System status endpoint with detailed information.
    
    Returns:
        Detailed system status including database and agent information
    """
    from .agents import get_agent_ids
    
    llm_service_factory = LLMServiceFactory(config=settings.llm.model_dump())
    llm_health = await llm_service_factory.provider.health_check()

    return {
        "status": "operational",
        "environment": settings.environment.value,
        "version": settings.version,
        "database": {
            "url": settings.database.url.split("///")[-1] if "sqlite" in settings.database.url else "configured",
            "type": "sqlite" if "sqlite" in settings.database.url else "other"
        },
        "llm": {
            "provider": settings.llm.provider.value,
            "fallback_strategy": settings.llm.fallback_strategy,
            "max_tokens": settings.llm.max_tokens,
            "temperature": settings.llm.temperature,
            "health_status": "healthy" if llm_health else "unhealthy"
        },
        "agents": {
            "count": len(get_agent_ids()),
            "available": get_agent_ids(),
            "max_rounds": settings.agents.max_conversation_rounds,
            "consensus_threshold": settings.agents.consensus_threshold,
            "response_timeout": settings.agents.response_timeout
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
    logger = logging.getLogger(__name__)
    logger.error(
        f"Unhandled exception: {exc}",
        exc_info=True
    )
    
    if settings.is_production:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error", 
                "message": "An unexpected error occurred"
            }
        )
    else:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error", 
                "message": str(exc),
                "type": type(exc).__name__
            }
        )


if __name__ == "__main__":
    # Run application with configuration
    uvicorn.run(
        "backend.app.main:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.reload and settings.is_development,
        workers=1 if settings.server.reload else settings.server.workers,
        access_log=settings.server.access_log,
        log_level=settings.logging.level.value.lower(),
        ssl_keyfile=settings.server.ssl_keyfile,
        ssl_certfile=settings.server.ssl_certfile,
    )
