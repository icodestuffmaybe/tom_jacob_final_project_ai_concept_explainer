from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict

from app.database.database import get_db
from app.models.models import Student, LearningSession, Quiz, Progress
from app.services.quiz_service import QuizService
from app.api.auth import get_current_user

router = APIRouter()

class GenerateQuizRequest(BaseModel):
    session_id: str
    difficulty: str = "medium"

class QuizAnswer(BaseModel):
    question_id: str
    answer: str

class SubmitQuizRequest(BaseModel):
    quiz_id: str
    answers: List[QuizAnswer]

@router.post("/generate")
async def generate_quiz(
    request: GenerateQuizRequest,
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(LearningSession).filter(
        LearningSession.id == request.session_id,
        LearningSession.student_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Learning session not found")
    
    quiz_service = QuizService()
    
    try:
        quiz_data = await quiz_service.generate_quiz(
            session.explanation, 
            request.difficulty
        )
        
        quiz = Quiz(
            session_id=request.session_id,
            questions=quiz_data,
            student_responses={},
            score=0.0,
            mastery_achieved=False
        )
        
        db.add(quiz)
        db.commit()
        db.refresh(quiz)
        
        return {
            "quiz_id": quiz.id,
            "questions": quiz_data.get("questions", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")

@router.post("/submit")
async def submit_quiz(
    request: SubmitQuizRequest,
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    quiz = db.query(Quiz).join(LearningSession).filter(
        Quiz.id == request.quiz_id,
        LearningSession.student_id == current_user.id
    ).first()
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    quiz_service = QuizService()
    
    try:
        answers_dict = [{"question_id": ans.question_id, "answer": ans.answer} for ans in request.answers]
        
        evaluation = quiz_service.evaluate_quiz(quiz.questions, answers_dict)
        
        quiz.student_responses = {"answers": answers_dict}
        quiz.score = evaluation["score"]
        quiz.mastery_achieved = evaluation["mastery_achieved"]
        
        db.commit()
        
        session = db.query(LearningSession).filter(LearningSession.id == quiz.session_id).first()
        if session and session.concept_id:
            progress = db.query(Progress).filter(
                Progress.student_id == current_user.id,
                Progress.concept_id == session.concept_id
            ).first()
            
            if progress:
                progress.mastery_level = max(progress.mastery_level or 0, evaluation["score"])
                progress.attempts = (progress.attempts or 0) + 1
            else:
                progress = Progress(
                    student_id=current_user.id,
                    concept_id=session.concept_id,
                    mastery_level=evaluation["score"],
                    attempts=1
                )
                db.add(progress)
            
            db.commit()
        
        return {
            "score": evaluation["score"],
            "feedback": evaluation["feedback"],
            "mastery_achieved": evaluation["mastery_achieved"],
            "correct_answers": evaluation["correct_answers"],
            "total_questions": evaluation["total_questions"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting quiz: {str(e)}")

@router.get("/{quiz_id}")
async def get_quiz(
    quiz_id: str,
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    quiz = db.query(Quiz).join(LearningSession).filter(
        Quiz.id == quiz_id,
        LearningSession.student_id == current_user.id
    ).first()
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return {
        "quiz_id": quiz.id,
        "questions": quiz.questions.get("questions", []),
        "score": quiz.score,
        "mastery_achieved": quiz.mastery_achieved,
        "created_at": quiz.created_at
    }