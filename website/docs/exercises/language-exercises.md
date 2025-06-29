# Language-Specific Exercises

Practice your polyglot skills with these language-specific exercises designed to help you transition between Python, Go, and TypeScript/Deno.

## Go Exercises

### Exercise 1: From Python to Go - Web Scraper
**File:** `course/exercises/go-exercise-01.go`

Convert a Python web scraper to idiomatic Go code, learning Go's approach to:
- Struct-based design (vs classes)
- Explicit error handling (vs exceptions)
- Goroutines and channels
- Type safety

**To Run:**
```bash
go run course/exercises/go-exercise-01.go
```

**Key Concepts:**
- No classes - use structs and methods
- No `__init__` - use `NewXXX` constructor functions
- No exceptions - return errors explicitly
- No sets - use `map[string]bool`

## TypeScript/Deno Exercises

### Exercise 1: Type-Safe Web Scraper
**File:** `course/exercises/typescript-deno-exercise-01.ts`

Build a type-safe web scraper using TypeScript and Deno, focusing on:
- TypeScript's type system
- Deno's built-in APIs
- Type-safe error handling
- Async/await patterns

**To Run:**
```bash
deno run --allow-net --allow-read --allow-write course/exercises/typescript-deno-exercise-01.ts
```

**Key Concepts:**
- Interface definitions for type safety
- Generic types for reusable code
- Type guards for runtime validation
- Result types for error handling

## Learning Path

### For Python Developers

1. **Start with TypeScript** - Familiar async/await patterns
2. **Move to Go** - Learn explicit error handling
3. **Compare approaches** - See how each language handles common patterns

### Common Patterns Across Languages

| Pattern | Python | Go | TypeScript |
|---------|--------|-----|------------|
| Error Handling | `try/except` | `if err != nil` | Result types |
| Async Code | `async/await` | Goroutines | `async/await` |
| Type Safety | Type hints (optional) | Static types | Static types |
| Package Management | pip | go modules | deno/npm |

## Tips for Success

1. **Don't try to write Python in Go** - Embrace each language's idioms
2. **Focus on error handling differences** - This is where languages diverge most
3. **Use the type system** - Both Go and TypeScript catch bugs at compile time
4. **Read the standard library** - Great examples of idiomatic code

## Additional Resources

- See `learning_concepts_golang.md` for Go patterns
- See `learning_concepts_typescript_deno.md` for TypeScript/Deno patterns
- Join language-specific communities for help

Happy polyglot programming! 🌍