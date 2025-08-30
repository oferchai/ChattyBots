#!/usr/bin/env python3
"""
Manual API test script for Multi-Agent AI Chat System.

Run this script after starting the server with: python run_server.py
"""
import json
import time
import requests

BASE_URL = "http://localhost:8000"

def test_api():
    """Test the API endpoints manually."""
    print("🧪 Testing Multi-Agent AI Chat System API")
    print(f"📡 Testing server at: {BASE_URL}")
    
    try:
        # Test health endpoint
        print("\n❤️  Testing health endpoint...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        if response.ok:
            data = response.json()
            print(f"Health: {data['status']}")
        
        # Test system status
        print("\n📊 Testing system status...")
        response = requests.get(f"{BASE_URL}/api/status")
        print(f"Status: {response.status_code}")
        if response.ok:
            data = response.json()
            print(f"System: {data['status']}")
            print(f"Database: {data['database']['type']}")
            print(f"Agents: {data['agents']['count']}")
        
        # Test agents
        print("\n🤖 Testing agents endpoint...")
        response = requests.get(f"{BASE_URL}/api/agents")
        print(f"Status: {response.status_code}")
        if response.ok:
            data = response.json()
            print(f"Found {data['count']} agents:")
            for agent in data['agents']:
                print(f"  - {agent['name']} ({agent['role']})")
        
        # Test creating conversation
        print("\n💬 Testing conversation creation...")
        conversation_data = {
            "goal_description": "Test conversation created via API test"
        }
        response = requests.post(f"{BASE_URL}/api/conversations", json=conversation_data)
        print(f"Status: {response.status_code}")
        if response.ok:
            conv_data = response.json()
            print(f"Created: {conv_data['id']}")
            print(f"Goal: {conv_data['goal_description'][:50]}...")
            conversation_id = conv_data['id']
            
            # Test creating message
            print("\n💭 Testing message creation...")
            message_data = {
                "sender_type": "user",
                "sender_id": "user", 
                "content": "Hello from API test! This is a test message.",
                "message_type": "user_response"
            }
            response = requests.post(f"{BASE_URL}/api/conversations/{conversation_id}/messages", json=message_data)
            print(f"Status: {response.status_code}")
            if response.ok:
                msg_data = response.json()
                print(f"Message ID: {msg_data['id']}")
                print(f"From: {msg_data['agent_name']}")
                print(f"Content: {msg_data['content'][:40]}...")
        
        print("\n✅ API tests completed successfully!")
        print("📚 View full API docs at: http://localhost:8000/docs")
        
    except requests.ConnectionError:
        print("❌ Could not connect to server!")
        print("💡 Make sure the server is running: python run_server.py")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_api()
