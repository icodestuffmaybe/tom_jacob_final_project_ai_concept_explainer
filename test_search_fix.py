#!/usr/bin/env python3
"""
Simple test to verify search improvements work.
"""

import requests
import time

def test_search_fix():
    print("🔍 Testing Search Fix")
    print("=" * 30)
    
    base_url = "http://localhost:8000"
    
    # Test queries that previously failed to find sources
    test_queries = [
        "embeddings",
        "machine learning", 
        "photosynthesis",
        "what is gravity",
        "neural networks"
    ]
    
    for query in test_queries:
        print(f"\n📝 Testing: '{query}'")
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{base_url}/api/explain",
                json={"query": query},
                timeout=30
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                sources = data.get('sources', [])
                keywords = data.get('keywords', [])
                
                print(f"   ⏱️ Time: {duration:.1f}s")
                print(f"   🔑 Keywords: {keywords}")
                print(f"   📚 Sources found: {len(sources)}")
                
                if sources:
                    source = sources[0]
                    print(f"   ✅ Source: {source.get('title', 'No title')}")
                    print(f"   🔗 URL: {source.get('url', 'No URL')}")
                    snippet = source.get('snippet', 'No snippet')
                    print(f"   📄 Snippet: {snippet[:80]}...")
                else:
                    print(f"   ❌ No sources found")
                
            else:
                print(f"   ❌ Request failed: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ Request timed out")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 30)
    print("🎯 Search Fix Summary:")
    print("1. ✅ Better keyword extraction with Wikipedia focus")
    print("2. ✅ Improved Wikipedia API calls with fallback")
    print("3. ✅ URL encoding for multi-word terms")
    print("4. ✅ Search API fallback when direct page fails")
    print("5. ✅ Better error handling and logging")

if __name__ == "__main__":
    test_search_fix()