@echo off
echo Restarting Backend with Search Fixes...
echo.

echo 1. Stopping any existing backend processes...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im uvicorn.exe >nul 2>&1

echo 2. Waiting for processes to close...
timeout /t 2 /nobreak >nul

echo 3. Installing new dependencies...
cd backend
call venv\Scripts\activate
pip install duckduckgo-search==4.1.1

echo 4. Backend restarting with enhanced search:
echo    - Wikipedia search with fallbacks
echo    - DuckDuckGo educational search
echo    - Educational domain filtering
echo    - Better keyword extraction
echo    - Detailed logging
echo.

python -m uvicorn app.main_simple:app --reload --host 0.0.0.0 --port 8000