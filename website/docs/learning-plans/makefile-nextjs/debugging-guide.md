# Makefile + Next.js Debugging Guide
## When Your Build Fails at 3 AM: A Survival Guide for the Digitally Wounded

> "Debugging is like being the detective in a crime movie where you are also the murderer, the victim, and the murder weapon."

## 🚨 Emergency Triage

When everything is on fire and you need help NOW:

```bash
# The "What's Wrong?" Checklist
make debug-env          # Check environment variables
make debug-deps         # Verify dependencies
make debug-build        # Test build process
make debug-network      # Check network/API issues
make clean-everything   # Nuclear option - clean slate
```

## 🔍 Part 1: Makefile Debugging

### Common Makefile Errors and Solutions

#### 1. "missing separator" - The Tab vs Space Apocalypse

**Error:**
```
Makefile:10: *** missing separator.  Stop.
```

**Diagnosis:** You used spaces instead of a tab. Make is from 1976 and has strong opinions about whitespace.

**Solution:**
```makefile
# WRONG - uses spaces
target:
    echo "This will fail"

# RIGHT - uses tab
target:
	echo "This will work"

# Enable visible whitespace in your editor:
# VS Code: "editor.renderWhitespace": "all"
# Vim: :set list listchars=tab:>-
```

**Prevention Makefile:**
```makefile
# Add this to catch whitespace issues early
.PHONY: check-tabs
check-tabs:
	@if grep -n "^  " Makefile; then \
		echo "❌ Found spaces instead of tabs at lines above"; \
		exit 1; \
	else \
		echo "✅ No space/tab issues found"; \
	fi
```

#### 2. "Command not found" - The PATH Less Traveled

**Error:**
```
make: pnpm: Command not found
```

**Diagnosis:** The command exists on your system but Make can't find it.

**Solution:**
```makefile
# Explicitly set PATH in Makefile
SHELL := /bin/bash
PATH := ./node_modules/.bin:$(PATH)

# Or use full paths
PNPM := $(shell which pnpm || echo "pnpm")
NPX := $(shell which npx || echo "npx")

# Verify commands exist
.PHONY: check-commands
check-commands:
	@command -v node >/dev/null 2>&1 || { echo "❌ node is required"; exit 1; }
	@command -v $(PNPM) >/dev/null 2>&1 || { echo "❌ pnpm is required"; exit 1; }
```

#### 3. Variable Expansion Madness

**Problem:** Variables not expanding as expected

```makefile
# Debug variable expansion
.PHONY: debug-vars
debug-vars:
	@echo "PATH = $(PATH)"
	@echo "NODE_ENV = $(NODE_ENV)"
	@echo "Shell PATH = $$PATH"
	@echo "Make Version = $(MAKE_VERSION)"
	@echo "Working Directory = $(PWD)"
	@echo "Makefile Location = $(MAKEFILE_LIST)"
```

#### 4. Circular Dependencies

**Error:**
```
make: Circular dependency dropped.
```

**Diagnosis:** Your targets depend on each other in a loop.

```makefile
# WRONG - Circular dependency
a: b
	touch a

b: a
	touch b

# RIGHT - Clear dependency chain
a: b
	touch a

b: c
	touch b

c:
	touch c
```

### Advanced Makefile Debugging Techniques

```makefile
# Ultimate Makefile Debugger
.PHONY: debug
debug: ## Run comprehensive debugging
	@echo "🔍 Makefile Debugging Information"
	@echo "================================"
	@echo "Make Version: $(MAKE_VERSION)"
	@echo "Shell: $(SHELL)"
	@echo "OS: $(shell uname -s)"
	@echo "Directory: $(PWD)"
	@echo ""
	@echo "📁 Files in current directory:"
	@ls -la
	@echo ""
	@echo "🌍 Environment Variables:"
	@env | grep -E "(NODE|NPM|PNPM|PATH)" | sort
	@echo ""
	@echo "📦 Node/npm Information:"
	@node --version || echo "Node not found"
	@npm --version || echo "npm not found"
	@pnpm --version || echo "pnpm not found"
	@echo ""
	@echo "🎯 Available Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

# Trace execution
.PHONY: trace-%
trace-%:
	@echo "🔍 Tracing target: $*"
	@$(MAKE) --debug=v $*

# Dry run any target
.PHONY: dry-%
dry-%:
	@echo "🧪 Dry run of: $*"
	@$(MAKE) --dry-run $*
```

## 🎭 Part 2: Next.js Debugging

### Common Next.js Errors and Solutions

#### 1. "Module not found" - The Import Games

**Error:**
```
Module not found: Can't resolve '@/components/Header'
```

**Diagnosis:** Path alias not configured or typo in import.

**Solution:**
```typescript
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/lib/*": ["./src/lib/*"]
    }
  }
}

// next.config.js - Ensure webpack knows about aliases
module.exports = {
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': path.resolve(__dirname, './src'),
    };
    return config;
  },
};
```

