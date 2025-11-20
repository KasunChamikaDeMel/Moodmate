@echo off
title MoodMate Launcher 🚀
echo Starting MoodMate AI Server and App...

:: 1. Python Server එක වෙනම Window එකක පටන් ගන්නවා
start "MoodMate Brain 🧠" cmd /k "python app.py"

:: පොඩි විවේකයක් (Server එක පටන් ගන්නකම්)
timeout /t 3

:: 2. Electron App එක පටන් ගන්නවා
echo Starting Interface...
npm start