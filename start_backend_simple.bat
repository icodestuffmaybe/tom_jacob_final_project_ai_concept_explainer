@echo off
echo Starting AI Concept Explainer Backend (Simple Mode - NO AUTHENTICATION)
echo.

cd backend

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing/updating dependencies...
pip install python-dotenv

echo.
echo Checking environment configuration...
if not exist .env (
    echo Copying .env file...
    copy ..\.env .env
)

echo.
echo Starting Simple Backend (main_simple.py)...
echo API will be available at: http://localhost:8000
echo API documentation: http://localhost:8000/docs
echo.
echo IMPORTANT: This version has NO AUTHENTICATION
echo.

python -m uvicorn app.main_simple:app --reload --host 0.0.0.0 --port 8000