#!/usr/bin/env python3
"""
Simple test script to verify the backend setup is working.
"""

def test_imports():
    """Test that all required modules can be imported."""
    try:
        print("Testing imports...")
        
        # Test FastAPI
        import fastapi
        print("✓ FastAPI imported successfully")
        
        # Test SQLAlchemy
        import sqlalchemy
        print(f"✓ SQLAlchemy imported successfully (version: {sqlalchemy.__version__})")
        
        # Test Uvicorn
        import uvicorn
        print("✓ Uvicorn imported successfully")
        
        # Test our app modules
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from app.database.database import Base, engine
        print("✓ Database modules imported successfully")
        
        from app.models.models import Student, Concept
        print("✓ Models imported successfully")
        
        from app.core.config import settings
        print("✓ Config imported successfully")
        
        print("\n✅ All imports successful! Backend setup is working.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_database():
    """Test database creation."""
    try:
        print("\nTesting database setup...")
        from app.database.database import engine
        from app.models.models import Base
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully")
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_optional_apis():
    """Test if optional API keys are configured."""
    print("\nChecking API configuration...")
    from app.core.config import settings
    
    if settings.GEMINI_API_KEY:
        print("✓ Gemini API key is configured")
    else:
        print("⚠️ Gemini API key not configured (explanations will use fallback)")
        print("   Set GEMINI_API_KEY in your .env file for full functionality")
    
    return True

if __name__ == "__main__":
    print("AI Concept Explainer - Backend Setup Test")
    print("=" * 50)
    
    success = True
    success &= test_imports()
    success &= test_database() 
    success &= test_optional_apis()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Backend setup test PASSED!")
        print("You can now run: python -m uvicorn app.main:app --reload")
    else:
        print("❌ Backend setup test FAILED!")
        print("Please fix the errors above before running the server.")