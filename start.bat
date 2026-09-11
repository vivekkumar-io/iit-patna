@echo off

title Enterprise Knowledge Assistant

color 0A



REM ============================================================

REM  Enterprise Knowledge Assistant - Start Script

REM  Cleans old processes/cache, then launches the chat app.

REM

REM  First time? Run setup.bat before this file.

REM ============================================================



cd /d "%~dp0"



echo.

echo ========================================

echo   Enterprise Knowledge Assistant

echo ========================================

echo.



REM --- [1/3] Stop old Streamlit on port 8501 ---

echo [1/3] Stopping old Streamlit on port 8501...

set "FOUND=0"

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8501 ^| findstr LISTENING') do (

    echo   Stopping process PID %%a

    taskkill /F /PID %%a >nul 2>&1

    set "FOUND=1"

)

if "%FOUND%"=="0" (

    echo   No Streamlit process found on port 8501.

) else (

    echo   [OK] Port 8501 freed.

)

echo.



REM --- [2/3] Clear Python __pycache__ ---

echo [2/3] Clearing Python __pycache__ folders...

for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

echo   [OK] Cache folders cleared.

echo.



REM --- Check .env ---

if not exist ".env" (

    echo [WARNING] .env file not found!

    echo.

    echo Please do this first:

    echo   1. Copy .env.example to .env

    echo   2. Add your OpenAI API key inside .env

    echo   3. Run setup.bat

    echo.

    pause

    exit /b 1

)



REM --- Check Python ---

python --version >nul 2>&1

if errorlevel 1 (

    echo [ERROR] Python is not installed or not in PATH.

    pause

    exit /b 1

)



REM --- Check virtual environment ---

if not exist "venv\Scripts\activate.bat" (

    echo [WARNING] Virtual environment not found!

    echo.

    echo Please run setup.bat first to create venv and install packages.

    echo.

    pause

    exit /b 1

)



REM --- Activate virtual environment ---

echo Activating virtual environment...

call venv\Scripts\activate.bat

echo.



REM --- Check streamlit inside venv ---

python -c "import streamlit" >nul 2>&1

if errorlevel 1 (

    echo [WARNING] Packages not installed in venv.

    echo Please run setup.bat first.

    pause

    exit /b 1

)



REM --- Run ingestion if needed ---

if not exist "data\vector_store\chroma.sqlite3" (

    echo Documents not indexed yet. Running ingestion first...

    echo.

    python scripts\ingest.py

    if errorlevel 1 (

        echo.

        echo [ERROR] Ingestion failed. Check API key and documents folder.

        pause

        exit /b 1

    )

    echo.

)



REM --- [3/3] Start Streamlit ---

echo [3/3] Starting Streamlit app...

echo Open your browser at: http://localhost:8501

echo.

echo Press Ctrl+C in this window to stop the app.

echo.



streamlit run app\main.py



pause


