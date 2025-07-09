# Pre-commit Hooks: Claude Code Compliance Edition
## *Or: How to Make Git Reject Your Code Before Claude Code Gets a Chance To*

> "With great power comes great responsibility." - Uncle Ben  
> "With pre-commit hooks comes great annoyance, but also fewer production disasters." - Every Senior Dev Ever

## Table of Contents
- [The Gospel According to Git Hooks](#the-gospel-according-to-git-hooks)
- [Claude Code Specific Integrations](#claude-code-specific-integrations)
- [The Magnificent Seven: Creative Hook Examples](#the-magnificent-seven-creative-hook-examples)
- [Advanced Hook Sorcery](#advanced-hook-sorcery)
- [The pre-commit Framework: Industrial-Strength Hook Management](#the-pre-commit-framework-industrial-strength-hook-management)

---

## The Gospel According to Git Hooks

Git hooks are like bouncers at a nightclub, except instead of checking IDs, they're checking if your code is drunk on technical debt. They live in `.git/hooks/` and spring into action at various points in your git workflow, like digital tripwires for bad code.

### The Hook Hierarchy of Needs

**Client-side Hooks** (Your personal bodyguards):
- `pre-commit`: The last line of defense before committing crimes against the codebase
- `prepare-commit-msg`: The helpful assistant that writes your commit messages (or judges them)
- `commit-msg`: The grammar nazi of commit messages
- `post-commit`: The tattletale that reports what you've done
- `pre-push`: The final checkpoint before embarrassing yourself publicly

**Server-side Hooks** (The corporate overlords):
- `pre-receive`: The gatekeeper of the repository
- `update`: The branch-specific bouncer
- `post-receive`: The town crier announcing new code

### Why Pre-commit Hooks Matter More Than Your Morning Coffee

Pre-commit hooks are special because they:
1. **Run before the damage is done** - Like contraception for bad code
2. **Are completely under your control** - Unlike your project manager
3. **Can be bypassed** - `git commit --no-verify` (for emergencies only, like production being on fire)
4. **Save you from yourself** - Because at 3 AM, you're not as smart as you think

---

## Claude Code Specific Integrations

Let's create hooks that enforce Claude Code's high standards and peculiar preferences. These hooks ensure your code is worthy of Claude's sophisticated palate.

### Hook #1: The CLAUDE.md Compliance Checker

This hook ensures your code follows the sacred teachings of CLAUDE.md:

```bash
#!/bin/bash
# .git/hooks/pre-commit
# The CLAUDE.md Compliance Enforcer

# Check if CLAUDE.md exists
if [ ! -f "CLAUDE.md" ]; then
    echo "❌ ERROR: No CLAUDE.md found! Claude Code needs instructions!"
    echo "💡 TIP: Create a CLAUDE.md file with project-specific guidance"
    exit 1
fi

# Check for forbidden patterns based on CLAUDE.md
echo "🔍 Checking CLAUDE.md compliance..."

# No mocked data in production code
if grep -r "mock\|stub\|fake_data\|test_data" --include="*.py" --include="*.js" --include="*.ts" --exclude-dir=tests --exclude-dir=__pycache__ . 2>/dev/null | grep -v "^Binary"; then
    echo "❌ ERROR: Found mocked/stubbed data in production code!"
    echo "   Claude Code demands real data only (tests excluded)"
    echo "   Remove all mocks, stubs, and fake data from non-test files"
    exit 1
fi

# Security checks - no hardcoded secrets
if grep -rE "(password|secret|api_key|token)\s*=\s*[\"'][^\"']+[\"']" --include="*.py" --include="*.js" --include="*.ts" --exclude-dir=tests . 2>/dev/null | grep -v "getenv\|environ\|process.env"; then
    echo "❌ ERROR: Hardcoded secrets detected!"
    echo "   Claude Code says: 'Security is job zero'"
    echo "   Use environment variables instead"
    exit 1
fi

# Check for SQL injection vulnerabilities
if grep -rE "f[\"'].*SELECT.*FROM.*{" --include="*.py" . 2>/dev/null || \
   grep -rE "\"SELECT.*FROM.*\" \+" --include="*.js" --include="*.ts" . 2>/dev/null; then
    echo "❌ ERROR: Potential SQL injection vulnerability!"
    echo "   Use parameterized queries, not string concatenation"
    exit 1
fi

echo "✅ CLAUDE.md compliance check passed!"
```

### Hook #2: The TodoWrite Enforcer

Claude Code loves structured task management. This hook ensures you're using TodoWrite properly:

```bash
#!/bin/bash
# Check for TODO patterns and enforce TodoWrite usage

# Look for informal TODOs that should use TodoWrite
TODO_COUNT=$(grep -r "TODO\|FIXME\|HACK\|XXX" --include="*.py" --include="*.js" --include="*.ts" --include="*.go" . 2>/dev/null | wc -l)

if [ "$TODO_COUNT" -gt 0 ]; then
    echo "⚠️  WARNING: Found $TODO_COUNT informal TODO comments"
    echo "   Claude Code prefers structured task tracking with TodoWrite"
    echo "   Consider converting these to proper task items"
    
    # Check if TODO.md exists
    if [ ! -f "TODO.md" ]; then
        echo "❌ ERROR: No TODO.md found but informal TODOs exist!"
        echo "   Create TODO.md and use TodoWrite for task management"
        exit 1
    fi
fi

# If TODO.md exists, validate its format
if [ -f "TODO.md" ]; then
    # Check for proper sections
    if ! grep -q "## Current Task" TODO.md || \
       ! grep -q "## Completed" TODO.md || \
       ! grep -q "## Next Steps" TODO.md; then
        echo "❌ ERROR: TODO.md is missing required sections!"
        echo "   Required sections: Current Task, Completed, Next Steps"
        exit 1
    fi
    
    echo "✅ TODO.md structure validated"
fi
```

### Hook #3: The Test Coverage Guardian

Claude Code demands proper test coverage. This hook prevents commits that tank coverage:

```python
#!/usr/bin/env python3
# .git/hooks/pre-commit
# The Test Coverage Guardian

import subprocess
import sys
import re

def check_coverage():
    """Ensure test coverage doesn't drop below threshold"""
    try:
        # Run coverage report
        result = subprocess.run(
            ["coverage", "report", "--skip-covered"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("❌ ERROR: Could not generate coverage report")
            print("   Run 'make test' first")
            return False
            
        # Extract total coverage
        coverage_match = re.search(r'TOTAL.*\s+(\d+)%', result.stdout)
        if not coverage_match:
            print("⚠️  WARNING: Could not parse coverage report")
            return True
            
        coverage = int(coverage_match.group(1))
        
        # Claude Code demands 80% minimum
        if coverage < 80:
            print(f"❌ ERROR: Test coverage is {coverage}% (minimum: 80%)")
            print("   Claude Code demands proper test coverage!")
            print("   Write more tests or use 'git commit --no-verify' (shame!)")
            return False
            
        print(f"✅ Test coverage: {coverage}% - Claude Code approves!")
        return True
        
    except FileNotFoundError:
        print("⚠️  WARNING: Coverage tool not found, skipping check")
        return True

if __name__ == "__main__":
    if not check_coverage():
        sys.exit(1)
```

---

## The Magnificent Seven: Creative Hook Examples

Here are seven hooks that push the boundaries of pre-commit creativity:

### 1. 🎭 The Emotional Commit Message Analyzer

This hook uses sentiment analysis to reject overly negative commit messages:

```python
#!/usr/bin/env python3
# The Emotional Support Hook

import sys
import re
from textblob import TextBlob

def analyze_mood(message):
    """Ensure commit messages aren't too depressing"""
    blob = TextBlob(message)
    sentiment = blob.sentiment.polarity
    
    if sentiment < -0.5:
        print("❌ ERROR: Your commit message is too negative!")
        print(f"   Sentiment score: {sentiment:.2f}")
        print("   Try being more positive about your code changes")
        print("   Suggested rephrase:", message.replace("broken", "enhanced")
                                              .replace("stupid", "clever")
                                              .replace("hack", "solution"))
        return False
        
    if "hate" in message.lower() or "kill" in message.lower():
        print("❌ ERROR: No violence in commit messages!")
        print("   Claude Code promotes a peaceful codebase")
        return False
        
    return True

# Read commit message
with open(sys.argv[1], 'r') as f:
    message = f.read()
    
if not analyze_mood(message):
    sys.exit(1)
```

### 2. 🕐 The Time Zone Shame Hook

Prevents commits during unreasonable hours (customizable per developer):

```bash
#!/bin/bash
# The Work-Life Balance Enforcer

HOUR=$(date +%H)
DAY=$(date +%u)

# No commits between 2 AM and 6 AM
if [ "$HOUR" -ge 2 ] && [ "$HOUR" -lt 6 ]; then
    echo "❌ ERROR: Go to bed! No commits between 2 AM and 6 AM"
    echo "   Claude Code cares about your health"
    echo "   Use --no-verify if this is an emergency (it's not)"
    exit 1
fi

# Warning for weekend commits
if [ "$DAY" -ge 6 ]; then
    echo "⚠️  WARNING: Weekend commit detected!"
    echo "   Remember: Claude Code supports work-life balance"
    read -p "   Are you sure you want to commit on a weekend? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
```

### 3. 🎨 The ASCII Art Blocker

Prevents excessive ASCII art in code comments:

```python
#!/usr/bin/env python3
# The ASCII Art Police

import re
import subprocess

def check_ascii_art():
    """Detect and limit ASCII art in code"""
    # Get list of staged files
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True
    )
    
    for filename in result.stdout.strip().split('\n'):
        if not filename:
            continue
            
        # Read file content
        try:
            with open(filename, 'r') as f:
                content = f.read()
        except:
            continue
            
        # Look for ASCII art patterns
        lines = content.split('\n')
        art_score = 0
        
        for line in lines:
            # High ratio of special characters = probably art
            if len(line) > 0:
                special_chars = len(re.findall(r'[^a-zA-Z0-9\s]', line))
                if special_chars / len(line) > 0.6:
                    art_score += 1
                    
        if art_score > 5:
            print(f"❌ ERROR: Excessive ASCII art detected in {filename}")
            print("   Claude Code prefers clean, readable code")
            print("   Save your art for README files")
            return False
            
    return True

if __name__ == "__main__":
    if not check_ascii_art():
        sys.exit(1)
```

### 4. 🍕 The Pizza Tracker Hook

Correlates code quality with pizza consumption:

```bash
#!/bin/bash
# The Pizza-Driven Development Hook

PIZZA_FILE=".pizza_tracker"
TODAY=$(date +%Y-%m-%d)

# Ask about pizza consumption
echo "🍕 Pizza-Driven Development Check"
read -p "   Have you had pizza today? (y/N) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "$TODAY:pizza" >> "$PIZZA_FILE"
    echo "✅ Pizza detected - productivity boost applied!"
else
    # Check last pizza
    if [ -f "$PIZZA_FILE" ]; then
        LAST_PIZZA=$(tail -n 1 "$PIZZA_FILE" | cut -d: -f1)
        DAYS_SINCE=$(( ($(date +%s) - $(date -d "$LAST_PIZZA" +%s)) / 86400 ))
        
        if [ "$DAYS_SINCE" -gt 7 ]; then
            echo "⚠️  WARNING: It's been $DAYS_SINCE days since last pizza"
            echo "   Code quality may suffer without proper nutrition"
        fi
    fi
fi
```

### 5. 🎯 The Commit Message Haiku Validator

Ensures commit messages follow haiku structure (5-7-5 syllables):

```python
#!/usr/bin/env python3
# The Poetic Commit Enforcer

import sys
import re
from pyphen import Pyphen

def count_syllables(word):
    """Count syllables in a word"""
    dic = Pyphen(lang='en')
    hyphenated = dic.inserted(word)
    return max(1, hyphenated.count('-') + 1)

def is_haiku(message):
    """Check if message follows 5-7-5 structure"""
    lines = message.strip().split('\n')
    
    if len(lines) != 3:
        return False, "Haiku must have exactly 3 lines"
        
    expected = [5, 7, 5]
    for i, line in enumerate(lines):
        words = re.findall(r'\b\w+\b', line.lower())
        syllables = sum(count_syllables(word) for word in words)
        
        if syllables != expected[i]:
            return False, f"Line {i+1} has {syllables} syllables, expected {expected[i]}"
            
    return True, "Beautiful haiku!"

# Check if haiku mode is enabled
if os.path.exists(".haiku_commits"):
    with open(sys.argv[1], 'r') as f:
        message = f.read()
        
    valid, reason = is_haiku(message)
    if not valid:
        print("❌ ERROR: Commit message is not a valid haiku!")
        print(f"   {reason}")
        print("   Example haiku:")
        print("     Refactor complete")
        print("     Code flows like mountain water") 
        print("     Bugs dare not enter")
        sys.exit(1)
```

### 6. 🔮 The Fortune Teller Hook

Predicts the success of your commit based on mystical algorithms:

```bash
#!/bin/bash
# The Mystical Commit Oracle

# Generate fortune based on commit hash preview
STAGED_HASH=$(git write-tree)
FORTUNE_NUM=$((0x${STAGED_HASH:0:2} % 10))

FORTUNES=(
    "✨ The stars align! This commit will bring great prosperity"
    "⚠️  Caution: Mercury is in retrograde. Test thoroughly"
    "🔮 I foresee... a merge conflict in your future"
    "🌟 Excellent timing! The code spirits are pleased"
    "😈 Beware: This commit may summon ancient bugs"
    "🎯 Success is certain if you add more comments"
    "🌙 The moon phase suggests waiting until tomorrow"
    "⭐ Five stars! This commit will be legendary"
    "🎪 Chaos magic detected. Proceed with caution"
    "🏆 Victory assured! But only after code review"
)

echo "🔮 Consulting the Commit Oracle..."
sleep 1
echo "   ${FORTUNES[$FORTUNE_NUM]}"

# Bad fortune = optional abort
if [ $FORTUNE_NUM -eq 2 ] || [ $FORTUNE_NUM -eq 4 ] || [ $FORTUNE_NUM -eq 6 ]; then
    read -p "   Proceed despite the ominous fortune? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
```

### 7. 🏃 The Performance Regression Detector

Prevents commits that slow down the code:

```python
#!/usr/bin/env python3
# The Speed Demon Hook

import subprocess
import json
import sys
from pathlib import Path

def run_benchmarks():
    """Run performance benchmarks and compare"""
    baseline_file = Path(".performance_baseline.json")
    
    # Run current benchmarks
    print("⚡ Running performance benchmarks...")
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/benchmarks/", "--benchmark-json=current.json"],
        capture_output=True
    )
    
    if result.returncode != 0:
        print("⚠️  WARNING: Benchmarks failed to run")
        return True
        
    # Load results
    with open("current.json", "r") as f:
        current = json.load(f)
        
    # Compare with baseline if it exists
    if baseline_file.exists():
        with open(baseline_file, "r") as f:
            baseline = json.load(f)
            
        # Check for regressions
        regressions = []
        for bench in current["benchmarks"]:
            name = bench["name"]
            current_time = bench["stats"]["mean"]
            
            # Find matching baseline
            for base_bench in baseline["benchmarks"]:
                if base_bench["name"] == name:
                    baseline_time = base_bench["stats"]["mean"]
                    slowdown = (current_time - baseline_time) / baseline_time * 100
                    
                    if slowdown > 10:  # 10% regression threshold
                        regressions.append({
                            "name": name,
                            "slowdown": slowdown,
                            "current": current_time,
                            "baseline": baseline_time
                        })
                        
        if regressions:
            print("❌ ERROR: Performance regressions detected!")
            for reg in regressions:
                print(f"   {reg['name']}: {reg['slowdown']:.1f}% slower")
                print(f"     Baseline: {reg['baseline']:.4f}s")
                print(f"     Current:  {reg['current']:.4f}s")
            return False
            
    print("✅ Performance check passed!")
    return True

if __name__ == "__main__":
    if not run_benchmarks():
        sys.exit(1)
```

---

## Advanced Hook Sorcery

### Hook Chaining: The Voltron of Validation

Create a master hook that orchestrates multiple checks:

```bash
#!/bin/bash
# .git/hooks/pre-commit
# The Master Hook Orchestrator

# Enable strict error handling
set -euo pipefail

# Define hook chain
HOOKS=(
    "check-claude-compliance"
    "validate-todo-usage" 
    "ensure-test-coverage"
    "scan-security-issues"
    "verify-code-style"
    "check-dependencies"
)

# Run hooks in sequence
for hook in "${HOOKS[@]}"; do
    HOOK_PATH=".git/hooks/pre-commit.d/$hook"
    
    if [ -x "$HOOK_PATH" ]; then
        echo "🔄 Running $hook..."
        
        # Run with timeout
        if timeout 30s "$HOOK_PATH"; then
            echo "✅ $hook passed"
        else
            echo "❌ $hook failed"
            exit 1
        fi
    else
        echo "⏭️  Skipping $hook (not found or not executable)"
    fi
done

echo "🎉 All pre-commit checks passed!"
```

### Language-Specific Hook Routing

Route checks based on file types being committed:

```python
#!/usr/bin/env python3
# The Polyglot Hook Router

import subprocess
import sys
from pathlib import Path

def get_changed_files():
    """Get list of staged files grouped by extension"""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True
    )
    
    files_by_type = {}
    for filename in result.stdout.strip().split('\n'):
        if filename:
            ext = Path(filename).suffix
            files_by_type.setdefault(ext, []).append(filename)
            
    return files_by_type

def run_language_hooks(files_by_type):
    """Run appropriate hooks for each language"""
    
    # Language-specific hook mapping
    hooks = {
        '.py': ['python-lint', 'python-security', 'python-types'],
        '.js': ['eslint', 'js-security'],
        '.ts': ['typescript', 'eslint'],
        '.go': ['gofmt', 'govet', 'staticcheck'],
        '.rs': ['cargo-fmt', 'clippy'],
    }
    
    for ext, files in files_by_type.items():
        if ext in hooks:
            print(f"\n🔍 Checking {len(files)} {ext} files...")
            
            for hook_name in hooks[ext]:
                hook_path = f".git/hooks/pre-commit.d/{hook_name}"
                
                if Path(hook_path).exists():
                    # Pass file list to hook
                    result = subprocess.run(
                        [hook_path] + files,
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode != 0:
                        print(f"❌ {hook_name} failed:")
                        print(result.stdout)
                        print(result.stderr)
                        return False
                        
            print(f"✅ All {ext} checks passed")
            
    return True

if __name__ == "__main__":
    files = get_changed_files()
    
    if not files:
        print("⚠️  No files staged for commit")
        sys.exit(0)
        
    if not run_language_hooks(files):
        sys.exit(1)
```

### Performance Optimization: The Need for Speed

Make hooks blazingly fast with parallel execution:

```python
#!/usr/bin/env python3
# The Parallel Hook Executor

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import time

def run_hook(hook_path, timeout=30):
    """Run a single hook with timeout"""
    start = time.time()
    try:
        result = subprocess.run(
            [hook_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        duration = time.time() - start
        return {
            'hook': hook_path,
            'success': result.returncode == 0,
            'output': result.stdout + result.stderr,
            'duration': duration
        }
    except subprocess.TimeoutExpired:
        return {
            'hook': hook_path,
            'success': False,
            'output': f'Timeout after {timeout}s',
            'duration': timeout
        }

def run_hooks_parallel():
    """Run all hooks in parallel for maximum speed"""
    hook_dir = Path(".git/hooks/pre-commit.d")
    
    if not hook_dir.exists():
        return True
        
    hooks = [h for h in hook_dir.iterdir() if h.is_file() and h.stat().st_mode & 0o111]
    
    if not hooks:
        return True
        
    print(f"🚀 Running {len(hooks)} hooks in parallel...")
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(run_hook, str(hook)): hook for hook in hooks}
        
        failed = False
        for future in as_completed(futures):
            result = future.result()
            hook_name = Path(result['hook']).name
            
            if result['success']:
                print(f"✅ {hook_name} ({result['duration']:.2f}s)")
            else:
                print(f"❌ {hook_name} ({result['duration']:.2f}s)")
                print(f"   {result['output']}")
                failed = True
                
    return not failed

if __name__ == "__main__":
    if not run_hooks_parallel():
        sys.exit(1)
```

### The Emergency Bypass System

Sometimes you need to commit despite hook failures. Here's a sophisticated bypass system:

```bash
#!/bin/bash
# .git/hooks/pre-commit
# The Intelligent Bypass System

# Check for bypass file
BYPASS_FILE=".git/COMMIT_BYPASS"
BYPASS_REASON=""

if [ -f "$BYPASS_FILE" ]; then
    BYPASS_REASON=$(cat "$BYPASS_FILE")
    rm "$BYPASS_FILE"
    
    echo "⚠️  BYPASS ACTIVE: $BYPASS_REASON"
    echo "   This bypass has been logged and will be reviewed"
    
    # Log the bypass
    echo "$(date): Bypass used by $(git config user.name) - $BYPASS_REASON" >> .git/bypass.log
    
    # Still run critical security checks
    if ! .git/hooks/pre-commit.d/security-check 2>/dev/null; then
        echo "❌ ERROR: Security check failed - bypass not allowed!"
        exit 1
    fi
    
    exit 0
fi

# Normal hook execution
# ... rest of your hooks ...

# If hooks fail, provide bypass instructions
if [ $? -ne 0 ]; then
    echo ""
    echo "💡 To bypass hooks (use sparingly):"
    echo "   git commit --no-verify"
    echo "   OR"
    echo "   echo 'Emergency fix for production' > .git/COMMIT_BYPASS"
    echo "   git commit"
fi
```

---

## The pre-commit Framework: Industrial-Strength Hook Management

The [pre-commit framework](https://pre-commit.com) is like hiring a professional bouncer instead of relying on your drunk friend Steve.

### Installation and Setup

```bash
# Install pre-commit
pip install pre-commit

# Or with uv (Claude Code's preference)
uv pip install pre-commit

# Initialize in your repo
pre-commit install
```

### The Ultimate Claude Code .pre-commit-config.yaml

```yaml
# .pre-commit-config.yaml
# The Claude Code Compliance Configuration

# Fail fast - stop on first failure
fail_fast: false

# Default stages to run
default_stages: [commit, push]

repos:
  # Claude Code Essentials
  - repo: local
    hooks:
      # CLAUDE.md Compliance Checker
      - id: claude-compliance
        name: Check CLAUDE.md compliance
        entry: .hooks/check-claude-compliance.py
        language: python
        always_run: true
        pass_filenames: false
        
      # TodoWrite Enforcer
      - id: todo-write
        name: Enforce TodoWrite usage
        entry: .hooks/enforce-todowrite.sh
        language: bash
        always_run: true
        
      # Test Coverage Guardian
      - id: coverage-check
        name: Ensure test coverage
        entry: .hooks/check-coverage.py
        language: python
        always_run: true
        pass_filenames: false
        stages: [push]  # Only on push to save time

  # Python Tools (from Claude Code stack)
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
        
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
        
  # Security Scanning
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ['-c', 'pyproject.toml']
        
  # Go Tools (for Go projects)
  - repo: https://github.com/golangci/golangci-lint
    rev: v1.55.2
    hooks:
      - id: golangci-lint
        
  # TypeScript/JavaScript
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.54.0
    hooks:
      - id: eslint
        files: \.(js|jsx|ts|tsx)$
        
  # General Code Quality
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-case-conflict
      - id: check-merge-conflict
      - id: check-json
      - id: pretty-format-json
        args: ['--autofix']
        
  # Commit Message Formatting
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.13.0
    hooks:
      - id: commitizen
        stages: [commit-msg]
        
  # Documentation
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        files: \.(md|mdx)$
        
# Custom local hooks for creativity
  - repo: local
    hooks:
      # The Time Zone Shame Hook
      - id: work-life-balance
        name: Check work-life balance
        entry: .hooks/work-life-balance.sh
        language: bash
        always_run: true
        verbose: true
        
      # The Pizza Tracker
      - id: pizza-driven-development
        name: Pizza-driven development check
        entry: .hooks/pizza-tracker.sh
        language: bash
        always_run: true
        stages: [commit]
        
      # The Fortune Teller
      - id: commit-fortune
        name: Consult the commit oracle
        entry: .hooks/fortune-teller.sh
        language: bash
        always_run: true
        stages: [commit]
```

### Creating Custom pre-commit Hooks

Structure for a custom hook package:

```yaml
# .pre-commit-hooks.yaml
# In your custom hooks repository

- id: claude-code-compliance
  name: Claude Code Compliance Suite
  description: Ensure code meets Claude Code standards
  entry: claude-code-check
  language: python
  types: [python, javascript, typescript]
  require_serial: true
  
- id: ultrathink-detector
  name: Detect when ultrathinking is needed
  description: Identifies complex code requiring deep analysis
  entry: ultrathink-check
  language: python
  files: \.(py|js|ts|go)$
  
- id: mock-data-scanner
  name: Mock Data Scanner
  description: Prevent mock data in production code
  entry: mock-scanner
  language: python
  exclude: ^tests/
```

### Advanced pre-commit Techniques

#### Conditional Hooks Based on Branch

```python
#!/usr/bin/env python3
# .hooks/branch-specific-checks.py

import subprocess
import sys

def get_current_branch():
    """Get current git branch"""
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def main():
    branch = get_current_branch()
    
    # Stricter checks for main/master
    if branch in ["main", "master"]:
        print("🔒 Production branch detected - running strict checks")
        
        # No console.log in production
        result = subprocess.run(
            ["grep", "-r", "console.log", "--include=*.js", "--include=*.ts", "."],
            capture_output=True
        )
        
        if result.returncode == 0:
            print("❌ ERROR: console.log found in production branch!")
            return False
            
    # Feature branch checks
    elif branch.startswith("feature/"):
        print("🚧 Feature branch - ensuring tests exist")
        
        # Check for corresponding test files
        # ... implementation ...
        
    return True

if __name__ == "__main__":
    if not main():
        sys.exit(1)
```

#### Hook Performance Monitoring

```yaml
# .pre-commit-config.yaml
# Add timing information

repos:
  - repo: meta
    hooks:
      - id: check-hooks-apply
      - id: check-useless-excludes
      
  # Hook timing
  - repo: local
    hooks:
      - id: hook-timer-start
        name: Start hook timer
        entry: date +%s > .git/hook-timer
        language: system
        always_run: true
        pass_filenames: false
        stages: [commit]
        
      - id: hook-timer-end
        name: Report hook duration
        entry: bash -c 'echo "⏱️  Hooks completed in $(($(date +%s) - $(cat .git/hook-timer)))s"'
        language: system
        always_run: true
        pass_filenames: false
        stages: [post-commit]
```

### Sharing Hooks Across Teams

Create a shared hook repository:

```bash
# Create hook collection repository
mkdir claude-code-hooks
cd claude-code-hooks

# Standard structure
touch .pre-commit-hooks.yaml
mkdir hooks/
touch hooks/__init__.py

# Package for distribution
cat > setup.py << 'EOF'
from setuptools import setup, find_packages

setup(
    name="claude-code-hooks",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pre-commit",
        "GitPython",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "claude-compliance=hooks.compliance:main",
            "mock-scanner=hooks.mock_scanner:main",
        ],
    },
)
EOF

# Publish to GitHub or PyPI
git init
git add .
git commit -m "feat: Initial Claude Code hooks collection"
git remote add origin https://github.com/yourorg/claude-code-hooks
git push -u origin main
```

Teams can then use your hooks:

```yaml
# Team's .pre-commit-config.yaml
repos:
  - repo: https://github.com/yourorg/claude-code-hooks
    rev: v1.0.0
    hooks:
      - id: claude-code-compliance
      - id: mock-data-scanner
```

---

## Conclusion: Embrace the Hook Life

Pre-commit hooks are like seatbelts - annoying until they save your life. With Claude Code's high standards and these creative hooks, you'll catch issues before they become features.

Remember:
- **Hooks are your friends** - They catch the stupid mistakes so code review can focus on the clever ones
- **Make them fast** - Nobody likes waiting for hooks longer than their actual commit
- **Make them helpful** - Error messages should guide, not just complain
- **Make them bypassable** - Sometimes production is on fire and you need that `--no-verify`
- **Make them fun** - If you're going to be rejected, at least make it entertaining

Now go forth and hook all the things! Your future self (and Claude Code) will thank you.

*P.S. If your hooks are taking longer than your unit tests, you're doing it wrong.*
*P.P.S. If your unit tests are taking longer than your integration tests, you're also doing it wrong.*
*P.P.P.S. If you don't have tests, the hooks can't save you.*