# Makefile for Development Skills Laboratory
# Simplifies common development tasks

.PHONY: help install test lint format security clean docker-build docker-up docker-down docker-logs docker-shell docker-clean docs-build docs-serve docs-clear docs-deploy

# Default target
help:
	@echo "Development Skills Laboratory - Available Commands:"
	@echo "  make install       - Install Python dependencies using uv"
	@echo "  make test          - Run all Python tests"
	@echo "  make lint          - Run linting checks (ruff)"
	@echo "  make format        - Format Python code (black, ruff)"
	@echo "  make security      - Run security checks (bandit, safety)"
	@echo "  make clean         - Clean up temporary files and caches"
	@echo "  make docker-build  - Build Docker images for the project"
	@echo "  make docker-up     - Start Docker services (database, etc.)"
	@echo "  make docker-down   - Stop Docker services"
	@echo "  make docker-logs   - View Docker service logs"
	@echo "  make docker-shell  - Get a shell inside the main Docker container"
	@echo "  make docker-clean  - Stop and remove all Docker containers and images"
	@echo "  make docs-build    - Build the Docusaurus documentation site"
	@echo "  make docs-serve    - Serve the Docusaurus documentation site locally"
	@echo "  make docs-clear    - Clear Docusaurus build cache"
	@echo "  make docs-deploy   - Deploy the Docusaurus site to GitHub Pages"

# Install Python dependencies
install:
	@echo "Installing Python dependencies..."
	uv venv
	source .venv/bin/activate && uv pip install -r requirements.txt -r requirements-dev.txt
	pre-commit install

# Run Python tests
test:
	@echo "Running Python tests..."
	source .venv/bin/activate && pytest website/docs/ -v --cov=website/docs/ --cov-report=html

# Run linting checks
lint:
	@echo "Running linting checks..."
	source .venv/bin/activate && ruff check .
	source .venv/bin/activate && mypy .

# Format Python code
format:
	@echo "Formatting Python code..."
	source .venv/bin/activate && black .
	source .venv/bin/activate && ruff format .

# Run security checks
security:
	@echo "Running security checks..."
	source .venv/bin/activate && bandit -r .
	source .venv/bin/activate && safety check

# Clean temporary files and caches
clean:
	@echo "Cleaning temporary files and caches..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf .venv/
	cd website && npm run clear

# Docker commands
docker-build:
	@echo "Building Docker images..."
	docker build -t learning-platform .

docker-up:
	@echo "Starting Docker services..."
	docker-compose up -d

docker-down:
	@echo "Stopping Docker services..."
	docker-compose down

docker-logs:
	@echo "Viewing Docker service logs..."
	docker-compose logs -f

docker-shell:
	@echo "Getting a shell inside the main Docker container..."
	docker-compose exec learning bash

docker-clean:
	@echo "Stopping and removing all Docker containers and images..."
	docker-compose down -v --rmi all
	docker rmi learning-platform || true

# Docusaurus documentation commands
docs-build:
	@echo "Building Docusaurus documentation site..."
	cd website && npm install && npm run build

docs-serve:
	@echo "Serving Docusaurus documentation site locally..."
	cd website && npm install && npm start

docs-clear:
	@echo "Clearing Docusaurus build cache..."
	cd website && npm run clear

docs-deploy:
	@echo "Deploying Docusaurus site to GitHub Pages..."
	cd website && npm install && npm run deploy
