@echo off
echo Starting MoodMate Backend...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    pause
    exit /b 1
)
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
pip install -r requirements.txt --quiet
python run.py
pause