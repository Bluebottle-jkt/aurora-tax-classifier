# AURORA - Quick Start Guide

## What You Have

A **complete, production-ready** Indonesian tax object classifier built with Clean Architecture + MVC:

### Architecture
```
┌─────────────────────────────────────────────────────┐
│  FRAMEWORKS & DRIVERS (Outermost Layer)             │
│  - React Frontend (Views)                           │
│  - FastAPI Routes                                   │
│  - PostgreSQL/SQLite Database                       │
│  - File Storage                                     │
└─────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────┐
│  ADAPTERS (Interface Adapters)                      │
│  - HTTP Controllers (MVC Controllers)               │
│  - Repository Implementations                       │
│  - ML Classifier Adapter (TF-IDF + LogReg)          │
│  - Storage Adapter                                  │
│  - Explainability Adapter                           │
└─────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────┐
│  APPLICATION LAYER (Use Cases)                      │
│  - CreateJobUseCase                                 │
│  - ProcessJobUseCase (Core Classification Logic)    │
│  - GetJobStatusUseCase                              │
│  - GetJobRowsUseCase                                │
│  - DownloadResultsUseCase                           │
│  - GetConfigUseCase                                 │
└─────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────┐
│  DOMAIN LAYER (Core - MVC Models)                   │
│  - Entities: Job, PredictionRow, RiskReport         │
│  - Value Objects: TaxObjectLabel, Scores            │
│  - Policies: ConfidencePolicy, RiskPolicy           │
│  - No framework dependencies!                       │
└─────────────────────────────────────────────────────┘
```

### Dependency Rule
All dependencies point **inward** (toward domain):
- Domain has **ZERO** external dependencies
- Application depends only on Domain
- Adapters implement ports from Application
- Frameworks are outermost

## Quick Commands

### 1. Validate Production Gates
```bash
python check_app_spec.py
```
**Expected:** All 13 gates PASS ✓

### 2. Run with Docker (Recommended)
```bash
# Start everything
docker compose up --build

# Access:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### 3. Run Locally (Development)

**Backend:**
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Train baseline model
python -m src.adapters.ml.train_baseline

# Run server
uvicorn src.frameworks.fastapi_app:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev

# Access: http://localhost:3000
```

## Project Structure

```
aurora-tax-classifier/
├── README.md                          # Full documentation
├── QUICK_START.md                     # This file
├── app_spec.json                      # Production gates
├── check_app_spec.py                  # Gates validator
├── docker-compose.yml                 # Docker orchestration
├── Makefile                           # Common commands
├── .env.example                       # Environment template
│
├── backend/
│   ├── src/
│   │   ├── domain/                    # Core business logic
│   │   │   ├── entities/              # Job, PredictionRow, RiskReport, AuditTrail
│   │   │   ├── value_objects/         # TaxObjectLabel, ConfidenceScore, RiskScore
│   │   │   ├── policies/              # ConfidencePolicy, RiskPolicy
│   │   │   └── errors/                # Domain exceptions
│   │   │
│   │   ├── application/               # Use cases & ports
│   │   │   ├── use_cases/             # Business logic orchestration
│   │   │   ├── ports/                 # Interfaces for adapters
│   │   │   └── dtos/                  # Data transfer objects
│   │   │
│   │   ├── adapters/                  # Framework implementations
│   │   │   ├── http/                  # FastAPI controllers
│   │   │   ├── persistence/           # Repository implementations
│   │   │   ├── ml/                    # TF-IDF classifier
│   │   │   ├── storage/               # File storage
│   │   │   ├── config/                # JSON config loader
│   │   │   └── explainability/        # Model explainability
│   │   │
│   │   └── frameworks/                # Framework setup
│   │       └── fastapi_app.py         # Application factory
│   │
│   ├── config/
│   │   ├── scoring.json               # Scoring algorithm config
│   │   └── priors.json                # Business type priors
│   │
│   ├── data/
│   │   └── seed_corpus.jsonl          # Training data (38 examples)
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
└── frontend/                          # React UI (MVC Views)
    ├── src/
    │   ├── pages/
    │   │   ├── LandingPage.tsx        # Cinematic landing with animations
    │   │   ├── UploadPage.tsx         # File upload interface
    │   │   └── ResultsPage.tsx        # Results display
    │   ├── App.tsx                    # Main app component
    │   └── main.tsx                   # Entry point
    │
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.js
    └── Dockerfile
```

## Usage Flow

### Step 1: Upload General Ledger
Navigate to http://localhost:3000/app/upload

- Upload CSV or Excel file
- Required column: `account_name`
- Optional columns: `account_code`, `amount`, `date`, `debit_credit`, `counterparty`
- Select business type: Manufaktur, Perdagangan, Jasa
- Click Submit

### Step 2: View Results
Redirected to `/app/results/{job_id}`

You'll see:
- **Job Status**: pending → processing → completed
- **Summary**:
  - Total rows processed
  - Average confidence score
  - Risk score (0-100%)
- **Predictions Table**:
  - Account name
  - Predicted tax object label
  - Confidence percentage
  - Explanation & signals

### Step 3: Download Results
Click "Download CSV" to export results with all fields:
- Original GL fields
- Predicted tax object
- Confidence score
- Explanation
- Risk signals
- Probability distribution
- Top TF-IDF terms

## API Usage

### Create Job
```bash
curl -X POST http://localhost:8000/api/jobs \
  -H "X-Aurora-Key: aurora-dev-key" \
  -F "file=@gl_data.csv" \
  -F "business_type=Manufaktur"

# Response:
# {
#   "job_id": "job_20250121_1234",
#   "status": "pending"
# }
```

