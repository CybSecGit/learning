# Module 5: Makefile + Next.js Integration Mastery
## Week 5: When Your Build Tool Meets Your Framework

> "Separately, Make and Next.js are powerful tools. Together, they're like peanut butter and jelly, if peanut butter could automate your deployments and jelly could server-side render."

## 🎯 Module Objectives

By the end of this module, you will:
- Create Makefiles that manage entire Next.js project lifecycles
- Automate development workflows that make you look like a wizard
- Build sophisticated testing pipelines with proper orchestration
- Implement caching strategies that actually save time
- Deploy to multiple environments without breaking a sweat

## 📚 Part 1: The Ultimate Next.js Makefile

### Building the Foundation

```makefile
# Next.js Project Makefile - The Complete Version
SHELL := /bin/bash
.DEFAULT_GOAL := help

# Configuration
-include .env
export

# Project Settings
PROJECT_NAME := $(shell node -p "require('./package.json').name")
VERSION := $(shell node -p "require('./package.json').version")
NODE_VERSION := $(shell node --version)
PNPM_VERSION := $(shell pnpm --version)

# Colors for pretty output
BOLD := $(shell tput bold)
RED := $(shell tput setaf 1)
GREEN := $(shell tput setaf 2)
YELLOW := $(shell tput setaf 3)
BLUE := $(shell tput setaf 6)
RESET := $(shell tput sgr0)

# Directories
BUILD_DIR := .next
CACHE_DIR := .cache
COVERAGE_DIR := coverage
DIST_DIR := dist

# Detect OS for cross-platform commands
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    OPEN_CMD := open
else
    OPEN_CMD := xdg-open
endif

# Help system with categories
.PHONY: help
help: ## Show this help message
	@echo "$(BOLD)$(BLUE)$(PROJECT_NAME) v$(VERSION)$(RESET)"
	@echo "Node: $(NODE_VERSION), pnpm: $(PNPM_VERSION)"
	@echo ""
	@echo "$(BOLD)Available commands:$(RESET)"
	@echo ""
	@echo "$(BOLD)$(GREEN)Development:$(RESET)"
	@awk -F ':|##' '/^[a-zA-Z_-]+:.*?##/ && /dev|start|watch/ {printf "  $(BLUE)%-20s$(RESET) %s\n", $$1, $$NF}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(BOLD)$(GREEN)Testing:$(RESET)"
	@awk -F ':|##' '/^[a-zA-Z_-]+:.*?##/ && /test|lint|check/ {printf "  $(BLUE)%-20s$(RESET) %s\n", $$1, $$NF}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(BOLD)$(GREEN)Building:$(RESET)"
	@awk -F ':|##' '/^[a-zA-Z_-]+:.*?##/ && /build|compile|bundle/ {printf "  $(BLUE)%-20s$(RESET) %s\n", $$1, $$NF}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(BOLD)$(GREEN)Deployment:$(RESET)"
	@awk -F ':|##' '/^[a-zA-Z_-]+:.*?##/ && /deploy|release|publish/ {printf "  $(BLUE)%-20s$(RESET) %s\n", $$1, $$NF}' $(MAKEFILE_LIST)

# Version check
.PHONY: check-versions
check-versions:
	@echo "$(YELLOW)Checking tool versions...$(RESET)"
	@node_version=$$(node -v | sed 's/v//'); \
	required_version="18.0.0"; \
	if [ "$$(printf '%s\n' "$$required_version" "$$node_version" | sort -V | head -n1)" != "$$required_version" ]; then \
		echo "$(RED)Error: Node.js $$required_version or higher is required (found $$node_version)$(RESET)"; \
		exit 1; \
	fi
	@command -v pnpm >/dev/null 2>&1 || { echo "$(RED)Error: pnpm is required but not installed.$(RESET)" >&2; exit 1; }
	@echo "$(GREEN)✓ All version requirements met$(RESET)"
```

### Development Workflow Automation

