# Web Scraping Course Makefile
# Simplifies common development tasks

.PHONY: help install install-dev test lint format clean docker-build docker-up docker-down docs

# Default target
help:
	@echo "Web Scraping Course - Available Commands:"
	@echo "  make install       - Install production dependencies"
	@echo "  make install-dev   - Install all dependencies (including dev)"
	@echo "  make test         - Run all tests"
	@echo "  make lint         - Run linting checks"
	@echo "  make format       - Format code with black"
	@echo "  make clean        - Clean up temporary files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-up    - Start Docker services"
	@echo "  make docker-down  - Stop Docker services"
	@echo "  make docs         - Build documentation"
	@echo "  make serve-docs   - Serve documentation locally"

# Install production dependencies
install:
	pip install -r requirements.txt

# Install all dependencies including development
install-dev:
	pip install -r requirements.txt -r requirements-dev.txt
	pre-commit install

# Run tests
test:
	pytest course/tests/ -v --cov=course --cov-report=html

# Run specific test
test-one:
	@read -p "Enter test name: " test_name; \
	pytest course/tests/ -v -k $$test_name

# Run linting
lint:
	flake8 course/
	mypy course/
	black --check course/
	isort --check-only course/

# Format code
format:
	black course/
	isort course/

# Security check
security:
	bandit -r course/
	safety check

# Clean temporary files
clean:
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

# Docker commands
docker-build:
	docker build -t webscraping-course .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f course

docker-shell:
	docker-compose exec course bash

docker-clean:
	docker-compose down -v
	docker rmi webscraping-course

# Documentation
docs:
	cd website && npm run build

serve-docs:
	cd website && npm start

# Course exercises
run-exercise:
	@echo "Available exercises:"
	@ls -1 course/exercises/*.py | sed 's/course\/exercises\//  - /'
	@read -p "Enter exercise name (without .py): " exercise; \
	python course/exercises/$$exercise.py

# Database operations
db-init:
	docker-compose exec postgres psql -U scraper -d scraping_db -f /docker-entrypoint-initdb.d/init.sql

db-shell:
	docker-compose exec postgres psql -U scraper -d scraping_db

# Development server
dev:
	@echo "Starting development environment..."
	docker-compose up -d postgres redis
	python -m ipython

# Jupyter notebook
notebook:
	jupyter notebook --notebook-dir=course/

# Check Python version
check-python:
	@python --version
	@pip --version

# Initialize project
init: install-dev
	@echo "Setting up git hooks..."
	pre-commit install
	@echo "Creating necessary directories..."
	mkdir -p workspace data logs output
	@echo "Project initialized!"

# Run specific Python file
run:
	@read -p "Enter Python file path: " filepath; \
	python $$filepath

# Update dependencies
update-deps:
	pip-compile requirements.in -o requirements.txt
	pip-compile requirements-dev.in -o requirements-dev.txt

# Create new exercise
new-exercise:
	@read -p "Enter exercise name: " name; \
	cp course/exercises/template.py course/exercises/$$name.py; \
	echo "Created course/exercises/$$name.py"

# Run performance profiling
profile:
	@read -p "Enter script to profile: " script; \
	python -m cProfile -s cumulative $$script

# Generate coverage report
coverage:
	pytest course/tests/ --cov=course --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

# Watch for changes and run tests
watch:
	@echo "Watching for changes..."
	@while true; do \
		inotifywait -e modify -r course/; \
		clear; \
		make test; \
	done

# Backup course data
backup:
	@timestamp=$$(date +%Y%m%d_%H%M%S); \
	tar -czf backup_$$timestamp.tar.gz course/ data/ logs/; \
	echo "Backup created: backup_$$timestamp.tar.gz"

# Quick start for new students
quickstart: docker-build docker-up
	@echo "====================================="
	@echo "Web Scraping Course is ready!"
	@echo "====================================="
	@echo "Access Jupyter at: http://localhost:8889"
	@echo "Enter course shell: make docker-shell"
	@echo "View logs: make docker-logs"
	@echo "====================================="