**Debug imports:**
```makefile
.PHONY: debug-imports
debug-imports:
	@echo "🔍 Checking import aliases..."
	@cat tsconfig.json | jq '.compilerOptions.paths'
	@echo ""
	@echo "📁 Directory structure:"
	@tree src -I 'node_modules' -L 3
```

#### 2. "Hydration Failed" - Server vs Client Mismatch

**Error:**
```
Error: Hydration failed because the initial UI does not match what was rendered on the server.
```

**Common Causes and Solutions:**

```typescript
// WRONG - Date will differ between server and client
function BadComponent() {
  return <div>{new Date().toLocaleString()}</div>;
}

// RIGHT - Use useEffect for client-only content
function GoodComponent() {
  const [date, setDate] = useState<string>('');
  
  useEffect(() => {
    setDate(new Date().toLocaleString());
  }, []);
  
  return <div>{date || 'Loading...'}</div>;
}

// Or use dynamic import with ssr: false
const ClientOnlyComponent = dynamic(
  () => import('./ClientOnlyComponent'),
  { ssr: false }
);
```

**Debug hydration issues:**
```makefile
.PHONY: debug-hydration
debug-hydration:
	@echo "🔍 Debugging hydration issues..."
	@echo "1. Check for date/time rendering"
	@grep -r "new Date()" src/ || echo "✅ No direct Date usage found"
	@echo ""
	@echo "2. Check for browser-only APIs"
	@grep -r "window\." src/ --include="*.tsx" --include="*.ts" | grep -v "useEffect" || echo "✅ No unsafe window usage"
	@echo ""
	@echo "3. Check for localStorage usage"
	@grep -r "localStorage" src/ --include="*.tsx" --include="*.ts" | grep -v "useEffect" || echo "✅ No unsafe localStorage usage"
```

#### 3. "API Route Error" - The Backend Blues

**Error:**
```
API resolved without sending a response
```

**Solution:**
```typescript
// WRONG - Forgot to send response
export async function GET(request: Request) {
  const data = await fetchData();
  // Oops, forgot to return!
}

// RIGHT - Always return a response
export async function GET(request: Request) {
  try {
    const data = await fetchData();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}
```

**API Route Debugger:**
```makefile
.PHONY: debug-api
debug-api:
	@echo "🔍 API Route Debugging"
	@echo "Testing all API routes..."
	@for route in $$(find app/api -name "route.ts" -o -name "route.js"); do \
		path=$$(echo $$route | sed 's|app/api||' | sed 's|/route.ts||' | sed 's|/route.js||'); \
		echo "Testing $$path"; \
		curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api$$path || echo "Failed"; \
	done
```

#### 4. Build Errors - The Compilation Catastrophe

**Error:**
```
Type error: Cannot find name 'window'.
```

**Solution:**
```typescript
// Add type guards
if (typeof window !== 'undefined') {
  // Client-side only code
}

// Or use a hook
function useIsClient() {
  const [isClient, setIsClient] = useState(false);
  
  useEffect(() => {
    setIsClient(true);
  }, []);
  
  return isClient;
}
```

### Performance Debugging

```makefile
# Performance debugging tools
.PHONY: perf-analyze
perf-analyze: ## Analyze bundle and performance
	@echo "📊 Performance Analysis"
	@echo "====================="
	@echo ""
	@echo "1. Bundle Analysis:"
	@ANALYZE=true pnpm build
	@echo ""
	@echo "2. Lighthouse Scores:"
	@pnpm lighthouse http://localhost:3000 --view
	@echo ""
	@echo "3. Build Size:"
	@du -sh .next/
	@echo ""
	@echo "4. Dependencies Size:"
	@npx bundle-phobia-cli package.json

.PHONY: perf-profile
perf-profile: ## Profile runtime performance
	@echo "🔍 Starting performance profiler..."
	@echo "1. Open Chrome DevTools"
	@echo "2. Go to chrome://inspect"
	@echo "3. Click 'inspect' under Remote Target"
	@NODE_OPTIONS='--inspect' pnpm dev
```

## 🛠️ Part 3: Integration Debugging

### Docker + Make + Next.js Issues

```makefile
# Docker debugging utilities
.PHONY: docker-debug
docker-debug: ## Debug Docker environment
	@echo "🐳 Docker Debugging"
	@echo "=================="
	@echo "Docker Version:"
	@docker --version
	@echo ""
	@echo "Running Containers:"
	@docker ps
	@echo ""
	@echo "Container Logs (last 50 lines):"
	@docker logs $(PROJECT_NAME) --tail 50
	@echo ""
	@echo "Container Environment:"
	@docker exec $(PROJECT_NAME) env | sort

.PHONY: docker-shell
docker-shell: ## Enter Docker container for debugging
	@docker exec -it $(PROJECT_NAME) /bin/bash

.PHONY: docker-clean
docker-clean: ## Clean Docker artifacts
	@echo "🧹 Cleaning Docker..."
	@docker-compose down -v
	@docker system prune -f
	@echo "✅ Docker cleaned"
```

### Database Connection Issues

