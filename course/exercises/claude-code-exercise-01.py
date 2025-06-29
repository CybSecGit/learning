#!/usr/bin/env python3
"""
Claude Code Exercise 01: Building an Effective CLAUDE.md
=========================================================

Learning Objectives:
- Understand CLAUDE.md structure and best practices
- Practice writing clear, concise instructions
- Learn to use imports and modular configuration
- Master context management for Claude Code

Exercise Description:
You're starting a new Python web API project. Create a comprehensive CLAUDE.md
file that will help Claude Code understand your project requirements and 
maintain consistency across development sessions.

Requirements:
1. Project uses FastAPI for the web framework
2. PostgreSQL for database with SQLAlchemy ORM
3. Follow PEP 8 style guide with Black formatting
4. Minimum 90% test coverage required
5. API versioning strategy needed
6. Security-first approach
7. Comprehensive logging

Your Task:
Complete the CLAUDE.md template below with appropriate instructions.
"""

CLAUDE_MD_TEMPLATE = """# Project: {project_name}

## Project Overview
{project_description}

## Technology Stack
- Framework: {framework}
- Database: {database}
- ORM: {orm}
- Testing: {testing_framework}

## Development Principles
{development_principles}

## Code Style
{code_style_rules}

## Testing Requirements
{testing_requirements}

## Security Guidelines
{security_guidelines}

## API Design
{api_design_rules}

## Database Conventions
{database_conventions}

## Logging Standards
{logging_standards}

## Common Commands
{common_commands}

## Git Workflow
{git_workflow}

## Import Additional Configurations
{imports}
"""

def create_claude_md(config: dict) -> str:
    """
    Create a CLAUDE.md file from configuration.
    
    Args:
        config: Dictionary containing all configuration values
        
    Returns:
        Formatted CLAUDE.md content
    """
    # TODO: Implement this function
    # Hint: Use string formatting to fill in the template
    pass

def validate_claude_md(content: str) -> list:
    """
    Validate CLAUDE.md content for common issues.
    
    Args:
        content: CLAUDE.md file content
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Check for required sections
    required_sections = [
        "## Project Overview",
        "## Technology Stack", 
        "## Development Principles",
        "## Code Style",
        "## Testing Requirements",
        "## Security Guidelines"
    ]
    
    for section in required_sections:
        if section not in content:
            errors.append(f"Missing required section: {section}")
    
    # Check for placeholder values
    if "{" in content or "}" in content:
        errors.append("Found unformatted placeholders")
    
    # Check minimum length
    if len(content) < 500:
        errors.append("CLAUDE.md seems too short - add more detail")
    
    # Check for import statements
    if "@" not in content and "import" not in content.lower():
        errors.append("Consider using imports for modular configuration")
    
    return errors

def main():
    """Main exercise function."""
    print("Claude Code Exercise 01: Building an Effective CLAUDE.md")
    print("=" * 50)
    
    # Your configuration
    my_config = {
        "project_name": "FastAPI Todo API",
        "project_description": "A REST API for managing todo items with user authentication",
        "framework": "FastAPI",
        "database": "PostgreSQL",
        "orm": "SQLAlchemy",
        "testing_framework": "pytest",
        "development_principles": """
- Test-driven development (TDD) for all features
- Security is job zero - validate all inputs
- Keep functions small and focused
- Document all public APIs
- Use type hints everywhere
""",
        "code_style_rules": """
- Follow PEP 8 with Black formatting
- Maximum line length: 88 characters
- Use descriptive variable names
- Sort imports with isort
""",
        "testing_requirements": """
- Minimum 90% code coverage
- Write tests before implementation
- Use pytest fixtures for common setups
- Mock all external dependencies
- Test both success and error cases
""",
        "security_guidelines": """
- Never store passwords in plain text
- Use parameterized queries only
- Validate all user inputs
- Implement rate limiting on all endpoints
- Use JWT tokens for authentication
- Log security events
""",
        "api_design_rules": """
- Use API versioning (v1, v2, etc.)
- Follow RESTful conventions
- Return consistent error responses
- Use proper HTTP status codes
- Implement pagination for lists
- Document with OpenAPI/Swagger
""",
        "database_conventions": """
- Use migrations for schema changes
- Name tables in plural (users, todos)
- Add created_at, updated_at to all tables
- Use UUID for primary keys
- Index foreign keys
""",
        "logging_standards": """
- Use structured logging (JSON)
- Log all API requests/responses
- Include correlation IDs
- Different log levels per environment
- Never log sensitive data
""",
        "common_commands": """
- `make dev` - Start development server
- `make test` - Run all tests
- `make migrate` - Run database migrations
- `make lint` - Check code style
- `make coverage` - Generate coverage report
""",
        "git_workflow": """
- Branch naming: feature/*, bugfix/*, hotfix/*
- Commit style: conventional commits
- Require PR reviews before merge
- Squash commits on merge
- Tag releases with semver
""",
        "imports": """
@config/database.md
@config/security.md
@standards/api-design.md
@standards/testing.md
"""
    }
    
    # Exercise tasks
    print("\nTask 1: Implement create_claude_md function")
    print("Task 2: Create your CLAUDE.md file")
    print("Task 3: Validate your configuration")
    print("Task 4: Add custom sections for your specific needs")
    
    # Test your implementation
    try:
        claude_md = create_claude_md(my_config)
        
        if claude_md:
            print("\nGenerated CLAUDE.md:")
            print("-" * 50)
            print(claude_md[:500] + "..." if len(claude_md) > 500 else claude_md)
            
            # Validate
            errors = validate_claude_md(claude_md)
            if errors:
                print("\nValidation Errors:")
                for error in errors:
                    print(f"- {error}")
            else:
                print("\n✅ CLAUDE.md is valid!")
                
            # Save to file
            with open("CLAUDE.md", "w") as f:
                f.write(claude_md)
            print("\n📝 Saved to CLAUDE.md")
            
    except NotImplementedError:
        print("\n⚠️  Please implement create_claude_md function")

    # Additional challenges
    print("\nAdditional Challenges:")
    print("1. Add environment-specific sections (dev, staging, prod)")
    print("2. Create modular imports for different aspects")
    print("3. Add team-specific conventions")
    print("4. Include troubleshooting section")
    print("5. Add performance optimization guidelines")

if __name__ == "__main__":
    main()

"""
Solution Hints:
1. Use string.format() or f-strings to fill the template
2. Consider using textwrap.dedent() for clean multiline strings
3. Add conditional sections based on project type
4. Think about what Claude Code needs to know for consistency
5. Keep instructions action-oriented and specific

Expected Output:
A complete CLAUDE.md file that:
- Provides clear project context
- Defines all development standards
- Includes practical commands
- Uses imports for modularity
- Passes all validation checks
"""