```makefile
# Installation with lockfile validation
node_modules/.timestamp: package.json pnpm-lock.yaml
	@echo "$(YELLOW)📦 Installing dependencies...$(RESET)"
	@pnpm install --frozen-lockfile
	@touch node_modules/.timestamp

.PHONY: install
install: node_modules/.timestamp ## Install dependencies

# Development server with environment detection
.PHONY: dev
dev: install ## Start development server
	@echo "$(GREEN)🚀 Starting development server...$(RESET)"
	@echo "$(BLUE)➜ Local:$(RESET) http://localhost:3000"
	@pnpm dev

# Advanced development with monitoring
.PHONY: dev-full
dev-full: install ## Start dev with monitoring dashboard
	@echo "$(GREEN)🚀 Starting full development environment...$(RESET)"
	@if command -v tmux >/dev/null 2>&1; then \
		tmux new-session -d -s $(PROJECT_NAME)-dev 'make dev'; \
		tmux split-window -h 'make logs-dev'; \
		tmux split-window -v 'make monitor'; \
		tmux select-pane -t 0; \
		tmux attach-session -t $(PROJECT_NAME)-dev; \
	else \
		echo "$(YELLOW)tmux not found. Running simple dev mode.$(RESET)"; \
		make dev; \
	fi

# File watching for auto-restart
.PHONY: watch
watch: ## Watch files and restart on changes
	@echo "$(YELLOW)👁️  Watching for changes...$(RESET)"
	@nodemon --watch 'src/**/*' --ext ts,tsx,css --exec 'make build-fast'

# Database management
.PHONY: db-push
db-push: ## Push database schema changes
	@echo "$(YELLOW)🗄️  Pushing database schema...$(RESET)"
	@pnpx prisma db push

.PHONY: db-studio
db-studio: ## Open Prisma Studio
	@echo "$(BLUE)🎨 Opening Prisma Studio...$(RESET)"
	@pnpx prisma studio

.PHONY: db-reset
db-reset: ## Reset database (WARNING: Destructive)
	@echo "$(RED)⚠️  This will reset your database!$(RESET)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		pnpx prisma db push --force-reset; \
		make db-seed; \
	fi

.PHONY: db-seed
db-seed: ## Seed database with sample data
	@echo "$(YELLOW)🌱 Seeding database...$(RESET)"
	@pnpm run seed
```

### Testing Pipeline with Proper Orchestration

```makefile
# Test file detection
TEST_FILES := $(shell find . -name "*.test.ts" -o -name "*.test.tsx" 2>/dev/null)
E2E_FILES := $(shell find . -name "*.e2e.ts" 2>/dev/null)

# Unit tests with coverage
.PHONY: test
test: install ## Run unit tests
	@echo "$(YELLOW)🧪 Running unit tests...$(RESET)"
	@pnpm test

.PHONY: test-watch
test-watch: install ## Run tests in watch mode
	@echo "$(YELLOW)🧪 Running tests in watch mode...$(RESET)"
	@pnpm test -- --watch

.PHONY: test-coverage
test-coverage: install ## Run tests with coverage report
	@echo "$(YELLOW)📊 Running tests with coverage...$(RESET)"
	@pnpm test -- --coverage
	@echo "$(GREEN)✓ Coverage report generated at $(COVERAGE_DIR)/index.html$(RESET)"

.PHONY: test-changed
test-changed: ## Run tests for changed files only
	@echo "$(YELLOW)🧪 Testing changed files...$(RESET)"
	@changed_files=$$(git diff --name-only HEAD~1 | grep -E '\.(ts|tsx)$$' | grep -v '.test.'); \
	if [ -n "$$changed_files" ]; then \
		pnpm test -- --findRelatedTests $$changed_files; \
	else \
		echo "$(GREEN)No changed files to test$(RESET)"; \
	fi

# E2E tests with proper setup
.PHONY: test-e2e
test-e2e: build ## Run E2E tests
	@echo "$(YELLOW)🎭 Running E2E tests...$(RESET)"
	@pnpm exec playwright install --with-deps chromium
	@pnpm test:e2e

.PHONY: test-e2e-ui
test-e2e-ui: ## Run E2E tests with UI
	@echo "$(YELLOW)🎭 Running E2E tests with UI...$(RESET)"
	@pnpm exec playwright test --ui

# Linting and code quality
.PHONY: lint
lint: install ## Run ESLint
	@echo "$(YELLOW)🔍 Running ESLint...$(RESET)"
	@pnpm lint

.PHONY: lint-fix
lint-fix: install ## Fix ESLint errors
	@echo "$(YELLOW)🔧 Fixing ESLint errors...$(RESET)"
	@pnpm lint -- --fix

.PHONY: typecheck
typecheck: install ## Run TypeScript compiler
	@echo "$(YELLOW)📝 Type checking...$(RESET)"
	@pnpm tsc --noEmit

# Complete quality check
.PHONY: check-all
check-all: lint typecheck test ## Run all checks
	@echo "$(GREEN)✅ All checks passed!$(RESET)"
```

