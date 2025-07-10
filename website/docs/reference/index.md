# Reference
## *Quick Access to Essential Information*

> "The best documentation is the one you actually use." - Developers Who've Been Burned by Bad Docs

This section contains quick reference materials, troubleshooting guides, and resources you'll want to bookmark for daily development. No lengthy explanations here - just the information you need when you need it.

## Quick References

### 🚀 **Setup & Installation**

#### [Docker Quick Start](./docker-quick-start.md)
<div class="skills-progress-indicator beginner">🟢 Essential</div>

**When You Need It:** Setting up development environments quickly.

**What's Inside:**
- Common Docker commands
- Development environment templates
- Troubleshooting connection issues
- Performance optimization tips

```bash
# Quick container setup
docker-compose up -d postgres redis
docker-compose exec app bash
```

### 🔒 **Security Guidelines**

#### [Security Note](./security-note.md)
<div class="skills-progress-indicator intermediate">🟡 Important</div>

**When You Need It:** Before deploying anything to production.

**Key Reminders:**
- Environment variable management
- Secret handling best practices
- Common security vulnerabilities
- Compliance considerations

```bash
# Security checklist
make security-scan
make audit-dependencies
make check-secrets
```

### 📝 **Contributing Guidelines**

#### [Contributing](./contributing.md)
<div class="skills-progress-indicator beginner">🟢 Community</div>

**When You Need It:** Contributing to this project or any open source project.

**Process Overview:**
- How to report issues
- Code contribution workflow
- Documentation improvements
- Review process

## Command Quick Reference

### Development Commands
```bash
# Project setup
make install-dev
make quickstart

# Testing
make test
make test-one TEST=test_specific.py
make coverage

# Code quality
make format
make lint
make security

# Development environment
make dev
make docker-shell
make db-shell
```

### Docker Operations
```bash
# Start services
docker-compose up -d
docker-compose --profile selenium up -d

# Container management
docker-compose exec service bash
docker-compose logs service
docker-compose restart service

# Cleanup
docker-compose down
docker system prune
```

### Git Workflows
```bash
# Feature development
git checkout -b feature/new-thing
git add .
git commit -m "feat: add new thing"
git push origin feature/new-thing

# Code review
gh pr create --title "Add new thing"
gh pr review --approve
gh pr merge --squash
```

## Troubleshooting Guides

### 🔧 **Common Issues**

#### Environment Setup Problems
```bash
# Python version issues
python --version  # Should be 3.11+
pyenv install 3.11.5
pyenv global 3.11.5

# Docker connection issues
docker info
sudo systemctl restart docker
```

#### Database Connection Issues
```bash
# Check PostgreSQL status
docker-compose logs postgres
docker-compose exec postgres psql -U scraper -d scraping_db

# Reset database
docker-compose down -v
docker-compose up -d postgres
make db-init
```

#### Port Conflicts
```bash
# Find what's using a port
lsof -i :8000
netstat -tulpn | grep :8000

# Kill process using port
kill -9 $(lsof -t -i:8000)
```

### 🐛 **Debugging Techniques**

#### Python Debugging
```python
# Add debug breakpoint
import pdb; pdb.set_trace()

# Print with context
print(f"Debug: {variable=}, {type(variable)=}")

# Log with details
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"Processing {item}")
```

#### Docker Debugging
```bash
# Check container logs
docker-compose logs -f service

# Interactive debugging
docker-compose exec service bash
docker-compose run --rm service python -m pdb script.py

# Network debugging
docker network ls
docker network inspect learning_default
```

## Configuration Templates

### 🔧 **Project Configuration**

#### Python Project Setup
```toml
# pyproject.toml template
[tool.uv]
dev-dependencies = [
    "pytest>=7.0",
    "ruff>=0.1",
    "mypy>=1.0",
    "pre-commit>=3.0",
]

[tool.ruff]
line-length = 88
target-version = "py311"
select = ["E", "F", "W", "I", "N", "UP"]

[tool.mypy]
python_version = "3.11"
strict = true
```

