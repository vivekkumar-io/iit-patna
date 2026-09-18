@echo off
title Setup - Enterprise Knowledge Assistant
color 0B

REM ============================================================
REM  FIRST TIME SETUP SCRIPT
REM  Run this ONCE before using the app.
REM
REM  What it does:
REM  1. Creates virtual environment and installs packages
REM  2. Builds document indexes (chunking + embeddings) ONE TIME
REM ============================================================

cd /d "%~dp0"

echo.
echo ========================================
echo   First Time Setup
echo   Enterprise Knowledge Assistant
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo [OK] Python found:
python --version
echo.

if not exist ".env" (
    echo [WARNING] .env file not found.
    copy .env.example .env
    echo.
    echo Please open .env and add your OPENAI_API_KEY, then run setup.bat again.
    pause
    exit /b 1
)

echo [OK] .env file found.
echo.

if exist "venv\Scripts\activate.bat" (
    echo [OK] Virtual environment already exists in venv\
) else (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
)
echo.

call venv\Scripts\activate.bat
set PYTHONIOENCODING=utf-8
echo [OK] Virtual environment activated.
echo.

echo Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Installing packages from requirements.txt...
echo This may take 10-20 minutes. Please wait...
echo.

pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Installation failed.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Package install complete
echo ========================================
echo.

python scripts\check_api_key.py >nul 2>&1
if errorlevel 1 (
    echo [ERROR] OPENAI_API_KEY is missing in .env
    echo Add your API key, then run setup.bat again.
    pause
    exit /b 1
)

python scripts\check_index.py >nul 2>&1
if errorlevel 1 (
    echo Building document indexes - one-time chunking and embeddings...
    echo This may take a few minutes.
    echo.
    python scripts\ingest.py
    if errorlevel 1 (
        echo.
        echo [ERROR] Indexing failed. Check API key and data\documents\ folder.
        pause
        exit /b 1
    )
) else (
    echo [OK] Document indexes already exist. Skipping ingestion.
)

echo.
echo ========================================
echo   SETUP COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Next step: double-click start.bat
echo.
echo If you add new documents later, run reindex.bat
echo.
pause
