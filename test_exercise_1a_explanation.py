#!/usr/bin/env python3
"""
Test Script for Exercise 1A: Explanation Generation (Prompt Engineering)

This script helps students test their implementation of the generate_explanation_with_sources() function.
Run this script to verify your prompt engineering techniques are working correctly.

Usage: python test_exercise_1a_explanation.py
"""

import sys
import os
import asyncio

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.explanation_service import ExplanationService
from app.core.config import settings

async def test_explanation_generation():
    """Test the explanation generation with different scenarios"""
    
    print("🧪 TESTING EXERCISE 1A: Explanation Generation")
    print("=" * 60)
    
    # Initialize the service
    service = ExplanationService()
    
    # Test data
    test_cases = [
        {
            "query": "What is photosynthesis?",
            "source_summary": "Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen. It occurs in chloroplasts and involves two main stages: light reactions and dark reactions.",
            "sources": [
                {"title": "Photosynthesis - Wikipedia", "url": "https://en.wikipedia.org/wiki/Photosynthesis"}
            ]
        },
        {
            "query": "Explain machine learning",
            "source_summary": "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed. It uses algorithms to analyze data and make predictions.",
            "sources": [
                {"title": "Machine Learning - Wikipedia", "url": "https://en.wikipedia.org/wiki/Machine_learning"}
            ]
        }
    ]
    
    print(f"📊 API Key Status: {'✅ Configured' if settings.GEMINI_API_KEY else '❌ Not configured'}")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🔍 Test Case {i}: {test_case['query']}")
        print("-" * 40)
        
        try:
            # Test the explanation generation
            explanation = await service.generate_explanation_with_sources(
                test_case["query"],
                test_case["source_summary"],
                test_case["sources"]
            )
            
            # Analyze the result
            print("✅ EXPLANATION GENERATED SUCCESSFULLY!")
            print(f"📝 Length: {len(explanation)} characters")
            print(f"📝 Preview: {explanation[:200]}...")
            
            # Check for key elements (Feynman Technique)
            checks = []
            checks.append(("Simple language", any(word in explanation.lower() for word in ["simple", "easy", "like", "imagine"])))
            checks.append(("Analogies/examples", any(word in explanation.lower() for word in ["like", "similar", "example", "imagine", "think of"])))
            checks.append(("Why it matters", any(phrase in explanation.lower() for phrase in ["important", "matter", "because", "reason", "why"])))
            checks.append(("Citations", "[1]" in explanation or "[2]" in explanation))
            
            print("\n📋 Feynman Technique Check:")
            for check_name, passed in checks:
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
            
            print()
            
        except AssertionError as e:
            print(f"❌ IMPLEMENTATION ERROR: {e}")
            print("💡 TIP: Make sure you've implemented the function and removed the assertion!")
            print()
            
        except Exception as e:
            print(f"❌ RUNTIME ERROR: {e}")
            print("💡 TIP: Check your prompt structure and API call implementation")
            print()
    
    print("🎯 TESTING TIPS:")
    print("1. Your explanation should use simple, clear language")
    print("2. Include analogies or real-world examples")
    print("3. Explain why the concept matters")
    print("4. Include citations like [1], [2] when referencing sources")
    print("5. Follow the Feynman Technique structure")
    print()
    print("📚 Session 1 Concepts to Apply:")
    print("• Persona prompting: 'You are an expert teacher...'")
    print("• Clear instructions: Step-by-step explanation structure")
    print("• Format specification: How to include citations")
    print("• Few-shot examples: Show the AI what good explanations look like")

def main():
    """Run the explanation generation tests"""
    try:
        asyncio.run(test_explanation_generation())
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"💥 Test failed with error: {e}")

if __name__ == "__main__":
    main()