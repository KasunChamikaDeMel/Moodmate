@echo off
setlocal enabledelayedexpansion

echo =====================
echo   Starting MoodMate
echo =====================
echo.

REM
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM
echo Launching Backend...
start "MoodMate Backend" cmd /k "cd /d C:\Users\User\Desktop\Moodmate\backend && call venv\Scripts\activate.bat && pip install -r requirements.txt --quiet && python run.py"

REM
timeout /t 20 /nobreak

REM
echo Launching Frontend...
start "MoodMate Frontend" cmd /k "cd /d C:\Users\User\Desktop\Moodmate\frontend && call venv\Scripts\activate.bat && echo Checking backend connection... && curl -s http://localhost:5000/api/health >nul 2>&1 || echo WARNING: Backend may not be running && pip install -r requirements.txt --quiet && echo Starting PyQt6 application... && python main.py"

echo.
echo Backend: MoodMate Backend window loaded
echo Frontend: MoodMate Frontend window loaded
echo.
pause