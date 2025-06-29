# Go Project CLAUDE.md

## Project Overview
This is a Go microservice following clean architecture principles. We use the standard library where possible, with minimal external dependencies. The service implements RESTful APIs with a focus on performance, simplicity, and reliability.

## Core Development Principles

### Go Philosophy
- Simplicity over cleverness
- Explicit over implicit
- Composition over inheritance
- Errors are values, handle them explicitly
- Concurrent by design

### Code Standards
- Go 1.21+ for latest features
- Follow standard Go formatting (gofmt)
- Effective Go guidelines strictly followed
- Meaningful variable names, avoid abbreviations
- Package names are singular, lowercase

## Project Structure
```
project/
├── cmd/
│   └── api/           # Application entrypoints
│       └── main.go
├── internal/          # Private application code
│   ├── config/        # Configuration management
│   ├── handler/       # HTTP handlers
│   ├── service/       # Business logic
│   ├── repository/    # Data access layer
│   ├── middleware/    # HTTP middleware
│   └── model/         # Domain models
├── pkg/              # Public packages
│   ├── logger/       # Structured logging
│   └── errors/       # Error handling utilities
├── migrations/       # Database migrations
├── scripts/         # Build and deployment scripts
├── api/            # API specifications (OpenAPI)
└── test/           # Integration tests
```

## Error Handling
```go
// Always wrap errors with context
if err != nil {
    return fmt.Errorf("failed to fetch user %d: %w", userID, err)
}

// Custom error types for domain errors
type ValidationError struct {
    Field   string
    Message string
}

func (e ValidationError) Error() string {
    return fmt.Sprintf("validation error on field %s: %s", e.Field, e.Message)
}

// Error checking pattern
user, err := repo.GetUser(ctx, id)
if err != nil {
    if errors.Is(err, ErrNotFound) {
        return nil, ErrUserNotFound
    }
    return nil, fmt.Errorf("get user: %w", err)
}
```

## Concurrency Patterns
```go
// Use context for cancellation
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

// Goroutine error handling with errgroup
g, ctx := errgroup.WithContext(ctx)
g.Go(func() error {
    return processItem(ctx, item)
})

// Channel patterns
results := make(chan Result, bufferSize)
defer close(results)

// Worker pool pattern
for i := 0; i < numWorkers; i++ {
    go worker(ctx, jobs, results)
}
```

## Database Access
```go
// Use database/sql with prepared statements
const getUserQuery = `
    SELECT id, email, created_at
    FROM users
    WHERE id = $1
`

// Transaction handling
tx, err := db.BeginTx(ctx, nil)
if err != nil {
    return fmt.Errorf("begin transaction: %w", err)
}
defer tx.Rollback() // Safe to call after commit

// Execute operations
if err := doOperation(tx); err != nil {
    return fmt.Errorf("operation failed: %w", err)
}

return tx.Commit()
```

## HTTP Server Setup
```go
// Graceful shutdown
srv := &http.Server{
    Addr:         ":8080",
    Handler:      router,
    ReadTimeout:  5 * time.Second,
    WriteTimeout: 10 * time.Second,
    IdleTimeout:  120 * time.Second,
}

// Shutdown handling
quit := make(chan os.Signal, 1)
signal.Notify(quit, os.Interrupt, syscall.SIGTERM)

go func() {
    <-quit
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()
    
    if err := srv.Shutdown(ctx); err != nil {
        log.Fatal("Server forced to shutdown:", err)
    }
}()
```

## Testing Standards

### Unit Tests
```go
// Table-driven tests
func TestCalculatePrice(t *testing.T) {
    tests := []struct {
        name     string
        input    PriceInput
        expected float64
        wantErr  bool
    }{
        {
            name:     "with discount",
            input:    PriceInput{Amount: 100, Discount: 0.1},
            expected: 90,
            wantErr:  false,
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := CalculatePrice(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("unexpected error: %v", err)
            }
            if got != tt.expected {
                t.Errorf("got %v, want %v", got, tt.expected)
            }
        })
    }
}
```

### Integration Tests
- Use testcontainers for database tests
- Real HTTP requests for API tests
- Separate test database
- Clean up test data after each test

## Performance Guidelines
- Profile before optimizing
- Minimize allocations in hot paths
- Use sync.Pool for temporary objects
- Buffer channels appropriately
- Prefer streaming over loading all data

## Security Practices
```go
// Input validation
func validateEmail(email string) error {
    if email == "" {
        return ValidationError{Field: "email", Message: "required"}
    }
    if !emailRegex.MatchString(email) {
        return ValidationError{Field: "email", Message: "invalid format"}
    }
    return nil
}

// SQL injection prevention
query := `SELECT * FROM users WHERE id = $1`
row := db.QueryRow(query, userID) // Parameterized query

// Environment configuration
type Config struct {
    DatabaseURL string `env:"DATABASE_URL,required"`
    APIKey      string `env:"API_KEY,required"`
    LogLevel    string `env:"LOG_LEVEL" envDefault:"info"`
}
```

## Logging and Monitoring
```go
// Structured logging with slog
logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))

// Log with context
logger.InfoContext(ctx, "user action",
    slog.String("user_id", userID),
    slog.String("action", "login"),
    slog.Duration("duration", time.Since(start)),
)

// Metrics with OpenTelemetry
meter := otel.Meter("api")
requestCounter, _ := meter.Int64Counter("http_requests_total")
requestCounter.Add(ctx, 1, attribute.String("method", r.Method))
```

## Build and Deployment

### Makefile Commands
```makefile
.PHONY: build test lint

build:
	go build -o bin/api cmd/api/main.go

test:
	go test -race -cover ./...

lint:
	golangci-lint run

docker:
	docker build -t myservice:latest .
```

### Docker Best Practices
```dockerfile
# Multi-stage build
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o api cmd/api/main.go

FROM alpine:latest
RUN apk --no-cache add ca-certificates
COPY --from=builder /app/api /api
ENTRYPOINT ["/api"]
```

## Development Workflow

### Local Development
```bash
# Run with hot reload
air

# Run tests with coverage
go test -race -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# Lint and format
golangci-lint run
gofmt -w .

# Dependency management
go mod tidy
go mod verify
```

### Pre-commit Checklist
- [ ] All tests pass
- [ ] No race conditions detected
- [ ] golangci-lint passes
- [ ] No unused dependencies
- [ ] Documentation updated

## Performance Benchmarks
- HTTP response time < 50ms (p99)
- Memory usage < 100MB
- Startup time < 2 seconds
- Graceful shutdown < 30 seconds

## Common Patterns

### Repository Pattern
```go
type UserRepository interface {
    GetByID(ctx context.Context, id string) (*User, error)
    Create(ctx context.Context, user *User) error
    Update(ctx context.Context, user *User) error
    Delete(ctx context.Context, id string) error
}
```

### Service Layer
```go
type UserService struct {
    repo   UserRepository
    logger *slog.Logger
}

func (s *UserService) CreateUser(ctx context.Context, req CreateUserRequest) (*User, error) {
    // Business logic here
}
```

## Import External Standards
@../imports/error-handling.md
@../imports/testing-conventions.md
@../imports/security-guidelines.md
@../imports/git-workflow.md