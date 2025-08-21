#!/usr/bin/env python3
"""
Test Script for Exercise 1B: Quiz Generation (Prompt Engineering)

This script helps students test their implementation of the generate_quiz() function.
Run this script to verify your quiz generation prompts are working correctly.

Usage: python test_exercise_1b_quiz.py
"""

import sys
import os
import asyncio
import json

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.quiz_service import QuizService
from app.core.config import settings

async def test_quiz_generation():
    """Test the quiz generation with different scenarios"""
    
    print("🧪 TESTING EXERCISE 1B: Quiz Generation")
    print("=" * 60)
    
    # Initialize the service
    service = QuizService()
    
    # Test explanations
    test_cases = [
        {
            "explanation": "Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen. It occurs in chloroplasts using chlorophyll. The process has two main stages: light reactions that capture energy, and dark reactions that produce glucose. This process is essential for life on Earth as it produces oxygen and forms the base of most food chains.",
            "difficulty": "medium"
        },
        {
            "explanation": "Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed. It uses algorithms to identify patterns in data and make predictions. Common types include supervised learning (learning from labeled examples), unsupervised learning (finding patterns in unlabeled data), and reinforcement learning (learning through trial and error).",
            "difficulty": "easy"
        }
    ]
    
    print(f"📊 API Key Status: {'✅ Configured' if settings.GEMINI_API_KEY else '❌ Not configured'}")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🔍 Test Case {i}: {test_case['difficulty'].title()} Difficulty")
        print(f"📖 Explanation: {test_case['explanation'][:100]}...")
        print("-" * 40)
        
        try:
            # Test the quiz generation
            quiz_data = await service.generate_quiz(
                test_case["explanation"],
                test_case["difficulty"]
            )
            
            # Analyze the result
            print("✅ QUIZ GENERATED SUCCESSFULLY!")
            
            # Validate JSON structure
            if isinstance(quiz_data, dict) and "questions" in quiz_data:
                questions = quiz_data["questions"]
                print(f"📝 Number of questions: {len(questions)}")
                
                # Check each question
                for j, question in enumerate(questions, 1):
                    print(f"\n❓ Question {j}: {question.get('question', 'Missing question')[:80]}...")
                    
                    # Validate question structure
                    required_fields = ["id", "question", "type", "options", "correct_answer", "explanation"]
                    missing_fields = [field for field in required_fields if field not in question]
                    
                    if missing_fields:
                        print(f"   ❌ Missing fields: {missing_fields}")
                    else:
                        print(f"   ✅ All required fields present")
                        
                    # Check options
                    options = question.get("options", [])
                    if len(options) == 4:
                        print(f"   ✅ Has 4 options: {options}")
                    else:
                        print(f"   ❌ Expected 4 options, got {len(options)}")
                        
                    # Check correct answer
                    correct = question.get("correct_answer", "")
                    if correct in options:
                        print(f"   ✅ Correct answer '{correct}' is in options")
                    else:
                        print(f"   ❌ Correct answer '{correct}' not found in options")
                
                print("\n📋 Overall Quiz Quality Check:")
                checks = []
                checks.append(("5 questions", len(questions) == 5))
                checks.append(("All have 4 options", all(len(q.get("options", [])) == 4 for q in questions)))
                checks.append(("Valid correct answers", all(q.get("correct_answer") in q.get("options", []) for q in questions)))
                checks.append(("All have explanations", all(q.get("explanation") for q in questions)))
                checks.append(("Questions vary", len(set(q.get("question", "") for q in questions)) == len(questions)))
                
                for check_name, passed in checks:
                    status = "✅" if passed else "❌"
                    print(f"   {status} {check_name}")
                    
            else:
                print("❌ Invalid quiz structure - missing 'questions' key")
                print(f"📝 Received: {quiz_data}")
            
            print()
            
        except AssertionError as e:
            print(f"❌ IMPLEMENTATION ERROR: {e}")
            print("💡 TIP: Make sure you've implemented the function and removed the assertion!")
            print()
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON PARSING ERROR: {e}")
            print("💡 TIP: Make sure your prompt generates valid JSON format")
            print()
            
        except Exception as e:
            print(f"❌ RUNTIME ERROR: {e}")
            print("💡 TIP: Check your prompt structure and JSON parsing logic")
            print()
    
    print("🎯 TESTING TIPS:")
    print("1. Your quiz should have exactly 5 multiple choice questions")
    print("2. Each question should have 4 options (A, B, C, D)")
    print("3. The correct answer must be one of the 4 options")
    print("4. Include an explanation for why the answer is correct")
    print("5. Questions should be based on the explanation content")
    print()
    print("📚 Session 1 Concepts to Apply:")
    print("• Clear format specification: Exact JSON structure")
    print("• Specific requirements: 5 questions, 4 options each")
    print("• Difficulty adaptation: Adjust question complexity")
    print("• Output validation: Ensure proper JSON format")

def main():
    """Run the quiz generation tests"""
    try:
        asyncio.run(test_quiz_generation())
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"💥 Test failed with error: {e}")

if __name__ == "__main__":
    main()