# AURORA - Indonesian Tax Object Classifier

> Production-grade AI application for classifying Indonesian tax objects from General Ledger descriptions with confidence scoring and business-to-ledger compliance risk assessment.

---

## 🎉 **LATEST UPDATE - December 21, 2025**

**Version 2.0.1 - Modern UI with Bug Fixes**

✅ **Status:** All code complete - Ready to use after restart
📚 **Quick Start:** See [START_HERE_AFTER_SESSION.md](START_HERE_AFTER_SESSION.md)
🔧 **Restart Guide:** See [RESTART_INSTRUCTIONS.txt](RESTART_INSTRUCTIONS.txt)
🆘 **Troubleshooting:** See [QUICK_FIX_GUIDE.md](QUICK_FIX_GUIDE.md)

**What's New:**
- ✅ Modern gradient UI (purple → pink → indigo)
- ✅ Drag-and-drop file upload with preview
- ✅ 4 interactive charts (Pie, Bar, Histogram, Summary)
- ✅ Direct text analysis feature (instant predictions)
- ✅ Color-coded confidence levels (🟢🟡🔴)
- ✅ Tax object emojis for quick identification
- ✅ Smooth Framer Motion animations
- ✅ All bugs fixed (imports, error handling)

**Action Required:** Restart backend + frontend servers to apply latest fixes!

---

## Architecture Overview

### Clean Architecture / Hexagonal (Ports & Adapters) + MVC

```mermaid
graph TB
    subgraph "Frameworks & Drivers (Outermost)"
        UI[React Frontend - Views]
        API[FastAPI Routes]
        DB[(SQLite/Postgres)]
        FS[File Storage]
    end

    subgraph "Adapters (Interface Adapters)"
        Controllers[HTTP Controllers - MVC Controllers]
        Repos[Repository Implementations]
        MLAdapter[ML Classifier Adapter]
        StorageAdapter[Storage Adapter]
        ExplainAdapter[Explainability Adapter]
    end

    subgraph "Application Layer (Use Cases)"
        UC1[CreateJobUseCase]
        UC2[ProcessJobUseCase]
        UC3[GetJobStatusUseCase]
        UC4[GetJobRowsUseCase]
        UC5[DownloadResultsUseCase]
        UC6[GetConfigUseCase]
    end

    subgraph "Domain Layer (Core - MVC Models)"
        Entities[Entities: Job, PredictionRow, RiskReport]
        ValueObjects[Value Objects: TaxObjectLabel, Scores]
        Policies[Policies: ConfidencePolicy, RiskPolicy]
        Ports[Ports: Interfaces]
    end

    UI --> Controllers
    API --> Controllers
    Controllers --> UC1 & UC2 & UC3 & UC4 & UC5 & UC6
    UC1 & UC2 & UC3 & UC4 & UC5 & UC6 --> Ports
    Ports -.implements.- Repos & MLAdapter & StorageAdapter & ExplainAdapter
    Repos --> DB
    StorageAdapter --> FS
    Policies --> ValueObjects
    UC2 --> Policies

    style Domain fill:#f9f,stroke:#333,stroke-width:4px
    style Application fill:#bbf,stroke:#333,stroke-width:2px
    style Adapters fill:#bfb,stroke:#333,stroke-width:2px
```

### MVC Mapping

- **Views**: React components (`frontend/src/pages/`, `frontend/src/components/`)
- **Controllers**: FastAPI HTTP controllers (`backend/src/adapters/http/controllers/`)
- **Models**: Domain layer + Application layer + ML adapters
  - Domain entities, value objects, policies
  - Use cases orchestrating business logic
  - Ports defining interfaces
  - Adapters implementing ports

### Dependency Rule

All dependencies point **inward**:
- Frameworks/UI → Adapters → Application → Domain
- Domain has ZERO external dependencies
- Application depends only on Domain
- Adapters depend on Application + Domain but implement ports

## Features

✅ **Multi-label Tax Classification**
- PPh21, PPh22, PPh23 variants, PPh26, PPN, PPh4(2) Final
- Fiscal corrections (positive/negative)
- Non-taxable objects

✅ **Confidence Scoring**
- Row-level confidence (0-100%)
- Margin-based uncertainty quantification
- Quality penalties for poor data

✅ **Business Compliance Risk**
- Dataset-level risk score (0-100%)
- Jensen-Shannon divergence from expected business priors
- Anomaly detection (corrections, end-of-period clustering)

✅ **Explainability**
- TF-IDF token attribution
- Nearest neighbor examples from training corpus
- Transparent rule-based signals

✅ **Production-Ready**
- Clean Architecture enforced
- API key authentication
- Audit trails with SHA256 file hashing
- Structured logging with request/job IDs
- Docker Compose deployment
- Production gates validation

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local frontend dev)
- Python 3.11+ (for local backend dev)

