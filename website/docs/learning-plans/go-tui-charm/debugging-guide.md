# TUI Debugging & Troubleshooting Guide
## *"When your beautiful TUI turns into a beautiful disaster"*

> "Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it." - Brian Kernighan (who clearly never debugged a TUI)

---

## 🎯 The Golden Rules of TUI Debugging

1. **You can't `fmt.Println()` your way out of this** - It'll destroy your UI
2. **The terminal state is probably corrupted** - And it's probably your fault
3. **That panic is hiding behind a goroutine** - They always are
4. **It works on your machine** - But fails spectacularly on others
5. **Clear the screen** - When in doubt, start fresh

---

## 🚑 Emergency Triage

### Symptom: "My TUI is a garbled mess!"

**Immediate Action:**
```go
// Reset terminal to sane state
fmt.Print("\033[0m")     // Reset all attributes
fmt.Print("\033[2J")     // Clear screen
fmt.Print("\033[H")      // Move cursor home
fmt.Print("\033[?25h")   // Show cursor

// Or nuclear option:
os.Exit(1)  // Let the shell clean up
```

**Root Causes:**
- Forgot to restore terminal state
- Mixed `fmt.Println` with TUI rendering
- Race condition in render loop
- ANSI escape sequence typo

### Symptom: "My TUI freezes!"

**Debug Checklist:**
```go
// 1. Check for blocking operations
select {
case msg := <-msgChan:
    // Handle message
case <-time.After(5 * time.Second):
    log.Println("DEBUG: Operation timed out")
default:
    // Non-blocking fallback
}

// 2. Add goroutine dump on SIGUSR1
import "runtime/debug"

go func() {
    sigChan := make(chan os.Signal, 1)
    signal.Notify(sigChan, syscall.SIGUSR1)
    <-sigChan
    debug.PrintStack()
}()
```

### Symptom: "Works locally, breaks in production!"

**Terminal Capability Detection:**
```go
func detectTerminalCapabilities() {
    // Check if we're in a real terminal
    if !isatty.IsTerminal(os.Stdout.Fd()) {
        log.Fatal("Not running in a terminal")
    }
    
    // Check color support
    term := os.Getenv("TERM")
    colorterm := os.Getenv("COLORTERM")
    
    switch {
    case colorterm == "truecolor" || colorterm == "24bit":
        fmt.Println("True color support detected")
    case strings.Contains(term, "256"):
        fmt.Println("256 color support detected")
    case term == "dumb":
        fmt.Println("No color support")
    }
}
```

---

## 🔬 Advanced Debugging Techniques

### 1. The Debug Logger Pattern
*"Because fmt.Println is the enemy"*

```go
package debug

import (
    "fmt"
    "log"
    "os"
    "sync"
)

type DebugLogger struct {
    mu     sync.Mutex
    file   *os.File
    logger *log.Logger
}

var Debug *DebugLogger

func init() {
    if os.Getenv("TUI_DEBUG") != "" {
        file, err := os.Create("tui-debug.log")
        if err != nil {
            panic(err)
        }
        
        Debug = &DebugLogger{
            file:   file,
            logger: log.New(file, "[DEBUG] ", log.LstdFlags|log.Lshortfile),
        }
    }
}

func (d *DebugLogger) Printf(format string, args ...interface{}) {
    if d == nil {
        return
    }
    
    d.mu.Lock()
    defer d.mu.Unlock()
    
    d.logger.Printf(format, args...)
    d.file.Sync() // Force write
}

// Usage:
// TUI_DEBUG=1 go run main.go
// tail -f tui-debug.log  # In another terminal
```

### 2. The Time-Travel Debugger
*"Record everything, debug later"*

```go
type Event struct {
    Type      string
    Timestamp time.Time
    Data      interface{}
}

type Recorder struct {
    events []Event
    mu     sync.Mutex
}

func (r *Recorder) Record(eventType string, data interface{}) {
    r.mu.Lock()
    defer r.mu.Unlock()
    
    r.events = append(r.events, Event{
        Type:      eventType,
        Timestamp: time.Now(),
        Data:      data,
    })
}

func (r *Recorder) Dump() {
    r.mu.Lock()
    defer r.mu.Unlock()
    
    file, _ := os.Create("events.json")
    defer file.Close()
    
    encoder := json.NewEncoder(file)
    encoder.SetIndent("", "  ")
    encoder.Encode(r.events)
}

// On crash/exit:
defer recorder.Dump()
```

### 3. The Remote Debugger
*"SSH into your TUI's brain"*

```go
import "net/http"
import _ "net/http/pprof"

// Start debug server in goroutine
go func() {
    log.Println(http.ListenAndServe("localhost:6060", nil))
}()

// Now you can:
// go tool pprof http://localhost:6060/debug/pprof/goroutine
// go tool pprof http://localhost:6060/debug/pprof/heap
```

---

## 🐛 Common Bubble Tea Gotchas

### 1. The Init() Command That Never Runs

