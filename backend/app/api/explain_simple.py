from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database.database import get_db
from app.models.models import LearningSession, Concept
from app.services.explanation_service import ExplanationService
from app.services.svg_generator import SVGGenerator

router = APIRouter()

class ExplanationRequest(BaseModel):
    query: str

@router.post("/explain")
async def explain_concept(
    request: ExplanationRequest,
    db: Session = Depends(get_db)
):
    explanation_service = ExplanationService()
    svg_generator = SVGGenerator()
    
    try:
        explanation_result = await explanation_service.explain_concept(request.query)
        svg_flashcard = await svg_generator.generate_svg_flashcard(
            request.query, 
            explanation_result["explanation"]
        )
        
        # Create or find concept (without user association)
        concept = db.query(Concept).filter(Concept.name == request.query).first()
        if not concept:
            concept = Concept(
                name=request.query,
                description=explanation_result["explanation"][:500]
            )
            db.add(concept)
            db.commit()
            db.refresh(concept)
        
        # Create learning session (without user association)
        session = LearningSession(
            student_id="demo-user",  # Static demo user
            concept_id=concept.id,
            query=request.query,
            explanation=explanation_result["explanation"],
            sources=explanation_result["sources"],
            svg_diagrams=[svg_flashcard]
        )
        
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return {
            "explanation": explanation_result["explanation"],
            "sources": explanation_result["sources"],
            "svg_flashcard": svg_flashcard,
            "session_id": session.id,
            "keywords": explanation_result.get("keywords", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating explanation: {str(e)}")

@router.get("/recommendations/{concept_id}")
async def get_recommendations(
    concept_id: str,
    db: Session = Depends(get_db)
):
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    
    related_concepts = db.query(Concept).filter(
        Concept.subject == concept.subject,
        Concept.id != concept.id
    ).limit(5).all()
    
    return {
        "prerequisites": concept.prerequisites or [],
        "next_topics": [
            {
                "id": c.id,
                "name": c.name,
                "reason": f"Related to {concept.subject}"
            } for c in related_concepts[:3]
        ],
        "related": [
            {
                "id": c.id,
                "name": c.name,
                "subject": c.subject
            } for c in related_concepts
        ]
    }