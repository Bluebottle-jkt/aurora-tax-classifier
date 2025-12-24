# AURORA Tax Classifier - Environment Configuration Guide

Complete guide to setting up and managing environment variables for the AURORA Tax Classifier project.

---

## Table of Contents

1. [Overview](#overview)
2. [Environment Files](#environment-files)
3. [Quick Start](#quick-start)
4. [Configuration Reference](#configuration-reference)
5. [Security Best Practices](#security-best-practices)
6. [Deployment Guides](#deployment-guides)
7. [Troubleshooting](#troubleshooting)

---

## Overview

The AURORA Tax Classifier uses environment variables to configure application behavior across different environments (development, staging, production). This approach provides:

- **Security**: Sensitive credentials never stored in code
- **Flexibility**: Easy configuration changes without code modifications
- **Environment Separation**: Different settings for dev, staging, and production
- **Docker Compatibility**: Seamless integration with Docker Compose

### Environment Files Provided

| File | Purpose | Commit to Git? |
|------|---------|----------------|
| `.env.example` | Complete template with all variables and documentation | ✅ Yes |
| `.env.development` | Development defaults (safe values) | ✅ Yes |
| `.env.production` | Production template (placeholders) | ✅ Yes |
| `.env` | Actual environment config (with secrets) | ❌ No (gitignored) |
| `.env.local` | Local overrides | ❌ No (gitignored) |

---

## Environment Files

### .env.example

**Purpose**: Complete reference template with all available environment variables

**Contents**:
- All environment variables with descriptions
- Default values and examples
- Comments explaining each setting
- Setup instructions

**Usage**:
```bash
# Copy and customize
cp .env.example .env
# Edit .env with your actual values
```

### .env.development

**Purpose**: Ready-to-use development configuration

**Features**:
- SQLite database (no setup required)
- Safe API keys for local use
- Debug logging enabled
- CORS configured for common dev ports
- All features enabled
- No external dependencies required

**Usage**:
```bash
# Quick start for development
cp .env.development .env
npm run dev  # or docker compose up
```

**Safe to commit**: Yes (contains no real secrets)

### .env.production

**Purpose**: Production template with security best practices

**Features**:
- PostgreSQL configuration (required)
- Placeholder values (must be replaced)
- Security settings enabled
- Production logging configuration
- Comprehensive deployment checklist
- Secret management guidelines

**Usage**:
```bash
# For production deployment
cp .env.production .env
# Replace ALL REPLACE_WITH_* placeholders
# Use secret management service for sensitive values
```

**Safe to commit**: Yes (placeholders only, no actual secrets)

---

## Quick Start

### For Local Development (Fastest)

```bash
# 1. Navigate to project directory
cd aurora-tax-classifier

# 2. Copy development environment
cp .env.development .env

# 3. Start the application
docker compose up

# 4. Access the app
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

That's it! The development environment is pre-configured and ready to use.

### For Custom Development Setup

```bash
# 1. Copy template
cp .env.example .env

# 2. Edit with your preferred settings
nano .env  # or use your favorite editor

# 3. Minimum required changes:
# - Set API_KEY to a unique value
# - Adjust ports if needed
# - Configure database if using PostgreSQL

# 4. Start the application
docker compose up
```

### For Production Deployment

```bash
# 1. Copy production template
cp .env.production .env

# 2. CRITICAL: Replace all placeholders
# Search for "REPLACE_WITH_" and update with actual values

# 3. Use secret management service
# Store sensitive values in:
# - AWS Secrets Manager
# - Azure Key Vault
# - Google Secret Manager
# - HashiCorp Vault

# 4. Review the deployment checklist in .env.production

# 5. Deploy
docker compose -f docker-compose.yml up -d
```

---

## Configuration Reference

### Required Variables

These variables **must** be set for the application to function:

```bash
# Backend API Authentication (REQUIRED)
API_KEY=your-secret-api-key-here

# Database Connection (REQUIRED)
DATABASE_URL=sqlite:///./aurora.db  # or PostgreSQL URL

# Application URLs (REQUIRED)
BACKEND_URL=http://localhost:8000
VITE_API_BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000

# CORS Configuration (REQUIRED)
CORS_ORIGINS=http://localhost:3000
```

### Optional Integrations

#### Clerk Authentication

For user authentication and management:

```bash
# Get keys from: https://clerk.com/
CLERK_PUBLISHABLE_KEY=pk_test_***
CLERK_SECRET_KEY=sk_test_***
CLERK_WEBHOOK_SECRET=whsec_***
```

**Setup Steps**:
1. Create account at https://clerk.com/
2. Create new application
3. Copy keys from Dashboard → API Keys
4. Set up webhook endpoint for user events

#### Anthropic API

For enhanced AI features (future use):

```bash
# Get key from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-***
```

**Setup Steps**:
1. Create account at https://console.anthropic.com/
2. Go to Settings → API Keys
3. Create new API key
4. Set spending limits

#### Resend Email Service

For transactional emails and notifications:

```bash
# Get key from: https://resend.com/
RESEND_API_KEY=re_***
RESEND_FROM_EMAIL=noreply@yourdomain.com
ENABLE_EMAIL_NOTIFICATIONS=true
ADMIN_EMAIL=admin@yourdomain.com
```

**Setup Steps**:
1. Create account at https://resend.com/
2. Verify your domain
3. Create API key
4. Configure DNS records (SPF, DKIM, DMARC)

#### Sentry Error Tracking

For production error monitoring (highly recommended):

```bash
# Get from: https://sentry.io/
SENTRY_DSN=https://***@o***.ingest.sentry.io/***
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1
```

**Setup Steps**:
1. Create account at https://sentry.io/
2. Create new project (Python + JavaScript)
3. Copy DSN from Settings → Client Keys
4. Configure alerts and integrations

### Database Configuration

#### SQLite (Development Only)

Simple file-based database, no setup required:

```bash
DATABASE_URL=sqlite:///./aurora.db
```

**Pros**:
- Zero configuration
- Perfect for development
- Fast for small datasets

**Cons**:
- Not suitable for production
- Limited concurrency
- No replication

#### PostgreSQL (Production)

Production-grade database with full features:

```bash
# Local PostgreSQL
DATABASE_URL=postgresql://aurora:password@localhost:5432/aurora

# Docker Compose PostgreSQL
DATABASE_URL=postgresql://aurora:password@postgres:5432/aurora

# Cloud PostgreSQL (with SSL)
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
```

**Production Checklist**:
- [ ] Use managed service (AWS RDS, Azure Database, Google Cloud SQL)
- [ ] Enable SSL/TLS encryption
- [ ] Set up automated backups (daily + point-in-time recovery)
- [ ] Configure read replicas for high availability
- [ ] Set up connection pooling (PgBouncer)
- [ ] Enable monitoring and alerting
- [ ] Implement disaster recovery plan
- [ ] Use strong passwords (20+ characters)
- [ ] Restrict network access (VPC/firewall)
- [ ] Enable query logging for auditing

**Cloud Provider Examples**:

```bash
# AWS RDS
DATABASE_URL=postgresql://aurora:SecurePass123@aurora-db.abc123.us-east-1.rds.amazonaws.com:5432/aurora_prod?sslmode=require

# Azure Database for PostgreSQL
DATABASE_URL=postgresql://aurora@myserver:SecurePass123@myserver.postgres.database.azure.com:5432/aurora_prod?sslmode=require

# Google Cloud SQL
DATABASE_URL=postgresql://aurora:SecurePass123@/aurora_prod?host=/cloudsql/project:region:instance

# Heroku Postgres
DATABASE_URL=postgres://username:password@host.compute.amazonaws.com:5432/dbname
```

### Port Configuration

```bash
# Backend API port (internal and external)
BACKEND_PORT=8000

# Frontend UI port
FRONTEND_PORT=3000

# PostgreSQL port (if using Docker Compose)
POSTGRES_PORT=5432
```

**Port Conflicts**:
If ports are already in use, change them:

```bash
# Use alternative ports
BACKEND_PORT=8001
FRONTEND_PORT=3001
POSTGRES_PORT=5433
```

### Storage Configuration

```bash
# Local file storage
STORAGE_PATH=./storage
MAX_FILE_SIZE_MB=10
ALLOWED_FILE_EXTENSIONS=.csv,.xlsx,.xls

# Cloud storage (recommended for production)
# AWS S3
AWS_S3_BUCKET=aurora-uploads-prod
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=***
AWS_REGION=us-east-1

# Azure Blob Storage
AZURE_STORAGE_ACCOUNT=aurorastorage
AZURE_STORAGE_KEY=***
AZURE_STORAGE_CONTAINER=uploads

# Google Cloud Storage
GCS_BUCKET=aurora-uploads-prod
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

### Logging Configuration

```bash
# Development
LOG_LEVEL=DEBUG
LOG_FORMAT=text
LOG_REQUESTS=true

# Production
LOG_LEVEL=WARNING
LOG_FORMAT=json
LOG_REQUESTS=false

# Log to file (optional)
LOG_FILE_PATH=/var/log/aurora/app.log
```

**Log Levels**:
- `DEBUG`: Detailed information for debugging
- `INFO`: General informational messages
- `WARNING`: Warning messages (recommended for production)
- `ERROR`: Error messages only
- `CRITICAL`: Critical errors only

### Feature Flags

Enable or disable features without code changes:

```bash
# Enable/disable features
ENABLE_DIRECT_ANALYSIS=true      # Direct text classification
ENABLE_RISK_REPORTS=true         # Risk assessment reports
ENABLE_EXPLAINABILITY=true       # ML model explanations
ENABLE_JOB_HISTORY=true          # Job history tracking
MAX_HISTORY_JOBS=100             # Maximum jobs in history

# Example: Disable explainability for faster processing
ENABLE_EXPLAINABILITY=false
```

---

## Security Best Practices

### 1. Generate Strong Secrets

**Never use default or example values in production!**

```bash
# Generate strong API key (64 characters)
openssl rand -hex 32

# Generate session secret (64 bytes, base64 encoded)
openssl rand -base64 48

# Generate CSRF secret
openssl rand -base64 32

# Generate using Python
python -c "import secrets; print(secrets.token_hex(32))"

# Generate using Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

### 2. Secret Management

#### Development
- Use `.env.development` with safe defaults
- Never commit `.env` with real credentials
- Use different API keys than production

#### Production
- **Use a secret management service**:
  - AWS Secrets Manager
  - Azure Key Vault
  - Google Secret Manager
  - HashiCorp Vault

- **Rotate secrets regularly**:
  - API keys: Every 90 days
  - Database passwords: Every 90 days
  - Session secrets: Every 180 days

- **Audit secret access**:
  - Enable logging for all secret retrievals
  - Monitor for unauthorized access
  - Set up alerts for anomalies

### 3. Environment File Security

```bash
# Safe to commit (no secrets)
✅ .env.example
✅ .env.development
✅ .env.production

# NEVER commit (contains secrets)
❌ .env
❌ .env.local
❌ .env.production.local
❌ .env.*.local
```

### 4. CORS Configuration

**Development**: Allow localhost
```bash
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Production**: Only allow your domains
```bash
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Never use**: `*` (allows all origins - major security risk!)

### 5. HTTPS in Production

```bash
# Development
FORCE_HTTPS=false

# Production
FORCE_HTTPS=true
```

Configure SSL/TLS:
- Use Let's Encrypt for free certificates
- Set up automatic renewal
- Enable HSTS headers
- Use strong cipher suites

### 6. Rate Limiting

Protect against abuse and DDoS:

```bash
# Development (lenient)
ENABLE_RATE_LIMIT=false
RATE_LIMIT_PER_MINUTE=1000

# Production (strict)
ENABLE_RATE_LIMIT=true
RATE_LIMIT_PER_MINUTE=60
```

---

## Deployment Guides

### Local Development

```bash
# 1. Setup environment
cp .env.development .env

# 2. Install dependencies
cd backend && pip install -r requirements.txt
cd ../frontend && npm install

# 3. Train baseline model
cd backend && python -m src.adapters.ml.train_baseline

# 4. Start backend
cd backend && uvicorn src.frameworks.fastapi_app:app --reload

# 5. Start frontend (new terminal)
cd frontend && npm run dev
```

### Docker Compose (Recommended)

```bash
# Development
docker compose up

# Production
docker compose -f docker-compose.yml up -d

# With specific env file
docker compose --env-file .env.production up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

### AWS Deployment

#### Using ECS (Elastic Container Service)

1. **Setup secrets in AWS Secrets Manager**:
```bash
aws secretsmanager create-secret \
  --name aurora/production/api-key \
  --secret-string "your-secure-api-key"

aws secretsmanager create-secret \
  --name aurora/production/database-url \
  --secret-string "postgresql://..."
```

2. **Configure ECS task definition** (reference secrets):
```json
{
  "containerDefinitions": [{
    "secrets": [
      {
        "name": "API_KEY",
        "valueFrom": "arn:aws:secretsmanager:region:account:secret:aurora/production/api-key"
      }
    ]
  }]
}
```

3. **Deploy**:
```bash
aws ecs update-service \
  --cluster aurora-cluster \
  --service aurora-service \
  --force-new-deployment
```

### Azure Deployment

#### Using App Service

1. **Create App Service**:
```bash
az webapp create \
  --name aurora-tax-classifier \
  --resource-group aurora-rg \
  --plan aurora-plan
```

2. **Configure environment variables**:
```bash
az webapp config appsettings set \
  --name aurora-tax-classifier \
  --resource-group aurora-rg \
  --settings \
    API_KEY=@Microsoft.KeyVault(SecretUri=...) \
    DATABASE_URL=@Microsoft.KeyVault(SecretUri=...)
```

3. **Deploy**:
```bash
az webapp deployment source config \
  --name aurora-tax-classifier \
  --resource-group aurora-rg \
  --repo-url https://github.com/yourorg/aurora \
  --branch main
```

### Google Cloud Deployment

#### Using Cloud Run

1. **Setup secrets**:
```bash
echo -n "your-api-key" | gcloud secrets create api-key --data-file=-
```

2. **Deploy**:
```bash
gcloud run deploy aurora-tax-classifier \
  --image gcr.io/project/aurora:latest \
  --set-secrets=API_KEY=api-key:latest
```

---

## Troubleshooting

### Common Issues

#### 1. "API Key Invalid"

**Symptoms**: 401 Unauthorized errors

**Solution**:
```bash
# Check backend .env
cat .env | grep API_KEY
# API_KEY=my-secret-key

# Verify request header matches
curl -H "X-Aurora-Key: my-secret-key" http://localhost:8000/api/healthz
```

#### 2. "CORS Error"

**Symptoms**: Browser console shows CORS errors

**Solution**:
```bash
# Add frontend URL to CORS_ORIGINS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# For multiple domains
CORS_ORIGINS=https://app.example.com,https://www.example.com

# Restart backend after changes
```

#### 3. "Database Connection Failed"

**Symptoms**: Application fails to start, database errors

**Solutions**:

```bash
# SQLite: Check file path
DATABASE_URL=sqlite:///./aurora.db  # Relative to backend directory

# PostgreSQL: Verify connection string format
DATABASE_URL=postgresql://user:password@host:5432/database

# PostgreSQL: Test connection
psql $DATABASE_URL -c "SELECT 1"

# Docker: Ensure database service is running
docker compose ps postgres
```

#### 4. "Environment Variables Not Loaded"

**Symptoms**: Application uses default values

**Solutions**:

```bash
# Check file location (must be in project root)
ls -la .env

# Check file format (no spaces around =)
# Correct:
API_KEY=value
# Wrong:
API_KEY = value

# Docker Compose: Verify env file
docker compose config

# Check for typos in variable names
grep -E "^[A-Z_]+=" .env
```

#### 5. "Port Already in Use"

**Symptoms**: "Address already in use" error

**Solution**:
```bash
# Find process using port
# Linux/Mac:
lsof -i :8000
# Windows:
netstat -ano | findstr :8000

# Kill process
kill -9 <PID>

# Or change port in .env
BACKEND_PORT=8001
FRONTEND_PORT=3001
```

#### 6. "File Upload Fails"

**Symptoms**: Upload errors, file too large

**Solution**:
```bash
# Increase max file size
MAX_FILE_SIZE_MB=50

# Check allowed extensions
ALLOWED_FILE_EXTENSIONS=.csv,.xlsx,.xls

# Verify storage path exists and is writable
mkdir -p storage
chmod 755 storage
```

### Debug Mode

Enable detailed logging for troubleshooting:

```bash
# Backend
LOG_LEVEL=DEBUG
LOG_FORMAT=text
LOG_REQUESTS=true

# Frontend
VITE_DEBUG_MODE=true

# Restart services to apply changes
```

### Validation Checklist

Before deployment, verify your configuration:

```bash
# 1. Check required variables are set
grep -E "^(API_KEY|DATABASE_URL|CORS_ORIGINS)=" .env

# 2. Verify no placeholder values remain
grep -E "REPLACE_WITH_|your-|change-this" .env

# 3. Test database connection
# (depends on your database type)

# 4. Test API key authentication
curl -H "X-Aurora-Key: $API_KEY" http://localhost:8000/api/healthz

# 5. Verify CORS configuration
# Open browser console and check for CORS errors

# 6. Check logs for errors
docker compose logs backend
docker compose logs frontend
```

---

## Additional Resources

- **Main README**: [README.md](README.md)
- **Quick Start Guide**: [QUICK_START.md](QUICK_START.md)
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md) (if exists)
- **Security Guide**: [SECURITY.md](SECURITY.md) (if exists)
- **API Documentation**: http://localhost:8000/docs (when running)

---

## Support

For issues or questions:
1. Check this guide and README.md
2. Review application logs
3. Search existing GitHub issues
4. Create new issue with:
   - Environment (dev/staging/prod)
   - Error messages
   - Steps to reproduce
   - Configuration (sanitized, no secrets!)

---

**Last Updated**: December 24, 2025
**Version**: 2.0.1
