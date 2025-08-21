@echo off
echo Starting AI Concept Explainer Backend...
echo.

cd backend

echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment. Make sure Python is installed.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip uninstall -y sqlalchemy
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo Testing setup...
python test_setup.py
if %errorlevel% neq 0 (
    echo Setup test failed. Please check the errors above.
    pause
    exit /b 1
)

echo.
echo Starting FastAPI server...
echo API will be available at: http://localhost:8000
echo API documentation: http://localhost:8000/docs
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000