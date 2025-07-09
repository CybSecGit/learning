# Module 1: Go Fundamentals for Terminal Wizardry
## *"Because you can't paint the Sistine Chapel without knowing how to hold a brush"*

> **Duration**: 1 week of Go enlightenment
> 
> **Goal**: Master Go patterns essential for building responsive, concurrent TUI applications
> 
> **Philosophy**: Learn Go the way TUI developers need it - focused on channels, goroutines, and terminal I/O

---

## Learning Objectives

By the end of this module, you'll:
- **Understand Go's concurrency model** deeply enough to build non-blocking UIs
- **Master channels and goroutines** for handling user input while updating displays
- **Work with terminal I/O** at a low level (before Charm makes it easy)
- **Handle errors gracefully** without making users see panic messages
- **Structure Go projects** properly for maintainable TUI applications

---

## Day 1-2: Go Concurrency for TUI Developers
*"Because blocking the UI thread is a crime against humanity"*

### Morning: Goroutines and Channels Deep Dive

```go
// The TUI developer's bread and butter
package main

import (
    "fmt"
    "time"
)

// Simulating a TUI update loop
func main() {
    // Channel for user input
    input := make(chan string)
    // Channel for data updates
    updates := make(chan string)
    // Channel for quit signal
    quit := make(chan bool)

    // Simulate user input
    go func() {
        inputs := []string{"up", "down", "enter", "q"}
        for _, in := range inputs {
            time.Sleep(500 * time.Millisecond)
            input <- in
        }
    }()

    // Simulate data updates (like API calls)
    go func() {
        ticker := time.NewTicker(1 * time.Second)
        defer ticker.Stop()
        count := 0
        for {
            select {
            case <-ticker.C:
                updates <- fmt.Sprintf("Update #%d", count)
                count++
            case <-quit:
                return
            }
        }
    }()

    // Main event loop (what Bubble Tea will handle for us later)
    for {
        select {
        case in := <-input:
            fmt.Printf("User pressed: %s\n", in)
            if in == "q" {
                quit <- true
                return
            }
        case update := <-updates:
            fmt.Printf("Data update: %s\n", update)
        }
    }
}
```

### Afternoon: Advanced Channel Patterns

**Exercise 1: Build a Non-Blocking Progress Bar**
```go
// Your task: Create a progress bar that updates smoothly
// while processing a long-running task
// Hint: Use buffered channels and select with default
```

**Exercise 2: Implement a Rate Limiter**
```go
// Build a rate limiter for API calls in your TUI
// This prevents overwhelming external services
// while keeping the UI responsive
```

### Key Concepts to Master:
- **Channel directions** (`chan<-` vs `<-chan`)
- **Buffered vs unbuffered channels**
- **Select with default case** (non-blocking operations)
- **Context for cancellation** (crucial for cleanup)

---

## Day 3-4: Terminal I/O and ANSI Escape Sequences
*"Understanding the dark arts before Charm abstracts them away"*

### Morning: Raw Terminal Manipulation

```go
package main

import (
    "fmt"
    "os"
    "os/exec"
    "runtime"
)

// ANSI escape sequences - the building blocks of TUIs
const (
    Clear       = "\033[2J"
    MoveCursor  = "\033[%d;%dH"
    HideCursor  = "\033[?25l"
    ShowCursor  = "\033[?25h"
    
    // Colors
    Red         = "\033[31m"
    Green       = "\033[32m"
    Yellow      = "\033[33m"
    Blue        = "\033[34m"
    Reset       = "\033[0m"
)

// Clear screen cross-platform
func clearScreen() {
    switch runtime.GOOS {
    case "linux", "darwin":
        fmt.Print(Clear)
        fmt.Printf(MoveCursor, 0, 0)
    case "windows":
        cmd := exec.Command("cmd", "/c", "cls")
        cmd.Stdout = os.Stdout
        cmd.Run()
    }
}

// Your first "TUI" without any framework
func main() {
    fmt.Print(HideCursor)
    defer fmt.Print(ShowCursor)
    
    clearScreen()
    
    // Draw a simple box
    fmt.Println("┌────────────────────┐")
    fmt.Println("│ Hello, TUI World!  │")
    fmt.Println("└────────────────────┘")
    
    // Move cursor and add color
    fmt.Printf(MoveCursor, 5, 1)
    fmt.Printf("%sThis is red text%s\n", Red, Reset)
}
```

### Afternoon: Handling Terminal Input

**Exercise 3: Build a Key Logger**
```go
// Create a program that:
// 1. Puts terminal in raw mode
// 2. Captures individual keystrokes
// 3. Displays them with proper formatting
// 4. Handles special keys (arrows, escape, etc.)
```

**Exercise 4: Terminal Size Detection**
```go
// Build a utility that:
// 1. Detects terminal dimensions
// 2. Watches for resize events
// 3. Redraws content appropriately
// This is crucial for responsive TUIs
```

---

## Day 5-6: Error Handling and Project Structure
*"Because panic() in a TUI is just embarrassing"*

### Morning: Error Handling Patterns

