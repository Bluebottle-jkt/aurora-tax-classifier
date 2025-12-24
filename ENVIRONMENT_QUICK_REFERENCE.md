# Environment Configuration - Quick Reference

Quick reference guide for AURORA Tax Classifier environment setup.

---

## Files Overview

| File | Purpose | Commit? | Contains Secrets? |
|------|---------|---------|-------------------|
| `.env.example` | Complete template with all variables | ✅ Yes | ❌ No |
| `.env.development` | Development defaults | ✅ Yes | ❌ No (safe defaults) |
| `.env.production` | Production template | ✅ Yes | ❌ No (placeholders only) |
| `.env` | Actual configuration | ❌ No | ✅ Yes |
| `.env.local` | Local overrides | ❌ No | ✅ Maybe |

---

## Quick Setup Commands

### Development (Fastest Start)
```bash
cp .env.development .env
docker compose up
```
Access: http://localhost:3000

### Production
```bash
cp .env.production .env
# Edit .env and replace all REPLACE_WITH_* values
docker compose -f docker-compose.yml up -d
```

---

## Essential Variables

### Minimum Required
```bash
API_KEY=your-secret-api-key          # Backend authentication
DATABASE_URL=sqlite:///./aurora.db   # Database connection
CORS_ORIGINS=http://localhost:3000   # Allowed origins
```

### URLs
```bash
BACKEND_URL=http://localhost:8000
VITE_API_BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

### Ports
```bash
BACKEND_PORT=8000
FRONTEND_PORT=3000
POSTGRES_PORT=5432
```

---

## Common Configurations

### Development (SQLite)
```bash
DATABASE_URL=sqlite:///./aurora.db
LOG_LEVEL=DEBUG
LOG_FORMAT=text
ENABLE_RATE_LIMIT=false
```

### Production (PostgreSQL)
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
LOG_LEVEL=WARNING
LOG_FORMAT=json
ENABLE_RATE_LIMIT=true
FORCE_HTTPS=true
```

---

## Optional Integrations

### Clerk Authentication
```bash
CLERK_PUBLISHABLE_KEY=pk_***
CLERK_SECRET_KEY=sk_***
CLERK_WEBHOOK_SECRET=whsec_***
```

### Anthropic AI
```bash
ANTHROPIC_API_KEY=sk-ant-***
```

### Resend Email
```bash
RESEND_API_KEY=re_***
RESEND_FROM_EMAIL=noreply@yourdomain.com
```

### Sentry Error Tracking
```bash
SENTRY_DSN=https://***@sentry.io/***
SENTRY_ENVIRONMENT=production
```

---

## Security Checklist

### Development
- [x] Use `.env.development` template
- [x] Different API keys than production
- [ ] Never commit `.env` with real credentials

### Production
- [ ] Generate strong secrets (64+ chars)
- [ ] Use PostgreSQL (not SQLite)
- [ ] Enable HTTPS (`FORCE_HTTPS=true`)
- [ ] Enable rate limiting
- [ ] Set `LOG_LEVEL=WARNING` or `ERROR`
- [ ] Use secret management service
- [ ] Rotate secrets every 90 days
- [ ] Configure CORS for production domains only
- [ ] Enable Sentry error tracking
- [ ] Set up database backups

---

## Generate Secure Secrets

```bash
# API Key (64 characters)
openssl rand -hex 32

# Session Secret
openssl rand -base64 48

# CSRF Secret
openssl rand -base64 32
```

---

## Troubleshooting

### API Key Invalid
```bash
# Check .env
grep API_KEY .env

# Test
curl -H "X-Aurora-Key: your-key" http://localhost:8000/api/healthz
```

### CORS Error
```bash
# Add frontend URL
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Database Connection Failed
```bash
# SQLite (check path)
DATABASE_URL=sqlite:///./aurora.db

# PostgreSQL (verify format)
DATABASE_URL=postgresql://user:pass@host:5432/db

# Test connection
psql $DATABASE_URL -c "SELECT 1"
```

### Port Already in Use
```bash
# Change port
BACKEND_PORT=8001
FRONTEND_PORT=3001

# Or kill process
lsof -i :8000  # Find PID
kill -9 <PID>  # Kill process
```

---

## Docker Commands

```bash
# Start with default .env
docker compose up

# Use specific env file
docker compose --env-file .env.development up

# Production mode
docker compose -f docker-compose.yml up -d

# View logs
docker compose logs -f

# Stop
docker compose down

# Rebuild
docker compose up --build
```

---

## Environment Variables by Category

### Application
```bash
NODE_ENV=development
APP_NAME=AURORA Tax Classifier
APP_VERSION=2.0.1
```

### Database
```bash
DATABASE_URL=sqlite:///./aurora.db
POSTGRES_USER=aurora
POSTGRES_PASSWORD=***
POSTGRES_DB=aurora
POSTGRES_PORT=5432
```

### Security
```bash
API_KEY=***
SESSION_SECRET=***
CSRF_SECRET=***
FORCE_HTTPS=false
ENABLE_RATE_LIMIT=true
RATE_LIMIT_PER_MINUTE=100
```

### Logging
```bash
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_REQUESTS=true
LOG_FILE_PATH=
```

### Storage
```bash
STORAGE_PATH=./storage
MAX_FILE_SIZE_MB=10
ALLOWED_FILE_EXTENSIONS=.csv,.xlsx,.xls
```

### Features
```bash
ENABLE_DIRECT_ANALYSIS=true
ENABLE_RISK_REPORTS=true
ENABLE_EXPLAINABILITY=true
ENABLE_JOB_HISTORY=true
MAX_HISTORY_JOBS=100
```

---

## Resources

- **Full Guide**: [ENV_SETUP_GUIDE.md](ENV_SETUP_GUIDE.md)
- **Main README**: [README.md](README.md)
- **Template**: [.env.example](.env.example)
- **API Docs**: http://localhost:8000/docs

---

**Version**: 2.0.1
**Last Updated**: December 24, 2025
