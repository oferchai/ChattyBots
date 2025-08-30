#!/usr/bin/env python3
"""
Simple server startup script for Multi-Agent AI Chat System.

This script starts the FastAPI development server with proper configuration.
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Multi-Agent AI Chat System")
    print("📡 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 ReDoc Documentation: http://localhost:8000/redoc")
    print("\n✨ Available Endpoints:")
    print("  GET  /              - API information")
    print("  GET  /health        - Health check")
    print("  GET  /api/status    - System status")
    print("  GET  /api/agents    - List all agents")
    print("  POST /api/conversations - Create conversation")
    print("  GET  /api/conversations - List conversations")
    print("  WebSocket /ws/conversations/{id} - Real-time updates")
    print("\n🔥 Starting server...")
    
    uvicorn.run(
        "app.main:app",  # Use import string for reload to work properly
        host="127.0.0.1", 
        port=8000,
        log_level="info",
        reload=True,  # Auto-reload on code changes
        reload_dirs=["backend"]  # Only watch the backend directory for changes
    )