## 🚀 Part 2: Build Optimization and Caching

### Smart Build System with Caching

```makefile
# Build hash calculation for caching
BUILD_HASH := $(shell find src app -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.css" \) -exec sha256sum {} \; | sha256sum | cut -d' ' -f1 | head -c 8)
BUILD_MARKER := $(CACHE_DIR)/build-$(BUILD_HASH).marker

# Create cache directory
$(CACHE_DIR):
	@mkdir -p $(CACHE_DIR)

# Smart build with caching
$(BUILD_MARKER): $(CACHE_DIR) $(shell find src app -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.css" \))
	@echo "$(YELLOW)🏗️  Building project (hash: $(BUILD_HASH))...$(RESET)"
	@pnpm build
	@touch $(BUILD_MARKER)
	@# Clean old build markers
	@find $(CACHE_DIR) -name "build-*.marker" -not -name "build-$(BUILD_HASH).marker" -delete

.PHONY: build
build: install $(BUILD_MARKER) ## Build for production with caching
	@echo "$(GREEN)✅ Build complete (cached)$(RESET)"

.PHONY: build-force
build-force: install ## Force rebuild without cache
	@echo "$(YELLOW)🏗️  Force building project...$(RESET)"
	@rm -rf $(BUILD_DIR) $(CACHE_DIR)/build-*.marker
	@pnpm build

# Build analysis
.PHONY: build-analyze
build-analyze: ## Analyze bundle size
	@echo "$(YELLOW)📊 Analyzing bundle...$(RESET)"
	@ANALYZE=true pnpm build
	@$(OPEN_CMD) $(BUILD_DIR)/analyze.html

# Build with different configurations
.PHONY: build-staging
build-staging: ## Build for staging environment
	@echo "$(YELLOW)🏗️  Building for staging...$(RESET)"
	@NODE_ENV=staging pnpm build

.PHONY: build-preview
build-preview: build ## Build and preview production build
	@echo "$(GREEN)👁️  Starting production preview...$(RESET)"
	@pnpm start &
	@sleep 3
	@$(OPEN_CMD) http://localhost:3000
	@echo "$(YELLOW)Press Ctrl+C to stop the preview server$(RESET)"
	@wait
```

### Performance Monitoring Integration

```makefile
# Performance monitoring
.PHONY: lighthouse
lighthouse: build ## Run Lighthouse audit
	@echo "$(YELLOW)🔍 Running Lighthouse audit...$(RESET)"
	@# Start production server in background
	@pnpm start > /dev/null 2>&1 &
	@SERVER_PID=$$!; \
	sleep 5; \
	lighthouse http://localhost:3000 \
		--output=html \
		--output-path=./lighthouse-report.html \
		--only-categories=performance,accessibility,best-practices,seo \
		--chrome-flags="--headless" && \
	kill $$SERVER_PID
	@echo "$(GREEN)✅ Report saved to lighthouse-report.html$(RESET)"
	@$(OPEN_CMD) lighthouse-report.html

# Bundle size tracking
.PHONY: size-limit
size-limit: build ## Check bundle size limits
	@echo "$(YELLOW)📏 Checking bundle sizes...$(RESET)"
	@pnpm size-limit

# Memory profiling
.PHONY: profile-memory
profile-memory: ## Profile memory usage
	@echo "$(YELLOW)🧠 Profiling memory usage...$(RESET)"
	@NODE_OPTIONS='--inspect' pnpm dev &
	@echo "$(GREEN)Open chrome://inspect to view memory profiling$(RESET)"
```

## 🤖 Part 3: Multi-Environment Deployment

### Environment Management

