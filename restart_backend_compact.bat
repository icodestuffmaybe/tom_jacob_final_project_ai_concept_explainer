@echo off
taskkill /f /im python.exe >nul 2>&1
timeout /t 1 /nobreak >nul
cd backend && call venv\Scripts\activate && python -m uvicorn app.main_simple:app --reload --host 0.0.0.0 --port 8000