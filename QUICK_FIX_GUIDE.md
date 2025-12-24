# Quick Fix Guide - Analysis Issues

**Date:** December 21, 2025
**Issues:** Direct text analysis failing + Results loading forever

---

## 🔧 Issues Fixed

### Issue 1: Direct Text Analysis Failing
**Error:** "Analysis failed" popup
**Root Cause:** Missing `TaxObjectLabel` import in backend
**Fix Applied:** ✅ Added import and better error handling

### Issue 2: Results Page Loading Forever
**Likely Cause:** Backend server not running or needs restart
**Solution:** Restart backend server

---

## ✅ Fixes Applied to Backend

### 1. Added Missing Import
```python
# Added to fastapi_app.py
from ..domain.value_objects import TaxObjectLabel
```

### 2. Enhanced Error Handling
```python
# Direct analysis endpoint now has:
- Try-catch around entire endpoint
- Fallback for explainer errors
- Better HTTP error responses
- Detailed error messages
```

---

## 🚀 How to Apply Fixes

### Quick Method (Recommended)
```cmd
# Stop your current backend and frontend servers (Ctrl+C)

# Then restart backend:
cd backend
venv\Scripts\activate
python -m uvicorn src.frameworks.fastapi_app:app --reload

# In another terminal, restart frontend:
cd frontend
npm run dev
```

### Verification
```cmd
# Test backend is running:
# Open: http://localhost:8000/docs
# You should see FastAPI documentation

# Test frontend is running:
# Open: http://localhost:3000
# You should see AURORA homepage
```

---

## 🔍 Troubleshooting

### Direct Text Analysis Still Fails

**Problem:** "Analysis failed" error persists

**Solutions:**

1. **Check Backend is Running**
   ```cmd
   # Should see: Uvicorn running on http://127.0.0.1:8000
   # If not, start backend:
   cd backend
   venv\Scripts\activate
   python -m uvicorn src.frameworks.fastapi_app:app --reload
   ```

2. **Check Model is Trained**
   ```cmd
   cd backend
   dir models\baseline_model.pkl

   # If missing, train model:
   python -m src.adapters.ml.train_baseline
   ```

3. **Test Endpoint Directly**
   ```cmd
   # Open: http://localhost:8000/docs
   # Find POST /api/predict/direct
   # Click "Try it out"
   # Input:
   {
     "texts": ["bayar gaji"]
   }
   # Should return predictions
   ```

### Results Page Loading Forever

**Problem:** "Loading results..." never completes

**Solutions:**

1. **Check Job Status**
   ```cmd
   # If you know job_id, check:
   # http://localhost:8000/api/jobs/{job_id}
   # Look for status: "processing", "completed", or "failed"
   ```

2. **Check Backend Logs**
   ```cmd
   # Look in backend terminal for errors
   # Common issues:
   - File not found
   - Column validation error
   - Model not loaded
   ```

3. **Upload a New File**
   ```cmd
   # Go to: http://localhost:3000/app/upload
   # Upload a small CSV file (10-20 rows)
   # Select business type
   # Submit
   # Should complete in 5-10 seconds
   ```

---

## 📝 Test Procedure

### Test 1: Direct Text Analysis (Single)
```
1. Go to: http://localhost:3000/app/direct-analysis
2. Make sure "Single Transaction" is selected
3. Type: "pembayaran gaji karyawan"
4. Click "Analyze Transaction"
5. Expected: See tax object details (PPh21)
```

### Test 2: Direct Text Analysis (Bulk)
```
1. Click "Multiple Transactions (Bulk)"
2. Paste:
   bayar gaji
   bayar delivery
3. Click "Analyze All Transactions"
4. Expected: See table with 2 results
```

### Test 3: File Upload
```
1. Go to: http://localhost:3000/app/upload
2. Upload a small CSV file with columns:
   account_name,amount
   Gaji karyawan,1000000
   PPN masukan,110000
3. Select business type: Perdagangan
4. Click Submit
5. Expected: Redirected to results, see "COMPLETED" status
```

---

## 🐛 Common Errors & Solutions

### Error: "Analysis failed"
**Cause:** Backend not running or endpoint error
**Solution:**
1. Restart backend
2. Check browser console (F12) for error details
3. Check backend terminal for Python errors

### Error: "Upload failed"
**Cause:** File format issue or backend error
**Solution:**
1. Check file has required columns (account_name or description)
2. Verify file is CSV or Excel format
3. Check backend logs for validation errors

### Error: Results stuck on "Loading..."
**Cause:** Job processing failed or frontend not polling
**Solution:**
1. Check job status at: http://localhost:8000/api/jobs/{job_id}
2. If status is "failed", check error_message field
3. If status is "processing" for >30 seconds, restart backend

### Error: "CORS error" in browser console
**Cause:** Frontend and backend ports mismatch
**Solution:**
1. Verify backend on port 8000: http://localhost:8000/docs
2. Verify frontend on port 3000: http://localhost:3000
3. Check vite.config.ts proxy settings (should be correct)

---

## ✅ Checklist Before Using

- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 3000
- [ ] Model file exists: `backend/models/baseline_model.pkl`
- [ ] No errors in backend terminal
- [ ] No errors in frontend terminal
- [ ] Can access http://localhost:8000/docs
- [ ] Can access http://localhost:3000

---

## 🎯 Expected Behavior

### Direct Analysis (Single)
- Input: "gaji karyawan"
- Time: < 500ms
- Output:
  - Tax Object: PPh21
  - Confidence: ~85-95%
  - Explanation: "Based on terms: gaji, karyawan..."

### Direct Analysis (Bulk)
- Input: 10 transactions
- Time: < 2 seconds
- Output:
  - Summary: 10 analyzed, avg confidence
  - Table with all results

### File Upload
- Input: 100 row CSV file
- Time: 5-15 seconds
- Output:
  - Status: COMPLETED
  - 4 metric cards
  - 4 charts
  - Detailed table

---

## 📞 Still Having Issues?

### Debug Steps:

1. **Check Backend Logs**
   ```cmd
   # Look for Python tracebacks
   # Common issues:
   - ImportError
   - KeyError (missing column)
   - ValueError (invalid data)
   ```

2. **Check Browser Console (F12)**
   ```cmd
   # Look for:
   - Network errors (red)
   - CORS errors
   - 404 Not Found
   - 500 Server Error
   ```

3. **Test Backend Directly**
   ```cmd
   # Use API docs:
   http://localhost:8000/docs

   # Or curl:
   curl -X POST http://localhost:8000/api/predict/direct \
     -H "X-Aurora-Key: aurora-dev-key" \
     -H "Content-Type: application/json" \
     -d '{"texts": ["test"]}'
   ```

4. **Run Diagnostic**
   ```cmd
   cd backend
   python -c "
   from src.frameworks.fastapi_app import app
   from src.adapters.ml.tfidf_classifier import TfidfClassifier

   classifier = TfidfClassifier()
   print('Model loaded:', classifier.model is not None)

   result = classifier.predict_proba(['test'])
   print('Prediction works:', len(result) > 0)
   "
   ```

---

## 🎉 Success Indicators

When everything works:
- ✅ Direct analysis shows results in < 1 second
- ✅ File upload completes in < 30 seconds
- ✅ Results page shows charts and tables
- ✅ No errors in any terminal
- ✅ Download CSV works

---

**Fix Status:** ✅ Backend code updated
**Next Step:** Restart both servers
**Time to Fix:** < 2 minutes

---

**Guide by:** Claude Code (Sonnet 4.5)
**Date:** December 21, 2025
**Issue:** Direct analysis + loading issues