```makefile
# Environment validation
.PHONY: validate-env
validate-env:
	@echo "$(YELLOW)🔍 Validating environment variables...$(RESET)"
	@required_vars="DATABASE_URL NEXTAUTH_SECRET"; \
	for var in $$required_vars; do \
		if [ -z "$${!var}" ]; then \
			echo "$(RED)Error: $$var is not set$(RESET)"; \
			exit 1; \
		fi; \
	done
	@echo "$(GREEN)✅ Environment validated$(RESET)"

# Environment-specific builds
.PHONY: deploy-staging
deploy-staging: validate-env build-staging ## Deploy to staging
	@echo "$(YELLOW)🚀 Deploying to staging...$(RESET)"
	@vercel deploy --prebuilt

.PHONY: deploy-production
deploy-production: validate-env check-all build ## Deploy to production
	@echo "$(RED)🚀 Deploying to PRODUCTION$(RESET)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		vercel deploy --prod --prebuilt; \
		make notify-deploy; \
	fi

# Rollback functionality
.PHONY: rollback
rollback: ## Rollback to previous deployment
	@echo "$(YELLOW)⏪ Rolling back deployment...$(RESET)"
	@vercel rollback

# Deployment notifications
.PHONY: notify-deploy
notify-deploy:
	@echo "$(GREEN)📢 Deployment successful!$(RESET)"
	@# Add your notification logic here (Slack, Discord, etc.)
```

### Docker Integration for Consistency

```makefile
# Docker configuration
DOCKER_IMAGE := $(PROJECT_NAME):$(VERSION)
DOCKER_REGISTRY := ghcr.io/$(shell git config --get remote.origin.url | sed 's/.*://;s/.git$$//')

# Docker build with multi-stage optimization
.PHONY: docker-build
docker-build: ## Build Docker image
	@echo "$(YELLOW)🐳 Building Docker image...$(RESET)"
	@docker build \
		--build-arg VERSION=$(VERSION) \
		--target production \
		-t $(DOCKER_IMAGE) \
		-t $(DOCKER_IMAGE):latest \
		.

.PHONY: docker-run
docker-run: docker-build ## Run in Docker container
	@echo "$(GREEN)🐳 Running in Docker...$(RESET)"
	@docker run --rm \
		-p 3000:3000 \
		-e NODE_ENV=production \
		--env-file .env.production \
		$(DOCKER_IMAGE)

.PHONY: docker-push
docker-push: docker-build ## Push Docker image to registry
	@echo "$(YELLOW)📤 Pushing to registry...$(RESET)"
	@docker tag $(DOCKER_IMAGE) $(DOCKER_REGISTRY)/$(DOCKER_IMAGE)
	@docker push $(DOCKER_REGISTRY)/$(DOCKER_IMAGE)
```

## 🎨 Part 4: Advanced Patterns

### Monorepo Support

```makefile
# Monorepo management
PACKAGES := $(shell find packages -maxdepth 1 -type d -not -path packages)
APPS := $(shell find apps -maxdepth 1 -type d -not -path apps)

.PHONY: monorepo-install
monorepo-install: ## Install all monorepo dependencies
	@echo "$(YELLOW)📦 Installing monorepo dependencies...$(RESET)"
	@pnpm install -r

.PHONY: monorepo-build
monorepo-build: ## Build all packages and apps
	@echo "$(YELLOW)🏗️  Building all packages...$(RESET)"
	@for pkg in $(PACKAGES); do \
		echo "Building $$pkg..."; \
		(cd $$pkg && pnpm build) || exit 1; \
	done
	@for app in $(APPS); do \
		echo "Building $$app..."; \
		(cd $$app && pnpm build) || exit 1; \
	done

.PHONY: monorepo-test
monorepo-test: ## Test all packages and apps
	@pnpm -r test

# Workspace management
.PHONY: workspace
workspace: ## Run command in specific workspace
	@if [ -z "$(WS)" ]; then \
		echo "$(RED)Error: WS not specified$(RESET)"; \
		echo "Usage: make workspace WS=package-name CMD='pnpm test'"; \
		exit 1; \
	fi
	@pnpm --filter $(WS) $(CMD)
```

### Release Automation

