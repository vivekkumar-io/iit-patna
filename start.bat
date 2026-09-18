@echo off
title Enterprise Knowledge Assistant
color 0A

REM ============================================================
REM  Enterprise Knowledge Assistant - Start Script
REM  Fast daily startup: NO re-indexing (done once in setup.bat)
REM  First time? Run setup.bat before this file.
REM ============================================================

cd /d "%~dp0"
cls

if not exist ".env" (
    echo [ERROR] .env file not found! Run setup.bat first.
    pause
    exit /b 1
)

if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found! Run setup.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
set PYTHONIOENCODING=utf-8

echo.
echo ========================================
echo   Enterprise Knowledge Assistant
echo ========================================
echo.

python scripts\cleanup_start.py --kill-port --clear-cache
if errorlevel 1 (
    echo [ERROR] Startup cleanup failed.
    pause
    exit /b 1
)

python scripts\startup_progress.py 45 "[3/5] Checking document indexes..."
python scripts\check_index.py >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Document indexes not found.
    echo   Run setup.bat once for first time, or reindex.bat after adding documents.
    pause
    exit /b 1
)
python scripts\startup_progress.py 60 "[3/4] Indexes found - skipping ingestion"
python scripts\startup_progress.py 100 "[4/4] Ready to launch Streamlit"
echo.
echo Starting Streamlit server...
echo Models load inside the app on first page open.
echo Browser will open automatically when the server is ready.
echo Application URL: http://localhost:8501
echo Press Ctrl+C to stop the app.
echo.

streamlit run app\main.py

pause
