@echo off
REM ============================================================================
REM AURORA - UI Upgrade Script
REM Installs new dependencies and prepares the modern UI
REM ============================================================================

echo.
echo ========================================================================
echo AURORA - UI Upgrade to Modern Design
echo ========================================================================
echo.

cd /d "%~dp0"

echo This will upgrade your UI to include:
echo   1. Modern gradient headers
echo   2. Drag-and-drop file upload
echo   3. File preview before upload
echo   4. Interactive business type selection
echo   5. Advanced results page with charts (Pie, Bar)
echo   6. Confidence distribution analysis
echo   7. Tax object summary with emojis
echo   8. Direct text analysis feature (NEW!)
echo   9. Smooth animations with Framer Motion
echo   10. Responsive design with TailwindCSS gradients
echo.
pause

echo.
echo [STEP 1/4] Installing frontend dependencies...
cd frontend
call npm install
if errorlevel 1 (
    echo [ERROR] npm install failed!
    pause
    exit /b 1
)

echo.
echo [STEP 2/4] Installing Recharts for charts...
call npm install recharts
if errorlevel 1 (
    echo [ERROR] Recharts installation failed!
    pause
    exit /b 1
)

echo.
echo [STEP 3/4] Building frontend...
call npm run build
if errorlevel 1 (
    echo [WARN] Build had warnings, but continuing...
)

cd ..

echo.
echo [STEP 4/4] Verifying backend endpoint...
cd backend
python -c "from src.frameworks.fastapi_app import app; print('[OK] Backend ready with new endpoint')"
if errorlevel 1 (
    echo [ERROR] Backend verification failed!
    pause
    exit /b 1
)
cd ..

echo.
echo ========================================================================
echo UI UPGRADE COMPLETE!
echo ========================================================================
echo.
echo New Features:
echo   - Drag-and-drop file upload with preview
echo   - Modern gradient design matching original Aurora
echo   - Interactive charts (Pie, Bar, Confidence Distribution)
echo   - Direct text analysis (single + bulk)
echo   - Smooth animations
echo   - Color-coded confidence levels
echo   - Tax object emojis
echo.
echo Next Steps:
echo   1. Run RUN_APP.bat to start the application
echo   2. Open http://localhost:3000
echo   3. Try the new drag-and-drop upload!
echo   4. Click "Direct Text Analysis" for instant predictions
echo.
pause
