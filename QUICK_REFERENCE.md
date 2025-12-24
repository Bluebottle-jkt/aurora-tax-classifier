# Quick Reference Guide - AURORA Tax Classifier

## 🚀 Quick Start

### Start the Application
```bash
cd d:\TaxObjectFinder\aurora-tax-classifier
docker compose up -d
```

### Stop the Application
```bash
docker compose down
```

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres
```

### Check Status
```bash
docker compose ps
```

---

## 🔗 Access Points

| Service | URL |
|---------|-----|
| **Web Application** | http://localhost:3000 |
| **Upload Page** | http://localhost:3000/app/upload |
| **Direct Analysis** | http://localhost:3000/app/direct-analysis |
| **Backend API** | http://localhost:8000 |
| **API Docs (Swagger)** | http://localhost:8000/docs |

---

## 🔑 Authentication

**API Key (Development):** `aurora-dev-key-change-in-production`

**Database Credentials:**
- Username: `aurora`
- Password: `aurora-dev-password`
- Database: `aurora`
- Port: `5432`

---

## 🛠️ Common Commands

### Rebuild Containers
```bash
# Rebuild all
docker compose up -d --build

# Rebuild specific service
docker compose up -d --build backend
docker compose up -d --build frontend
```

### Restart Services
```bash
# Restart all
docker compose restart

# Restart specific service
docker compose restart backend
```

### Access Container Shell
```bash
# Backend
docker compose exec backend /bin/bash

# Frontend
docker compose exec frontend /bin/sh

# Database
docker compose exec postgres psql -U aurora -d aurora
```

### View Container Logs
```bash
# Last 50 lines
docker compose logs backend --tail 50

# Follow logs in real-time
docker compose logs -f backend
```

---

## 🧪 Testing the API

### Test Direct Prediction
```bash
curl -X POST "http://localhost:8000/api/predict/direct" \
  -H "Content-Type: application/json" \
  -H "x-aurora-key: aurora-dev-key-change-in-production" \
  -d '{
    "texts": [
      "Gaji Karyawan",
      "Beban Sewa Gedung",
      "Bunga Bank"
    ]
  }'
```

### Test Health Check
```bash
curl http://localhost:8000/api/healthz
```

### Test Configuration
```bash
curl -H "x-aurora-key: aurora-dev-key-change-in-production" \
  http://localhost:8000/api/config
```

---

## 📊 Model Information

### Current Models
- **Fiscal Correction:** `backend/models/koreksi_fiskal_lr.joblib`
- **Tax Object:** `backend/models/objek_pph_lr.joblib`

### Supported Tax Objects (14 Labels)
1. PPh21 - Employee Income Tax
2. PPh22 - Import & Specific Transaction Tax
3. PPh23_Bunga - Interest Tax
4. PPh23_Dividen - Dividend Tax
5. PPh23_Hadiah - Award/Prize Tax
6. PPh23_Jasa - Service Tax
7. PPh23_Royalti - Royalty Tax
8. PPh23_Sewa - Rent Tax
9. PPh26 - Foreign Recipient Tax
10. PPN - Value Added Tax
11. PPh4_2_Final - Final Income Tax
12. Fiscal_Correction_Positive - Positive Fiscal Correction
13. Fiscal_Correction_Negative - Negative Fiscal Correction
14. Non_Object - Non-Taxable

### Test the Classifier (Python)
```bash
cd backend
python -c "
from src.adapters.ml.two_stage_classifier import TwoStageClassifier

classifier = TwoStageClassifier()
print(f'Version: {classifier.get_version()}')

results = classifier.predict_proba(['Gaji Karyawan', 'Sewa Gedung'])
for text, probs in zip(['Gaji Karyawan', 'Sewa Gedung'], results):
    top = max(probs.items(), key=lambda x: x[1])
    print(f'{text}: {top[0]} ({top[1]:.1%})')
"
```

---

## 🐛 Troubleshooting

### Issue: Containers won't start
```bash
# Check for port conflicts
netstat -ano | findstr "3000\|8000\|5432"

# Remove old containers and volumes
docker compose down -v
docker compose up -d
```

### Issue: Frontend shows "Upload failed"
**Check:** API key mismatch
```bash
# Check backend logs
docker compose logs backend --tail 20

# Verify frontend has correct API key
grep -r "X-Aurora-Key" frontend/src/pages/
```

### Issue: Backend errors
```bash
# Check backend logs
docker compose logs backend --tail 50

# Restart backend
docker compose restart backend

# Rebuild if needed
docker compose up -d --build backend
```

### Issue: Database connection errors
```bash
# Check postgres is healthy
docker compose ps postgres

# View postgres logs
docker compose logs postgres

# Restart postgres
docker compose restart postgres
```

---

## 📝 Development Workflow

### Make Changes to Backend Code
```bash
# Changes are auto-reloaded (volume mount)
# No rebuild needed for code changes
# Just restart if needed:
docker compose restart backend
```

### Make Changes to Frontend Code
```bash
# Requires rebuild:
docker compose up -d --build frontend
```

### Update Dependencies
```bash
# Backend
# Edit backend/requirements.txt
docker compose up -d --build backend

# Frontend
# Edit frontend/package.json
docker compose up -d --build frontend
```

---

## 📦 Backup & Restore

### Backup Database
```bash
docker compose exec postgres pg_dump -U aurora aurora > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore Database
```bash
cat backup_20251223_120000.sql | docker compose exec -T postgres psql -U aurora aurora
```

### Backup Models
```bash
cp -r backend/models backend/models_backup_$(date +%Y%m%d)
```

---

## 🔍 Monitoring

### Check Container Resource Usage
```bash
docker stats
```

### View All Logs
```bash
docker compose logs --tail 100
```

### Check Disk Usage
```bash
docker system df
```

---

## ⚙️ Configuration Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Container orchestration |
| `backend/requirements.txt` | Python dependencies |
| `frontend/package.json` | Node.js dependencies |
| `frontend/nginx.conf` | Nginx web server config |
| `backend/config/scoring.json` | Confidence/risk scoring rules |
| `backend/config/priors.json` | Business type priors |

---

## 🎯 Common Use Cases

### Upload a CSV File
1. Go to http://localhost:3000/app/upload
2. Select file (CSV or Excel with 'account_name' column)
3. Choose business type
4. Click "Submit for Analysis"
5. View results with charts and analytics

### Analyze Text Directly
1. Go to http://localhost:3000/app/direct-analysis
2. Enter transaction description
3. Click "Analyze Transaction"
4. See prediction with confidence score

### Download Results
1. Complete a job upload
2. View results page
3. Click "Download Results CSV"
4. Open in Excel/Google Sheets

---

## 📞 Support

**Issues & Questions:**
- Check logs: `docker compose logs`
- Check documentation: `IMPLEMENTATION_SUMMARY.md`
- Review code: Backend at `backend/src/`, Frontend at `frontend/src/`

**Key Files to Check:**
- Classifier: `backend/src/adapters/ml/two_stage_classifier.py`
- API Routes: `backend/src/frameworks/fastapi_app.py`
- Upload Page: `frontend/src/pages/UploadPage.tsx`

---

*Last Updated: December 23, 2025*
*Version: two-stage-v1.0*
