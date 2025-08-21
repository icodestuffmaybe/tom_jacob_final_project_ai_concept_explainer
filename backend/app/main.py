from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, explain, quiz, progress
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

app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(explain.router, prefix="/api", tags=["explanation"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["quiz"])
app.include_router(progress.router, prefix="/api/progress", tags=["progress"])

@app.get("/")
async def root():
    return {"message": "AI Concept Explainer API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}