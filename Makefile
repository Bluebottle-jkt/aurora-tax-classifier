.PHONY: help build up down logs test-backend test-frontend validate-gates clean

help: ## Show this help message
	@echo "AURORA Tax Classifier - Makefile Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker images
	docker compose build

up: ## Start all services
	docker compose up -d

up-build: ## Build and start all services
	docker compose up -d --build

down: ## Stop all services
	docker compose down

down-v: ## Stop all services and remove volumes
	docker compose down -v

logs: ## Show logs from all services
	docker compose logs -f

logs-backend: ## Show backend logs
	docker compose logs -f backend

logs-frontend: ## Show frontend logs
	docker compose logs -f frontend

ps: ## Show running containers
	docker compose ps

restart: ## Restart all services
	docker compose restart

restart-backend: ## Restart backend service
	docker compose restart backend

restart-frontend: ## Restart frontend service
	docker compose restart frontend

test-backend: ## Run backend tests
	cd backend && python -m pytest tests/ -v

test-backend-cov: ## Run backend tests with coverage
	cd backend && python -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term

test-frontend: ## Run frontend tests
	cd frontend && npm test

validate-gates: ## Validate production gates
	python check_app_spec.py

lint-backend: ## Lint backend code
	cd backend && python -m pylint src/

lint-frontend: ## Lint frontend code
	cd frontend && npm run lint

format-backend: ## Format backend code
	cd backend && python -m black src/ tests/

train-model: ## Train baseline ML model
	cd backend && python -m src.adapters.ml.train_baseline

shell-backend: ## Open shell in backend container
	docker compose exec backend /bin/bash

shell-frontend: ## Open shell in frontend container
	docker compose exec frontend /bin/sh

db-shell: ## Open PostgreSQL shell
	docker compose exec postgres psql -U aurora -d aurora

clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf backend/htmlcov
	rm -rf backend/.pytest_cache
	rm -rf frontend/dist
	rm -rf frontend/node_modules/.cache

install-backend: ## Install backend dependencies locally
	cd backend && pip install -r requirements.txt

install-frontend: ## Install frontend dependencies locally
	cd frontend && npm install

dev-backend: ## Run backend in development mode
	cd backend && uvicorn src.frameworks.fastapi_app:app --reload --port 8000

dev-frontend: ## Run frontend in development mode
	cd frontend && npm run dev

seed-db: ## Seed database with sample data
	cd backend && python -m scripts.seed_database

backup-db: ## Backup database
	docker compose exec postgres pg_dump -U aurora aurora > backup_$$(date +%Y%m%d_%H%M%S).sql

check: validate-gates lint-backend ## Run all checks (gates + lint)

ci: validate-gates test-backend ## Run CI pipeline locally

deploy-prod: ## Deploy to production (placeholder)
	@echo "⚠️  Production deployment requires additional configuration"
	@echo "1. Update .env with production values"
	@echo "2. Ensure PostgreSQL is configured"
	@echo "3. Run: docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d"

status: ## Show system status
	@echo "=== Container Status ==="
	@docker compose ps
	@echo ""
	@echo "=== Production Gates ==="
	@python check_app_spec.py

all: clean install-backend install-frontend build up ## Clean, install, build, and start
