#!/usr/bin/env python3
"""
Test script to verify the optimizations work correctly.
"""

import requests
import time
import json

def test_optimized_backend():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Optimized AI Concept Explainer")
    print("=" * 50)
    
    # Test 1: Fast explanation generation
    print("1. Testing explanation speed optimization...")
    test_query = "What is gravity?"
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{base_url}/api/explain",
            json={"query": test_query},
            timeout=30
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"   ⏱️ Time taken: {duration:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Explanation generated successfully")
            print(f"   📝 Length: {len(data.get('explanation', ''))}")
            print(f"   🔗 Sources: {len(data.get('sources', []))}")
            print(f"   🎨 SVG: {'Yes' if data.get('svg_flashcard') else 'No'}")
            
            session_id = data.get('session_id')
            
            if session_id:
                # Test 2: Quiz generation with better prompts
                print("\n2. Testing improved quiz generation...")
                quiz_start = time.time()
                
                quiz_response = requests.post(
                    f"{base_url}/api/quiz/generate",
                    json={"session_id": session_id, "difficulty": "medium"},
                    timeout=15
                )
                
                quiz_end = time.time()
                quiz_duration = quiz_end - quiz_start
                
                print(f"   ⏱️ Quiz generation time: {quiz_duration:.2f} seconds")
                
                if quiz_response.status_code == 200:
                    quiz_data = quiz_response.json()
                    questions = quiz_data.get('questions', [])
                    
                    print(f"   ✅ Quiz generated successfully")
                    print(f"   📝 Questions: {len(questions)}")
                    
                    # Check question relevance
                    for i, q in enumerate(questions[:3]):  # Show first 3
                        print(f"   Q{i+1}: {q.get('question', '')[:60]}...")
                        print(f"       Options: {len(q.get('options', []))}")
                    
                    # Test 3: Quiz submission
                    print("\n3. Testing quiz evaluation...")
                    
                    # Create test answers (all first option)
                    test_answers = [
                        {"question_id": q.get("id"), "answer": q.get("options", [""])[0]}
                        for q in questions
                    ]
                    
                    eval_response = requests.post(
                        f"{base_url}/api/quiz/submit",
                        json={"quiz_id": quiz_data.get("quiz_id"), "answers": test_answers},
                        timeout=10
                    )
                    
                    if eval_response.status_code == 200:
                        result = eval_response.json()
                        print(f"   ✅ Quiz evaluation successful")
                        print(f"   📊 Score: {result.get('score', 0):.1f}%")
                        print(f"   ✓ Correct: {result.get('correct_answers', 0)}/{result.get('total_questions', 0)}")
                        print(f"   🎯 Mastery: {'Yes' if result.get('mastery_achieved') else 'No'}")
                    else:
                        print(f"   ❌ Quiz evaluation failed: {eval_response.status_code}")
                        print(f"   Error: {eval_response.text}")
                
                else:
                    print(f"   ❌ Quiz generation failed: {quiz_response.status_code}")
                    print(f"   Error: {quiz_response.text}")
            
        else:
            print(f"   ❌ Explanation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except requests.exceptions.Timeout:
        print(f"   ⏰ Request timed out (>{30}s)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Optimization Test Summary:")
    print("1. ⚡ Faster source searching (limited to 1 source)")
    print("2. 🧠 Gemini 2.5 Pro for better quality")
    print("3. 📝 Improved quiz relevance with better prompts")
    print("4. 🔧 Better error handling and JSON parsing")
    print("5. 🎨 Timeout optimizations (3s Wikipedia)")

if __name__ == "__main__":
    test_optimized_backend()