```go
// WRONG: Init returns nil
func (m model) Init() tea.Cmd {
    return nil  // Commands won't start!
}

// RIGHT: Return a command
func (m model) Init() tea.Cmd {
    return tea.Batch(
        textinput.Blink,
        m.spinner.Tick,
    )
}
```

### 2. The Update That Doesn't

```go
// WRONG: Forgetting to return the model
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    m.counter++  // This modifies a copy!
    return m, nil
}

// RIGHT: Work with pointer receiver
func (m *model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    m.counter++
    return m, nil
}
```

### 3. The Infinite Command Loop

```go
// WRONG: Command that triggers itself
func doSomething() tea.Msg {
    return doSomethingMsg{}
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg.(type) {
    case doSomethingMsg:
        return m, doSomething  // Infinite loop!
    }
}

// RIGHT: Add exit condition
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg.(type) {
    case doSomethingMsg:
        if m.shouldContinue {
            return m, doSomething
        }
        return m, nil
    }
}
```

---

## 🔍 Performance Profiling

### Finding Render Bottlenecks

```go
type TimedRenderer struct {
    render func() string
}

func (t TimedRenderer) View() string {
    start := time.Now()
    result := t.render()
    
    duration := time.Since(start)
    if duration > 16*time.Millisecond { // 60fps budget
        debug.Printf("SLOW RENDER: %v", duration)
    }
    
    return result
}
```

### Memory Leak Detection

```go
// Add to your main.go
import _ "net/http/pprof"

// Periodically check memory
go func() {
    var m runtime.MemStats
    for {
        runtime.ReadMemStats(&m)
        debug.Printf("Alloc = %v MB", m.Alloc / 1024 / 1024)
        time.Sleep(10 * time.Second)
    }
}()
```

---

## 🤔 Platform-Specific Issues

### Windows Terminal Woes

```go
// Enable ANSI on Windows
func enableWindowsANSI() error {
    stdout := windows.Handle(os.Stdout.Fd())
    var originalMode uint32
    
    windows.GetConsoleMode(stdout, &originalMode)
    windows.SetConsoleMode(stdout, originalMode|windows.ENABLE_VIRTUAL_TERMINAL_PROCESSING)
    
    return nil
}
```

### SSH Session Detection

```go
func isSSHSession() bool {
    return os.Getenv("SSH_TTY") != "" || 
           os.Getenv("SSH_CONNECTION") != ""
}

// Adjust rendering for SSH
if isSSHSession() {
    // Simplify animations
    // Reduce update frequency
    // Disable fancy Unicode
}
```

---

## 🎯 The Ultimate Debug Checklist

### Before You Start Debugging:
- [ ] Can you reproduce it consistently?
- [ ] Have you tried it in a different terminal?
- [ ] Is your Go version up to date?
- [ ] Did you check the Bubble Tea GitHub issues?

### Basic Checks:
- [ ] Terminal state properly restored on exit?
- [ ] All goroutines properly cancelled?
- [ ] No blocking operations in Update()?
- [ ] Model updates returning new model?

### Advanced Checks:
- [ ] Race conditions with `go run -race`?
- [ ] Memory leaks with pprof?
- [ ] CPU hotspots identified?
- [ ] Cross-platform tested?

---

## 🚀 Debug Mode Implementation

```go
// Add to your TUI
type debugModel struct {
    enabled   bool
    messages  []string
    mainModel tea.Model
}

func (d debugModel) View() string {
    mainView := d.mainModel.View()
    
    if !d.enabled {
        return mainView
    }
    
    // Add debug overlay
    debugInfo := lipgloss.NewStyle().
        Background(lipgloss.Color("#ff0000")).
        Foreground(lipgloss.Color("#ffffff")).
        Padding(1).
        Render(strings.Join(d.messages, "\n"))
    
    return lipgloss.JoinVertical(
        lipgloss.Left,
        mainView,
        debugInfo,
    )
}

// Toggle with Ctrl+D
```

---

## 📖 Essential Resources

### Documentation
- [Bubble Tea Debugging Tips](https://github.com/charmbracelet/bubbletea/tree/master/examples)
- [Terminal Capability Database](https://invisible-island.net/ncurses/terminfo.src.html)
- [ANSI Escape Code Reference](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797)

### Tools
- `tput` - Query terminal capabilities
- `script` - Record terminal sessions
- `asciinema` - Record and share terminal sessions
- `gotty` - Share terminal as web application

---

## 🤝 When All Else Fails

1. **Take a break** - Seriously, walk away for 10 minutes
2. **Explain it to a rubber duck** - Or a confused colleague
3. **Start fresh** - Sometimes a rewrite is faster than debugging
4. **Ask for help** - The Charm Discord is incredibly helpful
5. **Submit a bug report** - You might have found a real issue

---

*"Remember: Every segfault is just the computer's way of saying it needs a hug. Or more memory. Probably more memory."* - Anonymous Systems Programmer