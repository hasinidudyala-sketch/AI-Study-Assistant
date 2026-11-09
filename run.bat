@echo off
title AI Study Assistant - Module 06
cd /d "%~dp0"
echo ==========================================
echo       AI STUDY ASSISTANT - MODULE 06
echo ==========================================
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    py -m venv .venv
    if errorlevel 1 python -m venv .venv
)
echo Installing dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if not exist ".env" (
    copy ".env.example" ".env" >nul
    echo.
    echo A .env file has been created.
    echo Open it, add your Gemini API key, save, and run run.bat again.
    notepad .env
    pause
    exit /b
)
echo Starting AI Study Assistant...
".venv\Scripts\python.exe" -m streamlit run app.py
pause
