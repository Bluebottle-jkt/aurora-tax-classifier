# Multi-stage build for Python backend
FROM python:3.11-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/storage /app/models /app/logs

# Train baseline model if not exists
RUN python -m src.adapters.ml.train_baseline || echo "Model training will occur on first run"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/healthz || exit 1

# Run application
CMD ["uvicorn", "src.frameworks.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
