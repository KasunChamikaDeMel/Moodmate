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
REM Start Moodmate Pet (Electron/Python app) in parallel
echo Launching Moodmate Pet...
pushd ..\moodmate-pet
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
start "Moodmate Pet" cmd /k "python app.py"
popd

pip install -r requirements.txt --quiet
python run.py
pause