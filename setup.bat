@echo off
title Setup - Enterprise Knowledge Assistant
color 0B

REM ============================================================
REM  FIRST TIME SETUP SCRIPT
REM  Run this ONCE before using the app.
REM
REM  What it does:
REM  1. Creates a virtual environment (venv folder)
REM  2. Installs all packages inside venv (isolated from system Python)
REM  3. Keeps your project dependencies clean and separate
REM ============================================================

cd /d "%~dp0"

echo.
echo ========================================
echo   First Time Setup
echo   Enterprise Knowledge Assistant
echo ========================================
echo.

REM --- Check Python ---
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Install Python 3.10+ from https://www.python.org
    echo During install, check "Add Python to PATH".
    pause
    exit /b 1
)

echo [OK] Python found:
python --version
echo.

REM --- Check .env file ---
if not exist ".env" (
    echo [WARNING] .env file not found.
    echo Creating .env from .env.example ...
    copy .env.example .env
    echo.
    echo Please open .env and add your OPENAI_API_KEY, then run setup again.
    pause
    exit /b 1
)

echo [OK] .env file found.
echo.

REM --- Create virtual environment ---
if exist "venv\Scripts\activate.bat" (
    echo [OK] Virtual environment already exists in venv\
) else (
    echo Creating virtual environment in venv\ folder...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
)
echo.

REM --- Activate virtual environment ---
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Could not activate virtual environment.
    pause
    exit /b 1
)
echo [OK] Virtual environment activated.
echo.

REM --- Upgrade pip ---
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM --- Fix broken openai package if needed ---
echo Checking for broken package installations...
pip uninstall openai -y >nul 2>&1
echo.

REM --- Install requirements ---
echo Installing packages from requirements.txt...
echo This may take 10-20 minutes. Please wait...
echo Do NOT close this window.
echo.

pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] Installation failed.
    echo Try closing all Python/terminal windows and run setup.bat again.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SETUP COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Next steps:
echo   1. Double-click start.bat to run the app
echo   2. Open browser: http://localhost:8501
echo.
pause
