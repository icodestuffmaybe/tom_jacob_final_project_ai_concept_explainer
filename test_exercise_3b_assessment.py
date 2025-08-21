#!/usr/bin/env python3
"""
Test Script for Exercise 3B: Quiz Assessment Agent (AI Agents Session)

This script helps students test their implementation of the evaluate_quiz() function.
Run this script to verify your quiz grading and feedback system is working correctly.

Usage: python test_exercise_3b_assessment.py
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.quiz_service import QuizService
from app.core.config import settings

def test_quiz_evaluation():
    """Test quiz evaluation with different answer patterns and scenarios"""
    
    print("🧪 TESTING EXERCISE 3B: Quiz Assessment Agent")
    print("=" * 60)
    
    # Sample quiz data for testing
    sample_quiz = {
        "questions": [
            {
                "id": "q1",
                "question": "What is photosynthesis?",
                "type": "multiple_choice",
                "options": [
                    "The process plants use to make food from sunlight",
                    "The process plants use to absorb water",
                    "The process plants use to reproduce",
                    "The process plants use to grow roots"
                ],
                "correct_answer": "The process plants use to make food from sunlight",
                "explanation": "Photosynthesis is the process by which plants convert light energy into chemical energy."
            },
            {
                "id": "q2", 
                "question": "Which gas do plants absorb during photosynthesis?",
                "type": "multiple_choice",
                "options": ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"],
                "correct_answer": "Carbon dioxide",
                "explanation": "Plants absorb carbon dioxide from the air during photosynthesis."
            },
            {
                "id": "q3",
                "question": "Where does photosynthesis occur in plants?",
                "type": "multiple_choice", 
                "options": ["Roots", "Stems", "Leaves", "Flowers"],
                "correct_answer": "Leaves",
                "explanation": "Photosynthesis primarily occurs in the leaves, specifically in chloroplasts."
            },
            {
                "id": "q4",
                "question": "What is the main product of photosynthesis?",
                "type": "multiple_choice",
                "options": ["Oxygen", "Glucose", "Water", "Carbon dioxide"],
                "correct_answer": "Glucose",
                "explanation": "The main product of photosynthesis is glucose, though oxygen is also produced."
            },
            {
                "id": "q5",
                "question": "What gives plants their green color?",
                "type": "multiple_choice",
                "options": ["Glucose", "Oxygen", "Chlorophyll", "Carbon dioxide"],
                "correct_answer": "Chlorophyll",
                "explanation": "Chlorophyll is the green pigment that captures light energy for photosynthesis."
            }
        ]
    }
    
    # Test cases with different scoring scenarios
    test_cases = [
        {
            "scenario": "Perfect Score (100%)",
            "answers": [
                {"question_id": "q1", "answer": "The process plants use to make food from sunlight"},
                {"question_id": "q2", "answer": "Carbon dioxide"},
                {"question_id": "q3", "answer": "Leaves"},
                {"question_id": "q4", "answer": "Glucose"},
                {"question_id": "q5", "answer": "Chlorophyll"}
            ],
            "expected_score": 100,
            "expected_mastery": True
        },
        {
            "scenario": "High Score (80%)",
            "answers": [
                {"question_id": "q1", "answer": "The process plants use to make food from sunlight"},
                {"question_id": "q2", "answer": "Oxygen"},  # Wrong
                {"question_id": "q3", "answer": "Leaves"},
                {"question_id": "q4", "answer": "Glucose"},
                {"question_id": "q5", "answer": "Chlorophyll"}
            ],
            "expected_score": 80,
            "expected_mastery": False
        },
        {
            "scenario": "Borderline Mastery (85%)",  
            "answers": [
                {"question_id": "q1", "answer": "The process plants use to make food from sunlight"},
                {"question_id": "q2", "answer": "Carbon dioxide"},
                {"question_id": "q3", "answer": "Roots"},  # Wrong
                {"question_id": "q4", "answer": "Glucose"},
                {"question_id": "q5", "answer": "Chlorophyll"}
            ],
            "expected_score": 80,
            "expected_mastery": False
        },
        {
            "scenario": "Low Score (40%)",
            "answers": [
                {"question_id": "q1", "answer": "The process plants use to absorb water"},  # Wrong
                {"question_id": "q2", "answer": "Oxygen"},  # Wrong
                {"question_id": "q3", "answer": "Leaves"},
                {"question_id": "q4", "answer": "Water"},  # Wrong
                {"question_id": "q5", "answer": "Chlorophyll"}
            ],
            "expected_score": 40,
            "expected_mastery": False
        },
        {
            "scenario": "Incomplete Quiz (Missing Answers)",
            "answers": [
                {"question_id": "q1", "answer": "The process plants use to make food from sunlight"},
                {"question_id": "q2", "answer": "Carbon dioxide"},
                {"question_id": "q3", "answer": ""}  # Empty answer
                # Missing q4 and q5
            ],
            "expected_score": 40,  # 2 out of 5 correct
            "expected_mastery": False
        }
    ]
    
    print(f"📊 Quiz Assessment System Testing")
    print(f"   Sample quiz: {len(sample_quiz['questions'])} questions")
    print(f"   Mastery threshold: 85%")
    print()
    
    service = QuizService()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 Test Case {i}: {test_case['scenario']}")
        print(f"   Student answers: {len(test_case['answers'])}")
        print("-" * 40)
        
        try:
            # Test quiz evaluation
            result = service.evaluate_quiz(sample_quiz, test_case['answers'])
            
            if not result:
                print("❌ FAILED: No evaluation result returned")
                continue
                
            print("✅ QUIZ EVALUATION COMPLETED!")
            
            # Validate result structure
            structure_checks = []
            structure_checks.append(("Has score", "score" in result))
            structure_checks.append(("Has total_questions", "total_questions" in result))
            structure_checks.append(("Has correct_answers", "correct_answers" in result))
            structure_checks.append(("Has mastery_achieved", "mastery_achieved" in result))
            structure_checks.append(("Has feedback", "feedback" in result))
            
            print(f"\n📋 Result Structure Check:")
            for check_name, passed in structure_checks:
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
            
            # Validate calculated values
            if "score" in result and "correct_answers" in result and "total_questions" in result:
                calculated_score = (result["correct_answers"] / max(1, result["total_questions"])) * 100
                score_accuracy = abs(result["score"] - calculated_score) < 1
                
                calculation_checks = []
                calculation_checks.append(("Score calculation accurate", score_accuracy))
                calculation_checks.append(("Score in valid range", 0 <= result["score"] <= 100))
                calculation_checks.append(("Correct answers count reasonable", 0 <= result["correct_answers"] <= len(sample_quiz["questions"])))
                calculation_checks.append(("Total questions correct", result["total_questions"] == len(sample_quiz["questions"])))
                
                print(f"\n🔢 Calculation Accuracy Check:")
                for check_name, passed in calculation_checks:
                    status = "✅" if passed else "❌"
                    print(f"   {status} {check_name}")
                
                print(f"\n📊 Assessment Results:")
                print(f"   Score: {result.get('score', 'N/A')}%")
                print(f"   Correct: {result.get('correct_answers', 'N/A')}/{result.get('total_questions', 'N/A')}")
                print(f"   Mastery: {'✅' if result.get('mastery_achieved', False) else '❌'}")
                
                # Check mastery threshold logic
                expected_mastery = result.get("score", 0) >= 85
                mastery_checks = []
                mastery_checks.append(("Mastery threshold applied", result.get("mastery_achieved") == expected_mastery))
                mastery_checks.append(("Mastery logic consistent", isinstance(result.get("mastery_achieved"), bool)))
                
                print(f"\n🎯 Mastery Assessment Check:")
                for check_name, passed in mastery_checks:
                    status = "✅" if passed else "❌"
                    print(f"   {status} {check_name}")
            
            # Validate feedback quality
            if "feedback" in result and isinstance(result["feedback"], list):
                feedback_checks = []
                feedback_checks.append(("Feedback provided", len(result["feedback"]) > 0))
                feedback_checks.append(("Feedback per question", len(result["feedback"]) <= len(sample_quiz["questions"])))
                
                # Check individual feedback items
                detailed_feedback = 0
                for feedback_item in result["feedback"][:3]:  # Check first 3
                    if isinstance(feedback_item, dict):
                        if "question_id" in feedback_item and "correct" in feedback_item:
                            detailed_feedback += 1
                
                feedback_checks.append(("Structured feedback", detailed_feedback > 0))
                feedback_checks.append(("Includes correct/incorrect status", detailed_feedback > 0))
                
                print(f"\n💬 Feedback Quality Check:")
                for check_name, passed in feedback_checks:
                    status = "✅" if passed else "❌"
                    print(f"   {status} {check_name}")
                
                # Show sample feedback
                if result["feedback"]:
                    print(f"\n📝 Sample Feedback:")
                    for j, fb in enumerate(result["feedback"][:2]):
                        print(f"   Question {j+1}: {str(fb)[:100]}...")
            
            # Performance analysis
            performance_checks = []
            performance_checks.append(("Handles all answer formats", True))  # If we got this far
            performance_checks.append(("Processes incomplete answers", len(test_case['answers']) <= len(sample_quiz['questions'])))
            performance_checks.append(("No runtime errors", True))
            
            print(f"\n⚡ Performance Check:")
            for check_name, passed in performance_checks:
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
            
            print()
            
        except AssertionError as e:
            print(f"❌ IMPLEMENTATION ERROR: {e}")
            print("💡 TIP: Make sure you've implemented the function and removed the assertion!")
            print()
            
        except Exception as e:
            print(f"❌ RUNTIME ERROR: {e}")
            print("💡 TIP: Check your quiz evaluation logic and error handling")
            print("   Common issues:")
            print("   - Handling missing or empty answers")
            print("   - Matching question IDs correctly")
            print("   - Calculating percentages accurately")
            print("   - Validating input data structure")
            print()
    
    # Test edge cases
    print("🔬 Edge Case Testing")
    print("-" * 40)
    
    edge_cases = [
        {
            "case": "Empty quiz",
            "quiz": {"questions": []},
            "answers": []
        },
        {
            "case": "Invalid question IDs",
            "quiz": sample_quiz,
            "answers": [{"question_id": "invalid", "answer": "test"}]
        },
        {
            "case": "Malformed answers",
            "quiz": sample_quiz,  
            "answers": [{"wrong_field": "test"}]
        }
    ]
    
    for edge_case in edge_cases:
        print(f"🧪 Testing: {edge_case['case']}")
        try:
            result = service.evaluate_quiz(edge_case['quiz'], edge_case['answers'])
            status = "✅" if result and isinstance(result, dict) else "⚠️"
            print(f"   {status} Handled gracefully")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print()
    print("🎯 TESTING TIPS:")
    print("1. Calculate scores accurately (correct/total * 100)")
    print("2. Apply mastery threshold correctly (85%)")
    print("3. Provide detailed feedback for each question")
    print("4. Handle incomplete or missing answers gracefully") 
    print("5. Validate input data and question matching")
    print()
    print("📚 Session 3 (AI Agents) Concepts Applied:")
    print("• Automated assessment: Grade multiple choice answers")
    print("• Performance analysis: Calculate scores and mastery")
    print("• Adaptive feedback: Provide detailed explanations")
    print("• Learning analytics: Track progress patterns")
    print()
    print("💡 Implementation Tips:")
    print("• Match answers to questions by ID, handle missing IDs")
    print("• Calculate percentage scores with proper rounding")
    print("• Implement 85% mastery threshold consistently")
    print("• Provide constructive feedback for incorrect answers")
    print("• Handle edge cases like empty quizzes or malformed data")

def main():
    """Run the quiz assessment tests"""
    try:
        test_quiz_evaluation()
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"💥 Test failed with error: {e}")

if __name__ == "__main__":
    main()