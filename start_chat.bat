@echo off
echo Starting AI Concept Explainer - ChatGPT Style Interface
echo.

echo Starting Backend (Simple Mode)...
cd backend
start "AI Backend" cmd /k "venv\Scripts\activate && echo ✅ Backend running on http://localhost:8000 && python -m uvicorn app.main_simple:app --reload --host 0.0.0.0 --port 8000"

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo Starting Frontend (Chat Interface)...
cd ..\frontend
start "AI Frontend" cmd /k "echo ✅ Frontend running on http://localhost:5173 && npm run dev"

echo.
echo 🎉 AI Concept Explainer is starting...
echo.
echo 💬 Chat Interface: http://localhost:5173
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Features:
echo - ChatGPT-style conversation
echo - Feynman technique explanations
echo - AI-generated SVG flashcards
echo - Interactive quizzes
echo - Related topic suggestions
echo.
echo Press any key to close this window...
pause >nul