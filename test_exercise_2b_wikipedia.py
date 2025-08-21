#!/usr/bin/env python3
"""
Test Script for Exercise 2B: Wikipedia Search & Retrieval (RAG Session)

This script helps students test their implementation of the search_wikipedia() function.
Run this script to verify your Wikipedia API integration is working correctly.

Usage: python test_exercise_2b_wikipedia.py
"""

import sys
import os
import asyncio
import json

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.explanation_service import ExplanationService
from app.core.config import settings

async def test_wikipedia_search():
    """Test Wikipedia search and retrieval with various keywords"""
    
    print("🧪 TESTING EXERCISE 2B: Wikipedia Search & Retrieval")
    print("=" * 60)
    
    # Test cases with different types of search terms
    test_cases = [
        {
            "keyword": "photosynthesis",
            "expected_type": "Direct page hit",
            "should_find": True
        },
        {
            "keyword": "machine learning",
            "expected_type": "Direct page hit", 
            "should_find": True
        },
        {
            "keyword": "quantum physics basics",
            "expected_type": "Search results",
            "should_find": True
        },
        {
            "keyword": "nonexistent_topic_12345",
            "expected_type": "No results",
            "should_find": False
        },
        {
            "keyword": "DNA replication",
            "expected_type": "Direct or search",
            "should_find": True
        }
    ]
    
    print(f"📊 Internet Connection: Testing...")
    print(f"🌐 Wikipedia API: https://en.wikipedia.org/api/rest_v1/")
    print()
    
    service = ExplanationService()
    
    # Test connection with a simple request
    try:
        test_result = await service.search_wikipedia("test")
        print("✅ Wikipedia API connection successful")
    except Exception as e:
        print(f"⚠️ Wikipedia API connection issue: {e}")
        print("💡 This might affect test results")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🔍 Test Case {i}: '{test_case['keyword']}'")
        print(f"   Expected: {test_case['expected_type']}")
        print("-" * 40)
        
        try:
            # Test Wikipedia search
            results = await service.search_wikipedia(test_case['keyword'])
            
            print(f"📊 SEARCH RESULTS:")
            print(f"   Number of results: {len(results)}")
            
            if results:
                print("✅ Wikipedia search returned results!")
                
                # Validate result structure
                for j, result in enumerate(results):
                    print(f"\n   📝 Result {j+1}:")
                    
                    # Check required fields
                    required_fields = ['title', 'url', 'snippet', 'source_type']
                    structure_checks = []
                    
                    for field in required_fields:
                        has_field = field in result and result[field]
                        structure_checks.append((f"Has {field}", has_field))
                        if has_field:
                            if field == 'snippet':
                                print(f"      {field}: {result[field][:100]}...")
                            else:
                                print(f"      {field}: {result[field]}")
                    
                    print(f"\n   📋 Structure Validation:")
                    for check_name, passed in structure_checks:
                        status = "✅" if passed else "❌"
                        print(f"      {status} {check_name}")
                    
                    # Content quality checks
                    quality_checks = []
                    quality_checks.append(("Title not empty", len(result.get('title', '')) > 0))
                    quality_checks.append(("URL is Wikipedia", 'wikipedia.org' in result.get('url', '')))
                    quality_checks.append(("Snippet has content", len(result.get('snippet', '')) > 50))
                    quality_checks.append(("Source type correct", result.get('source_type') == 'wikipedia'))
                    quality_checks.append(("Snippet not too long", len(result.get('snippet', '')) <= 500))
                    
                    print(f"\n   📚 Content Quality Check:")
                    for check_name, passed in quality_checks:
                        status = "✅" if passed else "❌"
                        print(f"      {status} {check_name}")
            
            elif test_case['should_find']:
                print("❌ Expected to find results but got none")
                print("💡 Check if the keyword exists on Wikipedia or API is accessible")
            else:
                print("✅ Correctly returned no results for invalid keyword")
            
            # Test error handling
            error_checks = []
            error_checks.append(("Returns list type", isinstance(results, list)))
            error_checks.append(("Handles empty results", len(results) == 0 or all(isinstance(r, dict) for r in results)))
            error_checks.append(("No exceptions raised", True))  # We got this far without exception
            
            print(f"\n📋 Error Handling Check:")
            for check_name, passed in error_checks:
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
            
            print()
            
        except AssertionError as e:
            print(f"❌ IMPLEMENTATION ERROR: {e}")
            print("💡 TIP: Make sure you've implemented the function and removed the assertion!")
            print()
            
        except Exception as e:
            print(f"❌ RUNTIME ERROR: {e}")
            print("💡 TIP: Check your Wikipedia API integration and error handling")
            print("   Common issues:")
            print("   - URL encoding for special characters")
            print("   - Proper async/await usage")
            print("   - Handling API rate limits and timeouts")
            print("   - JSON parsing errors")
            print()
    
    # Test advanced scenarios
    print("🔬 Advanced Testing Scenarios")
    print("-" * 40)
    
    # Test special characters
    special_tests = [
        "E=mc²",  # Special characters
        "artificial intelligence",  # Spaces
        "COVID-19",  # Hyphens and numbers
    ]
    
    for keyword in special_tests:
        print(f"🧪 Testing special case: '{keyword}'")
        try:
            results = await service.search_wikipedia(keyword)
            status = "✅" if results else "⚠️"
            print(f"   {status} Results: {len(results)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print()
    print("🎯 TESTING TIPS:")
    print("1. Handle both direct page hits and search results")
    print("2. Properly encode URLs for special characters")
    print("3. Extract relevant content (title, URL, snippet)")
    print("4. Implement proper error handling and timeouts")
    print("5. Return consistent data structure")
    print()
    print("📚 Session 2 (RAG) Concepts Applied:")
    print("• API integration: Wikipedia REST API calls")
    print("• Content extraction: Get relevant article summaries")
    print("• Error handling: Handle missing articles gracefully")
    print("• Data processing: Clean and structure retrieved content")
    print()
    print("💡 Implementation Tips:")
    print("• Try direct page lookup first, then search API")
    print("• Use urllib.parse.quote() for URL encoding")
    print("• Set appropriate timeouts (5-10 seconds)")
    print("• Limit snippet length (300-500 characters)")
    print("• Return empty list [] for no results (don't raise exceptions)")

def main():
    """Run the Wikipedia search tests"""
    try:
        asyncio.run(test_wikipedia_search())
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"💥 Test failed with error: {e}")

if __name__ == "__main__":
    main()