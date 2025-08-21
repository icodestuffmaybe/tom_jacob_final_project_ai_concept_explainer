#!/usr/bin/env python3
"""
Test Script for Exercise 1C: SVG Flashcard Generation (Prompt Engineering Session)

This script helps students test their implementation of the generate_svg_flashcard() function.
Run this script to verify your SVG generation prompts are working correctly.

Usage: python test_exercise_1c_svg.py
"""

import sys
import os
import asyncio
import re

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.svg_generator import SVGGenerator
from app.core.config import settings

async def test_svg_flashcard_generation():
    """Test SVG flashcard generation with different topics and explanations"""
    
    print("🧪 TESTING EXERCISE 1C: SVG Flashcard Generation")
    print("=" * 60)
    
    # Test cases with different topics and explanations
    test_cases = [
        {
            "topic": "Photosynthesis",
            "explanation": "Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen. It occurs in chloroplasts using chlorophyll. The light reactions capture solar energy, while the Calvin cycle produces glucose. This process is essential for life on Earth as it produces oxygen and forms the base of most food chains."
        },
        {
            "topic": "Gravity", 
            "explanation": "Gravity is a fundamental force that attracts objects with mass toward each other. On Earth, gravity pulls objects toward the center of the planet with an acceleration of 9.8 m/s². The strength of gravitational force depends on the mass of the objects and the distance between them, following Newton's law of universal gravitation."
        },
        {
            "topic": "Democracy",
            "explanation": "Democracy is a system of government where power is held by the people, either directly or through elected representatives. It includes principles like majority rule, minority rights, individual freedoms, and regular elections. Citizens participate through voting and civic engagement."
        }
    ]
    
    print(f"📊 API Key Status: {'✅ Configured' if settings.GEMINI_API_KEY else '❌ Not configured'}")
    print()
    
    generator = SVGGenerator()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🎨 Test Case {i}: {test_case['topic']}")
        print("-" * 40)
        
        try:
            # Test SVG flashcard generation
            svg_content = await generator.generate_svg_flashcard(
                test_case['topic'], 
                test_case['explanation']
            )
            
            if not svg_content:
                print("❌ FAILED: No SVG content returned")
                continue
                
            print("✅ SVG FLASHCARD GENERATED!")
            print(f"📏 Content length: {len(svg_content)} characters")
            
            # Validate SVG structure
            svg_checks = []
            svg_checks.append(("Starts with <svg", svg_content.strip().startswith('<svg')))
            svg_checks.append(("Ends with </svg>", svg_content.strip().endswith('</svg>')))
            svg_checks.append(("Has width attribute", 'width=' in svg_content))
            svg_checks.append(("Has height attribute", 'height=' in svg_content))
            svg_checks.append(("Has dark theme background", '#1a1a1a' in svg_content.lower() or '#000' in svg_content.lower()))
            svg_checks.append(("Has light text color", '#f0f0f0' in svg_content.lower() or '#fff' in svg_content.lower()))
            svg_checks.append(("Contains topic text", test_case['topic'].lower() in svg_content.lower()))
            
            print("\n📋 SVG Structure Validation:")
            for check_name, passed in svg_checks:
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
            
            # Check design elements
            design_checks = []
            design_checks.append(("Has text elements", '<text' in svg_content))
            design_checks.append(("Has visual shapes", any(shape in svg_content for shape in ['<rect', '<circle', '<path', '<line', '<polygon'])))
            design_checks.append(("Uses appropriate font-size", re.search(r'font-size="\d{2,}"', svg_content) is not None))
            design_checks.append(("No markdown formatting", '```' not in svg_content))
            design_checks.append(("Valid SVG syntax", svg_content.count('<svg') == svg_content.count('</svg>') == 1))
            
            print("\n🎨 Design Quality Check:")
            for check_name, passed in design_checks:
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
            
            # Educational content check
            educational_checks = []
            educational_checks.append(("Contains educational content", len(svg_content) > 500))
            educational_checks.append(("Topic-specific content", any(word in svg_content.lower() for word in test_case['topic'].lower().split())))
            educational_checks.append(("Professional appearance", 'font-family' in svg_content))
            educational_checks.append(("Proper sizing (800x600)", '800' in svg_content and '600' in svg_content))
            
            print("\n📚 Educational Content Check:")
            for check_name, passed in educational_checks:
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
            
            # Show SVG preview info
            print(f"\n🔍 SVG Preview:")
            print(f"   First 150 chars: {svg_content[:150]}...")
            
            # Save SVG to file for manual inspection
            svg_filename = f"test_output_{test_case['topic'].lower().replace(' ', '_')}.svg"
            try:
                with open(svg_filename, 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                print(f"   💾 Saved to: {svg_filename} (open in browser to view)")
            except Exception as e:
                print(f"   ⚠️ Could not save file: {e}")
            
            print()
            
        except AssertionError as e:
            print(f"❌ IMPLEMENTATION ERROR: {e}")
            print("💡 TIP: Make sure you've implemented the function and removed the assertion!")
            print()
            
        except Exception as e:
            print(f"❌ RUNTIME ERROR: {e}")
            print("💡 TIP: Check your SVG generation prompt and response cleaning logic")
            print()
    
    # Test fallback behavior (no API key)
    print("🔄 Testing Fallback Behavior (No API)")
    print("-" * 40)
    
    # Temporarily disable model to test fallback
    original_model = generator.model
    generator.model = None
    
    try:
        fallback_svg = await generator.generate_svg_flashcard("Test Topic", "Test explanation")
        
        fallback_checks = []
        fallback_checks.append(("Returns valid SVG", fallback_svg.startswith('<svg')))
        fallback_checks.append(("Contains fallback message", 'progress' in fallback_svg.lower() or 'learning' in fallback_svg.lower()))
        fallback_checks.append(("Proper dimensions", '800' in fallback_svg and '600' in fallback_svg))
        fallback_checks.append(("Dark theme", '#1a1a1a' in fallback_svg))
        
        print("📋 Fallback SVG Check:")
        for check_name, passed in fallback_checks:
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")
            
    except Exception as e:
        print(f"❌ Fallback test failed: {e}")
    finally:
        generator.model = original_model
    
    print()
    print("🎯 TESTING TIPS:")
    print("1. Your SVG should be exactly 800x600 pixels")
    print("2. Use dark theme: background #1a1a1a, text #f0f0f0")
    print("3. Include educational content about the topic")
    print("4. Create clean, minimalist design")
    print("5. Return only SVG code (no markdown formatting)")
    print()
    print("📚 Session 1 (Prompt Engineering) Concepts Applied:")
    print("• Persona prompting: 'You are a minimalist designer...'")
    print("• Format specification: Exact SVG structure and dimensions")
    print("• Detailed requirements: Colors, layout, typography")
    print("• Output format: 'Generate ONLY valid SVG code'")
    print()
    print("💡 Implementation Tips:")
    print("• Extract core essence from the explanation")
    print("• Use visual metaphors and educational design principles")
    print("• Clean the AI response to extract only SVG content")
    print("• Test with different topics to ensure flexibility")

def main():
    """Run the SVG flashcard generation tests"""
    try:
        asyncio.run(test_svg_flashcard_generation())
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"💥 Test failed with error: {e}")

if __name__ == "__main__":
    main()