# Code Style Guide

## Formatting
- Use automated formatters for consistency (black, gofmt, prettier)
- Maximum line length: 100 characters
- Consistent indentation (language-specific)

## Naming Conventions
- **Variables**: descriptive_snake_case (Python), camelCase (JS/TS), camelCase (Go)
- **Functions**: verb_noun pattern (e.g., get_user, calculateTotal)
- **Classes**: PascalCase across all languages
- **Constants**: UPPER_SNAKE_CASE
- **Files**: snake_case.py, kebab-case.ts, snake_case.go

## Comments
- Write self-documenting code that needs minimal comments
- Comments explain "why", not "what"
- Update comments when code changes
- Use docstrings/JSDoc for public APIs

## Error Handling
- Always handle errors explicitly
- Provide context in error messages
- Use custom error types for domain errors
- Log errors with appropriate severity levels