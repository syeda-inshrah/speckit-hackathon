#!/usr/bin/env python3
"""Test script to verify Groq chatbot integration"""
import requests
import json

BASE_URL = "http://localhost:7860"

def test_health():
    """Test health endpoint"""
    print("1. Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    return response.status_code == 200

def test_signup():
    """Create a test user"""
    print("\n2. Creating test user...")
    data = {
        "email": "groq_test@example.com",
        "password": "testpass123",
        "name": "Groq Test User"
    }
    response = requests.post(f"{BASE_URL}/api/auth/signup", json=data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   User ID: {result.get('user', {}).get('id')}")
        return result
    else:
        print(f"   Error: {response.text}")
        return None

def test_signin():
    """Sign in to get token"""
    print("\n3. Signing in...")
    data = {
        "email": "groq_test@example.com",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/signin", json=data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Token received: {result.get('access_token')[:20]}...")
        return result
    else:
        print(f"   Error: {response.text}")
        return None

def test_chat(user_id, token):
    """Test chat endpoint with Groq"""
    print("\n4. Testing chat with Groq...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "message": "Create a task to test Groq integration",
        "user_id": user_id
    }

    print(f"   Sending message: '{data['message']}'")
    response = requests.post(
        f"{BASE_URL}/api/{user_id}/chat",
        json=data,
        headers=headers
    )

    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Response received!")
        print(f"   Message: {result.get('message', {}).get('content', '')[:200]}...")
        print(f"   Task operations: {len(result.get('task_operations', []))}")
        return result
    else:
        print(f"   Error: {response.text}")
        return None

def main():
    print("=" * 60)
    print("Groq Chatbot Integration Test")
    print("=" * 60)

    # Test health
    if not test_health():
        print("\n❌ Health check failed!")
        return

    # Try to sign up (might fail if user exists)
    signup_result = test_signup()

    # Sign in
    signin_result = test_signin()
    if not signin_result:
        print("\n❌ Sign in failed!")
        return

    user_id = signin_result.get("user", {}).get("id")
    token = signin_result.get("access_token")

    if not user_id or not token:
        print("\n❌ Missing user_id or token!")
        return

    # Test chat
    chat_result = test_chat(user_id, token)

    if chat_result:
        print("\n" + "=" * 60)
        print("✅ Groq chatbot is working!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Groq chatbot test failed!")
        print("=" * 60)

if __name__ == "__main__":
    main()