### Run with Docker (Recommended)

```bash
# 1. Clone and navigate
cd aurora-tax-classifier

# 2. Copy environment variables
cp .env.example .env

# 3. Build and start all services
docker compose up --build

# 4. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Run Locally (Development)

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m src.adapters.ml.train_baseline  # Train initial model
uvicorn src.frameworks.fastapi_app:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

### Run Tests

```bash
# Backend tests
make test-backend

# Frontend tests
make test-frontend

# Production gates validation
make validate-gates
```

## Project Structure

```
aurora-tax-classifier/
├── backend/
│   ├── src/
│   │   ├── domain/              # Core business logic (no frameworks)
│   │   │   ├── entities/        # Job, PredictionRow, RiskReport
│   │   │   ├── value_objects/   # TaxObjectLabel, Scores
│   │   │   ├── policies/        # ConfidencePolicy, RiskPolicy
│   │   │   └── errors/          # DomainValidationError
│   │   ├── application/         # Use cases (orchestration)
│   │   │   ├── use_cases/       # CreateJob, ProcessJob, etc.
│   │   │   ├── ports/           # Interfaces for adapters
│   │   │   └── dtos/            # Request/Response objects
│   │   ├── adapters/            # Framework implementations
│   │   │   ├── http/            # FastAPI controllers (MVC Controllers)
│   │   │   ├── persistence/     # Repository implementations
│   │   │   ├── storage/         # File storage adapter
│   │   │   ├── ml/              # Classifier adapter (TF-IDF + LR)
│   │   │   └── explainability/  # Explainer adapter
│   │   └── frameworks/          # Framework configuration
│   │       └── fastapi_app.py   # App factory
│   ├── config/
│   │   ├── scoring.json         # Scoring configuration
│   │   └── priors.json          # Business type priors
│   ├── data/
│   │   └── seed_corpus.jsonl    # Training data
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                    # React UI (MVC Views)
│   ├── src/
│   │   ├── pages/               # Landing, Upload, Results, History
│   │   ├── components/          # Reusable UI components
│   │   ├── api/                 # API client
│   │   └── App.tsx
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── Makefile
├── app_spec.json                # Production gates
├── check_app_spec.py            # Gates validator
├── .env.example
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/jobs` | Create new classification job |
| GET | `/api/jobs/{id}` | Get job status and summary |
| GET | `/api/jobs/{id}/rows` | Get paginated prediction rows |
| GET | `/api/jobs/{id}/download` | Download results as CSV |
| GET | `/api/config` | Get label taxonomy and config |
| GET | `/api/healthz` | Health check |

## Configuration

### Environment Setup

AURORA Tax Classifier uses environment variables for configuration. We provide three environment files:

- **`.env.example`** - Complete template with all available environment variables and documentation
- **`.env.development`** - Development configuration with safe defaults (ready to use)
- **`.env.production`** - Production template with placeholders (requires customization)

#### Quick Setup for Development

```bash
# Option 1: Use development defaults (recommended for quick start)
cp .env.development .env

# Option 2: Start from template (customize as needed)
cp .env.example .env
# Then edit .env with your preferred settings
```

#### Quick Setup for Production

```bash
# Copy production template
cp .env.production .env

# CRITICAL: Update all REPLACE_WITH_* placeholders with actual values
# Never use placeholder values in production!
# Use a secure secret management system for sensitive values
```

### Environment Variables Reference

#### Core Settings

```bash
# Application
NODE_ENV=development              # Environment: development, staging, production
APP_NAME=AURORA Tax Classifier    # Application name
APP_VERSION=2.0.1                 # Application version

# Database
DATABASE_URL=sqlite:///./aurora.db                    # SQLite for dev
# DATABASE_URL=postgresql://user:pass@host:5432/db   # PostgreSQL for production

# Authentication
API_KEY=your-secret-api-key-here  # Backend API key (REQUIRED)

# URLs
BACKEND_URL=http://localhost:8000        # Backend API URL
VITE_API_BASE_URL=http://localhost:8000  # Frontend -> Backend URL
FRONTEND_URL=http://localhost:3000       # Frontend URL
CORS_ORIGINS=http://localhost:3000       # Allowed origins (comma-separated)
```

#### Optional Integrations

```bash
# Clerk Authentication (optional)
CLERK_PUBLISHABLE_KEY=pk_***
CLERK_SECRET_KEY=sk_***
CLERK_WEBHOOK_SECRET=whsec_***

# Anthropic API (optional - for AI features)
ANTHROPIC_API_KEY=sk-ant-***

# Resend Email (optional - for notifications)
RESEND_API_KEY=re_***
RESEND_FROM_EMAIL=noreply@yourdomain.com

