@echo off
REM ============================================================================
REM AURORA - First Time Setup Script
REM Run this once before using RUN_APP.bat
REM ============================================================================

echo.
echo ========================================================================
echo AURORA - First Time Setup
echo ========================================================================
echo.

cd /d "%~dp0"

REM Validate production gates
echo [CHECK] Validating production gates...
python check_app_spec.py
if errorlevel 1 (
    echo [ERROR] Production gates validation failed!
    echo Please check app_spec.json
    pause
    exit /b 1
)

echo.
echo [SUCCESS] All production gates PASSED!
echo.

REM Backend setup
echo ========================================================================
echo BACKEND SETUP
echo ========================================================================
cd backend

REM Create virtual environment
echo [1/5] Creating Python virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
echo [2/5] Installing Python dependencies (this may take a few minutes)...
pip install -r requirements.txt

REM Create directories
echo [3/5] Creating necessary directories...
if not exist storage mkdir storage
if not exist models mkdir models
if not exist logs mkdir logs

REM Train model
echo [4/5] Training baseline ML model...
python -m src.adapters.ml.train_baseline

REM Test backend
echo [5/5] Testing backend imports...
python -c "from src.frameworks.fastapi_app import app; print('[OK] Backend imports successful')"

cd ..

echo.
echo [SUCCESS] Backend setup complete!
echo.

REM Frontend setup
echo ========================================================================
echo FRONTEND SETUP
echo ========================================================================
cd frontend

REM Install Node modules
echo [1/2] Installing Node.js dependencies (this may take a few minutes)...
call npm install

REM Build check
echo [2/2] Checking frontend build configuration...
if exist vite.config.ts (
    echo [OK] Vite configuration found
) else (
    echo [WARNING] Vite config not found
)

cd ..

echo.
echo [SUCCESS] Frontend setup complete!
echo.

REM Create .env file if not exists
if not exist .env (
    echo ========================================================================
    echo CREATING ENVIRONMENT FILE
    echo ========================================================================
    copy .env.example .env
    echo [OK] Created .env file - you can edit it to customize settings
    echo.
)

REM Summary
echo.
echo ========================================================================
echo SETUP COMPLETE!
echo ========================================================================
echo.
echo Next steps:
echo   1. Review .env file for any custom configuration
echo   2. Run RUN_APP.bat to start the application
echo.
echo File structure:
dir /s /b backend\src\domain\*.py | find /c ".py"
echo   Python domain files created
dir /s /b backend\src\*.py | find /c ".py"
echo   Total Python files created
dir /s /b frontend\src\*.tsx | find /c ".tsx"
echo   TypeScript files created
echo.
echo Documentation:
echo   - README.md           : Full documentation
echo   - QUICK_START.md      : Quick start guide
echo   - PROJECT_SUMMARY.md  : Complete implementation details
echo.
echo ========================================================================
echo Ready to run! Execute: RUN_APP.bat
echo ========================================================================
echo.
pause
