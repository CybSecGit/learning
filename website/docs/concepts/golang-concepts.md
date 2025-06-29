# Go Learning Concepts

A comprehensive guide to Go programming for Python developers, using simple explanations and practical examples.

## About This Guide

The full Go concepts guide is available at: [`learning_concepts_golang.md`](https://github.com/YOUR_USERNAME/learning/blob/main/learning_concepts_golang.md)

This guide helps Python developers transition to Go by:
- Comparing Python and Go approaches
- Explaining Go's unique features
- Providing practical examples
- Highlighting common gotchas

## Quick Go Reference

### Go vs Python At a Glance

| Python | Go |
|--------|-----|
| Interpreted | Compiled |
| Dynamic typing | Static typing |
| Exceptions | Explicit error returns |
| Classes | Structs and interfaces |
| List comprehensions | For loops (only one kind!) |
| `pip` packages | Go modules |

### Variables and Types

```go
// Variable declaration
var name string = "Alice"
var age int = 30

// Type inference
name := "Alice"  // := means declare and assign
age := 30

// Multiple variables
var (
    firstName = "Alice"
    lastName  = "Smith"
    active    = true
)

// Zero values (no uninitialized variables!)
var count int       // 0
var price float64   // 0.0
var message string  // ""
var done bool       // false
```

### Functions

```go
// Basic function
func add(a, b int) int {
    return a + b
}

// Multiple returns (very common!)
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// Usage
result, err := divide(10, 2)
if err != nil {
    log.Fatal(err)
}
fmt.Println(result)
```

### Structs (Go's "Classes")

```go
type User struct {
    Name  string
    Email string
    Age   int
}

// Methods are defined outside structs
func (u User) Greet() string {
    return fmt.Sprintf("Hello, I'm %s", u.Name)
}

// Constructor pattern
func NewUser(name, email string) *User {
    return &User{
        Name:  name,
        Email: email,
    }
}
```

### Error Handling

```go
// No try/except - check errors explicitly
file, err := os.Open("data.txt")
if err != nil {
    return fmt.Errorf("failed to open file: %w", err)
}
defer file.Close()  // Cleanup at function exit

// Custom errors
var ErrNotFound = errors.New("not found")

// Check specific errors
if err == ErrNotFound {
    // Handle not found case
}
```

### Goroutines and Channels

```go
// Start a goroutine (lightweight thread)
go doWork()

// Channels for communication
ch := make(chan string)

// Send
go func() {
    ch <- "Hello from goroutine!"
}()

// Receive
message := <-ch
fmt.Println(message)

// WaitGroup for synchronization
var wg sync.WaitGroup
for i := 0; i < 5; i++ {
    wg.Add(1)
    go func(id int) {
        defer wg.Done()
        fmt.Printf("Worker %d done\n", id)
    }(i)
}
wg.Wait()
```

### Interfaces

```go
// Define behavior, not data
type Writer interface {
    Write([]byte) (int, error)
}

// Any type that has Write method implements Writer
type ConsoleWriter struct{}

func (cw ConsoleWriter) Write(data []byte) (int, error) {
    fmt.Print(string(data))
    return len(data), nil
}

// Accept interfaces, return structs
func SaveData(w Writer, data []byte) error {
    _, err := w.Write(data)
    return err
}
```

## Key Differences for Python Developers

### 1. No Exceptions
```go
// Python: try/except
// Go: if err != nil
result, err := doSomething()
if err != nil {
    return err  // or handle it
}
```

### 2. Explicit is Better
```go
// No default parameters
// No method overloading
// No magic methods
// Everything is clear and obvious
```

### 3. Compilation Catches Errors
```go
// This won't compile:
var x int = "hello"  // Type mismatch caught at compile time
```

### 4. True Parallelism
```go
// No GIL! Goroutines run in parallel
// Thousands of goroutines are normal
```

## Common Patterns

### The Go Way™

1. **Accept interfaces, return structs**
2. **Keep interfaces small** (1-3 methods)
3. **Handle errors explicitly**
4. **Use channels for communication**
5. **Favor composition over inheritance**

### Quick Tips

- Capital letters = Public
- lowercase = private
- `defer` for cleanup
- `_` to ignore values
- No circular imports allowed

## Learning Path

1. **Tour of Go** - Official interactive tutorial
2. **Effective Go** - Best practices document
3. **Go by Example** - Practical code examples
4. **Build something** - A CLI tool or web server

For the complete guide with detailed explanations, see [learning_concepts_golang.md](https://github.com/YOUR_USERNAME/learning/blob/main/learning_concepts_golang.md).

Happy Go coding! 🐹