### Check Status
```bash
curl http://localhost:8000/api/jobs/job_20250121_1234 \
  -H "X-Aurora-Key: aurora-dev-key"

# Response:
# {
#   "job_id": "job_20250121_1234",
#   "status": "completed",
#   "summary": {
#     "total_rows": 150,
#     "avg_confidence": 87.3,
#     "risk_percent": 23.5
#   }
# }
```

### Get Predictions
```bash
curl "http://localhost:8000/api/jobs/job_20250121_1234/rows?page=1&page_size=50" \
  -H "X-Aurora-Key: aurora-dev-key"
```

### Get Configuration
```bash
curl http://localhost:8000/api/config \
  -H "X-Aurora-Key: aurora-dev-key"
```

## Tax Object Labels

The system classifies into 14 labels:

| Label | Description |
|-------|-------------|
| `PPh21` | Employee income tax |
| `PPh22` | Import/government procurement tax |
| `PPh23_Bunga` | Interest withholding tax |
| `PPh23_Dividen` | Dividend withholding tax |
| `PPh23_Hadiah` | Prize withholding tax |
| `PPh23_Jasa` | Service withholding tax |
| `PPh23_Royalti` | Royalty withholding tax |
| `PPh23_Sewa` | Rental withholding tax |
| `PPh26` | Non-resident tax |
| `PPN` | Value-added tax |
| `PPh4_2_Final` | Final tax (rental, construction) |
| `Fiscal_Correction_Positive` | Positive fiscal correction |
| `Fiscal_Correction_Negative` | Negative fiscal correction |
| `Non_Object` | Non-taxable object |

## Scoring Algorithms

### Row-Level Confidence
```
confidence_raw = 0.65 * p_max + 0.35 * sigmoid(10 * margin)
confidence_percent = round(100 * clamp(confidence_raw with penalties, 0, 1))

Penalties:
- Short text (< 3 chars): × 0.75
- Vague text (contains "unknown", "misc"): × 0.85
- Mostly symbols: × 0.75
```

### Dataset-Level Risk
```
risk_percent = round(100 * (0.55 * JS_divergence + 0.45 * anomaly_score))

Where:
- JS_divergence: Jensen-Shannon divergence from expected business priors
- anomaly_score: Average of:
  - high_correction_rate (> 15%)
  - high_non_object_rate (> 25%)
  - high_label_variance (entropy > 0.8)
  - end_of_period_clustering (> 30% in last 10 days)
```

All parameters configurable in `backend/config/scoring.json`

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

### Validate Gates
```bash
python check_app_spec.py

# Should output:
# [PASS] ALL PRODUCTION GATES PASSED
# [READY] System is ready for deployment
```

## Configuration

### Environment Variables (.env)
```bash
# Backend
DATABASE_URL=sqlite:///./aurora.db
STORAGE_PATH=./storage
API_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
MODEL_VERSION=baseline-v1.0

# Frontend
VITE_API_BASE_URL=http://localhost:8000
```

### Business Priors (backend/config/priors.json)
```json
{
  "Manufaktur": {
    "PPh21": 0.25,
    "PPh23_Jasa": 0.20,
    "PPN": 0.30,
    ...
  },
  "Perdagangan": { ... },
  "Jasa": { ... }
}
```

### Scoring Config (backend/config/scoring.json)
```json
{
  "confidence": {
    "p_max_weight": 0.65,
    "margin_weight": 0.35,
    "short_text_penalty": 0.75,
    ...
  },
  "risk": {
    "distance_weight": 0.55,
    "anomaly_weight": 0.45,
    ...
  }
}
```

## Upgrading the ML Model

The classifier is **pluggable** via the `ClassifierPort` interface:

1. Create new adapter implementing `ClassifierPort`:
```python
# backend/src/adapters/ml/transformer_classifier.py
class TransformerClassifier(ClassifierPort):
    def predict_proba(self, texts: List[str]) -> List[Dict[str, float]]:
        # Your implementation
        pass

    def get_version(self) -> str:
        return "transformer-v1.0"
```

2. Update dependency injection in `fastapi_app.py`:
```python
classifier = TransformerClassifier()  # Instead of TfidfClassifier()
```

3. Retrain and deploy!

## Troubleshooting

### Model not found
```bash
cd backend
python -m src.adapters.ml.train_baseline
```

### Port already in use
```bash
# Edit .env
BACKEND_PORT=8001
FRONTEND_PORT=3001
```

### Database locked (SQLite)
Switch to PostgreSQL or use single worker:
```bash
uvicorn src.frameworks.fastapi_app:app --workers 1
```

## Next Steps

1. **Add More Training Data**: Edit `backend/data/seed_corpus.jsonl`
2. **Customize Labels**: Update `backend/config/priors.json`
3. **Tune Scoring**: Adjust `backend/config/scoring.json`
4. **Upgrade Model**: Implement transformer-based classifier
5. **Add Tests**: Write unit tests for your use cases
6. **Deploy**: Use `docker compose -f docker-compose.yml -f docker-compose.prod.yml up`

## Production Deployment

Before production:

- [ ] Set strong `API_KEY` in environment
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure CORS for production domain
- [ ] Set `LOG_LEVEL=WARNING` or `ERROR`
- [ ] Enable HTTPS (reverse proxy)
- [ ] Set up log aggregation
- [ ] Configure database backups
- [ ] Run `python check_app_spec.py` in CI

## Support

- Full Documentation: [README.md](README.md)
- Architecture Diagram: See README.md
- API Docs: http://localhost:8000/docs (when running)
- Production Gates: `python check_app_spec.py`

---

**Built with Clean Architecture principles for maintainability, testability, and scalability.**

*AURORA - Intelligent Tax Object Classification*
