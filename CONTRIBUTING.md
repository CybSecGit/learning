# Contributing to Web Scraping & Development Course

First off, thank you for considering contributing to this educational project! 🎉 

This course aims to teach web scraping, modern development practices, and AI-assisted coding through practical examples and hands-on exercises. Your contributions help make this resource better for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Style Guidelines](#style-guidelines)
- [Community](#community)

## Code of Conduct

### Our Pledge

We are committed to providing a friendly, safe, and welcoming environment for all, regardless of level of experience, gender identity and expression, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, religion, nationality, or other similar characteristic.

### Our Standards

Examples of behavior that contributes to a positive environment:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior:
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs what actually happened
- **Environment details** (OS, Python version, etc.)
- **Screenshots** if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, provide:

- **Use case** - Why is this enhancement needed?
- **Detailed description** of the proposed change
- **Possible implementation** approach (if you have ideas)
- **Examples** from other projects (if applicable)

### Contributing Content

We welcome contributions in several areas:

#### 1. New Chapters or Sections
- Propose new topics that fit the course objectives
- Ensure content follows the established tone and style
- Include practical exercises and examples

#### 2. Exercises and Challenges
- Create hands-on coding exercises
- Provide clear problem statements
- Include solution hints without giving everything away
- Test exercises thoroughly

#### 3. Language Translations
- Help translate content to other languages
- Maintain the technical accuracy
- Preserve the friendly, educational tone

#### 4. Documentation Improvements
- Fix typos and grammatical errors
- Improve clarity of explanations
- Add missing information
- Update outdated content

### Code Contributions

#### For Course Examples
- Ensure code is educational and well-commented
- Follow the language-specific style guides
- Include error handling and edge cases
- Make examples self-contained when possible

#### For Infrastructure
- Improve Docker setup
- Enhance CI/CD pipelines
- Add development tools
- Optimize build processes

## Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/learning.git
   cd learning
   ```

2. **Set Up Development Environment**
   ```bash
   # Python environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt -r requirements-dev.txt
   
   # Or use Docker
   docker-compose up -d
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**
   - Write code
   - Add tests if applicable
   - Update documentation
   - Run linting and tests

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add amazing new feature"
   ```

## Development Process

### Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code changes that neither fix bugs nor add features
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: add chapter on async web scraping
fix: correct Python code example in chapter 3
docs: update README with new setup instructions
```

### Pull Request Process

1. **Update Documentation** - Ensure README and relevant docs are updated
2. **Add Tests** - Include tests for new functionality
3. **Pass All Checks** - Ensure linting and tests pass
4. **Request Review** - Tag relevant maintainers
5. **Address Feedback** - Make requested changes promptly

### Code Review Guidelines

When reviewing PRs:
- Be constructive and friendly
- Suggest improvements, don't demand them
- Praise good solutions
- Ask questions if something is unclear
- Test the changes locally when possible

## Style Guidelines

### Python Code Style

```python
# Good example with clear naming and documentation
def scrape_website(url: str, timeout: int = 30) -> dict:
    """
    Scrape a website and return parsed data.
    
    Args:
        url: The URL to scrape
        timeout: Request timeout in seconds
        
    Returns:
        Dictionary containing scraped data
        
    Raises:
        RequestException: If the request fails
    """
    # Implementation here
```

### Markdown Style

- Use descriptive headings
- Include code examples
- Add humor where appropriate (but keep it professional)
- Break up long sections with subheadings
- Use emoji sparingly but effectively 🎯

### Educational Writing Style

- Start with simple concepts
- Build complexity gradually
- Use analogies and real-world examples
- Include "Think of it like..." explanations
- Add exercises to reinforce learning

## Testing

### Running Tests

```bash
# Python tests
pytest course/tests/

# With coverage
pytest course/tests/ --cov=course

# Specific test
pytest course/tests/test_scraping.py::test_basic_scrape
```

### Writing Tests

```python
def test_scraper_handles_timeout():
    """Test that scraper properly handles timeouts."""
    scraper = WebScraper(timeout=0.001)
    
    with pytest.raises(TimeoutError):
        scraper.scrape("https://httpbin.org/delay/10")
```

## Documentation

### Course Content Structure

```
course/
├── chapters/           # Main educational content
├── exercises/          # Hands-on practice
├── demos/             # Live coding examples
└── resources/         # Additional materials
```

### Adding New Content

1. Choose appropriate location
2. Follow existing naming conventions
3. Include in table of contents
4. Cross-reference related content
5. Add to course README

## Community

### Getting Help

- 💬 **Discussions** - Ask questions in GitHub Discussions
- 🐛 **Issues** - Report bugs or suggest features
- 💡 **Ideas** - Share ideas for new content
- 📚 **Resources** - Share helpful learning resources

### Communication Channels

- Be respectful and patient
- Help others when you can
- Share your learning journey
- Celebrate others' contributions

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- Special contributors page (coming soon)

## Questions?

If you have questions about contributing, feel free to:
1. Open a discussion
2. Contact the maintainers
3. Join our community chat (coming soon)

---

Thank you for helping make this course better! Every contribution, no matter how small, is valued and appreciated. 🙏

Happy Learning and Contributing! 🚀