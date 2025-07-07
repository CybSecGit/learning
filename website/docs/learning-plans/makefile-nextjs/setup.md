# Development Environment Setup
## Makefile & Next.js Development Prerequisites

> "A developer's environment is like their kitchen - poorly organized, and you'll burn everything."

## 🖥️ System Requirements

Before we begin automating everything, ensure your system meets these requirements:

### Operating System Support
- **macOS**: First-class support (because developers love expensive aluminum)
- **Linux**: Perfect support (the way GNU intended)
- **Windows**: Use WSL2 (because Make and Windows have trust issues)
- **ChromeOS**: Surprisingly viable with Linux container

### Hardware Minimums
- **RAM**: 8GB minimum, 16GB recommended (Chrome needs to eat)
- **Storage**: 20GB free space (node_modules are hungry)
- **CPU**: Any modern processor (compilation is CPU-bound)
- **Internet**: Stable connection (npm install needs its fix)

## 🛠️ Core Tool Installation

### 1. Make Installation

**macOS** (likely already installed):
```bash
# Check if Make is installed
make --version

# If not installed (rare), install via Xcode Command Line Tools
xcode-select --install
```

**Linux** (Ubuntu/Debian):
```bash
# Update package list
sudo apt update

# Install build essentials (includes Make)
sudo apt install build-essential

# Verify installation
make --version
```

**Windows** (via WSL2):
```bash
# First, install WSL2 (in PowerShell as Admin)
wsl --install

# Then in WSL2 Ubuntu:
sudo apt update && sudo apt install build-essential
```

### 2. Node.js & Package Manager Setup

We'll use **fnm** (Fast Node Manager) because nvm is slow and we have things to build:

**Install fnm**:
```bash
# macOS/Linux
curl -fsSL https://fnm.vercel.app/install | bash

# Add to shell profile
echo 'eval "$(fnm env)"' >> ~/.bashrc  # or ~/.zshrc

# Reload shell
source ~/.bashrc
```

**Install Node.js**:
```bash
# Install latest LTS
fnm install --lts
fnm use lts-latest
fnm default lts-latest

# Verify installation
node --version  # Should be 20.x or higher
npm --version
```

### 3. Package Manager Choice

**Install pnpm** (our package manager of choice):
```bash
# Install pnpm globally
npm install -g pnpm

# Or use corepack (built into Node.js)
corepack enable
corepack prepare pnpm@latest --activate

# Verify installation
pnpm --version
```

## 📁 Project Structure Setup

Create your learning workspace:

```bash
# Create project directory
mkdir -p ~/code/makefile-nextjs-mastery
cd ~/code/makefile-nextjs-mastery

# Create initial Makefile
cat > Makefile << 'EOF'
# Makefile for Learning Journey
.PHONY: help
help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

.PHONY: setup
setup: ## Initial project setup
	@echo "Setting up your development environment..."
	@command -v node >/dev/null 2>&1 || { echo "Node.js is required but not installed. Aborting." >&2; exit 1; }
	@command -v pnpm >/dev/null 2>&1 || { echo "pnpm is required but not installed. Run: npm install -g pnpm" >&2; exit 1; }
	@echo "✅ Environment ready!"

.DEFAULT_GOAL := help
EOF

# Test your first Makefile
make help
```

## 🔧 Essential VS Code Extensions

Install these for maximum productivity:

```bash
# Create VS Code extensions recommendations
mkdir -p .vscode
cat > .vscode/extensions.json << 'EOF'
{
  "recommendations": [
    "ms-vscode.makefile-tools",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "bradlc.vscode-tailwindcss",
    "prisma.prisma",
    "styled-components.vscode-styled-components",
    "mikestead.dotenv",
    "christian-kohler.path-intellisense",
    "formulahendry.auto-rename-tag"
  ]
}
EOF
```

## 🎯 Quick Validation

Run this validation script to ensure everything is properly installed:

```bash
# Create validation script
cat > validate-setup.sh << 'EOF'
#!/bin/bash

echo "🔍 Validating development environment..."

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check function
check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 is installed: $(command -v $1)"
        return 0
    else
        echo -e "${RED}✗${NC} $1 is not installed"
        return 1
    fi
}

# Run checks
all_good=true

check_command "make" || all_good=false
check_command "node" || all_good=false
check_command "pnpm" || all_good=false
check_command "git" || all_good=false

# Check Node version
if command -v node &> /dev/null; then
    node_version=$(node -v)
    major_version=$(echo $node_version | cut -d. -f1 | sed 's/v//')
    if [ "$major_version" -ge 18 ]; then
        echo -e "${GREEN}✓${NC} Node.js version $node_version (18+ required)"
    else
        echo -e "${RED}✗${NC} Node.js version $node_version is too old (18+ required)"
        all_good=false
    fi
fi

# Summary
echo ""
if [ "$all_good" = true ]; then
    echo -e "${GREEN}🎉 All checks passed! You're ready to start learning.${NC}"
else
    echo -e "${RED}❌ Some checks failed. Please install missing dependencies.${NC}"
    exit 1
fi
EOF

# Make it executable and run
chmod +x validate-setup.sh
./validate-setup.sh
```

## 🚦 Environment Variables

Create a template `.env` file for your projects:

```bash
cat > .env.example << 'EOF'
# Development Environment Variables
NODE_ENV=development
PORT=3000

# Database (using local SQLite for learning)
DATABASE_URL="file:./dev.db"

# Next.js
NEXT_PUBLIC_APP_URL=http://localhost:3000

# API Keys (add your own)
# GITHUB_TOKEN=
# VERCEL_TOKEN=
EOF
```

## 📋 Makefile Template for Next.js Projects

Here's a starter Makefile template you'll expand throughout the course:

```bash
cat > Makefile.nextjs.template << 'EOF'
# Next.js Project Makefile
.DEFAULT_GOAL := help

# Variables
NODE_ENV ?= development
PORT ?= 3000

.PHONY: help
help: ## Show available commands
	@echo "Next.js Project Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

.PHONY: install
install: ## Install dependencies
	pnpm install

.PHONY: dev
dev: ## Start development server
	pnpm dev

.PHONY: build
build: ## Build for production
	pnpm build

.PHONY: start
start: ## Start production server
	pnpm start

.PHONY: test
test: ## Run tests
	pnpm test

.PHONY: lint
lint: ## Run linting
	pnpm lint

.PHONY: clean
clean: ## Clean build artifacts
	rm -rf .next node_modules

.PHONY: fresh
fresh: clean install ## Fresh install
	@echo "✨ Fresh environment ready!"
EOF
```

## 🎓 Learning Resources Setup

Clone the companion repository with examples:

```bash
# Create examples directory
mkdir -p ~/code/makefile-nextjs-examples

# We'll populate this throughout the course
cd ~/code/makefile-nextjs-examples
echo "# Makefile & Next.js Examples" > README.md
echo "Examples and exercises from the learning journey" >> README.md
```

## ✅ Final Checklist

Before proceeding to Module 1, ensure you have:

- [ ] Make installed and working
- [ ] Node.js 18+ installed via fnm
- [ ] pnpm package manager installed
- [ ] VS Code with recommended extensions
- [ ] A dedicated learning directory created
- [ ] Basic Makefile created and tested
- [ ] Validation script passing all checks

## 🚀 Ready to Begin?

If your validation script shows all green checks, you're ready to start your journey!

**Next Step**: [Module 1: Makefile Fundamentals](/learning-plans/makefile-nextjs/module-1)

---

*Remember: The best time to set up your environment correctly was yesterday. The second best time is right now, before you try to debug why `make` isn't found at 2 AM.*