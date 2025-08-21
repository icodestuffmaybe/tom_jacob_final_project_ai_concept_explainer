@echo off
echo Starting AI Concept Explainer Frontend...
echo.

cd frontend

echo Installing dependencies...
npm install
if %errorlevel% neq 0 (
    echo Failed to install dependencies. Make sure Node.js is installed.
    pause
    exit /b 1
)

echo.
echo Starting development server...
echo Frontend will be available at: http://localhost:5173
echo.

npm run dev