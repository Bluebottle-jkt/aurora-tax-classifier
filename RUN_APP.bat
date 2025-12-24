@echo off
REM ============================================================================
REM AURORA Tax Classifier - Complete Local Run Script
REM ============================================================================

echo.
echo ========================================================================
echo AURORA - Indonesian Tax Object Classifier
echo ========================================================================
echo.

cd /d "%~dp0"

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.11+
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found! Please install Node.js 18+
    pause
    exit /b 1
)

echo [STEP 1/6] Setting up backend...
cd backend

REM Create virtual environment if not exists
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -q -r requirements.txt

REM Train model if not exists
if not exist models\baseline_model.pkl (
    echo Training baseline ML model...
    python -m src.adapters.ml.train_baseline
) else (
    echo Model already trained, skipping...
)

REM Create necessary directories
if not exist storage mkdir storage
if not exist logs mkdir logs

echo.
echo [STEP 2/6] Backend setup complete!
echo.

cd ..

REM Setup frontend
echo [STEP 3/6] Setting up frontend...
cd frontend

if not exist node_modules (
    echo Installing Node.js dependencies...
    call npm install
) else (
    echo Node modules already installed, skipping...
)

cd ..

echo.
echo [STEP 4/6] Frontend setup complete!
echo.

REM Validate production gates
echo [STEP 5/6] Validating production gates...
python check_app_spec.py
if errorlevel 1 (
    echo [WARNING] Some production gates failed!
    echo Continuing anyway...
)

echo.
echo [STEP 6/6] Starting services...
echo.
echo ========================================================================
echo Services will start in separate windows:
echo.
echo   Backend API:  http://localhost:8000
echo   Frontend:     http://localhost:3000
echo   API Docs:     http://localhost:8000/docs
echo.
echo Press Ctrl+C in each window to stop services
echo ========================================================================
echo.
pause

REM Start backend in new window
start "AURORA Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\activate.bat && python -m uvicorn src.frameworks.fastapi_app:app --reload --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in new window
start "AURORA Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================================================
echo AURORA is starting!
echo.
echo Wait a few seconds, then open: http://localhost:3000
echo.
echo To stop: Close the backend and frontend windows
echo ========================================================================
echo.
pause
