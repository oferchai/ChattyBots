#!/usr/bin/env python3
"""
Test script for FastAPI application in Multi-Agent AI Chat System.

This script tests the FastAPI application by making HTTP requests
to the API endpoints and verifying responses.
"""
import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, Any

import httpx

# Add backend app to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))


class APITester:
    """Simple API testing class."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)
    
    async def get(self, endpoint: str) -> Dict[Any, Any]:
        """Make GET request to endpoint."""
        response = await self.client.get(endpoint)
        response.raise_for_status()
        return response.json()
    
    async def post(self, endpoint: str, data: Dict[Any, Any]) -> Dict[Any, Any]:
        """Make POST request to endpoint."""
        response = await self.client.post(endpoint, json=data)
        response.raise_for_status()
        return response.json()
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


async def test_basic_endpoints():
    """Test basic API endpoints."""
    print("🚀 Testing FastAPI Application Endpoints\n")
    
    tester = APITester()
    
    try:
        # Test root endpoint
        print("📍 Testing root endpoint...")
        root_response = await tester.get("/")
        print(f"  Root: {root_response['name']} - {root_response['status']}")
        
        # Test health check
        print("❤️  Testing health endpoint...")
        health_response = await tester.get("/health")
        print(f"  Health: {health_response['status']}")
        
        # Test system status
        print("📊 Testing system status...")
        status_response = await tester.get("/api/status")
        print(f"  Status: {status_response['status']}")
        print(f"  Database: {status_response['database']['type']}")
        print(f"  Agents: {status_response['agents']['count']} available")
        
        # Test agents endpoint
        print("🤖 Testing agents endpoint...")
        agents_response = await tester.get("/api/agents")
        print(f"  Found {agents_response['count']} agents:")
        for agent in agents_response['agents']:
            print(f"    - {agent['name']} ({agent['role']})")
        
        # Test specific agent
        print("🔍 Testing specific agent endpoint...")
        agent_response = await tester.get("/api/agents/project_manager")
        print(f"  Agent: {agent_response['name']} - {agent_response['role']}")
        print(f"  Traits: {', '.join(agent_response['personality_traits'][:3])}...")
        
        # Test creating conversation
        print("💬 Testing conversation creation...")
        conversation_data = {
            "goal_description": "Test conversation for API verification"
        }
        conv_response = await tester.post("/api/conversations", conversation_data)
        print(f"  Created conversation: {conv_response['id']}")
        print(f"  Goal: {conv_response['goal_description']}")
        print(f"  Status: {conv_response['status']}")
        
        conversation_id = conv_response['id']
        
        # Test getting conversation
        print("📖 Testing conversation retrieval...")
        conv_detail = await tester.get(f"/api/conversations/{conversation_id}")
        print(f"  Retrieved conversation: {conv_detail['goal_description']}")
        print(f"  Message count: {conv_detail['message_count']}")
        
        # Test creating message
        print("💭 Testing message creation...")
        message_data = {
            "sender_type": "user",
            "sender_id": "user",
            "content": "This is a test message for API verification",
            "message_type": "user_response"
        }
        msg_response = await tester.post(f"/api/conversations/{conversation_id}/messages", message_data)
        print(f"  Created message: {msg_response['id']}")
        print(f"  From: {msg_response['agent_name']}")
        print(f"  Content: {msg_response['content'][:50]}...")
        
        # Test getting messages
        print("📝 Testing message retrieval...")
        messages_response = await tester.get(f"/api/conversations/{conversation_id}/messages")
        print(f"  Retrieved {messages_response['count']} messages")
        
        # Test listing conversations
        print("📚 Testing conversation listing...")
        conversations_response = await tester.get("/api/conversations")
        print(f"  Found {conversations_response['count']} conversations")
        
        print("\n✅ All API endpoint tests passed successfully!")
        
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP Error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        raise
    finally:
        await tester.close()


def start_server_background():
    """Start FastAPI server in background for testing."""
    import subprocess
    import time
    
    print("🔧 Starting FastAPI server...")
    
    # Start server in background
    server_process = subprocess.Popen([
        sys.executable, "-c",
        """
import sys
from pathlib import Path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

import uvicorn
from app.main import app

uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
        """
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    return server_process


def check_server_running():
    """Check if server is already running."""
    try:
        import httpx
        response = httpx.get("http://localhost:8000/health", timeout=2)
        return response.status_code == 200
    except:
        return False


async def main():
    """Run the API tests."""
    server_process = None
    
    try:
        # Check if server is already running
        if not check_server_running():
            server_process = start_server_background()
            
            # Wait a bit more for server to be fully ready
            await asyncio.sleep(2)
        else:
            print("📡 Server is already running")
        
        # Run tests
        await test_basic_endpoints()
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        raise
    finally:
        # Clean up server process if we started it
        if server_process:
            print("🛑 Stopping test server...")
            server_process.terminate()
            server_process.wait()


if __name__ == "__main__":
    asyncio.run(main())
