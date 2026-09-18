@echo off
title Reindex Documents - Enterprise Knowledge Assistant
color 0E
cd /d "%~dp0"

echo.
echo ========================================
echo   Rebuild Document Indexes
echo ========================================
echo.
echo Use this after adding or changing files in data\documents\
echo.

if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Run setup.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

python scripts\ingest.py
if errorlevel 1 (
    echo.
    echo [ERROR] Reindex failed.
    pause
    exit /b 1
)

echo.
echo [OK] Reindex complete.
pause
