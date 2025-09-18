# Makefile for Reddit Stalker API Deployment

.PHONY: help install test run deploy clean dev-setup prod-check docker-build docker-run docker-stop

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install dependencies"
	@echo "  test         - Run tests"
	@echo "  run          - Run the application locally"
	@echo "  deploy       - Deploy to Render (manual trigger)"
	@echo "  clean        - Clean up temporary files"
	@echo "  dev-setup    - Setup development environment"
	@echo "  prod-check   - Check production readiness"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run Docker container"
	@echo "  docker-stop  - Stop Docker container"

# Install dependencies
install:
	pip install -r requirements.txt

# Run tests
test:
	python tests/test_api_simple.py

# Run the application locally
run:
	python main.py

# Deploy to Render (this is just a placeholder - actual deployment is via Render dashboard)
deploy:
	@echo "Deployment to Render is handled through the Render dashboard"
	@echo "Make sure your environment variables are set in Render"
	@echo "Trigger a manual deployment from the Render dashboard"

# Clean up temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/

# Development setup
dev-setup: install
	@echo "Setting up development environment..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env file from template"; fi
	@echo "Please edit .env file with your API credentials"

# Production check
prod-check:
	@echo "Checking production readiness..."
	@python -c "import main; print('✓ Main module imports successfully')"
	@python -c "import requests; print('✓ Requests module available')"
	@python -c "import praw; print('✓ PRAW module available')"
	@echo "✓ All checks passed"

# Docker commands
docker-build:
	@echo "Building Docker image..."
	docker build -t reddit-stalker-api .

docker-run:
	@echo "Running Docker container..."
	docker run -d --name reddit-stalker-api -p 8000:8000 --env-file .env reddit-stalker-api

docker-stop:
	@echo "Stopping Docker container..."
	docker stop reddit-stalker-api || true
	docker rm reddit-stalker-api || true
