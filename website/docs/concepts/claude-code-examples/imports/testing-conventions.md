# Testing Conventions

## Test Structure
- Arrange: Set up test data and dependencies
- Act: Execute the code under test
- Assert: Verify the results

## Test Naming
- Descriptive test names that explain what and why
- Format: `test_<function>_<scenario>_<expected_result>`
- Examples:
  - `test_parse_url_with_invalid_protocol_raises_error`
  - `TestCalculateTotal_WithDiscount_ReturnsCorrectAmount`

## Test Organization
```
project/
├── src/
│   └── module.py
└── tests/
    ├── unit/
    │   └── test_module.py
    ├── integration/
    │   └── test_api.py
    └── e2e/
        └── test_workflow.py
```

## Coverage Requirements
- Minimum 80% line coverage
- 100% coverage for critical paths
- Focus on behavior coverage, not just lines

## Mocking Guidelines
- Mock external dependencies
- Don't mock what you don't own
- Prefer dependency injection
- Use factories for test data

## Test Best Practices
- One assertion per test (when practical)
- Tests should be independent
- Use fixtures for common setup
- Keep tests fast and deterministic
- Test edge cases and error paths

## Language-Specific Tools

### Python
- pytest for test runner
- pytest-cov for coverage
- pytest-mock for mocking
- factory_boy for test data

### TypeScript
- Jest or Vitest
- Testing Library for UI
- MSW for API mocking
- Faker for test data

### Go
- Built-in testing package
- testify for assertions
- gomock for mocking
- go-cmp for comparisons