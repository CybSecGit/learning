# Setting Up Your Go TUI Development Environment
## *"Because even terminal wizards need proper tooling"*

> **Time Required**: 30-45 minutes (or 3 hours if you're on Windows and things go sideways)
> 
> **Goal**: Get your machine ready to build beautiful TUIs without wanting to throw it out the window

---

## Prerequisites Checklist

Before we dive into the setup, make sure you have:

- [ ] **A decent terminal emulator** (not cmd.exe, for the love of all that is holy)
  - **macOS**: iTerm2 or native Terminal.app
  - **Linux**: Terminator, Alacritty, or Kitty
  - **Windows**: Windows Terminal (the new one, not the one from 1995)
- [ ] **Basic command line knowledge** (you know what `cd` does)
- [ ] **Admin access** to install software
- [ ] **Internet connection** that doesn't make you cry
- [ ] **Coffee or beverage of choice** (this is important)

---

## Step 1: Install Go
*"The foundation of your TUI empire"*

### Option A: Official Installer (Recommended)

1. Visit [go.dev/dl](https://go.dev/dl/)
2. Download Go 1.21 or later (we need the good stuff)
3. Run the installer like a civilized person

### Option B: Package Managers (For the Cultured)

**macOS (Homebrew):**
```bash
brew install go
```

**Linux (Ubuntu/Debian):**
```bash
# Remove ancient version first
sudo apt remove golang-go

# Add the official repo
sudo add-apt-repository ppa:longsleep/golang-backports
sudo apt update
sudo apt install golang-go
```

**Windows (Chocolatey):**
```powershell
choco install golang
```

### Verify Installation
```bash
go version
# Should output: go version go1.21.x ...

# If this fails, your PATH is probably broken
# Don't panic, we'll fix it
```

---

## Step 2: Configure Your Go Environment
*"Setting up your workspace like a professional"*

### Set GOPATH (Optional but Recommended)

**macOS/Linux:**
```bash
# Add to ~/.bashrc, ~/.zshrc, or ~/.profile
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin

# Apply changes
source ~/.bashrc  # or ~/.zshrc
```

**Windows (PowerShell):**
```powershell
# Run as Administrator
[Environment]::SetEnvironmentVariable("GOPATH", "$HOME\go", "User")
[Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";$HOME\go\bin", "User")

# Restart PowerShell
```

### Enable Go Modules
```bash
# This should be default, but let's be sure
go env -w GO111MODULE=on
```

---

## Step 3: Choose Your Weapon (IDE/Editor)
*"Because notepad.exe is not a development environment"*

### Option A: VS Code (Most Popular)

1. Install [VS Code](https://code.visualstudio.com/)
2. Install the Go extension:
   ```bash
   code --install-extension golang.go
   ```
3. Open VS Code and let it install Go tools (it'll prompt you)

### Option B: Neovim (For the Hardcore)

```bash
# Install Neovim
brew install neovim  # macOS
sudo apt install neovim  # Ubuntu

# Install vim-go
# Add to ~/.config/nvim/init.vim
Plug 'fatih/vim-go', { 'do': ':GoUpdateBinaries' }
```

### Option C: GoLand (The Luxury Option)

1. Download [GoLand](https://www.jetbrains.com/go/)
2. Use the 30-day trial to see if you're fancy enough
3. Configure GOPATH in settings

---

## Step 4: Install Essential Go Tools
*"The tools that make Go development not suck"*

```bash
# Go formatter (you need this)
go install golang.org/x/tools/cmd/goimports@latest

# Linter (because we write quality code)
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Debugger (for when things go wrong)
go install github.com/go-delve/delve/cmd/dlv@latest

# Go version manager (optional but nice)
go install github.com/stefanmaric/g/cmd/g@latest
```

---

## Step 5: Test Your Setup
*"Making sure everything actually works"*

### Create a Test Project

```bash
# Create a new directory
mkdir ~/go-tui-test && cd ~/go-tui-test

# Initialize a module
go mod init github.com/yourusername/tui-test

# Create a test file
cat > main.go << 'EOF'
package main

import (
    "fmt"
    "runtime"
)

func main() {
    fmt.Printf("🎆 Hello, TUI World! 🎆\n")
    fmt.Printf("Go version: %s\n", runtime.Version())
    fmt.Printf("Terminal ready for beauty: YES\n")
    
    // ANSI color test
    fmt.Printf("\033[31mRed\033[0m ")
    fmt.Printf("\033[32mGreen\033[0m ")
    fmt.Printf("\033[34mBlue\033[0m\n")
    
    if terminalSupportsColor() {
        fmt.Println("✅ Your terminal supports colors!")
    } else {
        fmt.Println("⚠️  Your terminal might have color issues")
    }
}

func terminalSupportsColor() bool {
    return runtime.GOOS != "windows" || isWindowsTerminal()
}

func isWindowsTerminal() bool {
    // Simplified check
    return true // Modern Windows Terminal supports ANSI
}
EOF

# Run it
go run main.go
```

### Expected Output
```
🎆 Hello, TUI World! 🎆
Go version: go1.21.x
Terminal ready for beauty: YES
Red Green Blue
✅ Your terminal supports colors!
```

---

## Step 6: Terminal Configuration
*"Making your terminal not look like it's from 1982"*

### Enable True Color Support

**iTerm2 (macOS):**
1. Preferences → Profiles → Terminal
2. Report Terminal Type: `xterm-256color`
3. Enable "Treat ambiguous-width characters as double width"

**Windows Terminal:**
1. Settings → Profiles → Defaults
2. Color scheme: Choose something nice (not "Campbell")
3. Enable "Use acrylic" for transparency (optional but cool)

**Linux (varies by terminal):**
```bash
# Add to ~/.bashrc or ~/.zshrc
export TERM=xterm-256color
export COLORTERM=truecolor
```

### Install a Nerd Font (Highly Recommended)

Nerd Fonts include icons that make TUIs beautiful:

```bash
# macOS
brew tap homebrew/cask-fonts
brew install --cask font-fira-code-nerd-font

# Or download manually from
# https://www.nerdfonts.com/font-downloads
```

Then configure your terminal to use the Nerd Font.

---

## Step 7: Pre-flight Checklist
*"Making sure you're ready for takeoff"*

Run this verification script:

```bash
# Create check.sh
cat > check.sh << 'EOF'
#!/bin/bash

echo "TUI Development Environment Check"
echo "================================"

# Go check
if command -v go &> /dev/null; then
    echo "✅ Go installed: $(go version)"
else
    echo "❌ Go not found"
fi

# GOPATH check
if [ -n "$GOPATH" ]; then
    echo "✅ GOPATH set: $GOPATH"
else
    echo "⚠️  GOPATH not set (using default)"
fi

# Terminal check
echo "ℹ️  Terminal: $TERM"
echo "ℹ️  Color support: $COLORTERM"

# Tools check
tools=("goimports" "golangci-lint" "dlv")
for tool in "${tools[@]}"; do
    if command -v $tool &> /dev/null; then
        echo "✅ $tool installed"
    else
        echo "⚠️  $tool not found (optional)"
    fi
done

# Unicode test
echo -e "\n🌈 Unicode test: ❤️  🚀 🎉 ✨"
echo "If you see boxes above, install a better font"
EOF

chmod +x check.sh
./check.sh
```

---

## Troubleshooting Common Issues

### "go: command not found"
```bash
# Check if Go is in PATH
echo $PATH

# Add Go to PATH manually
export PATH=$PATH:/usr/local/go/bin
```

### Colors Look Weird
```bash
# Force 256 color mode
export TERM=xterm-256color

# Test colors
for i in {0..255}; do
    printf "\x1b[38;5;${i}mcolor%-5i\x1b[0m" $i
    if ! (( ($i + 1 ) % 8 )); then
        echo
    fi
done
```

### Windows Terminal Issues
```powershell
# Enable ANSI escape sequences
Set-ItemProperty HKCU:\Console VirtualTerminalLevel -Type DWORD 1

# Restart terminal
```

---

## Next Steps

Congratulations! Your terminal is now ready to display beautiful TUIs. You're prepared to:

1. ✅ Write concurrent Go code
2. ✅ Manipulate terminal output
3. ✅ Create gorgeous text-based interfaces
4. ✅ Make other developers jealous

[Continue to Module 1: Go Fundamentals →](/learning-plans/go-tui-charm/module-1)

---

## Optional: Advanced Setup

### Install Charm Tools Early
*"For the eager beavers who can't wait"*

```bash
# Install the Charm tool suite
go install github.com/charmbracelet/charm@latest
go install github.com/charmbracelet/gum@latest
go install github.com/charmbracelet/vhs@latest

# Test Gum (you'll love this)
gum style \
    --foreground 212 --border-foreground 212 --border double \
    --align center --width 50 --margin "1 2" --padding "2 4" \
    'Setup Complete!' 'Your terminal is now BEAUTIFUL'
```

---

*"A journey of a thousand TUIs begins with a single `go mod init`." - Ancient Gopher Wisdom*