# Module 2: Advanced Makefile Patterns & Project Automation
## Week 2: Teaching Your Computer to Do Your Job

> "The goal of automation is not to eliminate jobs, but to eliminate the boring parts so you can focus on breaking things in more interesting ways."

## 🎯 Module Objectives

By the end of this module, you will:
- Master advanced Make patterns used in production environments
- Build Makefiles that manage complex multi-project repositories
- Integrate Docker seamlessly into your Make workflows
- Create CI/CD pipelines orchestrated entirely by Make
- Write Makefiles that other developers will actually want to use

## 📚 Part 1: Advanced Make Patterns

### Recursive Make: Managing Multi-Project Repositories

When dealing with monorepos or complex project structures, recursive Make becomes essential:

```makefile
# Root Makefile for a monorepo
SUBDIRS := frontend backend shared docs

.PHONY: all $(SUBDIRS)

all: $(SUBDIRS)

$(SUBDIRS):
	@echo "🔨 Building $@..."
	@$(MAKE) -C $@ $(MAKECMDGOALS)

# Pass any target to all subdirectories
%:
	@for dir in $(SUBDIRS); do \
		echo "📁 Running $@ in $$dir"; \
		$(MAKE) -C $$dir $@ || exit 1; \
	done

# Example: 'make test' runs tests in all subdirectories
# Example: 'make frontend' only builds the frontend
```

### Advanced Variable Techniques

```makefile
# Lazy vs Immediate expansion
IMMEDIATE := $(shell date)  # Set once when Makefile is read
LAZY = $(shell date)       # Evaluated each time it's used

# Conditional variables
ENV ?= development  # Use environment variable, default to 'development'
DEBUG := $(if $(filter development,$(ENV)),true,false)

# Target-specific variables
production: ENV=production
production: build

staging: ENV=staging
staging: build

build:
	@echo "Building for $(ENV) environment"
	@echo "Debug mode: $(DEBUG)"

# Pattern-specific variables
%.min.js: UGLIFY_FLAGS = --compress --mangle
%.min.js: %.js
	uglifyjs $< $(UGLIFY_FLAGS) -o $@
```

### Functions: Make's Secret Weapons

```makefile
# Custom functions
define compile_template
	@echo "Compiling $(1) with $(2)..."
	@node scripts/compile.js --input=$(1) --template=$(2) --output=$(3)
endef

# Using the function
pages/%.html: templates/%.hbs
	$(call compile_template,$<,default-template,$@)

# Multi-line functions with commands
define docker_run
	@echo "🐳 Running $(1) in Docker..."
	@docker run --rm \
		-v $(PWD):/workspace \
		-w /workspace \
		$(DOCKER_IMAGE) \
		$(1)
endef

# Advanced text processing
reverse = $(if $(1),$(call reverse,$(wordlist 2,$(words $(1)),$(1))) $(firstword $(1)))
REVERSED := $(call reverse,one two three four)  # Returns: four three two one
```

## 🐳 Part 2: Docker Integration Mastery

### Docker + Make: A Love Story

```makefile
# Docker-integrated Makefile
DOCKER_IMAGE := myapp:latest
DOCKER_RUN := docker run --rm -v $(PWD):/app -w /app
DOCKER_COMPOSE := docker-compose

# Build Docker image with caching
.PHONY: docker-build
docker-build: ## Build Docker image
	@echo "🏗️  Building Docker image..."
	@docker build \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		--cache-from $(DOCKER_IMAGE) \
		-t $(DOCKER_IMAGE) .

# Run commands inside Docker
.PHONY: docker-shell
docker-shell: ## Open shell in Docker container
	@$(DOCKER_RUN) -it $(DOCKER_IMAGE) /bin/bash

# Development with Docker Compose
.PHONY: up
up: ## Start all services
	@$(DOCKER_COMPOSE) up -d
	@echo "✅ Services started. Access at http://localhost:3000"

.PHONY: down
down: ## Stop all services
	@$(DOCKER_COMPOSE) down

.PHONY: logs
logs: ## Follow service logs
	@$(DOCKER_COMPOSE) logs -f

# Run any command in Docker
.PHONY: docker-run
docker-run: ## Run command in Docker (use CMD=...)
	@$(DOCKER_RUN) $(DOCKER_IMAGE) $(CMD)

# Database operations
.PHONY: db-migrate
db-migrate: ## Run database migrations
	@echo "🗄️  Running migrations..."
	@$(DOCKER_COMPOSE) exec backend npm run migrate

.PHONY: db-seed
db-seed: ## Seed database
	@echo "🌱 Seeding database..."
	@$(DOCKER_COMPOSE) exec backend npm run seed
```