#### Docker Compose Template
```yaml
# docker-compose.yml essentials
services:
  app:
    build: .
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/dbname
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### ⚙️ **VS Code Configuration**

#### Essential Extensions
```json
// .vscode/extensions.json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.mypy-type-checker",
    "charliermarsh.ruff",
    "ms-vscode.vscode-typescript-next",
    "bradlc.vscode-tailwindcss"
  ]
}
```

#### Settings Template
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "ruff",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

## Resource Collections

### 📚 **External Resources**

#### Essential Documentation
- **Python:** [python.org/docs](https://docs.python.org/)
- **PostgreSQL:** [postgresql.org/docs](https://www.postgresql.org/docs/)
- **Docker:** [docs.docker.com](https://docs.docker.com/)
- **Git:** [git-scm.com/docs](https://git-scm.com/docs)

#### AI Development Tools
- **Claude Code:** [claude.ai/code](https://claude.ai/code)
- **GitHub Copilot:** [github.com/features/copilot](https://github.com/features/copilot)
- **Cursor:** [cursor.sh](https://cursor.sh/)

#### Testing and Quality
- **pytest:** [docs.pytest.org](https://docs.pytest.org/)
- **Ruff:** [beta.ruff.rs/docs](https://beta.ruff.rs/docs/)
- **mypy:** [mypy.readthedocs.io](https://mypy.readthedocs.io/)
- **pre-commit:** [pre-commit.com](https://pre-commit.com/)

### 🔗 **Internal Cross-References**

#### By Topic
- **Getting Started:** [Setup workflows](../getting-started/index.md)
- **Core Concepts:** [Programming fundamentals](../core-concepts/index.md)
- **Development Tools:** [AI-assisted development](../development-tools/index.md)
- **Technical Domains:** [Specialized knowledge](../technical-domains/index.md)
- **Learning Paths:** [Structured courses](../learning-paths/index.md)
- **Hands-on Practice:** [Exercises and tutorials](../hands-on-practice/index.md)

#### By Skill Level
- **🟢 Beginner:** Start with getting started guides
- **🟡 Intermediate:** Focus on technical domains
- **🔴 Advanced:** Tackle complex learning paths

## Cheat Sheets

### 🐍 **Python Quick Reference**
```python
# Modern Python patterns
from typing import Optional, List, Dict
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    database_url: str
    debug: bool = False
    api_keys: Dict[str, str] = None

# Async patterns
async def fetch_data(url: str) -> Optional[Dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json() if response.status_code == 200 else None
```

### 🐳 **Docker Quick Reference**
```bash
# Development workflow
docker-compose up -d              # Start services
docker-compose exec app bash      # Enter container
docker-compose logs -f app        # Follow logs
docker-compose down               # Stop services

# Debugging
docker-compose ps                 # List running containers
docker-compose top                # Show running processes
docker system df                  # Show disk usage
docker system prune              # Clean up
```

### 🔀 **Git Quick Reference**
```bash
# Feature workflow
git checkout main
git pull origin main
git checkout -b feature/new-thing
# ... make changes ...
git add .
git commit -m "feat: add new thing"
git push origin feature/new-thing

# Cleanup
git checkout main
git branch -d feature/new-thing
git remote prune origin
```

## Emergency Procedures

### 🚨 **When Everything Is Broken**

#### Nuclear Option (Reset Everything)
```bash
# Stop all services
docker-compose down -v

# Clean Docker
docker system prune -a

# Reset repository
git stash
git checkout main
git pull origin main

# Restart fresh
make quickstart
```

#### Selective Reset
```bash
# Just database
docker-compose down postgres
docker volume rm learning_postgres_data
docker-compose up -d postgres

# Just dependencies
rm -rf .venv
uv venv
uv sync
```

## Getting Help

### 📞 **Support Channels**

#### Self-Service
1. **Search this documentation**
2. **Check the debugging guides**
3. **Look at error logs**
4. **Try Claude Code for help**

#### Community Support
1. **GitHub Issues:** Bug reports and feature requests
2. **Discussions:** Questions and general help
3. **Pull Requests:** Code contributions

#### Professional Support
- Consider hiring a consultant for complex issues
- Many community members offer paid support
- Commercial support options may be available

---

**Remember:** Good documentation saves time for everyone. If you find something missing or unclear, please contribute improvements.

*The best reference is the one that gets you unstuck quickly so you can get back to building.*