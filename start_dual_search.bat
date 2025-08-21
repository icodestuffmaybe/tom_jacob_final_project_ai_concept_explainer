@echo off
echo ===============================================
echo   AI Concept Explainer - DUAL SEARCH MODE
echo ===============================================
echo.
echo Enhanced Search Features:
echo 🔍 Wikipedia + DuckDuckGo dual search
echo 📰 Authoritative Wikipedia content  
echo 🦆 Educational web content from DuckDuckGo
echo 🎓 Educational domain filtering (.edu, Khan Academy, etc.)
echo 📚 Better coverage for modern/niche topics
echo.

echo 1. Stopping any existing processes...
taskkill /f /im python.exe >nul 2>&1
timeout /t 1 /nobreak >nul

echo 2. Installing enhanced search dependencies...
cd backend
call venv\Scripts\activate
pip install duckduckgo-search==4.1.1

echo 3. Starting backend with dual search...
start "Backend - Dual Search" cmd /k "echo ✅ Backend with Wikipedia + DuckDuckGo search && echo 📡 Running on http://localhost:8000 && python -m uvicorn app.main_simple:app --reload --host 0.0.0.0 --port 8000"

echo 4. Starting frontend...
cd ..\frontend  
start "Frontend - Enhanced UI" cmd /k "echo ✅ Frontend with dual search UI && echo 🌊 Running on http://localhost:5173 && npm run dev"

echo.
echo 🚀 AI Concept Explainer DUAL SEARCH MODE is starting...
echo.
echo 💬 Enhanced Chat: http://localhost:5173
echo 📚 API Documentation: http://localhost:8000/docs
echo.
echo ===============================================
echo              DUAL SEARCH BENEFITS
echo ===============================================
echo.
echo 📈 Better Success Rate:
echo    - Wikipedia for established topics
echo    - DuckDuckGo for modern/niche concepts
echo    - Educational domain prioritization
echo.
echo 🎯 Smarter Source Selection:
echo    - Tries Wikipedia first (fastest, most reliable)
echo    - Falls back to DuckDuckGo educational search
echo    - Filters for .edu, Khan Academy, Coursera, etc.
echo.
echo 🔍 Enhanced Coverage:
echo    - Traditional topics: Wikipedia
echo    - Modern tech: Educational blogs, tutorials
echo    - Niche subjects: Specialized educational sites
echo.
echo ⚡ Performance Optimized:
echo    - Stops searching after first good source
echo    - Educational domain filtering
echo    - 5-second timeouts per search
echo.
echo Press any key to close this window...
pause >nul