### Advanced Docker Patterns

```makefile
# Multi-stage build optimization
.PHONY: docker-build-prod
docker-build-prod:
	@echo "📦 Building production image..."
	@docker build \
		--target production \
		--build-arg NODE_ENV=production \
		-t $(DOCKER_IMAGE):prod .

# Docker health checks
.PHONY: health-check
health-check:
	@echo "🏥 Checking service health..."
	@for service in frontend backend database; do \
		status=$$(docker-compose ps -q $$service | xargs docker inspect -f '{{.State.Health.Status}}' 2>/dev/null || echo "not running"); \
		if [ "$$status" = "healthy" ]; then \
			echo "✅ $$service: $$status"; \
		else \
			echo "❌ $$service: $$status"; \
		fi; \
	done

# Clean Docker artifacts
.PHONY: docker-clean
docker-clean: ## Clean Docker system
	@echo "🧹 Cleaning Docker system..."
	@docker system prune -f
	@docker volume prune -f
	@echo "Freed $$(docker system df | grep 'RECLAIM' | awk '{print $$4}')"
```

## 🤖 Part 3: CI/CD Integration

### GitHub Actions + Make: Better Together

```makefile
# CI/CD-friendly Makefile
CI ?= false
GITHUB_SHA ?= $(shell git rev-parse HEAD)
GITHUB_REF ?= $(shell git rev-parse --abbrev-ref HEAD)

# Detect CI environment
ifeq ($(CI),true)
	DOCKER_FLAGS += --no-cache
	TEST_FLAGS += --coverage --no-watch
else
	TEST_FLAGS += --watch
endif

# CI-specific targets
.PHONY: ci-setup
ci-setup: ## Setup CI environment
	@echo "🤖 Setting up CI environment..."
	@npm ci --quiet
	@cp .env.ci .env

.PHONY: ci-test
ci-test: ci-setup ## Run tests in CI
	@echo "🧪 Running CI tests..."
	@npm test -- $(TEST_FLAGS)
	@npm run test:e2e:headless

.PHONY: ci-build
ci-build: ## Build for CI
	@echo "🏗️  Building for CI..."
	@echo "Commit: $(GITHUB_SHA)"
	@echo "Branch: $(GITHUB_REF)"
	@npm run build
	@echo "::set-output name=build-id::$(GITHUB_SHA)"

# Deployment targets
.PHONY: deploy-staging
deploy-staging: guard-VERCEL_TOKEN ## Deploy to staging
	@echo "🚀 Deploying to staging..."
	@npx vercel deploy --token=$(VERCEL_TOKEN) --env=staging

.PHONY: deploy-production
deploy-production: guard-VERCEL_TOKEN ## Deploy to production
	@echo "🚀 Deploying to production..."
	@npx vercel deploy --prod --token=$(VERCEL_TOKEN)
```

### Self-Updating Makefiles

