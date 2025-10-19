@echo off
REM MoodMate Frontend Startup Script for Windows

echo ============================================================
echo   MoodMate Frontend Application
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Starting MoodMate Frontend...
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Check if backend is running
echo Checking backend connection...
curl -s http://localhost:5000/api/health >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Backend server is not running!
    echo Please start the backend first:
    echo   1. Open another terminal
    echo   2. Navigate to backend folder
    echo   3. Run: python run.py
    echo.
    echo Press any key to continue anyway, or Ctrl+C to cancel...
    pause >nul
)

REM Install dependencies if needed
echo Checking dependencies...
pip install -r requirements.txt --quiet

echo.
echo Starting PyQt6 application...
echo.

REM Start the frontend app
python main.py

REM Keep window open if error occurs
if errorlevel 1 (
    echo.
    echo ERROR: Application crashed!
    pause
)