# Sentry Error Tracking (optional - recommended for production)
SENTRY_DSN=https://***@sentry.io/***
SENTRY_ENVIRONMENT=production
```

#### Storage & File Upload

```bash
STORAGE_PATH=./storage           # File storage directory
MAX_FILE_SIZE_MB=10             # Max upload size in MB
ALLOWED_FILE_EXTENSIONS=.csv,.xlsx,.xls  # Allowed file types
```

#### Logging

```bash
LOG_LEVEL=INFO                  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=json                 # json or text
LOG_REQUESTS=true              # Log all HTTP requests
```

#### Security

```bash
FORCE_HTTPS=false              # Force HTTPS redirect (true in production)
SESSION_SECRET=***             # Session encryption secret
CSRF_SECRET=***                # CSRF token secret
ENABLE_RATE_LIMIT=true        # Enable API rate limiting
RATE_LIMIT_PER_MINUTE=100     # Max requests per minute
```

#### Feature Flags

```bash
ENABLE_DIRECT_ANALYSIS=true   # Enable direct text analysis
ENABLE_RISK_REPORTS=true      # Enable risk reporting
ENABLE_EXPLAINABILITY=true    # Enable ML explainability
ENABLE_JOB_HISTORY=true       # Enable job history tracking
MAX_HISTORY_JOBS=100          # Max jobs to keep in history
```

### Database Configuration

#### Development (SQLite)

SQLite is used by default for development - no setup required:

```bash
DATABASE_URL=sqlite:///./aurora.db
```

#### Production (PostgreSQL)

PostgreSQL is **required** for production:

```bash
# Standard connection string
DATABASE_URL=postgresql://username:password@host:5432/database

# With SSL (recommended)
DATABASE_URL=postgresql://username:password@host:5432/database?sslmode=require

# Example: AWS RDS
DATABASE_URL=postgresql://aurora:SecurePass123@aurora-db.abc123.us-east-1.rds.amazonaws.com:5432/aurora_prod
```

**Production Database Checklist:**
- [ ] Use a managed database service (AWS RDS, Azure Database, Google Cloud SQL)
- [ ] Enable SSL/TLS connections
- [ ] Use strong passwords (20+ characters)
- [ ] Enable automated backups
- [ ] Set up read replicas for high availability
- [ ] Configure connection pooling
- [ ] Monitor database performance

### Security Best Practices

#### Generating Secure Secrets

```bash
# Generate API key (64 characters)
openssl rand -hex 32

# Generate session secret
openssl rand -base64 48

# Generate CSRF secret
openssl rand -base64 32
```

#### Secret Management

**Development:**
- Use `.env.development` with safe defaults
- Never commit `.env` with real API keys

**Production:**
- Use a secret management service:
  - AWS Secrets Manager
  - Azure Key Vault
  - Google Secret Manager
  - HashiCorp Vault
- Rotate secrets every 90 days
- Use environment-specific IAM roles/service accounts
- Enable audit logging

#### Environment File Security

```bash
# These files are safe to commit:
.env.example          # Template with documentation
.env.development      # Development defaults (no real secrets)
.env.production       # Production template (placeholders only)

# NEVER commit these files:
.env                  # Actual environment (in .gitignore)
.env.local            # Local overrides (in .gitignore)
.env.*.local          # Environment-specific overrides (in .gitignore)
```

### Docker Configuration

When using Docker Compose, environment variables are loaded automatically:

```bash
# Default: Uses .env file
docker compose up

# Specify environment file
docker compose --env-file .env.development up

# Production
docker compose --env-file .env.production up -d
```

### Troubleshooting Environment Issues

#### Issue: "API Key Invalid"
**Solution:** Check that `API_KEY` in `.env` matches the `X-Aurora-Key` header in requests

```bash
# Backend .env
API_KEY=my-secret-key

# Frontend request
curl -H "X-Aurora-Key: my-secret-key" http://localhost:8000/api/healthz
```

#### Issue: "CORS Error"
**Solution:** Add your frontend URL to `CORS_ORIGINS`

```bash
# Allow multiple origins
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,https://yourdomain.com
```

#### Issue: "Database Connection Failed"
**Solution:** Verify database URL format and credentials

```bash
# SQLite (development)
DATABASE_URL=sqlite:///./aurora.db

# PostgreSQL (production)
DATABASE_URL=postgresql://user:password@host:5432/database
```

#### Issue: "Environment Variables Not Loaded"
**Solution:** Check file location and naming

```bash
# File must be named exactly .env and placed in project root
ls -la .env

