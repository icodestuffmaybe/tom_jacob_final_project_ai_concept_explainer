#!/usr/bin/env python3
"""
Test Script for Exercise 2A: Keyword Extraction (RAG Session)

This script helps students test their implementation of the extract_keywords() function.
Run this script to verify your keyword extraction for RAG is working correctly.

Usage: python test_exercise_2a_keywords.py
"""

import sys
import os
import asyncio

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.explanation_service import ExplanationService
from app.core.config import settings

async def test_keyword_extraction():
    """Test the keyword extraction with different scenarios"""
    
    print("🧪 TESTING EXERCISE 2A: Keyword Extraction")
    print("=" * 60)
    
    # Initialize the service
    service = ExplanationService()
    
    # Test queries
    test_cases = [
        {
            "query": "What is photosynthesis?",
            "expected_concepts": ["photosynthesis", "plants", "biology", "chlorophyll", "energy"]
        },
        {
            "query": "Explain machine learning algorithms",
            "expected_concepts": ["machine learning", "algorithms", "artificial intelligence", "computer science", "data"]
        },
        {
            "query": "How does gravity work?",
            "expected_concepts": ["gravity", "physics", "force", "mass", "Newton"]
        },
        {
            "query": "What causes climate change?",
            "expected_concepts": ["climate change", "greenhouse gases", "carbon dioxide", "global warming", "environment"]
        }
    ]
    
    print(f"📊 API Key Status: {'✅ Configured' if settings.GEMINI_API_KEY else '❌ Not configured'}")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🔍 Test Case {i}: {test_case['query']}")
        print("-" * 40)
        
        try:
            # Test the keyword extraction
            keywords = await service.extract_keywords(test_case["query"])
            
            # Analyze the result
            print("✅ KEYWORDS EXTRACTED SUCCESSFULLY!")
            print(f"📝 Keywords: {keywords}")
            print(f"📊 Count: {len(keywords)} keywords")
            
            # Check keyword quality
            checks = []
            checks.append(("3-5 keywords", 3 <= len(keywords) <= 5))
            checks.append(("Original query included", test_case["query"] in keywords or any(word in test_case["query"].lower() for word in [k.lower() for k in keywords])))
            checks.append(("No duplicates", len(keywords) == len(set(k.lower() for k in keywords))))
            checks.append(("Educational terms", any(keyword.lower() in [concept.lower() for concept in test_case["expected_concepts"]] for keyword in keywords)))
            
            print("\n📋 Keyword Quality Check:")
            for check_name, passed in checks:
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
            
            # Check for Wikipedia-searchable terms
            print(f"\n🔍 Wikipedia Readiness:")
            wikipedia_ready = []
            for keyword in keywords:
                # Simple heuristics for Wikipedia-searchable terms
                is_ready = (
                    len(keyword.split()) <= 3 and  # Not too long
                    keyword.replace(" ", "").replace("-", "").isalnum() and  # Alphanumeric
                    len(keyword) > 2  # Not too short
                )
                wikipedia_ready.append(is_ready)
                status = "✅" if is_ready else "❌"
                print(f"   {status} '{keyword}'")
            
            if all(wikipedia_ready):
                print("   🎯 All keywords appear Wikipedia-searchable!")
            
            print()
            
        except AssertionError as e:
            print(f"❌ IMPLEMENTATION ERROR: {e}")
            print("💡 TIP: Make sure you've implemented the function and removed the assertion!")
            print()
            
        except Exception as e:
            print(f"❌ RUNTIME ERROR: {e}")
            print("💡 TIP: Check your prompt structure and keyword parsing logic")
            print()
    
    print("🎯 TESTING TIPS:")
    print("1. Extract 3-5 keywords that would have Wikipedia articles")
    print("2. Include the main topic and related educational terms")
    print("3. Use simple, common terms (avoid technical jargon)")
    print("4. Prefer single words or short phrases")
    print("5. Always include the original query or its main concept")
    print()
    print("📚 Session 2 (RAG) Concepts Applied:")
    print("• Query processing: Breaking down educational questions")
    print("• Search optimization: Terms that work well with Wikipedia")
    print("• Knowledge representation: Key concepts and related terms")
    print("• Fallback strategies: Handle cases without API access")
    print()
    print("💡 Prompt Engineering Tips:")
    print("• Use few-shot examples in your prompt")
    print("• Specify output format (comma-separated)")
    print("• Include educational context in instructions")
    print("• Handle edge cases (very short/long queries)")

def main():
    """Run the keyword extraction tests"""
    try:
        asyncio.run(test_keyword_extraction())
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"💥 Test failed with error: {e}")

if __name__ == "__main__":
    main()