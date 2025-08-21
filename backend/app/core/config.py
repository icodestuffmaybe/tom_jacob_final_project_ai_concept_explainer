import os
from typing import Optional

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()  # This looks for .env in current directory
    print("Loaded .env file")
except ImportError:
    print("python-dotenv not installed, reading environment variables directly")

class Settings:
    PROJECT_NAME: str = "AI Concept Explainer"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    SEARCH_API_KEY: Optional[str] = os.getenv("SEARCH_API_KEY")
    
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()

# Debug: Print API key status (first 10 chars only for security)
if settings.GEMINI_API_KEY:
    print(f"Gemini API key loaded: {settings.GEMINI_API_KEY[:10]}...")
else:
    print("Gemini API key not found in environment")
    print("   Make sure .env file exists in backend directory")