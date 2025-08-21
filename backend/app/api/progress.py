from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database.database import get_db
from app.models.models import Student, Progress, Concept, LearningSession
from app.api.auth import get_current_user

router = APIRouter()

@router.get("/")
async def get_progress(
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    progress_records = db.query(Progress).filter(
        Progress.student_id == current_user.id
    ).all()
    
    concepts_progress = []
    for progress in progress_records:
        concept = db.query(Concept).filter(Concept.id == progress.concept_id).first()
        if concept:
            concepts_progress.append({
                "concept_id": concept.id,
                "name": concept.name,
                "subject": concept.subject,
                "mastery": progress.mastery_level or 0,
                "attempts": progress.attempts or 0,
                "last_reviewed": progress.last_reviewed
            })
    
    concepts_progress.sort(key=lambda x: x["mastery"], reverse=True)
    
    return {"concepts": concepts_progress}

@router.get("/stats")
async def get_progress_stats(
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total_concepts = db.query(Progress).filter(
        Progress.student_id == current_user.id
    ).count()
    
    mastered_concepts = db.query(Progress).filter(
        Progress.student_id == current_user.id,
        Progress.mastery_level >= 85
    ).count()
    
    recent_sessions = db.query(LearningSession).filter(
        LearningSession.student_id == current_user.id
    ).order_by(desc(LearningSession.started_at)).limit(5).all()
    
    total_sessions = db.query(LearningSession).filter(
        LearningSession.student_id == current_user.id
    ).count()
    
    return {
        "total_concepts_studied": total_concepts,
        "concepts_mastered": mastered_concepts,
        "mastery_percentage": (mastered_concepts / total_concepts * 100) if total_concepts > 0 else 0,
        "total_sessions": total_sessions,
        "recent_topics": [
            {
                "query": session.query,
                "started_at": session.started_at,
                "session_id": session.id
            } for session in recent_sessions
        ]
    }

@router.get("/concept/{concept_id}")
async def get_concept_progress(
    concept_id: str,
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    progress = db.query(Progress).filter(
        Progress.student_id == current_user.id,
        Progress.concept_id == concept_id
    ).first()
    
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    
    sessions = db.query(LearningSession).filter(
        LearningSession.student_id == current_user.id,
        LearningSession.concept_id == concept_id
    ).order_by(desc(LearningSession.started_at)).all()
    
    if not concept:
        return {"error": "Concept not found"}
    
    return {
        "concept": {
            "id": concept.id,
            "name": concept.name,
            "subject": concept.subject,
            "description": concept.description
        },
        "progress": {
            "mastery_level": progress.mastery_level if progress else 0,
            "attempts": progress.attempts if progress else 0,
            "last_reviewed": progress.last_reviewed if progress else None
        },
        "sessions": [
            {
                "id": session.id,
                "query": session.query,
                "started_at": session.started_at,
                "completed_at": session.completed_at
            } for session in sessions
        ]
    }