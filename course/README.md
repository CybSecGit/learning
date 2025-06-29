# Development Skills Laboratory: From Zero to Hero (via Epic Failures)

*A hands-on journey through modern software development, where we learn more from our mistakes than our successes*

## Course Philosophy: Failure-Driven Development

This course embraces the reality that the best way to learn software development is to encounter every possible error, debug each one methodically, and understand *why* each solution works. We'll start with broken code and work our way to robust, production-ready applications.

**Learning Approach:**
- 🚨 Start with code that fails (intentionally)
- 🔍 Debug step-by-step with real tools
- 💡 Understand the "why" behind each fix
- 🎯 Build increasingly robust solutions
- 🛡️ Develop defensive programming habits

## Course Structure

### Chapter 0: Environment Setup
- [Containerization](chapters/00-containerization.md) - Docker fundamentals for consistent development
- [Docker Quick Start](resources/docker-quick-start.md) - Get up and running fast

### Chapter 1: Foundation
- [Project Setup](chapters/01-setup.md) - Development environment and tooling
- [Preview](chapters/02-preview.md) - What we're building and why

### Chapter 2: Core Concepts
- [Web Scraping Techniques](chapters/02-web-scraping.md) - HTTP automation and data extraction
- [User Agents and Stealth](chapters/05-user-agents-and-stealth.md) - Avoiding detection

### Chapter 3: Development Methodology
- [Failure-Driven Development](chapters/03-failure-driven-development.md) - Learning through debugging
- [Testing Like You Mean It](chapters/04-testing-like-you-mean-it.md) - Comprehensive testing strategies

### Chapter 6: AI-Powered Development
- [Mastering Claude Code](chapters/06-mastering-claude-code.md) - Advanced techniques for AI pair programming

## Hands-On Learning

### Debugging Journey
- [Real Debugging Stories](debugging-journey.md) - War stories from the trenches

### Practical Exercises
- [Exercise 1: Basic HTTP Automation](exercises/debugging-exercise-01.py) - Your first automated client (and first failures)
- More exercises coming as we build...

### Demo Scripts
- [Testing Workshop](demos/testing_workshop.py) - Interactive testing demonstration

## Security & Ethics
- [Security Considerations](resources/security-note.md) - Responsible automation practices

## Prerequisites

**Required:**
- Basic Python knowledge (functions, classes, imports)
- Command line comfort (running scripts, virtual environments)
- Curiosity about how things break (and patience to fix them)

**Helpful but not required:**
- HTML/CSS basics
- HTTP request/response understanding
- Previous debugging experience

## Learning Outcomes

By the end of this course, you'll be able to:

1. **Build Robust Scrapers**
   - Use modern async libraries (`rnet`, `selectolax`)
   - Implement proper error handling and retries
   - Handle both static and dynamic content

2. **Debug Like a Pro**
   - Systematically diagnose scraping failures
   - Use browser dev tools effectively
   - Understand common anti-scraping measures

3. **Test Comprehensively**
   - Write unit tests for scraping logic
   - Create integration tests with real websites
   - Mock external dependencies effectively

4. **Scrape Ethically**
   - Respect robots.txt and rate limits
   - Use appropriate user agents
   - Implement proper caching strategies

5. **Master AI-Powered Development**
   - Use Claude Code effectively for pair programming
   - Implement test-driven development with AI assistance
   - Leverage AI for code review and documentation
   - Build complex systems through AI-human collaboration

## Course Navigation

- **Linear Path**: Follow chapters 0→1→2→3 for structured learning
- **Problem-First**: Start with [exercises/](exercises/) and refer to chapters as needed
- **Debug-Heavy**: Begin with [debugging-journey.md](debugging-journey.md) for real-world scenarios

## Support Resources

This course is part of the larger [Changelogger project](../README.md), which provides:
- Working examples in `../examples/`
- Comprehensive test suite in `../tests/`
- Production-ready code in `../src/`

---

*"The expert has failed more times than the beginner has even tried. Let's fail faster so we can succeed sooner."*
