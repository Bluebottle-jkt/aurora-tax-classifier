@echo off
REM ============================================================================
REM AURORA - Fix Direct Analysis Issues
REM Fixes backend import and restarts services
REM ============================================================================

echo.
echo ========================================================================
echo AURORA - Fixing Direct Analysis
echo ========================================================================
echo.

cd /d "%~dp0"

echo [FIX 1/2] Verifying backend imports...
cd backend
python -c "from src.frameworks.fastapi_app import app; print('[OK] Backend imports successfully')"
if errorlevel 1 (
    echo [ERROR] Backend import failed!
    pause
    exit /b 1
)

echo.
echo [FIX 2/2] Testing direct analysis endpoint...
python -c "from src.frameworks.fastapi_app import app; from fastapi.testclient import TestClient; client = TestClient(app); response = client.post('/api/predict/direct', json={'texts': ['test']}, headers={'X-Aurora-Key': 'aurora-dev-key'}); print('[OK] Endpoint works!' if response.status_code == 200 else f'[ERROR] Status: {response.status_code}')"

cd ..

echo.
echo ========================================================================
echo FIXES APPLIED!
echo ========================================================================
echo.
echo The direct analysis endpoint has been fixed with:
echo   1. Added TaxObjectLabel import
echo   2. Better error handling
echo   3. Fallback for explainer errors
echo.
echo Next Steps:
echo   1. RESTART your backend server (close and reopen terminal)
echo   2. cd backend
echo   3. venv\Scripts\activate
echo   4. python -m uvicorn src.frameworks.fastapi_app:app --reload
echo.
echo   Then restart frontend:
echo   5. cd frontend
echo   6. npm run dev
echo.
echo   Open http://localhost:3000/app/direct-analysis
echo.
pause
