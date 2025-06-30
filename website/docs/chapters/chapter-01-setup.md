# Chapter 1: Python Project Setup
## *The Art of Starting Right (Or at Least Not Wrong)*

Setting up a Python project is like preparing for a dinner party—do it right, and everything flows smoothly. Do it wrong, and you're serving disaster with a side of regret.

## The Existential Crisis of Dependency Management

Python dependency management is what happens when anarchists try to organize a library. Everyone has their own ideas about where things should go, what versions to use, and whether that semicolon is really necessary (it's not, this is Python).

The fundamental problem: Python's global package installation is like having one bathroom for an entire office building. Eventually, someone's going to have a bad time.

## Virtual Environments: Digital Isolationism That Works

Virtual environments are Python's answer to "but it works on my machine." They're isolated Python installations where each project gets its own set of packages, preventing the digital equivalent of roommates fighting over the thermostat.

### The Mechanics of Isolation

Here's what happens under the hood, explained like you're five (with a computer science degree):

1. **Python Installation**: Your system Python is like the apartment building
2. **Virtual Environment**: Each project gets its own apartment
3. **Package Installation**: Furniture that stays in that specific apartment
4. **Activation**: Moving into that apartment temporarily

```bash
# Creating a virtual environment (building the apartment)
python -m venv myenv

# Activating it (moving in)
source myenv/bin/activate  # Unix/macOS
myenv\Scripts\activate     # Windows

# Your prompt now shows (myenv) - you're home
```

## The Modern Approach: UV Package Manager

While `pip` is Python's traditional package manager (think postal service circa 1995), `uv` is the modern alternative (think same-day drone delivery). It's written in Rust, because apparently making things fast requires oxidation.

### Why UV Exists

UV solves several traditional Python packaging pain points:
- **Speed**: 10-100x faster than pip (achieved by caring about performance)
- **Reproducibility**: Deterministic dependency resolution (no more "works on my machine")
- **User Experience**: Clear error messages (revolutionary concept)

### Installing UV

```bash
# Unix/macOS (the enlightened path)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Add to PATH if needed (because computers are pedantic)
export PATH="$HOME/.local/bin:$PATH"
```

## Essential Python Development Tools

### The Core Toolkit

Every Python project needs certain tools, like every kitchen needs knives (sharp ones, preferably):

```bash
# Create and activate virtual environment with UV
uv venv
source .venv/bin/activate  # Unix/macOS
.venv\Scripts\activate     # Windows

# Install development essentials
uv pip install pytest black ruff mypy pre-commit
```

### Tool Breakdown: What Each Tool Actually Does

**pytest**: The Testing Framework
- Finds and runs your tests (the ones you definitely wrote)
- Makes testing almost enjoyable (emphasis on almost)
- Provides detailed failure reports (for educational purposes)

```python
# Example test (tests/test_example.py)
def test_truth():
    """The simplest test that could possibly work."""
    assert True  # Philosophical breakthrough
```

**Black**: The Code Formatter
- Reformats your code automatically
- Ends all formatting debates forever
- Named after Henry Ford's design philosophy: "Any color as long as it's black"

```bash
# Format everything (resistance is futile)
black .

# Check without changing (for the paranoid)
black --check .
```

**Ruff**: The Lightning-Fast Linter
- Written in Rust (because Python linting Python was too slow)
- Replaces flake8, isort, and others
- Finds bugs faster than you can create them

```bash
# Lint everything
ruff check .

# Fix what can be fixed automatically
ruff check --fix .
```

**MyPy**: The Type Checker
- Pretends Python is statically typed
- Catches type-related bugs before runtime
- Makes you write type hints (you'll thank it later)

```python
# Type hints example
def greet(name: str) -> str:
    """Properly typed function (MyPy approved)."""
    return f"Hello, {name}!"
```

## Modern Python Dependencies Worth Knowing

### HTTP and Web Scraping

**httpx**: Modern async HTTP client
```python
import httpx

# Async support built-in
async with httpx.AsyncClient() as client:
    response = await client.get('https://api.example.com')
```

**selectolax**: Fastest HTML parser in the west
```python
from selectolax.parser import HTMLParser

html = HTMLParser(response.text)
title = html.css_first('title').text()
```

### Data Processing

**polars**: DataFrame library that makes pandas look slow
```python
import polars as pl

# Lazy evaluation for performance
df = pl.scan_csv("huge_file.csv")
result = df.filter(pl.col("value") > 100).collect()
```

**pydantic**: Data validation using Python type annotations
```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    
# Automatic validation
user = User(name="Alice", age="30")  # age converted to int
```

## Configuration Management

### Environment Variables and Secrets

Never hardcode secrets. This is not advice, it's a commandment etched in the stone tablets of security.

```python
# .env file (NEVER commit this)
API_KEY=your_secret_key_here
DATABASE_URL=postgresql://user:pass@localhost/db

# Load in Python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
```

### Configuration Files

Modern Python projects typically use:
- `pyproject.toml`: Project metadata and tool configuration
- `.env`: Environment-specific secrets (git-ignored)
- `requirements.txt` or `requirements.in`: Dependency lists

Example `pyproject.toml`:
```toml
[project]
name = "my-awesome-project"
version = "0.1.0"
dependencies = [
    "httpx>=0.24.0",
    "pydantic>=2.0.0",
]

[tool.black]
line-length = 88
target-version = ["py311"]

[tool.ruff]
line-length = 88
select = ["E", "F", "I"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
```

## Git Configuration for Python Projects

### The Sacred `.gitignore`

```gitignore
# Virtual environments (never commit these)
venv/
.venv/
env/

# Python artifacts
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Environment variables
.env
.env.*

# IDE nonsense
.vscode/
.idea/
*.swp
*.swo

# OS detritus
.DS_Store
Thumbs.db
```

### Pre-commit Hooks: Automated Quality Control

Pre-commit runs checks before each commit, like having a very pedantic friend review your code:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
  
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.291
    hooks:
      - id: ruff
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
```

Install and activate:
```bash
pre-commit install
pre-commit run --all-files  # Run manually
```

## Project Structure: How to Organize Without Losing Your Mind

```
my_project/
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── docs/
│   └── README.md
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

This structure provides:
- Clear separation of source code and tests
- Proper Python packaging structure
- Documentation location
- Configuration at the root level

## Common Setup Pitfalls and Solutions

### The "Wrong Python Version" Trap
**Problem**: System has Python 3.8, project needs 3.11  
**Solution**: Use pyenv or container-based development

### The "Dependency Conflict" Nightmare
**Problem**: Package A needs urllib3<2.0, Package B needs urllib3>=2.0  
**Solution**: Use tools like pip-tools or poetry for dependency resolution

### The "Works on My Machine" Classic
**Problem**: Different behavior across environments  
**Solution**: Pin exact versions, use lock files, embrace containers

### The "Committed Secrets" Disaster
**Problem**: AWS keys in Git history  
**Solution**: Use git-secrets, rotate compromised credentials, cry a little

## Advanced Setup Patterns

### Makefile for Common Tasks

```makefile
.PHONY: install test lint format clean

install:
	uv pip install -r requirements.txt
	pre-commit install

test:
	pytest tests/ -v

lint:
	ruff check .
	mypy src/

format:
	black .
	ruff check --fix .

clean:
	find . -type d -name __pycache__ -rm -rf
	find . -type f -name "*.pyc" -delete
```

### Development vs Production Dependencies

```bash
# requirements.in (source file)
httpx
pydantic

# requirements-dev.in
-r requirements.in
pytest
black
ruff

# Generate locked versions
pip-compile requirements.in
pip-compile requirements-dev.in
```

## The Philosophy of Good Setup

A well-set-up project is like a well-organized kitchen: everything has its place, tools are within reach, and you can cook without constantly searching for that one spice you swear you bought last week.

The goal isn't perfection—it's consistency and maintainability. Your future self (or unfortunate colleague) should be able to:
1. Clone the repository
2. Run 2-3 commands maximum
3. Have a working development environment

If it takes a PhD in DevOps to run your Python script, you've gone too far.

---

*"Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away."* - Antoine de Saint-Exupéry (definitely talking about Python dependencies)

## Practical Exercises

1. **Virtual Environment Kata**: Create virtual environments using three different tools (venv, virtualenv, uv) and compare the experience. Document which you prefer and why.

2. **Dependency Detective**: Take any popular Python project from GitHub and analyze its dependency tree. How many sub-dependencies does it really have?

3. **Configuration Challenge**: Set up a project that reads configuration from (in order): environment variables, config file, command-line arguments. Make it not terrible.

4. **Pre-commit Perfectionist**: Configure pre-commit hooks that are actually useful without being annoying. Find the balance between safety and developer happiness.

5. **The Reproducibility Test**: Package your project setup so completely that a stranger can run it with just a README. Test on an actual stranger (with their consent).