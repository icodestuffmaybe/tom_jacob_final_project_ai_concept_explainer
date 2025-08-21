@echo off
echo Starting AI Concept Explainer (Simple Mode - No Authentication)...
echo.

echo Starting Backend...
cd backend
start "Backend Server" cmd /k "venv\Scripts\activate && echo Backend starting on http://localhost:8000 && python -m uvicorn app.main_simple:app --reload --host 0.0.0.0 --port 8000"

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo Starting Frontend...
cd ..\frontend
start "Frontend Server" cmd /k "echo Frontend starting on http://localhost:5173 && npm run dev"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000/docs
echo Frontend: http://localhost:5173
echo.
echo Press any key to close this window...
pause >nul