@echo off
echo Starting MoodMate Backend...
echo.
echo This will:
echo 1. Install required packages
echo 2. Start the Flask backend
echo 3. Open http://localhost:5000 in your browser
echo.
echo Press any key to continue...
pause >nul

echo.
echo Installing requirements...
pip install -r requirements.txt

echo.
echo Starting backend...
python app.py

echo.
echo Backend stopped. Press any key to exit...
pause >nul
