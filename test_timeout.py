#!/usr/bin/env python3
"""
Test script to check how long explanations take and what might be causing delays.
"""

import requests
import time

def test_explanation_timing():
    base_url = "http://localhost:8000"
    test_query = "What is water?"  # Simple query to test timing
    
    print("Testing AI Explanation Timing")
    print("=" * 40)
    print(f"Query: {test_query}")
    print("Starting request...")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{base_url}/api/explain",
            json={"query": test_query},
            headers={"Content-Type": "application/json"},
            timeout=120  # 2 minutes timeout
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n⏱️ Total time: {duration:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(f"📝 Explanation length: {len(data.get('explanation', ''))}")
            print(f"🔗 Sources found: {len(data.get('sources', []))}")
            print(f"🎨 SVG generated: {'Yes' if data.get('svg_flashcard') else 'No'}")
            print(f"🏷️ Keywords: {data.get('keywords', [])}")
            
            # Show first 200 characters of explanation
            explanation = data.get('explanation', '')
            if explanation:
                print(f"\n📖 Explanation preview:")
                print(f"   {explanation[:200]}...")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            
    except requests.exceptions.Timeout:
        print(f"⏰ Request timed out after 2 minutes")
        print("   This might indicate a backend issue")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_explanation_timing()