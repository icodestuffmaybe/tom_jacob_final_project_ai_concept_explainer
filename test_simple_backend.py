#!/usr/bin/env python3
"""
Quick test to verify the simple backend is working without authentication.
"""

import requests
import json

def test_simple_backend():
    base_url = "http://localhost:8000"
    
    print("Testing AI Concept Explainer - Simple Backend")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check: OK")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        print("   Make sure the backend is running on http://localhost:8000")
        return False
    
    # Test explanation endpoint
    try:
        test_query = "What is photosynthesis?"
        response = requests.post(
            f"{base_url}/api/explain",
            json={"query": test_query},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Explanation API: OK")
            data = response.json()
            print(f"   Query: {test_query}")
            print(f"   Response keys: {list(data.keys())}")
            print(f"   Explanation length: {len(data.get('explanation', ''))}")
            print(f"   Sources found: {len(data.get('sources', []))}")
            print(f"   Keywords: {data.get('keywords', [])}")
            
            # Test quiz generation if we have a session
            session_id = data.get('session_id')
            if session_id:
                print(f"   Session ID: {session_id}")
                
                # Test quiz generation
                quiz_response = requests.post(
                    f"{base_url}/api/quiz/generate",
                    json={"session_id": session_id, "difficulty": "easy"},
                    headers={"Content-Type": "application/json"}
                )
                
                if quiz_response.status_code == 200:
                    print("✅ Quiz generation: OK")
                    quiz_data = quiz_response.json()
                    print(f"   Quiz ID: {quiz_data.get('quiz_id')}")
                    print(f"   Questions: {len(quiz_data.get('questions', []))}")
                else:
                    print(f"⚠️ Quiz generation failed: {quiz_response.status_code}")
                    print(f"   Error: {quiz_response.text}")
            
        else:
            print(f"❌ Explanation API failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Explanation API error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Simple backend is working correctly!")
    print("✅ No authentication required")
    print("✅ Core features functional")
    print("\nYou can now use the frontend at: http://localhost:5173")
    return True

if __name__ == "__main__":
    test_simple_backend()