# Verify format (no spaces around =)
NODE_ENV=development  # Correct
NODE_ENV = development  # Wrong
```

### Advanced Configuration

### Scoring Configuration

Edit `backend/config/scoring.json`:

```json
{
  "confidence": {
    "p_max_weight": 0.65,
    "margin_weight": 0.35,
    "short_text_penalty": 0.75,
    "vague_text_penalty": 0.85
  },
  "risk": {
    "distance_weight": 0.55,
    "anomaly_weight": 0.45,
    "thresholds": {
      "high_correction_rate": 0.15,
      "high_non_object_rate": 0.25
    }
  }
}
```

### Business Priors

Edit `backend/config/priors.json`:

```json
{
  "Manufaktur": {
    "PPh21": 0.25,
    "PPh23_Jasa": 0.20,
    "PPN": 0.30,
    ...
  }
}
```

## Usage Example

### 1. Upload GL File

```bash
curl -X POST http://localhost:8000/api/jobs \
  -H "X-Aurora-Key: your-api-key" \
  -F "file=@general_ledger.csv" \
  -F "business_type=Manufaktur"
```

Response:
```json
{
  "job_id": "job_20250121_abc123",
  "status": "processing"
}
```

### 2. Check Status

```bash
curl http://localhost:8000/api/jobs/job_20250121_abc123 \
  -H "X-Aurora-Key: your-api-key"
```

Response:
```json
{
  "job_id": "job_20250121_abc123",
  "status": "completed",
  "summary": {
    "total_rows": 1250,
    "avg_confidence": 87.3,
    "risk_percent": 23.5
  },
  "risk_report": {
    "risk_percent": 23.5,
    "breakdown": {...}
  },
  "audit_trail": {...}
}
```

### 3. Download Results

```bash
curl http://localhost:8000/api/jobs/job_20250121_abc123/download \
  -H "X-Aurora-Key: your-api-key" \
  -o results.csv
```

## Development Workflow

### Adding New Tax Labels

1. Add to `backend/config/priors.json`
2. Add training examples to `backend/data/seed_corpus.jsonl`
3. Retrain model: `python -m src.adapters.ml.train_baseline`
4. Update frontend label display in `frontend/src/components/LabelBadge.tsx`

### Extending Classification Model

The classifier is pluggable via `ClassifierPort`:

```python
# backend/src/application/ports/classifier_port.py
class ClassifierPort(ABC):
    @abstractmethod
    def predict_proba(self, texts: List[str]) -> List[Dict[str, float]]:
        pass
```

To add transformer-based model:
1. Create new adapter: `backend/src/adapters/ml/transformer_classifier.py`
2. Implement `ClassifierPort` interface
3. Update DI in `backend/src/frameworks/fastapi_app.py`

### Production Gates

Before deploying, ensure all gates pass:

```bash
python check_app_spec.py
```

Failed gates will cause CI to fail and require restart from `step_1_architecture_design`.

## Security

- **API Key Authentication**: All endpoints require `X-Aurora-Key` header
- **CORS**: Restricted to configured origins
- **PII Protection**: NPWP patterns hashed in logs
- **File Validation**: Type and size limits enforced
- **Audit Trail**: All jobs include SHA256 file hash and model versions

## Testing

```bash
# Unit tests (domain + application)
pytest backend/tests/unit/

# Integration tests (adapters)
pytest backend/tests/integration/

# End-to-end tests
pytest backend/tests/e2e/

# Coverage report
pytest --cov=src --cov-report=html
```

## Deployment

### Production Checklist

- [ ] Set strong `API_KEY` in environment
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure CORS for production domain
- [ ] Set `LOG_LEVEL=WARNING` or `ERROR`
- [ ] Enable HTTPS (reverse proxy)
- [ ] Set up monitoring (logs aggregation)
- [ ] Configure backup for database and storage
- [ ] Run `python check_app_spec.py` in CI

### Docker Compose Production

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Monitoring

Logs are JSON-structured and include:

- `request_id`: Unique per API request
- `job_id`: Unique per classification job
- `timestamp`: ISO 8601
- `level`: INFO, WARNING, ERROR
- `message`: Human-readable message
- `context`: Additional metadata

Example:
```json
{
  "timestamp": "2025-01-21T10:30:45.123Z",
  "level": "INFO",
  "request_id": "req_xyz789",
  "job_id": "job_20250121_abc123",
  "message": "Job processing completed",
  "context": {
    "duration_ms": 3245,
    "rows_processed": 1250
  }
}
```

## Troubleshooting

### Model not found error

```bash
cd backend
python -m src.adapters.ml.train_baseline
```

### Port already in use

```bash
# Change ports in docker-compose.yml or .env
BACKEND_PORT=8001
FRONTEND_PORT=3001
```

### Database locked (SQLite)

Switch to PostgreSQL in production or ensure single worker process.

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Ensure tests pass (`make test`)
4. Ensure gates pass (`make validate-gates`)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open Pull Request

## License

MIT License - see LICENSE file

## Support

- Documentation: [docs/](docs/)
- Issues: GitHub Issues
- Email: support@aurora-tax.example.com

---

Built with Clean Architecture principles for maintainability, testability, and scalability.
