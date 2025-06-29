# Contributing Guide

Thank you for your interest in contributing to the Development Skills Laboratory!

## Quick Links

- [Full Contributing Guide](https://github.com/YOUR_USERNAME/learning/blob/main/CONTRIBUTING.md)
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)

## Code of Conduct

We are committed to providing a friendly, safe, and welcoming environment for all contributors.

### Expected Behavior
- Use welcoming and inclusive language
- Be respectful of different viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Unacceptable Behavior
- Harassment of any kind
- Trolling or insulting comments
- Personal attacks
- Publishing private information

## How to Contribute

### 1. Report Issues
- Check existing issues first
- Provide clear reproduction steps
- Include environment details

### 2. Suggest Features
- Explain the use case
- Provide examples if possible
- Be open to feedback

### 3. Submit Code
- Fork the repository
- Create a feature branch
- Write tests for new features
- Follow the style guide
- Submit a pull request

### 4. Improve Documentation
- Fix typos and errors
- Add missing information
- Improve clarity
- Add examples

## Development Setup

### Using Docker (Recommended)
```bash
# Build and start services
docker-compose up -d

# Enter development environment
docker-compose exec dev bash

# Run tests
make test
```

### Manual Setup
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/learning.git
cd learning

# Python setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

# Run tests
pytest
```

## Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring

Example:
```bash
git commit -m "feat: add web scraping retry logic"
```

## Pull Request Process

1. **Create focused PRs** - One feature/fix per PR
2. **Write descriptive titles** - Explain what changed
3. **Update documentation** - Keep docs in sync
4. **Add tests** - Maintain test coverage
5. **Follow style guide** - Use linters and formatters

## Testing

### Run All Tests
```bash
make test
```

### Run Specific Tests
```bash
pytest course/tests/test_scraping.py
```

### Check Coverage
```bash
pytest --cov=course --cov-report=html
```

## Style Guidelines

### Python
- Follow PEP 8
- Use Black for formatting
- Add type hints
- Write docstrings

### Documentation
- Use clear, simple language
- Include code examples
- Add humor appropriately
- Break up long sections

## Getting Help

- Open a GitHub issue
- Start a discussion
- Review existing documentation
- Ask in pull request comments

## Recognition

All contributors are recognized in:
- README.md contributors section
- Release notes
- GitHub insights

Thank you for contributing! 🙏