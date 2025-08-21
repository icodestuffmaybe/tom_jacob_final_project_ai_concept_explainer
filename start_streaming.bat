@echo off
echo ===============================================
echo    AI Concept Explainer - STREAMING MODE
echo ===============================================
echo.
echo Features:
echo ✨ Real-time thinking process visualization
echo 🧠 Step-by-step AI reasoning display
echo 📊 Live progress tracking
echo 🎨 Enhanced animations and effects
echo.

echo Starting Backend (Simple Mode)...
cd backend
start "AI Backend - Streaming" cmd /k "venv\Scripts\activate && echo ✅ Backend running on http://localhost:8000 && echo 📡 Streaming mode enabled && python -m uvicorn app.main_simple:app --reload --host 0.0.0.0 --port 8000"

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo Starting Frontend (Streaming Chat Interface)...
cd ..\frontend
start "AI Frontend - Streaming" cmd /k "echo ✅ Frontend running on http://localhost:5173 && echo 🌊 Streaming interface active && npm run dev"

echo.
echo 🚀 AI Concept Explainer STREAMING MODE is starting...
echo.
echo 💬 Streaming Chat: http://localhost:5173
echo 📚 API Documentation: http://localhost:8000/docs
echo.
echo ===============================================
echo                STREAMING FEATURES
echo ===============================================
echo 🔄 Real-time process visualization:
echo    - Keyword extraction
echo    - Source searching 
echo    - Explanation generation
echo    - Visual creation
echo    - Quiz preparation
echo.
echo 📈 Live progress bars and status updates
echo ⚡ Smooth animations and transitions
echo 🎯 Step-by-step learning process
echo.
echo Press any key to close this window...
pause >nul