#!/usr/bin/env python3
"""
Test script for SillyTavern API compatibility
This script tests the API endpoints to ensure they work with SillyTavern
"""

import requests
import json
import sys

API_BASE = "http://localhost:8080"

def test_models_endpoint():
    """Test the /v1/models endpoint"""
    print("Testing /v1/models endpoint...")
    try:
        response = requests.get(f"{API_BASE}/v1/models")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Models endpoint working: {data}")
            return True
        else:
            print(f"❌ Models endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Models endpoint error: {e}")
        return False

def test_chat_completions():
    """Test the /v1/chat/completions endpoint"""
    print("\nTesting /v1/chat/completions endpoint...")
    
    test_cases = [
        {
            "name": "Simple user message",
            "payload": {
                "model": "local-llama",
                "messages": [
                    {"role": "user", "content": "Hello, how are you?"}
                ]
            }
        },
        {
            "name": "System + User message",
            "payload": {
                "model": "local-llama", 
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "What's the weather like?"}
                ]
            }
        },
        {
            "name": "Conversation with assistant history",
            "payload": {
                "model": "local-llama",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi there! How can I help you?"},
                    {"role": "user", "content": "Tell me a joke"}
                ]
            }
        }
    ]
    
    all_passed = True
    
    for test_case in test_cases:
        print(f"\n  Testing: {test_case['name']}")
        try:
            response = requests.post(
                f"{API_BASE}/v1/chat/completions",
                json=test_case["payload"],
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required fields
                required_fields = ["id", "object", "created", "model", "choices", "usage"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    print(f"    ❌ Missing fields: {missing_fields}")
                    all_passed = False
                else:
                    # Check choice structure
                    if data["choices"] and len(data["choices"]) > 0:
                        choice = data["choices"][0]
                        if "message" in choice and "role" in choice["message"] and "content" in choice["message"]:
                            print(f"    ✅ Response: {choice['message']['content'][:50]}...")
                        else:
                            print(f"    ❌ Invalid choice structure")
                            all_passed = False
                    else:
                        print(f"    ❌ No choices in response")
                        all_passed = False
            else:
                print(f"    ❌ HTTP {response.status_code}: {response.text}")
                all_passed = False
                
        except Exception as e:
            print(f"    ❌ Error: {e}")
            all_passed = False
    
    return all_passed

def main():
    print("🧪 SillyTavern API Compatibility Test")
    print("=" * 40)
    
    # Test if server is running
    try:
        requests.get(f"{API_BASE}/v1/models", timeout=5)
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to API server at {API_BASE}")
        print("Make sure the server is running with: python main.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
    
    models_ok = test_models_endpoint()
    chat_ok = test_chat_completions()
    
    print("\n" + "=" * 40)
    if models_ok and chat_ok:
        print("🎉 All tests passed! API is ready for SillyTavern.")
        print("\nNext steps:")
        print("1. In SillyTavern, go to API Settings")
        print("2. Select 'OpenAI' as API type")
        print("3. Set API URL to: http://localhost:8080/v1")
        print("4. Set Model to: local-llama")
        print("5. Test the connection")
    else:
        print("❌ Some tests failed. Check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
