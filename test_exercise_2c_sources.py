#!/usr/bin/env python3
"""
Test Script for Exercise 2C: Source Integration & Summarization (RAG Session)

This script helps students test their implementation of the summarize_sources() function.
Run this script to verify your multi-source content synthesis is working correctly.

Usage: python test_exercise_2c_sources.py
"""

import sys
import os
import asyncio

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.explanation_service import ExplanationService
from app.core.config import settings

async def test_source_summarization():
    """Test source summarization with different types and numbers of sources"""
    
    print("🧪 TESTING EXERCISE 2C: Source Integration & Summarization")
    print("=" * 60)
    
    # Test cases with different source combinations
    test_cases = [
        {
            "topic": "Photosynthesis",
            "sources": [
                {
                    "title": "Photosynthesis - Wikipedia",
                    "url": "https://en.wikipedia.org/wiki/Photosynthesis",
                    "snippet": "Photosynthesis is a process used by plants and other organisms to convert light energy into chemical energy that, through cellular respiration, can later be released to fuel the organism's activities. This chemical energy is stored in carbohydrate molecules, such as sugars and starches, which are synthesized from carbon dioxide and water.",
                    "source_type": "wikipedia"
                },
                {
                    "title": "How Photosynthesis Works",
                    "url": "https://example.com/photosynthesis",
                    "snippet": "The process of photosynthesis occurs in two main stages: the light reactions and the Calvin cycle. During light reactions, chlorophyll absorbs light energy and converts it to chemical energy. The Calvin cycle uses this energy to convert carbon dioxide into glucose.",
                    "source_type": "educational"
                }
            ]
        },
        {
            "topic": "Machine Learning",
            "sources": [
                {
                    "title": "Machine Learning Basics",
                    "url": "https://example.com/ml-basics",
                    "snippet": "Machine learning is a type of artificial intelligence that enables computers to learn and make decisions without being explicitly programmed. It uses algorithms to identify patterns in data and make predictions or classifications.",
                    "source_type": "educational"
                },
                {
                    "title": "Types of Machine Learning",
                    "url": "https://example.com/ml-types", 
                    "snippet": "There are three main types of machine learning: supervised learning, unsupervised learning, and reinforcement learning. Supervised learning uses labeled data, unsupervised learning finds patterns in unlabeled data, and reinforcement learning learns through interaction with an environment.",
                    "source_type": "educational"
                },
                {
                    "title": "Neural Networks",
                    "url": "https://example.com/neural-networks",
                    "snippet": "Neural networks are computational models inspired by biological neural networks. They consist of interconnected nodes (neurons) that process information and can learn complex patterns in data through training.",
                    "source_type": "technical"
                }
            ]
        },
        {
            "topic": "Single Source Test",
            "sources": [
                {
                    "title": "Gravity Explained",
                    "url": "https://example.com/gravity",
                    "snippet": "Gravity is a fundamental force of nature that attracts objects with mass toward each other. On Earth, gravity gives weight to physical objects and causes them to fall toward the ground when dropped.",
                    "source_type": "educational"
                }
            ]
        },
        {
            "topic": "Empty Sources Test", 
            "sources": []
        }
    ]
    
    print(f"📊 API Key Status: {'✅ Configured' if settings.GEMINI_API_KEY else '❌ Not configured'}")
    print()
    
    service = ExplanationService()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📚 Test Case {i}: {test_case['topic']}")
        print(f"   Sources: {len(test_case['sources'])}")
        print("-" * 40)
        
        try:
            # Test source summarization
            summary = await service.summarize_sources(test_case['sources'])
            
            if not test_case['sources']:
                # Empty sources test
                print("📝 EMPTY SOURCES TEST:")
                empty_checks = []
                empty_checks.append(("Handles empty sources", summary == "" or "no sources" in summary.lower()))
                empty_checks.append(("Doesn't crash", True))  # We got this far
                
                for check_name, passed in empty_checks:
                    status = "✅" if passed else "❌"
                    print(f"   {status} {check_name}")
                print()
                continue
            
            print("📝 SOURCE SUMMARIZATION COMPLETED!")
            print(f"   Summary length: {len(summary)} characters")
            print(f"   First 200 chars: {summary[:200]}...")
            
            # Analyze summarization quality
            quality_checks = []
            quality_checks.append(("Generated content", len(summary) > 0))
            quality_checks.append(("Reasonable length", 50 <= len(summary) <= 2000))
            quality_checks.append(("Contains key terms", any(term.lower() in summary.lower() for term in test_case['topic'].split())))
            quality_checks.append(("Synthesis not just copying", summary != test_case['sources'][0]['snippet']))
            
            print(f"\n📊 Summary Quality Check:")
            for check_name, passed in quality_checks:
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
            
            # Content analysis
            content_checks = []
            
            # Check if summary includes information from multiple sources (if multiple exist)
            if len(test_case['sources']) > 1:
                source_keywords = []
                for source in test_case['sources']:
                    # Extract key terms from each source
                    words = source['snippet'].split()[:10]  # First 10 words
                    source_keywords.extend([w.lower().strip('.,!?') for w in words if len(w) > 4])
                
                multi_source_coverage = sum(1 for keyword in source_keywords if keyword in summary.lower())
                content_checks.append(("Multi-source synthesis", multi_source_coverage >= 2))
            
            content_checks.append(("Educational focus", any(word in summary.lower() for word in ['process', 'concept', 'principle', 'important', 'key'])))
            content_checks.append(("Factual content", not any(word in summary.lower() for word in ['i think', 'maybe', 'probably'])))
            content_checks.append(("Coherent text", '.' in summary and len(summary.split('.')) >= 2))
            
            print(f"\n📚 Content Analysis:")
            for check_name, passed in content_checks:
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
            
            # Information extraction check
            extraction_checks = []
            
            # Check if key concepts from sources are preserved
            all_snippets = ' '.join(source['snippet'] for source in test_case['sources'])
            common_concepts = []
            for word in all_snippets.split():
                word_clean = word.lower().strip('.,!?()')
                if len(word_clean) > 6 and word_clean not in common_concepts:
                    if word_clean in summary.lower():
                        common_concepts.append(word_clean)
            
            extraction_checks.append(("Preserves key concepts", len(common_concepts) >= 1))
            extraction_checks.append(("Appropriate detail level", not len(summary) > sum(len(s['snippet']) for s in test_case['sources'])))
            extraction_checks.append(("Removes redundancy", summary.count('.') <= sum(s['snippet'].count('.') for s in test_case['sources'])))
            
            print(f"\n🔍 Information Extraction:")
            for check_name, passed in extraction_checks:
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
            
            # Show source integration details
            print(f"\n📋 Source Integration Details:")
            print(f"   Input sources: {len(test_case['sources'])}")
            print(f"   Total source text: {sum(len(s['snippet']) for s in test_case['sources'])} chars")
            print(f"   Summary length: {len(summary)} chars") 
            print(f"   Compression ratio: {len(summary) / max(1, sum(len(s['snippet']) for s in test_case['sources'])):.2f}")
            
            print()
            
        except AssertionError as e:
            print(f"❌ IMPLEMENTATION ERROR: {e}")
            print("💡 TIP: Make sure you've implemented the function and removed the assertion!")
            print()
            
        except Exception as e:
            print(f"❌ RUNTIME ERROR: {e}")
            print("💡 TIP: Check your source summarization prompt and logic")
            print()
    
    # Test fallback behavior (no API key)
    print("🔄 Testing Fallback Behavior (No API)")
    print("-" * 40)
    
    # Temporarily disable model to test fallback
    original_model = service.model
    service.model = None
    
    try:
        test_sources = [
            {
                "title": "Test Source",
                "snippet": "Test content for fallback testing",
                "source_type": "test"
            }
        ]
        
        fallback_summary = await service.summarize_sources(test_sources)
        
        fallback_checks = []
        fallback_checks.append(("Handles no API gracefully", isinstance(fallback_summary, str)))
        fallback_checks.append(("Returns appropriate response", len(fallback_summary) == 0 or "not available" in fallback_summary.lower()))
        fallback_checks.append(("No exceptions raised", True))
        
        print("📋 Fallback Behavior Check:")
        for check_name, passed in fallback_checks:
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")
            
    except Exception as e:
        print(f"❌ Fallback test failed: {e}")
    finally:
        service.model = original_model
    
    print()
    print("🎯 TESTING TIPS:")
    print("1. Combine information from multiple sources effectively")
    print("2. Extract key educational concepts and facts")
    print("3. Remove redundancy while preserving important details")
    print("4. Create coherent, well-structured summaries")
    print("5. Handle edge cases (empty sources, single source)")
    print()
    print("📚 Session 2 (RAG) Concepts Applied:")
    print("• Information synthesis: Combine multiple sources")
    print("• Content summarization: Extract key facts and concepts")
    print("• Context preparation: Format for AI consumption")
    print("• Quality filtering: Focus on educational content")
    print()
    print("💡 Implementation Tips:")
    print("• Use clear prompts that ask for synthesis, not just copying")
    print("• Focus on educational value and key concepts")
    print("• Maintain factual accuracy while reducing redundancy")
    print("• Handle empty or single-source cases appropriately")

def main():
    """Run the source summarization tests"""
    try:
        asyncio.run(test_source_summarization())
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"💥 Test failed with error: {e}")

if __name__ == "__main__":
    main()