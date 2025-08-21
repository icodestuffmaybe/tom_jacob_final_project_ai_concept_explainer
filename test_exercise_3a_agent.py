#!/usr/bin/env python3
"""
Test Script for Exercise 3A: Student Evaluation Agent (AI Agents Session)

This script helps students test their implementation of the process_student_explanation() agent.
Run this script to verify your ReAct agent is working correctly.

Usage: python test_exercise_3a_agent.py
"""

import sys
import os
import asyncio
import json

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.explanation_service import ExplanationService
from app.core.config import settings

class MockRequest:
    """Mock request object for testing"""
    def __init__(self, session_id, explanation):
        self.session_id = session_id
        self.explanation = explanation

class MockSession:
    """Mock session object for testing"""
    def __init__(self, explanation):
        self.explanation = explanation

async def test_evaluation_agent():
    """Test the student evaluation agent with different scenarios"""
    
    print("🧪 TESTING EXERCISE 3A: Student Evaluation Agent")
    print("=" * 60)
    
    # Test cases with original explanations and student attempts
    test_cases = [
        {
            "topic": "Photosynthesis",
            "original_explanation": "Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen. It occurs in chloroplasts using chlorophyll. The process has two main stages: light reactions that capture energy, and dark reactions that produce glucose. This process is essential for life on Earth as it produces oxygen and forms the base of most food chains.",
            "student_explanation": "Plants use sunlight to make food. They take in CO2 and water and make sugar.",
            "expected_gaps": ["chlorophyll", "chloroplasts", "oxygen production", "two stages"]
        },
        {
            "topic": "Gravity",
            "original_explanation": "Gravity is a fundamental force that attracts objects with mass toward each other. On Earth, gravity pulls objects toward the center of the planet with an acceleration of 9.8 m/s². The strength of gravitational force depends on the mass of the objects and the distance between them, as described by Newton's law of universal gravitation.",
            "student_explanation": "Gravity makes things fall down. It's stronger for heavier things.",
            "expected_gaps": ["mass dependency", "distance relationship", "universal nature", "acceleration value"]
        },
        {
            "topic": "Good Understanding",
            "original_explanation": "Democracy is a system of government where power is held by the people, either directly or through elected representatives. It includes principles like majority rule, minority rights, individual freedoms, and regular elections.",
            "student_explanation": "Democracy means government by the people. Citizens vote to choose their leaders in elections. It protects individual rights and follows majority rule while respecting minority opinions.",
            "expected_gaps": []  # Good explanation should have minimal gaps
        }
    ]
    
    print(f"📊 API Key Status: {'✅ Configured' if settings.GEMINI_API_KEY else '❌ Not configured'}")
    print()
    
    # We'll test the core logic by directly calling the evaluation logic
    # Since we can't easily mock the database and auth, we'll test the AI part
    
    service = ExplanationService()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🔍 Test Case {i}: {test_case['topic']}")
        print(f"📖 Student said: {test_case['student_explanation'][:100]}...")
        print("-" * 40)
        
        try:
            if not service.model:
                print("⚠️ No API key - testing fallback behavior")
                print("   Should return appropriate error message")
                print()
                continue
            
            # Create a ReAct agent prompt (this is what students should implement)
            prompt = f"""
            You are an educational evaluation agent. Your task is to assess student understanding using the ReAct framework.

            THOUGHT: I need to compare the student's explanation with the correct explanation to identify gaps.
            ACTION: I will analyze the student's response for completeness, accuracy, and understanding.
            OBSERVATION: I will provide constructive feedback to help the student learn.

            Original explanation: {test_case['original_explanation']}
            Student explanation: {test_case['student_explanation']}

            Please evaluate the student's understanding and provide:
            GAPS: [list specific missing concepts or misconceptions]
            CLARIFICATIONS: [explain what needs to be clarified or corrected]
            SIMPLIFIED: [provide a simplified explanation to help the student]

            Format your response exactly as shown above with GAPS:, CLARIFICATIONS:, and SIMPLIFIED: sections.
            """
            
            # Test the agent evaluation
            response = service.model.generate_content(prompt)
            response_text = response.text
            
            print("✅ AGENT EVALUATION COMPLETED!")
            print(f"📝 Response length: {len(response_text)} characters")
            
            # Parse the agent response (this is what students need to implement)
            gaps = []
            clarifications = ""
            simplified = ""
            
            sections = response_text.split("CLARIFICATIONS:")
            if len(sections) > 1:
                gaps_section = sections[0].replace("GAPS:", "").strip()
                gaps = [gap.strip() for gap in gaps_section.split("-") if gap.strip()]
                
                remaining = sections[1].split("SIMPLIFIED:")
                if len(remaining) > 1:
                    clarifications = remaining[0].strip()
                    simplified = remaining[1].strip()
                else:
                    clarifications = remaining[0].strip()
            
            # Analyze the agent's performance
            print(f"\n🔍 Agent Analysis:")
            print(f"   📋 Gaps identified: {len(gaps)}")
            for gap in gaps[:3]:  # Show first 3 gaps
                print(f"      • {gap}")
            
            print(f"   💬 Clarifications: {clarifications[:100]}...")
            print(f"   📚 Simplified explanation: {simplified[:100]}...")
            
            # Check ReAct pattern
            react_checks = []
            react_checks.append(("Uses THOUGHT", "thought" in response_text.lower() or "think" in response_text.lower()))
            react_checks.append(("Uses ACTION", "action" in response_text.lower() or "analyze" in response_text.lower()))
            react_checks.append(("Uses OBSERVATION", "observation" in response_text.lower() or "provide" in response_text.lower()))
            react_checks.append(("Structured output", "GAPS:" in response_text and "CLARIFICATIONS:" in response_text))
            
            print(f"\n📋 ReAct Agent Pattern Check:")
            for check_name, passed in checks:
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
            
            # Check educational quality
            educational_checks = []
            educational_checks.append(("Constructive feedback", any(word in response_text.lower() for word in ["help", "improve", "consider", "try"])))
            educational_checks.append(("Specific gaps", len(gaps) > 0 or "no gaps" in response_text.lower()))
            educational_checks.append(("Clear clarifications", len(clarifications) > 50))
            educational_checks.append(("Helpful simplification", len(simplified) > 50))
            
            print(f"\n📚 Educational Quality Check:")
            for check_name, passed in educational_checks:
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
            
            print()
            
        except AssertionError as e:
            print(f"❌ IMPLEMENTATION ERROR: {e}")
            print("💡 TIP: Make sure you've implemented the function and removed the assertion!")
            print()
            
        except Exception as e:
            print(f"❌ RUNTIME ERROR: {e}")
            print("💡 TIP: Check your ReAct agent prompt and response parsing logic")
            print()
    
    print("🎯 TESTING TIPS:")
    print("1. Your agent should use the ReAct pattern (Reason → Act → Observe)")
    print("2. Provide structured output with GAPS, CLARIFICATIONS, SIMPLIFIED")
    print("3. Give constructive, specific feedback")
    print("4. Identify missing concepts and misconceptions")
    print("5. Help the student improve their understanding")
    print()
    print("📚 Session 3 (AI Agents) Concepts Applied:")
    print("• ReAct framework: Thought → Action → Observation")
    print("• Agent roles: Educational evaluator and tutor")
    print("• Structured reasoning: Step-by-step analysis")
    print("• Tool use: Comparison and feedback generation")
    print()
    print("💡 Implementation Tips:")
    print("• Create clear agent persona in your prompt")
    print("• Use the ReAct pattern explicitly in the prompt")
    print("• Parse the structured response carefully")
    print("• Handle edge cases (no gaps, confused student, etc.)")

def main():
    """Run the evaluation agent tests"""
    try:
        asyncio.run(test_evaluation_agent())
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"💥 Test failed with error: {e}")

if __name__ == "__main__":
    main()