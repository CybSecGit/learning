# Containerization
## *Or: How to Ship Your Problems to Someone Else's Computer*

Welcome to containerization - the technology that exists because we learned the hard way that "it works on my machine" is not a sustainable business model.

## Quick Start (For Students Who Just Want to Code)

If you're here to learn and don't want to spend 3 hours debugging Python installations, start here:

### Prerequisites
- **Windows/macOS**: Download Docker Desktop from [docker.com](https://docker.com)
- **Linux**: Install with your package manager: `sudo apt install docker.io docker-compose`

### Two-Command Setup
```bash
# 1. Get the code
git clone <repository-url>
cd changelogger

# 2. Start everything
docker-compose up --build
```

**That's it.** Seriously. Jump to [Quick Access Guide](#quick-access-guide) below if you just want to start coding.

---

## The Problem with Traditional Setup

Picture this common scenario:
- **Instructor**: "Just install Python, create a virtual environment, install these 47 dependencies..."
- **Student**: "I'm getting an SSL certificate error on Windows"
- **Another Student**: "My macOS has Python 2.7 and I can't figure out brew"
- **Third Student**: "What's a PATH variable?"
- **Instructor**: *quietly weeps into coffee*

## Enter Docker: The Great Equalizer

Docker is like shipping your entire kitchen along with your recipe. Instead of saying "you need a stove, these specific pots, and exactly this brand of olive oil," you just ship everything pre-configured.

### Why Containerization for This Course?

1. **Consistency**: Everyone gets the exact same environment
2. **Simplicity**: Two commands to get started (we can handle that)
3. **No Dependency Hell**: All the modern tools pre-installed
4. **Cross-Platform**: Works on Windows, macOS, Linux, and probably your smart fridge
5. **Instructor Sanity**: No more debugging 47 different Python installations

## What You'll Need

Just two things:
- **Docker Desktop** (or Docker Engine on Linux)
- **Docker Compose** (usually comes with Desktop)

That's it. No Python version debates, no virtual environment confusion, no "but I already have a different version installed" discussions.

## Course Structure (Containerized Edition)

### Option 1: Traditional Setup (Chapter 1)
For masochists and people who enjoy troubleshooting dependency conflicts at 2 AM.

### Option 2: Containerized Setup (This Chapter)
For people who want to actually learn web scraping instead of package management.

## Hands-On Lab: Docker Setup

### Step 1: Install Docker

**Windows/macOS**: Download Docker Desktop from docker.com
**Linux**: Your distribution's package manager probably has it

### Step 2: Verify Installation

```bash
docker --version
docker-compose --version
```

If these commands work, you're ready. If not, consult the Docker installation docs (and maybe a therapist).

### Step 3: Clone and Run

```bash
# Clone the repository
git clone <repository-url>
cd changelogger

# The magic command
docker-compose up --build

# Wait for the magic to happen...
# (Docker downloads and configures everything)
```

## Quick Access Guide

Once your container is running, you have multiple ways to work:

### Method 1: Command Line Access
```bash
# Connect to the container
docker-compose exec changelogger bash

# You're now in a Linux shell with everything pre-installed
python --version  # Python 3.12.x
rnet --version    # Should work perfectly
pytest            # Run tests
```

### Method 2: Jupyter Lab (Interactive Development)
Open your browser to: **http://localhost:8888**

You'll see Jupyter Lab with all dependencies ready to go - perfect for experimentation and learning.

### Method 3: VS Code Integration (Advanced)
Install the "Dev Containers" extension and attach to the running container for a full IDE experience.

### File Persistence Magic
Your code files are automatically synced between your computer and the container. Edit files with your favorite editor on your host machine, and changes appear instantly in the container. No data loss when the container stops!

## The Container Configuration

Our Docker setup includes:

### Base Image (Security-First)
- **Chainguard Python** (CVE-free, continuously scanned)
- **Distroless design** (minimal attack surface)
- **Non-root by default** (principle of least privilege)
- **All our dependencies** pre-installed and tested

### Development Tools
- **VS Code Server** (optional: code in your browser)
- **Jupyter Lab** (for interactive experimentation)
- **All quality assurance tools** ready to go

### Volume Mounting
Your code stays on your host machine, so:
- ✅ Changes persist when container stops
- ✅ Use your favorite editor
- ✅ Git commits work normally
- ✅ No data loss nightmares

## Container vs Traditional Development

| Traditional Setup | Containerized Setup |
|------------------|-------------------|
| 30 minutes of dependency installation | 5 minutes of Docker setup |
| "Works on my machine" syndrome | Works everywhere Docker runs |
| Version conflicts | Isolated environment |
| Python 2 vs 3 debates | Pre-configured Python 3.12 |
| Virtual environment confusion | Container IS the environment |
| Platform-specific issues | Cross-platform consistency |

## Docker Compose: The Orchestra Conductor

Our `docker-compose.yml` is like a recipe that tells Docker:
- What base image to use
- What ports to expose
- What volumes to mount
- What services to run

It's infrastructure as code, which sounds fancy but really just means "documented server setup."

## For the Curious: What's Actually Happening

When you run `docker-compose up`, Docker:

1. **Downloads** the Chainguard Python image (CVE-free!)
2. **Installs** our dependencies using UV in the secure container
3. **Creates** an isolated, minimal container environment
4. **Mounts** your local code directory (with proper permissions)
5. **Starts** all services as non-root user
6. **Exposes** ports so you can access everything securely

It's like having a dedicated server for this project, but it lives inside your computer and disappears when you're done.

## Essential Docker Commands

### Daily Development Commands
```bash
# Start everything (first time or after changes)
docker-compose up --build

# Start in background (when you don't need to see logs)
docker-compose up -d

# Stop everything (preserves data)
docker-compose down

# Access container shell (most common command)
docker-compose exec changelogger bash
```

### Development Workflow Commands
```bash
# Run tests
docker-compose exec changelogger pytest

# Format code
docker-compose exec changelogger black .

# Type checking
docker-compose exec changelogger mypy .

# Install new packages (if needed)
docker-compose exec changelogger uv add package-name
```

### Debugging Commands
```bash
# View container logs
docker-compose logs

# View logs in real-time
docker-compose logs -f

# Restart everything (common fix)
docker-compose restart

# Nuclear option (delete everything and start over)
docker-compose down -v && docker system prune
```

## Troubleshooting Guide

### Common Issues and Solutions

**Problem**: "Port 8888 already in use"
**Solution**: Change the port in docker-compose.yml or stop whatever is using port 8888
```bash
# Find what's using the port
lsof -i :8888  # macOS/Linux
netstat -ano | findstr :8888  # Windows
```

**Problem**: Container won't start
**Solution**: Clean rebuild
```bash
docker-compose down && docker-compose up --build
```

**Problem**: "Permission denied" or "Docker daemon not running"
**Solution**: Make sure Docker Desktop is running and you have proper permissions

**Problem**: "Cannot connect to the Docker daemon"
**Solution**: On Linux, you might need to add your user to the docker group:
```bash
sudo usermod -aG docker $USER
# Then log out and log back in
```

**Problem**: Everything is broken and nothing makes sense
**Solution**: Nuclear option (deletes everything, fresh start)
```bash
docker-compose down -v && docker system prune -a
```

### Performance Tips
- **Slow builds?** Make sure Docker Desktop has enough allocated RAM (4GB minimum)
- **File changes not reflecting?** Check that volume mounting is working properly
- **Network issues?** Try restarting Docker Desktop entirely

## What We've Accomplished

- ✅ **Eliminated environment setup issues** (no more "Python version X.Y not found")
- ✅ **Created reproducible development environment** (works everywhere)
- ✅ **Simplified course prerequisites** (just Docker)
- ✅ **Enabled focus on actual learning** (not dependency management)

## Course Path Decision

Choose your adventure:

### Path A: Traditional Setup (Chapter 1)
- Learn about virtual environments, package managers, and dependency management
- Deal with platform-specific issues
- Gain deep understanding of Python ecosystem
- Spend time on setup instead of core content

### Path B: Containerized Setup (This Chapter)
- Skip directly to the good stuff
- Focus on web scraping and LLM integration
- Consistent environment for everyone
- Learn containerization as a bonus skill

**Recommendation**: If you're here to learn web scraping and AI integration, choose Path B. If you want to become a Python environment troubleshooting expert, choose Path A.

## For Course Instructors

Students should use this containerized setup to eliminate environment issues. All course examples will work identically across all platforms.

The container includes:
- All required dependencies (rnet, selectolax, etc.)
- Development tools (black, ruff, mypy, pytest)
- Jupyter Lab for interactive learning
- VS Code server integration (optional)
- Volume mounting for persistent code changes
- Security-focused base image (Chainguard Python)

## What Just Happened? (The Magic Explained)

When you ran `docker-compose up --build`, Docker:
- ✅ Created a Linux environment with Python 3.12
- ✅ Installed all dependencies automatically
- ✅ Set up development tools (black, ruff, mypy, etc.)
- ✅ Started a Jupyter Lab server
- ✅ Made everything accessible from your browser
- ✅ Mounted your code directory for persistent changes

## Next Steps

Once your container is running:
1. **Test the environment**: Run `docker-compose exec changelogger python -c "import rnet; print('Success!')"`
2. **Access Jupyter Lab**: Open http://localhost:8888 in your browser
3. **Start coding**: Jump directly to [Modern Web Scraping](../hands-on-practice/web-scraping-tutorial.md) and begin building!

---

*"It works on my machine" - Famous last words of developers everywhere*

*"It works in the container" - Famous first words of DevOps engineers*

## Hands-On Exercises

### Exercise 1: Environment Verification
```bash
# Test that everything is working
docker-compose exec changelogger python -c "import rnet; print('✅ rnet imported successfully')"
docker-compose exec changelogger python -c "import selectolax; print('✅ selectolax imported successfully')"
docker-compose exec changelogger pytest --version
```

### Exercise 2: File Persistence Test
```bash
# Create a test file inside the container
docker-compose exec changelogger bash -c "echo 'Hello from container' > test_persistence.txt"

# Stop and restart the container
docker-compose down
docker-compose up -d

# Verify the file still exists
docker-compose exec changelogger cat test_persistence.txt
```

### Exercise 3: Development Workflow
1. **Access Jupyter Lab**: Open http://localhost:8888 in your browser
2. **Create a new Python notebook**: Test importing our dependencies
3. **Edit a file on your host machine**: Verify changes appear in the container
4. **Run the code formatting tools**: `docker-compose exec changelogger black .`

### Exercise 4: Troubleshooting Practice
1. **Stop the container**: `docker-compose down`
2. **Try to access Jupyter Lab**: You should get a connection error
3. **Start it again**: `docker-compose up -d`
4. **Verify everything works**: Access Jupyter Lab again

### Bonus Challenge: Container Archaeology
Try to "break" the container environment in creative ways, then fix it:
- Fill up the disk space
- Corrupt a Python package
- Change file permissions
- Break the network configuration

This is excellent practice for real-world Docker usage where things inevitably go wrong.
