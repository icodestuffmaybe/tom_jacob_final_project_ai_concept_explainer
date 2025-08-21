#!/usr/bin/env python3
"""
Test both Wikipedia and DuckDuckGo search functionality.
"""

import requests
import time

def test_dual_search():
    print("Testing Dual Search: Wikipedia + DuckDuckGo")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test queries that demonstrate different search scenarios
    test_cases = [
        {
            "query": "photosynthesis",
            "expected": "Should find Wikipedia page easily"
        },
        {
            "query": "embeddings", 
            "expected": "Wikipedia might fail, DuckDuckGo should find educational content"
        },
        {
            "query": "machine learning basics",
            "expected": "Should find educational sources"
        },
        {
            "query": "quantum computing explained",
            "expected": "Should find educational explanations"
        },
        {
            "query": "data structures",
            "expected": "Should find programming educational content"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        query = test_case["query"]
        expected = test_case["expected"]
        
        print(f"\n{i}. Testing: '{query}'")
        print(f"   Expected: {expected}")
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{base_url}/api/explain",
                json={"query": query},
                timeout=45  # Longer timeout for dual search
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                sources = data.get('sources', [])
                keywords = data.get('keywords', [])
                
                print(f"   ⏱️ Time: {duration:.1f}s")
                print(f"   🔑 Keywords: {keywords[:3]}")  # Show first 3
                print(f"   📚 Sources found: {len(sources)}")
                
                for j, source in enumerate(sources):
                    source_type = source.get('source_type', 'unknown')
                    title = source.get('title', 'No title')
                    url = source.get('url', 'No URL')[:50]  # Truncate long URLs
                    
                    # Add emoji based on source type
                    emoji = "📰" if source_type == "wikipedia" else "🦆" if "duckduckgo" in source_type else "🔗"
                    
                    print(f"   {emoji} Source {j+1}: {title} ({source_type})")
                    print(f"      URL: {url}...")
                
                if not sources:
                    print(f"   ❌ No sources found - this should not happen with dual search!")
                    
            else:
                print(f"   ❌ Request failed: {response.status_code}")
                print(f"   Error: {response.text[:100]}")
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ Request timed out")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Dual Search Summary:")
    print("✅ Wikipedia: Fast, authoritative, great for established topics")
    print("✅ DuckDuckGo: Broader coverage, educational filtering, finds explanations")
    print("✅ Combined: Should find sources for virtually any educational query")
    print("✅ Educational filtering: Prioritizes .edu, Khan Academy, etc.")

def test_search_coverage():
    """Test edge cases that should now work with dual search"""
    print(f"\n🧪 Testing Search Coverage")
    print("=" * 30)
    
    edge_cases = [
        "embeddings",           # Previously failed Wikipedia
        "vector representations", # Academic term
        "neural network basics",  # Educational query
        "deep learning intro",    # Tutorial-style query
        "AI for beginners"        # Beginner-focused query
    ]
    
    base_url = "http://localhost:8000"
    
    for query in edge_cases:
        print(f"\n📝 Testing edge case: '{query}'")
        
        try:
            response = requests.post(
                f"{base_url}/api/explain",
                json={"query": query},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                sources = data.get('sources', [])
                
                if sources:
                    print(f"   ✅ Success: Found {len(sources)} source(s)")
                    for source in sources:
                        source_type = source.get('source_type', 'unknown')
                        print(f"      - {source_type}: {source.get('title', 'No title')}")
                else:
                    print(f"   ❌ Failed: No sources found")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_dual_search()
    test_search_coverage()