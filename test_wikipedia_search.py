#!/usr/bin/env python3
"""
Test script to debug Wikipedia search issues.
"""

import asyncio
import httpx

async def test_wikipedia_api():
    print("🔍 Testing Wikipedia API Search")
    print("=" * 40)
    
    # Test different API endpoints and search terms
    test_keywords = [
        "Vector Representation",
        "Word Embeddings", 
        "Natural Language Processing",
        "photosynthesis",
        "gravity",
        "embeddings",
        "machine learning"
    ]
    
    for keyword in test_keywords:
        print(f"\n📝 Testing keyword: '{keyword}'")
        
        # Test 1: Wikipedia Summary API (current approach)
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{keyword}"
                print(f"   URL: {search_url}")
                
                response = await client.get(search_url)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    title = data.get('title', 'No title')
                    extract = data.get('extract', 'No extract')
                    print(f"   ✅ Found: {title}")
                    print(f"   📄 Extract: {extract[:100]}...")
                else:
                    print(f"   ❌ Failed: {response.text[:200]}")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 2: Wikipedia Search API (alternative approach)
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                search_url = f"https://en.wikipedia.org/w/api.php"
                params = {
                    'action': 'query',
                    'format': 'json',
                    'list': 'search',
                    'srsearch': keyword,
                    'srlimit': 1
                }
                print(f"   Search API URL: {search_url}")
                
                response = await client.get(search_url, params=params)
                print(f"   Search Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    search_results = data.get('query', {}).get('search', [])
                    if search_results:
                        result = search_results[0]
                        title = result.get('title', 'No title')
                        snippet = result.get('snippet', 'No snippet')
                        print(f"   ✅ Search found: {title}")
                        print(f"   📄 Snippet: {snippet[:100]}...")
                    else:
                        print(f"   ❌ No search results")
                else:
                    print(f"   ❌ Search failed: {response.text[:200]}")
                    
        except Exception as e:
            print(f"   ❌ Search error: {e}")

async def test_improved_search():
    """Test an improved search implementation"""
    print(f"\n🚀 Testing Improved Search Implementation")
    print("=" * 40)
    
    async def improved_wikipedia_search(keyword: str):
        """Improved Wikipedia search with fallback"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Clean the keyword for URL
                clean_keyword = keyword.replace(' ', '_')
                
                # Try direct page summary first
                summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{clean_keyword}"
                response = await client.get(summary_url)
                
                if response.status_code == 200:
                    data = response.json()
                    return [{
                        'title': data.get('title', ''),
                        'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                        'snippet': data.get('extract', '')[:300],
                        'source_type': 'wikipedia'
                    }]
                
                # Fallback to search API
                search_url = "https://en.wikipedia.org/w/api.php"
                search_params = {
                    'action': 'query',
                    'format': 'json',
                    'list': 'search',
                    'srsearch': keyword,
                    'srlimit': 1
                }
                
                search_response = await client.get(search_url, params=search_params)
                if search_response.status_code == 200:
                    search_data = search_response.json()
                    search_results = search_data.get('query', {}).get('search', [])
                    
                    if search_results:
                        result = search_results[0]
                        title = result.get('title', '')
                        
                        # Get the actual page summary
                        clean_title = title.replace(' ', '_')
                        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{clean_title}"
                        summary_response = await client.get(summary_url)
                        
                        if summary_response.status_code == 200:
                            summary_data = summary_response.json()
                            return [{
                                'title': summary_data.get('title', title),
                                'url': summary_data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                                'snippet': summary_data.get('extract', '')[:300],
                                'source_type': 'wikipedia'
                            }]
                
        except Exception as e:
            print(f"   ❌ Improved search error: {e}")
        
        return []
    
    # Test the improved search
    test_keywords = ["embeddings", "photosynthesis", "machine learning", "gravity"]
    
    for keyword in test_keywords:
        print(f"\n📝 Improved search for: '{keyword}'")
        results = await improved_wikipedia_search(keyword)
        
        if results:
            result = results[0]
            print(f"   ✅ Found: {result['title']}")
            print(f"   🔗 URL: {result['url']}")
            print(f"   📄 Snippet: {result['snippet'][:100]}...")
        else:
            print(f"   ❌ No results found")

if __name__ == "__main__":
    asyncio.run(test_wikipedia_api())
    asyncio.run(test_improved_search())