```makefile
# Database debugging
.PHONY: db-debug
db-debug: ## Debug database connection
	@echo "🗄️  Database Debugging"
	@echo "==================="
	@echo "DATABASE_URL: $${DATABASE_URL:0:30}..."
	@echo ""
	@echo "Testing connection..."
	@npx prisma db execute --stdin <<< "SELECT 1;" && echo "✅ Connection successful" || echo "❌ Connection failed"
	@echo ""
	@echo "Schema status:"
	@npx prisma migrate status

.PHONY: db-reset-hard
db-reset-hard: ## Nuclear database reset
	@echo "☢️  WARNING: This will delete all data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		npx prisma migrate reset --force; \
	fi
```

## 🎯 Part 4: Common Scenarios

### "It Works Locally But Not in Production"

```makefile
# Production parity check
.PHONY: prod-check
prod-check: ## Check production parity
	@echo "🔍 Production Parity Check"
	@echo "======================="
	@echo ""
	@echo "1. Environment Variables:"
	@diff <(cat .env.local | sort) <(cat .env.production | sort) || echo "⚠️  Differences found"
	@echo ""
	@echo "2. Dependencies:"
	@diff <(cat package.json | jq '.dependencies') <(cat package-lock.json | jq '.dependencies' | head -20)
	@echo ""
	@echo "3. Node Version:"
	@echo "Local: $$(node --version)"
	@echo "Production (.nvmrc): $$(cat .nvmrc 2>/dev/null || echo 'Not specified')"

# Build production locally
.PHONY: prod-local
prod-local: ## Test production build locally
	@echo "🏗️  Building production locally..."
	@rm -rf .next
	@NODE_ENV=production pnpm build
	@NODE_ENV=production pnpm start
```

### "Tests Pass But App Breaks"

```makefile
# Integration test reality check
.PHONY: test-real
test-real: ## Test against real running app
	@echo "🧪 Real-world testing..."
	@pnpm build
	@pnpm start & SERVER_PID=$$!; \
	sleep 5; \
	pnpm test:e2e; \
	TEST_RESULT=$$?; \
	kill $$SERVER_PID; \
	exit $$TEST_RESULT
```

## 🚑 Part 5: Emergency Procedures

### The "Nothing Works" Protocol

```makefile
# Nuclear reset - when all else fails
.PHONY: nuke-all
nuke-all: ## Delete everything and start fresh
	@echo "☢️  NUCLEAR RESET INITIATED"
	@echo "This will delete:"
	@echo "  - node_modules"
	@echo "  - .next"
	@echo "  - All caches"
	@echo "  - Database"
	@read -p "Continue? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		rm -rf node_modules .next .cache dist coverage; \
		rm -rf $$HOME/.npm $$HOME/.pnpm-store; \
		pnpm store prune; \
		pnpm install; \
		make setup; \
		echo "✅ Fresh start complete"; \
	fi

# Time machine - revert to last known good state
.PHONY: time-machine
time-machine: ## Revert to last working commit
	@echo "⏰ Time Machine Activated"
	@last_good=$$(git log --format="%H %s" | grep -E "(works|fixed|stable)" | head -1 | cut -d' ' -f1); \
	if [ -n "$$last_good" ]; then \
		echo "Found last good commit: $$last_good"; \
		git stash; \
		git checkout $$last_good; \
		make clean-install; \
	else \
		echo "❌ No known good commit found"; \
	fi
```

### Performance Emergency

```makefile
# When the site is slow
.PHONY: perf-emergency
perf-emergency: ## Emergency performance fixes
	@echo "🚑 Performance Emergency Response"
	@echo "================================"
	@echo ""
	@echo "1. Clearing all caches..."
	@rm -rf .next/cache
	@echo ""
	@echo "2. Optimizing images..."
	@find public -name "*.jpg" -o -name "*.png" | xargs -I {} npx @squoosh/cli --webp auto {}
	@echo ""
	@echo "3. Checking bundle size..."
	@npx bundle-buddy .next/analyze/*.json
	@echo ""
	@echo "4. Emergency measures applied ✅"
```

## 📋 Debugging Checklist

When debugging, always check:

1. **Environment**
   - [ ] All environment variables are set
   - [ ] Correct Node.js version
   - [ ] Dependencies installed correctly

2. **Code**
   - [ ] No syntax errors (run linter)
   - [ ] Type checking passes
   - [ ] Imports are correct

3. **Build**
   - [ ] Clean build directory
   - [ ] No cached bad builds
   - [ ] Production build works

4. **Runtime**
   - [ ] API routes respond
   - [ ] Database connects
   - [ ] No hydration errors

5. **Deployment**
   - [ ] Environment variables in production
   - [ ] Build command correct
   - [ ] Health checks pass

## 🎓 Debugging Wisdom

> "The first step in debugging is to admit you have a bug. The second step is to blame npm."

Remember:
- **Read the error message** - It's trying to help
- **Check the basics first** - Is it plugged in?
- **Binary search** - Cut the problem in half
- **Take breaks** - Fresh eyes see obvious bugs
- **Ask for help** - Someone else has had this problem

---

*"In the face of ambiguity, refuse the temptation to guess. Unless you're debugging Make, then guessing is a valid strategy."*