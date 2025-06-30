# Error Handling Standards

## General Principles
- Fail fast and fail clearly
- Provide actionable error messages
- Include context for debugging
- Never suppress errors silently

## Language-Specific Patterns

### Python
```python
# Custom error types
class ValidationError(Exception):
    """Raised when input validation fails"""
    pass

# Context managers for cleanup
with open(file_path) as f:
    # File automatically closed on error

# Explicit error handling
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
    raise ProcessingError(f"Could not process {item_id}") from e
```

### TypeScript
```typescript
// Result types for explicit error handling
type Result<T, E = Error> = 
  | { ok: true; value: T }
  | { ok: false; error: E };

// Custom error classes
class ValidationError extends Error {
  constructor(message: string, public field: string) {
    super(message);
    this.name = 'ValidationError';
  }
}
```

### Go
```go
// Always check errors
result, err := doSomething()
if err != nil {
    return fmt.Errorf("failed to do something: %w", err)
}

// Custom error types
type ValidationError struct {
    Field   string
    Message string
}

func (e ValidationError) Error() string {
    return fmt.Sprintf("validation failed for %s: %s", e.Field, e.Message)
}
```

## Error Recovery
- Use circuit breakers for external services
- Implement retry logic with exponential backoff
- Graceful degradation over complete failure
- Always have a fallback plan