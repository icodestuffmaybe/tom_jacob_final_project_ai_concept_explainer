from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import explain_simple, quiz_simple
from app.database.database import engine
from app.models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Concept Explainer API",
    description="Educational AI system for explaining concepts with source verification",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(explain_simple.router, prefix="/api", tags=["explanation"])
app.include_router(quiz_simple.router, prefix="/api/quiz", tags=["quiz"])

@app.get("/")
async def root():
    return {"message": "AI Concept Explainer API - Simple Mode"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}