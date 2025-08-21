import google.generativeai as genai
import json
from typing import Dict, List
from app.core.config import settings

class QuizService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.5-pro')  # Using Pro version
        else:
            self.model = None
    
    async def generate_quiz(self, explanation: str, difficulty: str = "medium") -> Dict:
        if not self.model:
            return self.get_fallback_quiz()
            
        # Truncate explanation to prevent token limits
        explanation_summary = explanation[:1000] if len(explanation) > 1000 else explanation
            
        prompt = f"""
        IMPORTANT: Generate ONLY 5 multiple choice questions based DIRECTLY on this explanation:

        EXPLANATION TO BASE QUIZ ON:
        {explanation_summary}
        
        DIFFICULTY: {difficulty}
        
        REQUIREMENTS:
        - Create exactly 5 multiple choice questions
        - Each question must be directly about concepts mentioned in the explanation above
        - Include 4 options (A, B, C, D) for each question
        - Questions should test understanding of the explanation content
        - Age-appropriate for grades 7-12
        
        RETURN ONLY THIS JSON FORMAT (no other text):
        {{
            "questions": [
                {{
                    "id": "q1",
                    "question": "Based on the explanation, what is...",
                    "type": "multiple_choice",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option B",
                    "explanation": "This is correct because..."
                }},
                {{
                    "id": "q2",
                    "question": "According to the explanation, which...",
                    "type": "multiple_choice", 
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option C",
                    "explanation": "This is correct because..."
                }},
                {{
                    "id": "q3",
                    "question": "The explanation mentions that...",
                    "type": "multiple_choice",
                    "options": ["Option A", "Option B", "Option C", "Option D"], 
                    "correct_answer": "Option A",
                    "explanation": "This is correct because..."
                }},
                {{
                    "id": "q4",
                    "question": "From the explanation, we learn that...",
                    "type": "multiple_choice",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option D", 
                    "explanation": "This is correct because..."
                }},
                {{
                    "id": "q5",
                    "question": "The explanation describes...",
                    "type": "multiple_choice",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option B",
                    "explanation": "This is correct because..."
                }}
            ]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean the response - remove any markdown formatting
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            print(f"📝 Quiz JSON response: {response_text[:200]}...")
            
            quiz_data = json.loads(response_text)
            
            # Validate the structure
            if "questions" not in quiz_data or len(quiz_data["questions"]) != 5:
                print("❌ Invalid quiz structure, using fallback")
                return self.get_fallback_quiz()
                
            # Ensure all questions have required fields
            for i, q in enumerate(quiz_data["questions"]):
                if not all(key in q for key in ["id", "question", "type", "options", "correct_answer", "explanation"]):
                    print(f"❌ Question {i+1} missing required fields")
                    return self.get_fallback_quiz()
            
            print(f"✅ Generated {len(quiz_data['questions'])} questions successfully")
            return quiz_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"Raw response: {response.text}")
            return self.get_fallback_quiz()
        except Exception as e:
            print(f"❌ Error generating quiz: {e}")
            return self.get_fallback_quiz()
    
    def evaluate_quiz(self, quiz_data: Dict, student_answers: List[Dict]) -> Dict:
        print(f"🔍 Evaluating quiz with {len(student_answers)} answers")
        
        questions = quiz_data.get("questions", [])
        total_questions = len(questions)
        correct_answers = 0
        feedback = []
        
        for i, answer in enumerate(student_answers):
            question_id = answer.get("question_id")
            student_answer = answer.get("answer", "").strip()
            
            print(f"📝 Processing answer {i+1}: {question_id} = {student_answer}")
            
            # Find the corresponding question
            question = next(
                (q for q in questions if q.get("id") == question_id),
                None
            )
            
            if not question:
                print(f"❌ Question not found: {question_id}")
                continue
            
            correct_answer = question.get("correct_answer", "").strip()
            is_correct = student_answer.lower() == correct_answer.lower()
            
            if is_correct:
                correct_answers += 1
                print(f"✅ Correct! {student_answer} == {correct_answer}")
            else:
                print(f"❌ Incorrect: {student_answer} != {correct_answer}")
                
            feedback.append({
                "question_id": question_id,
                "correct": is_correct,
                "explanation": question.get("explanation", ""),
                "correct_answer": correct_answer,
                "student_answer": student_answer
            })
        
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        mastery_achieved = score >= 85
        
        print(f"📊 Final score: {score}% ({correct_answers}/{total_questions})")
        
        return {
            "score": score,
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "feedback": feedback,
            "mastery_achieved": mastery_achieved
        }
    
    def evaluate_short_answer(self, student_answer: str, sample_answer: str) -> float:
        if not student_answer or not sample_answer:
            return 0.0
            
        student_words = set(student_answer.lower().split())
        sample_words = set(sample_answer.lower().split())
        
        if not sample_words:
            return 0.0
            
        intersection = student_words.intersection(sample_words)
        similarity = len(intersection) / len(sample_words)
        
        return min(similarity, 1.0)
    
    def get_fallback_quiz(self) -> Dict:
        return {
            "questions": [
                {
                    "id": "q1",
                    "question": "What was the main concept explained?",
                    "type": "short_answer",
                    "sample_answer": "Please refer to the explanation provided",
                    "explanation": "Summarize the key points from the explanation"
                }
            ]
        }