```makefile
# Semantic versioning
.PHONY: version-patch
version-patch: ## Bump patch version
	@pnpm version patch
	@git push --follow-tags

.PHONY: version-minor
version-minor: ## Bump minor version
	@pnpm version minor
	@git push --follow-tags

.PHONY: version-major
version-major: ## Bump major version
	@pnpm version major
	@git push --follow-tags

# Changelog generation
.PHONY: changelog
changelog: ## Generate changelog
	@echo "$(YELLOW)📝 Generating changelog...$(RESET)"
	@conventional-changelog -p angular -i CHANGELOG.md -s

# Release process
.PHONY: release
release: check-all build ## Create a new release
	@echo "$(YELLOW)🎉 Creating release...$(RESET)"
	@current_version=$(VERSION); \
	echo "Current version: $$current_version"; \
	read -p "Release type (patch/minor/major): " release_type; \
	make version-$$release_type; \
	make changelog; \
	git add CHANGELOG.md; \
	git commit -m "docs: update changelog"; \
	make deploy-production
```

## 🏗️ Module Project: Complete Development Pipeline

Create a sophisticated Makefile that manages everything:

```makefile
# The Ultimate Next.js Makefile
# Save this as your project template

# Include all the patterns we've learned
-include makefiles/*.mk

# Project-specific configuration
PROJECT := my-awesome-app
ENVIRONMENTS := dev staging production

# Main targets that combine everything
.PHONY: setup-project
setup-project: ## Complete project setup
	@echo "$(BOLD)$(BLUE)Setting up $(PROJECT)...$(RESET)"
	@make check-versions
	@make install
	@make db-push
	@make db-seed
	@cp .env.example .env.local
	@echo "$(GREEN)✅ Project ready! Run 'make dev' to start$(RESET)"

.PHONY: daily
daily: ## Daily development workflow
	@echo "$(BOLD)$(BLUE)Starting daily workflow...$(RESET)"
	@git pull
	@make install
	@make db-push
	@make test-changed
	@make dev-full

.PHONY: pre-commit
pre-commit: ## Pre-commit checks
	@echo "$(BOLD)$(YELLOW)Running pre-commit checks...$(RESET)"
	@make lint-fix
	@make typecheck
	@make test-changed
	@make build-fast

.PHONY: ship
ship: ## Ship to production
	@echo "$(BOLD)$(RED)Shipping to production...$(RESET)"
	@make check-all
	@make build
	@make lighthouse
	@make deploy-production
	@make notify-deploy
```

## 🧪 Hands-On Exercises

### Exercise 1: CI/CD Pipeline
Create a Makefile that:
- Runs different test suites in parallel
- Caches dependencies between builds
- Deploys to correct environment based on branch
- Sends notifications on success/failure

### Exercise 2: Development Environment
Build a complete development environment that:
- Starts all necessary services
- Sets up database with sample data
- Opens browser to correct URLs
- Provides helpful development commands

### Exercise 3: Performance Pipeline
Implement performance monitoring:
- Automated Lighthouse runs
- Bundle size tracking over time
- Performance regression detection
- Automated performance reports

## ✅ Module Completion Checklist

Before moving to Module 6, ensure you can:

- [ ] Create comprehensive Next.js Makefiles
- [ ] Implement smart caching strategies
- [ ] Automate multi-environment deployments
- [ ] Integrate testing pipelines effectively
- [ ] Build monorepo-compatible workflows
- [ ] Create self-documenting automation

## 📚 Additional Resources

- [GNU Make Manual - Advanced Features](https://www.gnu.org/software/make/manual/html_node/Advanced.html)
- [Next.js CLI Reference](https://nextjs.org/docs/api-reference/cli)
- [Example: Production Makefile](examples/production-nextjs-makefile)

## 🎯 Next Steps

You've mastered the integration! You can now:
- Automate complex Next.js workflows
- Deploy with confidence and rollback capability
- Maintain consistent development environments

**Ready for the final challenges?** Continue to [Module 6: Testing, CI/CD, and Production Patterns](/learning-plans/makefile-nextjs/module-6)

---

*Remember: A well-crafted Makefile is like a good assistant - it anticipates your needs, handles the routine stuff, and never complains about doing the same thing 100 times.*