@echo off
title MoodMate Launcher 🚀
echo Starting MoodMate AI Server and App...

:: 1. Python Server 
start "MoodMate Brain 🧠" cmd /k "python app.py"

:: getting ready time
timeout /t 3

:: 2. Electron App 
echo Starting Interface...
npm start