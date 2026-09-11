@echo off
title Push to GitHub - Enterprise Knowledge Assistant
cd /d "%~dp0"

echo.
echo ========================================
echo   Push to GitHub: vivekkumar-io/iit-patna
echo ========================================
echo.

where git >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed.
    echo.
    echo Install Git first:
    echo   1. Download: https://git-scm.com/download/win
    echo   2. Install with default options
    echo   3. Close and reopen this window, then run this file again
    echo.
    echo OR use GitHub Desktop: https://desktop.github.com/
    pause
    exit /b 1
)

if not exist ".git" (
    echo Initializing git repository...
    git init
)

echo.
echo Checking files to commit...
git add .
git status

echo.
echo ========================================
echo VERIFY: The list above must NOT include:
echo   - .env
echo   - venv/
echo   - logs/
echo   - any .mp4 file
echo ========================================
echo.
set /p CONFIRM="Continue with commit and push? (Y/N): "
if /I not "%CONFIRM%"=="Y" (
    echo Cancelled.
    pause
    exit /b 0
)

git commit -m "Final submission: Enterprise Knowledge Assistant with Advanced RAG (Project 2)" 2>nul
if errorlevel 1 (
    echo Note: Nothing new to commit, or commit already exists.
)

git branch -M main

git remote remove origin >nul 2>&1
git remote add origin https://github.com/vivekkumar-io/iit-patna.git

echo.
echo Pushing to GitHub...
echo You may be asked to sign in to GitHub.
echo.
git push -u origin main

if errorlevel 1 (
    echo.
    echo [ERROR] Push failed. Common fixes:
    echo   - Sign in: git config credential.helper manager
    echo   - Or use GitHub Desktop to publish the folder
    echo   - Or create a Personal Access Token for HTTPS push
    pause
    exit /b 1
)

echo.
echo [OK] Code pushed to https://github.com/vivekkumar-io/iit-patna
echo.
echo Remember: Demo video is NOT on GitHub. Share Google Drive link separately.
pause
