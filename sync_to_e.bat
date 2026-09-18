@echo off
title Sync to E:\_GenAIProject
cd /d "%~dp0"

set "SOURCE=D:\_GenAIProject\Enterprise_Knowledge_Assistant"
set "TARGET=E:\_GenAIProject\Enterprise_Knowledge_Assistant"

echo.
echo ========================================
echo   Syncing project to E:\_GenAIProject
echo ========================================
echo.
echo Source: %SOURCE%
echo Target: %TARGET%
echo.

if not exist "E:\_GenAIProject" (
    echo [ERROR] E:\_GenAIProject not found.
    pause
    exit /b 1
)

robocopy "%SOURCE%" "%TARGET%" /MIR /XD venv logs __pycache__ .git ^
    /XF .env *.mp4 ^
    /NFL /NDL /NJH /NJS /nc /ns /np

if %ERRORLEVEL% GEQ 8 (
    echo.
    echo [ERROR] Robocopy failed with code %ERRORLEVEL%
    pause
    exit /b 1
)

echo.
echo [OK] Sync complete. Mirror updated at:
echo      %TARGET%
echo.
echo Note: .env, venv, logs, and indexes were NOT copied.
echo.
pause
