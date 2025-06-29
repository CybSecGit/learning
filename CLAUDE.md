# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Development Skills Laboratory** - a personal knowledge wiki for software development, testing, and modern engineering practices. It covers Python (primary), Go, and TypeScript, with a strong focus on web scraping, test-driven development, and AI-powered development workflows. While primarily a personal reference, the content is structured to be useful for others exploring these topics.

## Common Development Commands

### Initial Setup
```bash
# Install all dependencies and setup pre-commit hooks
make install-dev

# Quick start with Docker environment
make quickstart
```

### Testing
```bash
# Run all tests with coverage
make test

# Run a specific test interactively
make test-one
# Then enter the test name when prompted

# Generate HTML coverage report
make coverage
```

### Code Quality
```bash
# Run all linting checks (flake8, mypy, black, isort)
make lint

# Auto-format code
make format

# Security checks
make security
```

### Docker Operations
```bash
# Start all services (PostgreSQL, Redis, main container)
docker-compose up -d

# Start with Selenium Grid for browser automation
docker-compose --profile selenium up -d

# Access the main container shell
make docker-shell
# or
docker-compose exec course bash

# View logs
make docker-logs

# Access PostgreSQL
make db-shell
```

### Documentation
```bash
# Start Docusaurus documentation site
make serve-docs
# or
cd website && npm start

# Build documentation
make docs
```

### Development Workflow
```bash
# Start interactive Python development environment
make dev

# Run Jupyter notebook
make notebook
# Access at http://localhost:8889

# Run a specific exercise
make run-exercise
# Then choose from the list

# Watch for changes and auto-run tests
make watch
```

## Architecture & Structure

### Directory Layout
- **`course/`** - Main knowledge base content
  - `chapters/` - Topic-focused documentation (containerization, web scraping, testing, etc.)
  - `exercises/` - Hands-on coding examples and experiments
  - `tests/` - Test suite for example code
  - `demos/` - Demo scripts and workshops
  - `resources/` - Supporting files (Docker configs, SQL scripts)
  
- **`website/`** - Docusaurus documentation site
  - React-based documentation platform
  - Web-accessible version of the wiki content
  - Runs on port 3000

- **Root level**
  - `learning_concepts_*.md` - Programming concept reference guides for different languages
  - Docker configuration files
  - Python requirements files

### Key Design Patterns

1. **Containerized Development**
   - All development happens in Docker containers
   - PostgreSQL for data persistence
   - Redis for caching and job queues
   - Optional Selenium Grid for browser automation

2. **Test-Driven Development (TDD)**
   - Tests are in `course/tests/`
   - pytest with coverage reporting
   - Mock data only for tests, never for dev/prod

3. **Multi-Language Support**
   - Python is primary language
   - Go and TypeScript exercises included
   - Each language has its own `learning_concepts_*.md`

4. **Knowledge Organization**
   - Practical, example-driven documentation
   - Comprehensive code examples and experiments
   - Focus on real-world applications and patterns

### Database Schema
PostgreSQL database initialized from `course/resources/init-db.sql` with:
- User: `scraper`
- Database: `scraping_db`
- Connection available via `DATABASE_URL` environment variable

### Testing Strategy
- Unit tests with pytest
- Coverage reporting with pytest-cov
- Security testing with bandit and safety
- Type checking with mypy
- Code formatting with black and isort

### Environment Variables
- `PYTHONPATH=/app` (set in Docker)
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `POSTGRES_PASSWORD` - defaults to `dev_password_not_for_prod`

## Development Tips

### Running Single Tests
Instead of running the entire test suite:
```bash
pytest course/tests/test_specific.py::TestClass::test_method -v
```

### Debugging in Docker
```bash
# Enter container with full environment
docker-compose exec course bash

# Run Python with debugger
docker-compose exec course python -m pdb course/exercises/some_exercise.py
```

### Adding New Exercises
```bash
make new-exercise
# Enter exercise name when prompted
```

### Performance Profiling
```bash
make profile
# Enter script path to profile
```

## Security Considerations
- Never commit `.env` files
- All SQL queries must use parameterized statements
- Run `make security` before committing
- Use Chainguard base images for containers when possible
- Dependencies are checked with safety for CVEs