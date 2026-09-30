@echo off

echo ===================================================
echo           SpectraNote Environment Setup
echo ===================================================

REM Check Python availability
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not added to system PATH!
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

set FORCE_INSTALL=0
if "%~1"=="--force" set FORCE_INSTALL=1
if "%~1"=="-f" set FORCE_INSTALL=1

REM Step 1: Create Virtual Environment if missing
if exist .venv\Scripts\activate.bat goto VENV_EXISTS

echo [INFO] Virtual environment (.venv) not found. Creating...
python -m venv .venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment!
    pause
    exit /b 1
)
echo [OK] Virtual environment created successfully.
set FORCE_INSTALL=1

:VENV_EXISTS
echo [OK] Virtual environment (.venv) active.
call .venv\Scripts\activate.bat

REM Step 3: Install Dependencies if force or newly created
if "%FORCE_INSTALL%"=="0" goto DONE

echo [INFO] Installing / updating required libraries...
python -m pip install --upgrade pip
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    if exist requirements (
        pip install -r requirements
    )
)

if errorlevel 1 (
    echo [WARNING] Dependency installation finished with errors.
) else (
    echo [OK] All dependencies installed successfully.
)

:DONE
echo [OK] SpectraNote environment ready.
echo ===================================================
