# AURORA - Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: JSON Decode Error in seed_corpus.jsonl

**Error Message:**
```
json.decoder.JSONDecodeError: Extra data: line 1 column 44 (char 43)
```

**Cause:** The JSONL file has all JSON on one line instead of one JSON per line.

**Solution:**
```cmd
FIX_ALL_ISSUES.bat
```

Or manually:
```cmd
cd backend
python -c "import json; seed_data = [...]; f = open('data/seed_corpus.jsonl', 'w'); [f.write(json.dumps(item) + '\n') for item in seed_data]; f.close()"
```

---

### Issue 2: Missing tsconfig.node.json

**Error Message:**
```
parsing tsconfig.node.json failed: Error: ENOENT: no such file or directory
```

**Cause:** Frontend TypeScript configuration file is missing.

**Solution:**
```cmd
FIX_ALL_ISSUES.bat
```

Or manually create `frontend/tsconfig.node.json`:
```json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
```

---

### Issue 3: Model Not Found

**Error Message:**
```
FileNotFoundError: models/baseline_model.pkl
```

**Cause:** ML model hasn't been trained yet.

**Solution:**
```cmd
cd backend
python -m src.adapters.ml.train_baseline
```

**Expected Output:**
```
[OK] Model trained and saved to models\baseline_model.pkl
  Labels: ['Fiscal_Correction_Negative' 'Fiscal_Correction_Positive' ...]
  Training samples: 38
```

---

### Issue 4: Port Already in Use

**Error Message:**
```
OSError: [WinError 10048] Only one usage of each socket address
```

**Cause:** Port 8000 or 3000 is already in use.

**Solution:**

Option 1 - Stop the other process:
```cmd
# Find process using port 8000
netstat -ano | findstr :8000
# Kill process (replace PID with actual process ID)
taskkill /F /PID <PID>
```

Option 2 - Change port in `.env`:
```
BACKEND_PORT=8001
FRONTEND_PORT=3001
```

---

### Issue 5: Module Not Found Errors

**Error Message:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Cause:** Python dependencies not installed or wrong Python environment.

**Solution:**
```cmd
cd backend
# Make sure virtual environment is activated
venv\Scripts\activate.bat
# Reinstall dependencies
pip install -r requirements.txt
```

---

### Issue 6: Frontend Build Errors

**Error Message:**
```
npm ERR! missing script: dev
```

**Cause:** Node modules not installed properly.

**Solution:**
```cmd
cd frontend
# Remove node_modules and reinstall
rmdir /s /q node_modules
npm install
```

---

### Issue 7: CORS Error in Browser

**Error Message (in browser console):**
```
Access to fetch at 'http://localhost:8000' has been blocked by CORS policy
```

**Cause:** Frontend URL not in CORS whitelist.

**Solution:**

Edit `.env`:
```
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

Then restart backend.

---

### Issue 8: Database Locked (SQLite)

**Error Message:**
```
sqlite3.OperationalError: database is locked
```

**Cause:** Multiple workers accessing SQLite simultaneously.

**Solution:**

Option 1 - Use single worker:
```cmd
uvicorn src.frameworks.fastapi_app:app --reload --workers 1
```

Option 2 - Switch to PostgreSQL (production):
```
DATABASE_URL=postgresql://user:pass@localhost:5432/aurora
```

---

### Issue 9: Virtual Environment Not Activating

**Error Message:**
```
'venv' is not recognized as an internal or external command
```

**Cause:** Virtual environment not created or wrong path.

**Solution:**
```cmd
cd backend
# Create fresh virtual environment
python -m venv venv
# Activate
venv\Scripts\activate.bat
# Verify
where python
```

---

### Issue 10: API Key Authentication Failed

**Error Message (in API response):**
```
{"detail":"Invalid API key"}
```

**Cause:** Missing or incorrect API key in request.

**Solution:**

Check `.env` file:
```
API_KEY=aurora-dev-key
```

Use in requests:
```bash
curl -H "X-Aurora-Key: aurora-dev-key" http://localhost:8000/api/jobs
```

---

## Complete Reset Procedure

If nothing works, perform a complete reset:

```cmd
# 1. Stop all services (close all terminal windows)

# 2. Clean backend
cd backend
rmdir /s /q venv
rmdir /s /q models
rmdir /s /q storage
rmdir /s /q __pycache__

# 3. Clean frontend
cd ..\frontend
rmdir /s /q node_modules
rmdir /s /q dist

# 4. Fix all issues
cd ..
FIX_ALL_ISSUES.bat

# 5. Run setup again
SETUP_FIRST_TIME.bat

# 6. Start app
RUN_APP.bat
```

---

## Quick Diagnostic Commands

### Check Python Version
```cmd
python --version
```
Expected: Python 3.11 or higher

### Check Node.js Version
```cmd
node --version
```
Expected: v18.0.0 or higher

### Check Virtual Environment
```cmd
cd backend
venv\Scripts\activate.bat
where python
```
Should show path inside `venv` folder

### Check Installed Packages
```cmd
cd backend
venv\Scripts\activate.bat
pip list | findstr fastapi
```
Should show: `fastapi X.X.X`

### Check Model File
```cmd
dir /s backend\models\baseline_model.pkl
```
Should exist and be > 1KB

### Check Seed Corpus Format
```cmd
python -c "import json; [json.loads(line) for line in open('backend/data/seed_corpus.jsonl')]"
```
Should complete without error

### Test Backend Import
```cmd
cd backend
venv\Scripts\activate.bat
python -c "from src.frameworks.fastapi_app import app; print('[OK] Backend imports work')"
```

### Test Frontend Dependencies
```cmd
cd frontend
npm list react
```
Should show react installed

---

## Validation Script

Run this to verify everything is set up correctly:

```cmd
@echo off
echo Validating AURORA setup...
echo.

echo [CHECK] Python version:
python --version

echo [CHECK] Node.js version:
node --version

echo [CHECK] Backend virtual environment:
if exist backend\venv (echo [OK] venv exists) else (echo [ERROR] venv missing)

echo [CHECK] Model file:
if exist backend\models\baseline_model.pkl (echo [OK] model exists) else (echo [ERROR] model missing)

echo [CHECK] Seed corpus:
if exist backend\data\seed_corpus.jsonl (echo [OK] corpus exists) else (echo [ERROR] corpus missing)

echo [CHECK] Frontend config:
if exist frontend\tsconfig.node.json (echo [OK] tsconfig exists) else (echo [ERROR] tsconfig missing)

echo [CHECK] Node modules:
if exist frontend\node_modules (echo [OK] node_modules exists) else (echo [ERROR] node_modules missing)

echo [CHECK] Production gates:
python check_app_spec.py

echo.
echo Validation complete!
pause
```

---

## Getting Help

If issues persist:

1. **Check this guide** for your specific error
2. **Run FIX_ALL_ISSUES.bat** to auto-fix common issues
3. **Run complete reset** procedure above
4. **Check logs** in terminal windows for detailed error messages
5. **Verify file sizes** - all Python files should be > 30 lines (no stubs)

---

## Success Criteria

After setup, you should have:

- ✅ Backend starts without errors on http://localhost:8000
- ✅ Frontend starts without errors on http://localhost:3000
- ✅ Can upload a CSV file
- ✅ Receive predictions with confidence scores
- ✅ Can download results as CSV
- ✅ API docs accessible at http://localhost:8000/docs
- ✅ All 13 production gates pass

---

**Last Updated:** December 21, 2025
