# Python Project CLAUDE.md

## Project Overview
This is a Python web application using FastAPI for the backend API and SQLAlchemy for database operations. The project follows Domain-Driven Design principles with a focus on testability and maintainability.

## Core Development Principles

### Python-Specific Standards
- Python 3.11+ required for modern type hints and performance
- Follow PEP 8 with Black formatting (line length 100)
- Type hints required for all function signatures
- Use `ruff` for linting with strict settings

### Architecture Patterns
- Repository pattern for data access
- Service layer for business logic
- Dependency injection for testability
- CQRS for complex domains

## Code Style and Conventions

### Import Organization
```python
# Standard library imports
import os
import sys
from datetime import datetime
from typing import Optional, List, Dict

# Third-party imports
import httpx
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Local imports
from app.core.config import settings
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
```

### Error Handling
```python
# Always use custom exceptions
class DomainError(Exception):
    """Base exception for domain errors"""
    pass

class ValidationError(DomainError):
    """Raised when validation fails"""
    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"{field}: {message}")

# Context managers for resource cleanup
async with httpx.AsyncClient() as client:
    response = await client.get(url)
```

### Testing Requirements
- Minimum 85% test coverage
- Use pytest exclusively
- Fixtures in conftest.py
- Mock external dependencies
- Test both happy and error paths

## Project Structure
```
project/
├── app/
│   ├── api/           # FastAPI routes
│   ├── core/          # Config, security, database
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic
│   ├── repositories/  # Data access layer
│   └── utils/         # Helper functions
├── tests/
│   ├── unit/          # Unit tests
│   ├── integration/   # Integration tests
│   └── conftest.py    # Shared fixtures
├── migrations/        # Alembic migrations
├── scripts/          # Utility scripts
└── docker/           # Docker configurations
```

## Database Guidelines
- Use Alembic for all schema changes
- Never modify migrations after deployment
- Index foreign keys and commonly queried fields
- Use async SQLAlchemy for better performance

## API Design
- RESTful endpoints with clear resource names
- Consistent error response format
- Pagination for list endpoints
- API versioning through URL path
- OpenAPI documentation required

## Performance Optimization
- Use Redis for caching
- Profile with py-spy for bottlenecks
- Async everywhere possible
- Connection pooling for databases
- Lazy loading for relationships

## Security Practices
```python
# Use environment variables
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    api_key: str
    
    class Config:
        env_file = ".env"

# SQL injection prevention
from sqlalchemy import text
query = text("SELECT * FROM users WHERE id = :user_id")
result = session.execute(query, {"user_id": user_id})

# Password hashing
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

## Development Workflow

### Virtual Environment
```bash
# Always use virtual environments
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Common Commands
```bash
# Run tests with coverage
pytest --cov=app --cov-report=html

# Format code
black app tests
isort app tests

# Lint code
ruff check app tests
mypy app

# Run development server
uvicorn app.main:app --reload

# Database migrations
alembic upgrade head
alembic revision --autogenerate -m "description"
```

## Git Commit Guidelines
- Use conventional commits
- Reference issue numbers
- Sign commits with GPG when possible
- Examples:
  - `feat(auth): implement JWT refresh tokens`
  - `fix(db): resolve connection pool exhaustion`
  - `test(user): add integration tests for registration`

## Documentation Standards
- Docstrings for all public functions
- Type hints serve as documentation
- README must include setup instructions
- API documentation auto-generated from code

## Monitoring and Logging
```python
import structlog

logger = structlog.get_logger()

# Structured logging with context
logger.info(
    "user_action",
    user_id=user.id,
    action="login",
    ip_address=request.client.host
)
```

## Performance Benchmarks
- API response time < 100ms (p95)
- Database queries < 50ms
- Background jobs processed within 5 seconds
- Memory usage < 512MB per worker

## Dependencies Management
- Pin all dependencies in requirements.txt
- Regular security updates (monthly)
- Use pip-tools for dependency resolution
- Separate dev dependencies

## Deployment Checklist
- [ ] All tests passing
- [ ] Code coverage > 85%
- [ ] No security vulnerabilities (bandit, safety)
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] Database migrations tested
- [ ] Environment variables configured
- [ ] Monitoring alerts set up

## Learning Resources
- Effective Python by Brett Slatkin
- FastAPI documentation
- SQLAlchemy 2.0 documentation
- Python testing with pytest

## Import External Standards
@../imports/error-handling.md
@../imports/testing-conventions.md
@../imports/security-guidelines.md
@../imports/git-workflow.md