# Installing the Charm Toolkit
## *"Your gateway to terminal enlightenment"*

> **Time Required**: 10-15 minutes of pure joy
> 
> **Prerequisites**: Completed the [Go environment setup](/learning-plans/go-tui-charm/setup)
> 
> **Result**: Access to the most delightful TUI libraries in existence

---

## 🎉 What You're Installing

The Charm toolkit is like the Avengers of TUI development:

- **Bubble Tea** 🧁 - The reactive framework (Iron Man)
- **Lip Gloss** 💄 - The style engine (Black Widow) 
- **Bubbles** 🧊 - Pre-built components (The whole team)
- **Wish** 🧞 - SSH application framework (Doctor Strange)
- **Glamour** ✨ - Markdown rendering (Thor's hammer for text)
- **Gum** 🍬 - Scriptable TUI components (Spider-Man's web shooters)
- **VHS** 📹 - Terminal GIF recorder (The documentary crew)

---

## 🚀 Quick Install (The Impatient Method)

```bash
# Install all the essentials in one go
go install github.com/charmbracelet/bubbletea@latest
go install github.com/charmbracelet/lipgloss@latest
go install github.com/charmbracelet/bubbles@latest
go install github.com/charmbracelet/wish@latest
go install github.com/charmbracelet/glamour@latest
go install github.com/charmbracelet/gum@latest
go install github.com/charmbracelet/vhs@latest
go install github.com/charmbracelet/soft-serve@latest

# Verify installation
gum style \
    --foreground 212 --border-foreground 212 \
    --border double --align center --width 50 \
    'Charm tools installed!' 'Your terminal is now magical ✨'
```

---

## 📚 Step-by-Step Installation

### Step 1: Create a Test Project
*"Always test in isolation first"*

```bash
# Create a playground
mkdir ~/charm-playground && cd ~/charm-playground
go mod init charm-test

# Create a test file to verify installations
cat > test_charm.go << 'EOF'
package main

import (
    "fmt"
    "os"
    
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"
)

type model struct {
    choices  []string
    cursor   int
    selected map[int]struct{}
}

func initialModel() model {
    return model{
        choices:  []string{"Bubble Tea", "Lip Gloss", "Glamour", "Wish"},
        selected: make(map[int]struct{}),
    }
}

func (m model) Init() tea.Cmd {
    return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "ctrl+c", "q":
            return m, tea.Quit
        case "up", "k":
            if m.cursor > 0 {
                m.cursor--
            }
        case "down", "j":
            if m.cursor < len(m.choices)-1 {
                m.cursor++
            }
        case "enter", " ":
            _, ok := m.selected[m.cursor]
            if ok {
                delete(m.selected, m.cursor)
            } else {
                m.selected[m.cursor] = struct{}{}
            }
        }
    }
    return m, nil
}

func (m model) View() string {
    style := lipgloss.NewStyle().
        Bold(true).
        Foreground(lipgloss.Color("#FF06B7"))
    
    s := style.Render("Which Charm tools do you love?\n\n")
    
    for i, choice := range m.choices {
        cursor := " "
        if m.cursor == i {
            cursor = ">"
        }
        
        checked := " "
        if _, ok := m.selected[i]; ok {
            checked = "x"
        }
        
        s += fmt.Sprintf("%s [%s] %s\n", cursor, checked, choice)
    }
    
    s += "\nPress q to quit.\n"
    return s
}

func main() {
    p := tea.NewProgram(initialModel())
    if _, err := p.Run(); err != nil {
        fmt.Printf("Alas, there's been an error: %v", err)
        os.Exit(1)
    }
}
EOF
```

### Step 2: Install Core Libraries
*"The foundation of beauty"*

```bash
# Install Bubble Tea (the framework)
go get github.com/charmbracelet/bubbletea

# Install Lip Gloss (the styler)
go get github.com/charmbracelet/lipgloss

# Test the installation
go run test_charm.go
```

You should see a working checkbox list! Navigate with arrow keys, select with space.

### Step 3: Install Bubbles Components
*"Pre-built UI components that spark joy"*

```bash
# Install the component library
go get github.com/charmbracelet/bubbles

# Create a spinner example
cat > spinner_test.go << 'EOF'
package main

import (
    "fmt"
    "os"
    
    "github.com/charmbracelet/bubbles/spinner"
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"
)

type model struct {
    spinner spinner.Model
    loading bool
}

func initialModel() model {
    s := spinner.New()
    s.Spinner = spinner.Dot
    s.Style = lipgloss.NewStyle().Foreground(lipgloss.Color("205"))
    return model{spinner: s, loading: true}
}

func (m model) Init() tea.Cmd {
    return m.spinner.Tick
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.String() == "ctrl+c" || msg.String() == "q" {
            return m, tea.Quit
        }
    case spinner.TickMsg:
        var cmd tea.Cmd
        m.spinner, cmd = m.spinner.Update(msg)
        return m, cmd
    }
    return m, nil
}

func (m model) View() string {
    if m.loading {
        return fmt.Sprintf("\n %s Loading Charm tools...\n\n", m.spinner.View())
    }
    return "Done!\n"
}

func main() {
    p := tea.NewProgram(initialModel())
    if _, err := p.Run(); err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
}
EOF

go run spinner_test.go
```

### Step 4: Install Command Line Tools
*"The Swiss Army knife of TUIs"*

```bash
# Gum - for shell scripts with style
go install github.com/charmbracelet/gum@latest

# Test Gum
gum choose "Bubble Tea" "Lip Gloss" "Glamour" "All of them!"

# More Gum magic
gum spin --spinner dot --title "Installing remaining tools..." -- sleep 2

# Interactive input
NAME=$(gum input --placeholder "What's your name?")
gum style --foreground 212 "Hello, $NAME! Welcome to Charm!"
```

### Step 5: Install VHS (Terminal Recorder)
*"For showing off your creations"*

```bash
# Install VHS
go install github.com/charmbracelet/vhs@latest

# Create a demo tape
cat > demo.tape << 'EOF'
# demo.tape
Output demo.gif

Require gum

Set Shell "bash"
Set FontSize 32
Set Width 1200
Set Height 600

Type "gum style --foreground 212 --border double 'Hello, TUI World!'"
Enter
Sleep 2s

Type "clear"
Enter

Type "gum choose 'Build a TUI' 'Build another TUI' 'Build ALL the TUIs'"
Enter
Sleep 1s
Down
Down
Enter
Sleep 2s
EOF

# Record the GIF
vhs demo.tape
```

---

## 🧪 Advanced Components

### Install Additional Bubbles

```bash
# Create a comprehensive example
cat > advanced_test.go << 'EOF'
package main

import (
    "github.com/charmbracelet/bubbles/textinput"
    "github.com/charmbracelet/bubbles/viewport"
    "github.com/charmbracelet/bubbles/list"
    "github.com/charmbracelet/bubbles/table"
    "github.com/charmbracelet/bubbles/progress"
    "github.com/charmbracelet/bubbles/paginator"
    "github.com/charmbracelet/bubbles/help"
)

// Now you have access to:
// - Text inputs with validation
// - Scrollable viewports  
// - Filterable lists
// - Sortable tables
// - Progress bars
// - Pagination
// - Help menus
// And more!
EOF
```

---

## 🔧 Environment Variables

```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)

# Charm Cloud (optional)
export CHARM_HOST=cloud.charm.sh

# Color preferences
export GLAMOUR_STYLE=dark  # or light, notty

# Gum customization
export GUM_INPUT_CURSOR_FOREGROUND="212"
export GUM_INPUT_PROMPT_FOREGROUND="240"
```

---

## 🎯 Verification Script

```bash
# Create verify.sh
cat > verify.sh << 'EOF'
#!/bin/bash

echo "🎆 Charm Toolkit Verification 🎆"
echo "=============================="

# Function to check if a command exists
check_command() {
    if command -v $1 &> /dev/null; then
        echo "✅ $1 is installed"
        return 0
    else
        echo "❌ $1 is NOT installed"
        return 1
    fi
}

# Function to check Go package
check_package() {
    if go list $1 &> /dev/null; then
        echo "✅ $1 is available"
        return 0
    else
        echo "❌ $1 is NOT available"
        return 1
    fi
}

echo -e "\n🔧 Command Line Tools:"
check_command gum
check_command vhs
check_command soft-serve

echo -e "\n📦 Go Packages:"
check_package github.com/charmbracelet/bubbletea
check_package github.com/charmbracelet/lipgloss
check_package github.com/charmbracelet/bubbles
check_package github.com/charmbracelet/glamour
check_package github.com/charmbracelet/wish

echo -e "\n🎨 Visual Test:"
if command -v gum &> /dev/null; then
    gum style \
        --foreground 212 \
        --border-foreground 62 \
        --border double \
        --align center \
        --width 50 \
        --margin "1 2" \
        --padding "1 2" \
        '✨ All systems go! ✨' \
        'Your Charm toolkit is ready!'
fi
EOF

chmod +x verify.sh
./verify.sh
```

---

## 🚀 Quick Start Templates

### Minimal Bubble Tea App

```bash
gum style --border double "Creating Bubble Tea template..."

cat > minimal-tea/main.go << 'EOF'
package main

import (
    tea "github.com/charmbracelet/bubbletea"
)

type model struct{}

func (m model) Init() tea.Cmd { return nil }

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.String() == "ctrl+c" {
            return m, tea.Quit
        }
    }
    return m, nil
}

func (m model) View() string {
    return "Hello, Bubble Tea! (press ctrl+c to quit)"
}

func main() {
    tea.NewProgram(model{}).Run()
}
EOF
```

---

## 🎉 Celebration Time!

You've successfully installed the Charm toolkit! Here's what you can do now:

```bash
# Play with Gum
gum spin --spinner pulse --title "Celebrating..." -- sleep 3

# Create a celebration message
gum style \
    --foreground "#FF06B7" \
    --background "#1B1B1B" \
    --border double \
    --border-foreground "#FF06B7" \
    --align center \
    --width 60 \
    --margin 2 \
    --padding "2 4" \
    '🎆 CONGRATULATIONS! 🎆' \
    '' \
    'You have unlocked the power of beautiful TUIs!' \
    '' \
    'Next stop: Module 2!'
```

---

## 🎓 Next Steps

Now that you have the tools installed:

1. **Explore the examples**: Each Charm repo has an `examples/` directory full of gold
2. **Read the source**: The code is beautifully written and well-documented
3. **Join the community**: The Charm Discord is friendly and helpful
4. **Start building**: The best way to learn is by creating

[Continue to Module 2: Introduction to the Charm Universe →](/learning-plans/go-tui-charm/module-2)

---

*"With great TUI power comes great responsibility to make beautiful interfaces." - Uncle Ben, if he were a developer*