```makefile
# Makefile that updates itself
MAKEFILE_URL := https://raw.githubusercontent.com/yourrepo/makefiles/main/node.mk

.PHONY: update-makefile
update-makefile: ## Update this Makefile from template
	@echo "📥 Downloading latest Makefile..."
	@curl -sL $(MAKEFILE_URL) -o Makefile.new
	@echo "📊 Showing differences:"
	@diff -u Makefile Makefile.new || true
	@echo ""
	@read -p "Apply update? [y/N] " confirm && \
		if [ "$$confirm" = "y" ]; then \
			mv Makefile.new Makefile; \
			echo "✅ Makefile updated!"; \
		else \
			rm Makefile.new; \
			echo "❌ Update cancelled"; \
		fi
```

## 🎨 Part 4: Creating Developer-Friendly Makefiles

### Enhanced Help System

```makefile
# Advanced help system with categories
.PHONY: help
help: ## Show this help
	@echo "$(BOLD)$(CYAN)Available commands:$(RESET)"
	@echo ""
	@echo "$(BOLD)Development:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		grep -E '(dev|serve|watch)' | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BOLD)Testing:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		grep -E '(test|lint|check)' | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BOLD)Deployment:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		grep -E '(deploy|release)' | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'

# Colors for beautiful output
BOLD := \033[1m
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
CYAN := \033[36m
RESET := \033[0m
```

### Interactive Makefiles

```makefile
# Interactive target selection
.PHONY: interactive
interactive: ## Interactive command menu
	@echo "$(CYAN)What would you like to do?$(RESET)"
	@echo "1) Start development server"
	@echo "2) Run tests"
	@echo "3) Build for production"
	@echo "4) Deploy to staging"
	@echo "5) View logs"
	@read -p "Enter choice [1-5]: " choice; \
	case $$choice in \
		1) $(MAKE) dev ;; \
		2) $(MAKE) test ;; \
		3) $(MAKE) build ;; \
		4) $(MAKE) deploy-staging ;; \
		5) $(MAKE) logs ;; \
		*) echo "Invalid choice" ;; \
	esac

# Confirmation for dangerous operations
.PHONY: confirm
confirm:
	@echo "$(RED)$(BOLD)⚠️  Warning: This will $(ACTION)$(RESET)"
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]

.PHONY: clean-all
clean-all: ACTION=delete all build artifacts and dependencies
clean-all: confirm
	rm -rf node_modules dist .next
```

## 💡 Part 5: Real-World Patterns

### Monorepo Management

```makefile
# Advanced monorepo Makefile
PACKAGES := $(shell find packages -name package.json -not -path "*/node_modules/*" -exec dirname {} \;)
APPS := $(shell find apps -name package.json -not -path "*/node_modules/*" -exec dirname {} \;)
ALL_PROJECTS := $(PACKAGES) $(APPS)

# Install all dependencies
.PHONY: install-all
install-all: ## Install dependencies for all packages
	@echo "📦 Installing root dependencies..."
	@pnpm install
	@for project in $(ALL_PROJECTS); do \
		echo "📦 Installing $$project dependencies..."; \
		(cd $$project && pnpm install) || exit 1; \
	done

# Build all packages in dependency order
.PHONY: build-all
build-all: ## Build all packages
	@echo "🏗️  Building packages in dependency order..."
	@for pkg in $(PACKAGES); do \
		echo "📦 Building $$pkg..."; \
		(cd $$pkg && pnpm build) || exit 1; \
	done
	@for app in $(APPS); do \
		echo "🚀 Building $$app..."; \
		(cd $$app && pnpm build) || exit 1; \
	done

# Run command in specific package
.PHONY: pkg
pkg: ## Run command in package (PKG=name CMD=command)
	@if [ -z "$(PKG)" ]; then \
		echo "Error: PKG not specified"; \
		echo "Usage: make pkg PKG=package-name CMD='npm test'"; \
		exit 1; \
	fi
	@pkg_path=$$(find . -name package.json -not -path "*/node_modules/*" -exec dirname {} \; | grep -E "($(PKG))$$" | head -1); \
	if [ -z "$$pkg_path" ]; then \
		echo "Error: Package '$(PKG)' not found"; \
		exit 1; \
	fi; \
	echo "Running in $$pkg_path: $(CMD)"; \
	(cd $$pkg_path && $(CMD))
```