```go
// TUI-appropriate error handling
type UIError struct {
    Op      string    // Operation that failed
    Kind    ErrorKind // Category of error
    Err     error     // Underlying error
    Message string    // User-friendly message
}

type ErrorKind int

const (
    ErrorInput ErrorKind = iota
    ErrorNetwork
    ErrorFile
    ErrorInternal
)

// Implement error interface
func (e *UIError) Error() string {
    if e.Message != "" {
        return e.Message
    }
    return fmt.Sprintf("%s: %v", e.Op, e.Err)
}

// Graceful error handling in TUI context
func (e *UIError) Display() string {
    switch e.Kind {
    case ErrorNetwork:
        return "📡 Network hiccup. Retrying..."
    case ErrorFile:
        return "📁 File access issue. Check permissions?"
    default:
        return "😅 Oops! Something went wrong."
    }
}
```

### Afternoon: Project Structure for TUI Apps

```
my-tui-app/
├── cmd/
│   └── app/
│       └── main.go         # Entry point
├── internal/
│   ├── ui/
│   │   ├── components/     # Reusable UI components
│   │   ├── styles/         # Style definitions
│   │   └── views/          # Different screens/views
│   ├── config/             # Configuration handling
│   ├── data/               # Data models and storage
│   └── events/             # Event handling
├── pkg/
│   └── utils/              # Exported utilities
├── go.mod
├── go.sum
└── README.md
```

**Exercise 5: Build a Project Template**
```go
// Create a reusable TUI project template with:
// 1. Proper module structure
// 2. Configuration loading
// 3. Logging that doesn't interfere with TUI
// 4. Graceful shutdown handling
```

---

## Day 7: Putting It All Together
*"Your first real TUI - no frameworks allowed!"*

### Final Project: Terminal Task Manager

Build a simple task manager using only Go stdlib:

**Requirements:**
1. Display a list of tasks
2. Navigate with arrow keys
3. Add new tasks with 'a'
4. Mark tasks complete with 'space'
5. Delete tasks with 'd'
6. Save state to a file
7. Handle terminal resize
8. Graceful error handling

**Bonus Points:**
- Add task priorities with colors
- Implement search/filter
- Add due dates
- Create task categories

```go
// Skeleton to get you started
type Task struct {
    ID        string
    Title     string
    Completed bool
    Priority  int
}

type TaskManager struct {
    tasks    []Task
    selected int
    mode     Mode
}

type Mode int

const (
    ModeNormal Mode = iota
    ModeInsert
    ModeSearch
)

// Your implementation here...
```

---

## Weekend Challenge: Performance Profiling
*"Because smooth TUIs are happy TUIs"*

### Profile Your Task Manager

1. **CPU Profiling**: Find bottlenecks in your render loop
2. **Memory Profiling**: Detect leaks in long-running TUIs
3. **Goroutine Analysis**: Ensure no routine leaks

```bash
# Add profiling to your app
go run -cpuprofile=cpu.prof main.go
go tool pprof cpu.prof

# Memory profiling
go run -memprofile=mem.prof main.go
go tool pprof mem.prof
```

---

## Module 1 Checklist

### Must Complete:
- [ ] All 5 exercises with working code
- [ ] Final project (Terminal Task Manager)
- [ ] Understand goroutines & channels deeply
- [ ] Can manipulate terminal without frameworks
- [ ] Error handling without panics

### Nice to Have:
- [ ] Weekend performance profiling
- [ ] Cross-platform compatibility
- [ ] Unit tests for core logic
- [ ] README with GIF demo

---

## Common Pitfalls & Solutions

### Pitfall 1: Blocking the Main Loop
```go
// BAD: This freezes your TUI
data := slowAPICall() // Blocks everything

// GOOD: Non-blocking with goroutine
go func() {
    data := slowAPICall()
    dataChan <- data
}()
```

### Pitfall 2: Terminal State Corruption
```go
// ALWAYS restore terminal state
oldState, _ := term.MakeRaw(int(os.Stdin.Fd()))
defer term.Restore(int(os.Stdin.Fd()), oldState)
```

### Pitfall 3: Resource Leaks
```go
// Close your channels!
ch := make(chan string)
defer close(ch)

// Cancel your contexts!
ctx, cancel := context.WithCancel(context.Background())
defer cancel()
```

---

## Resources & References

### Essential Reading
- [The Go Programming Language](https://www.gopl.io/) - Chapters 8 & 9
- [Concurrency in Go](https://www.oreilly.com/library/view/concurrency-in-go/9781491941294/) - For deep concurrency knowledge
- [ANSI Escape Sequences](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797) - Your TUI color palette

### Useful Packages (for reference)
- `golang.org/x/term` - Terminal handling
- `github.com/mattn/go-isatty` - Terminal detection
- `github.com/mgutz/ansi` - ANSI color codes

---

## Next Steps

Congratulations! You now understand Go well enough to appreciate what Charm libraries do for you. In Module 2, we'll introduce Bubble Tea and see how it elegantly solves all the problems you just faced.

**Before moving on:**
1. Complete the task manager project
2. Try adding one "impossible" feature (like mouse support)
3. Appreciate how much work Bubble Tea will save you

[Continue to Module 2: Introduction to the Charm Universe →](/learning-plans/go-tui-charm/module-2)

---

*"Remember: Every beautiful TUI started with someone printing escape sequences and immediately regretting it." - Ancient Terminal Wisdom*