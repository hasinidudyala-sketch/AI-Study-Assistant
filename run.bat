@echo off
title AI Study Assistant
cd /d "%~dp0"

echo ==========================================
echo       AI STUDY ASSISTANT - STARTUP
echo ==========================================

if not exist ".venv\Scripts\python.exe" (
    echo Creating Python virtual environment...
    py -m venv .venv
    if errorlevel 1 (
        python -m venv .venv
    )
)

echo Installing required packages...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt

if not exist ".env" (
    copy ".env.example" ".env" >nul
    echo.
    echo IMPORTANT: A .env file was created.
    echo Open .env and paste your Gemini API key.
    echo Save it, then double-click run.bat again.
    pause
    exit /b
)

echo.
echo Starting AI Study Assistant...
".venv\Scripts\python.exe" -m streamlit run app.py
pause
