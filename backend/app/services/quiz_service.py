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
        # TODO: EXERCISE 1B - Implement Quiz Generation (Prompt Engineering Session)
        # INSTRUCTION: Create an AI prompt that generates multiple choice quizzes based on explanations
        # 
        # STEPS TO IMPLEMENT:
        # 1. Handle the case when self.model is None (return fallback quiz)
        # 2. Truncate explanation if too long (max 1000 chars to avoid token limits)
        # 3. Create a prompt that generates exactly 5 multiple choice questions
        # 4. Use JSON format specification (important for structured output)
        # 5. Parse and validate the JSON response
        # 6. Return properly formatted quiz data
        # 
        # PROMPT ENGINEERING TECHNIQUES (Session 1):
        # - Clear format specification (JSON structure)
        # - Specific requirements (5 questions, 4 options each)
        # - Examples of good questions
        # - Difficulty level adaptation
        # 
        # JSON FORMAT REQUIRED:
        # {
        #   "questions": [
        #     {
        #       "id": "q1",
        #       "question": "Question text here?",
        #       "type": "multiple_choice",
        #       "options": ["A", "B", "C", "D"],
        #       "correct_answer": "B",
        #       "explanation": "Why B is correct..."
        #     }
        #   ]
        # }
        # 
        # DIFFICULTY LEVELS:
        # - easy: Basic recall and recognition
        # - medium: Understanding and application  
        # - hard: Analysis and synthesis
        
        # TODO: Remove this assertion once you implement the function
        assert False, "❌ EXERCISE 1B NOT IMPLEMENTED: Please implement generate_quiz() function in quiz_service.py"
        
        # TODO: Implement your solution here
        
        if not self.model:
            return self.get_fallback_quiz()
            
        # TODO: Truncate explanation to prevent token limits
        explanation_summary = explanation[:1000] if len(explanation) > 1000 else explanation
            
        # TODO: Create your prompt here using Session 1 techniques
        prompt = f"""
        # Your quiz generation prompt goes here
        # Remember to:
        # - Specify exact JSON format
        # - Require 5 questions with 4 options each
        # - Base questions on the explanation content
        # - Adapt difficulty level: {difficulty}
        # - Include clear instructions
        """
        
        try:
            # TODO: Generate content using self.model.generate_content(prompt)
            # TODO: Clean the response (remove markdown formatting)
            # TODO: Parse JSON response
            # TODO: Validate the structure (5 questions, required fields)
            # TODO: Return quiz_data
            pass
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            return self.get_fallback_quiz()
        except Exception as e:
            print(f"❌ Error generating quiz: {e}")
            return self.get_fallback_quiz()
    
    def evaluate_quiz(self, quiz_data: Dict, student_answers: List[Dict]) -> Dict:
        # TODO: EXERCISE 3B - Implement Quiz Assessment Agent (AI Agents Session)
        # INSTRUCTION: Build intelligent quiz grading and feedback system
        # 
        # STEPS TO IMPLEMENT:
        # 1. Process the quiz_data and student_answers structures
        # 2. Match student answers to questions by question_id
        # 3. Grade each answer (multiple choice comparison)
        # 4. Calculate performance metrics:
        #    - Total score (percentage)
        #    - Number of correct answers
        #    - Total questions
        # 5. Determine mastery achievement (85% threshold)
        # 6. Generate detailed feedback per question
        # 7. Handle edge cases (missing answers, invalid IDs)
        # 
        # AI AGENTS TECHNIQUES (Session 3):
        # - Automated assessment: Systematic grading algorithms
        # - Performance analysis: Calculate meaningful metrics
        # - Adaptive feedback: Provide detailed explanations
        # - Learning analytics: Track progress patterns
        # 
        # INPUT DATA STRUCTURES:
        # quiz_data = {
        #     "questions": [
        #         {
        #             "id": "q1",
        #             "question": "Question text?",
        #             "type": "multiple_choice",
        #             "options": ["A", "B", "C", "D"],
        #             "correct_answer": "B",
        #             "explanation": "Why B is correct..."
        #         }, ...
        #     ]
        # }
        # 
        # student_answers = [
        #     {"question_id": "q1", "answer": "B"},
        #     {"question_id": "q2", "answer": "A"},
        #     ...
        # ]
        # 
        # EXPECTED RETURN FORMAT:
        # {
        #     "score": 80.0,
        #     "correct_answers": 4,
        #     "total_questions": 5,
        #     "mastery_achieved": False,  # True if >= 85%
        #     "feedback": [
        #         {
        #             "question_id": "q1",
        #             "correct": True,
        #             "explanation": "Explanation text...",
        #             "correct_answer": "B",
        #             "student_answer": "B"
        #         }, ...
        #     ]
        # }
        
        # TODO: Remove this assertion once you implement the function
        assert False, "❌ EXERCISE 3B NOT IMPLEMENTED: Please implement evaluate_quiz() function in quiz_service.py"
        
        # TODO: Implement your quiz evaluation solution here
        # Hints: 
        # - Use question_id to match answers to questions
        # - Handle missing or incomplete answers gracefully
        # - Calculate percentage: (correct/total) * 100
        # - Set mastery_achieved = score >= 85
        # - Include detailed feedback with explanations
        
        # REFERENCE IMPLEMENTATION STRUCTURE:
        questions = quiz_data.get("questions", [])
        total_questions = len(questions)
        correct_answers = 0
        feedback = []
        
        # TODO: Your grading logic goes here
        
        return {
            "score": 0,
            "correct_answers": 0,
            "total_questions": total_questions,
            "feedback": [],
            "mastery_achieved": False
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