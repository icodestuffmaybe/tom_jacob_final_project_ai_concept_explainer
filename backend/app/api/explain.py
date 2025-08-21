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
    # TODO: EXERCISE 3A - Implement Student Evaluation Agent (AI Agents Session)
    # INSTRUCTION: Create an AI agent that evaluates student explanations using ReAct framework
    # 
    # STEPS TO IMPLEMENT:
    # 1. Retrieve the learning session from database
    # 2. Create an evaluation agent that uses ReAct pattern (Reason → Act → Observe)
    # 3. Compare student explanation with original AI explanation
    # 4. Identify knowledge gaps and provide feedback
    # 5. Parse the agent's response into structured format
    # 6. Return evaluation results
    # 
    # REACT AGENT PATTERN (Session 3):
    # - Thought: Agent reasons about the comparison task
    # - Action: Agent analyzes gaps and generates feedback
    # - Observation: Agent reviews its analysis for completeness
    # 
    # AGENT BEHAVIOR REQUIREMENTS:
    # - Act as an educational evaluator
    # - Use step-by-step reasoning
    # - Provide constructive feedback
    # - Identify specific knowledge gaps
    # - Suggest improvements
    # 
    # EXAMPLE AGENT PROMPT STRUCTURE:
    # """
    # You are an educational evaluation agent. Your task is to assess student understanding.
    # 
    # THOUGHT: I need to compare the student's explanation with the correct explanation.
    # ACTION: I will analyze gaps, misconceptions, and areas for improvement.
    # OBSERVATION: I will ensure my feedback is constructive and specific.
    # 
    # Original explanation: {session.explanation}
    # Student explanation: {request.explanation}
    # 
    # Please provide:
    # GAPS: [specific missing concepts]
    # CLARIFICATIONS: [areas needing clarification]  
    # SIMPLIFIED: [simplified explanation to help]
    # """
    
    # TODO: Remove this assertion once you implement the function
    assert False, "❌ EXERCISE 3A NOT IMPLEMENTED: Please implement process_student_explanation() agent in explain.py"
    
    # TODO: Implement your solution here
    
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
            
        # TODO: Create your ReAct agent prompt here using Session 3 techniques
        prompt = f"""
        # Your evaluation agent prompt goes here
        # Remember to:
        # - Use ReAct pattern (Thought → Action → Observation)
        # - Act as educational evaluator
        # - Compare explanations systematically
        # - Provide structured output format
        # - Be constructive and helpful
        """
        
        # TODO: Generate content using the agent
        # TODO: Parse the response into gaps, clarifications, simplified
        # TODO: Return structured evaluation results
        pass
        
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