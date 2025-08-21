from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database.database import get_db
from app.models.models import Student, LearningSession, Concept
from app.services.explanation_service import ExplanationService
from app.services.svg_generator import SVGGenerator
from app.api.auth import get_current_user

router = APIRouter()

class ExplanationRequest(BaseModel):
    query: str

class FeynmanRequest(BaseModel):
    session_id: str
    explanation: str

@router.post("/explain")
async def explain_concept(
    request: ExplanationRequest,
    current_user: Student = Depends(get_current_user),
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
        
        concept = db.query(Concept).filter(Concept.name == request.query).first()
        if not concept:
            concept = Concept(
                name=request.query,
                description=explanation_result["explanation"][:500]
            )
            db.add(concept)
            db.commit()
            db.refresh(concept)
        
        session = LearningSession(
            student_id=current_user.id,
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

@router.post("/feynman/student-explanation")
async def process_student_explanation(
    request: FeynmanRequest,
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(LearningSession).filter(
        LearningSession.id == request.session_id,
        LearningSession.student_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Learning session not found")
    
    explanation_service = ExplanationService()
    
    try:
        if not explanation_service.model:
            return {
                "gaps_identified": ["Gemini API not configured"],
                "clarifications": "Please configure the Gemini API key to use this feature.",
                "simplified_explanation": "Feature unavailable without API configuration"
            }
            
        prompt = f"""
        Original explanation: {session.explanation}
        
        Student's explanation: {request.explanation}
        
        Compare these explanations and identify:
        1. What gaps exist in the student's understanding?
        2. What clarifications are needed?
        3. Provide a simplified explanation to help the student understand better.
        
        Format your response as:
        GAPS: [list key missing concepts]
        CLARIFICATIONS: [explain what needs to be clarified]
        SIMPLIFIED: [provide simpler explanation]
        """
        
        response = explanation_service.model.generate_content(prompt)
        response_text = response.text
        
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
        
        return {
            "gaps_identified": gaps,
            "clarifications": clarifications,
            "simplified_explanation": simplified
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing explanation: {str(e)}")

@router.get("/recommendations/{concept_id}")
async def get_recommendations(
    concept_id: str,
    current_user: Student = Depends(get_current_user),
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