### Performance Optimization

```makefile
# Parallel execution
MAKEFLAGS += -j$(shell nproc)

# Cached operations
.PHONY: test-fast
test-fast: node_modules/.cache/last-test-run ## Run only changed tests
	@changed_files=$$(git diff --name-only HEAD node_modules/.cache/last-test-run | grep -E '\.(js|ts)$$'); \
	if [ -z "$$changed_files" ]; then \
		echo "✅ No changes detected, skipping tests"; \
	else \
		echo "🧪 Running tests for changed files..."; \
		npm test -- $$changed_files; \
	fi
	@git rev-parse HEAD > node_modules/.cache/last-test-run

# Build caching
BUILD_HASH := $(shell find src -type f -name "*.ts" -o -name "*.tsx" | xargs sha256sum | sha256sum | cut -d' ' -f1)
BUILD_CACHE := .cache/build-$(BUILD_HASH)

$(BUILD_CACHE): $(shell find src -type f -name "*.ts" -o -name "*.tsx")
	@echo "🏗️  Building (hash: $(BUILD_HASH))..."
	@npm run build
	@mkdir -p .cache
	@touch $(BUILD_CACHE)
	@find .cache -name "build-*" -not -name "build-$(BUILD_HASH)" -delete

.PHONY: build-cached
build-cached: $(BUILD_CACHE) ## Build with caching
	@echo "✅ Build is up to date"
```

## 🎯 Module Project: Production-Ready Automation

Create a complete automation system for a Next.js monorepo:

```makefile
# Production Makefile Template
# Save this as the starting point for all your projects

# Configuration
-include .env
export

# Project structure
APPS := web mobile admin
PACKAGES := ui utils api-client
NODE := node
PNPM := pnpm

# Colors
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m

# Default target
.DEFAULT_GOAL := help

# Include sub-makefiles
-include makefiles/*.mk

# Main targets here...
```

## 🧪 Hands-On Exercises

### Exercise 1: Multi-Environment Makefile
Create a Makefile that:
- Manages development, staging, and production environments
- Uses environment-specific variables and configs
- Validates environment before deployment
- Includes rollback capabilities

### Exercise 2: Docker-Integrated Workflow
Build a complete Docker-based workflow that:
- Builds multi-stage Docker images
- Manages Docker Compose services
- Includes health checks and monitoring
- Cleans up resources automatically

### Exercise 3: CI/CD Pipeline
Implement a full CI/CD pipeline with:
- Automated testing on commits
- Build caching for performance
- Deployment to multiple environments
- Rollback on failure

## ✅ Module Completion Checklist

Before moving to Module 3, ensure you can:

- [ ] Write recursive Makefiles for complex projects
- [ ] Use advanced variable and function techniques
- [ ] Integrate Docker seamlessly with Make
- [ ] Create CI/CD pipelines using Make
- [ ] Build interactive and user-friendly Makefiles
- [ ] Implement caching and performance optimizations
- [ ] Handle monorepo structures effectively

## 📚 Additional Resources

- [Advanced GNU Make](https://www.gnu.org/software/make/manual/html_node/Advanced.html)
- [Makefile Best Practices](https://clarkgrubb.com/makefile-style-guide)
- [Example: Production Makefile](examples/production-makefile)

## 🎯 Next Steps

You've mastered advanced Make patterns! You can now:
- Automate complex multi-project workflows
- Create production-ready build systems
- Integrate with modern DevOps tools

**Ready for Next.js?** Continue to [Module 3: Next.js Foundations](/learning-plans/makefile-nextjs/module-3)

---

*Remember: A good Makefile is like a good joke - if you have to explain it, it's not that good. But unlike jokes, Makefiles should always include documentation.*