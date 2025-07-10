# Docker Quick Start Guide
## *For Students Who Just Want to Code*

If you're taking this course and don't want to spend 3 hours debugging Python installations, this is your page.

## Prerequisites

Just install Docker Desktop:
- **Windows/macOS**: Download from [docker.com](https://docker.com)
- **Linux**: Use your package manager (e.g., `sudo apt install docker.io docker-compose`)

## Two-Command Setup

```bash
# 1. Get the code
git clone <repository-url>
cd changelogger

# 2. Start everything
docker-compose up --build
```

That's it. Seriously.

## What Just Happened?

Docker just:
- ✅ Created a Linux environment with Python 3.12
- ✅ Installed all dependencies (rnet, selectolax, etc.)
- ✅ Set up development tools (black, ruff, mypy, etc.)
- ✅ Started a Jupyter Lab server
- ✅ Made everything accessible from your browser

## Access Your Environment

### Method 1: Command Line
```bash
# Connect to the container
docker-compose exec changelogger bash

# You're now in a Linux shell with everything pre-installed
python --version  # Python 3.12.x
rnet --version    # Should work
```

### Method 2: Jupyter Lab
Open your browser to: `http://localhost:8888`

You'll see Jupyter Lab with all our dependencies ready to go.

### Method 3: VS Code (Advanced)
Install the "Dev Containers" extension and attach to the running container.

## Common Commands

```bash
# Start everything
docker-compose up

# Start in background
docker-compose up -d

# Stop everything
docker-compose down

# Rebuild (after changing Dockerfile)
docker-compose up --build

# Access container shell
docker-compose exec changelogger bash

# Run tests
docker-compose exec changelogger pytest

# Format code
docker-compose exec changelogger black .
```

## File Persistence

Your code files are automatically synced between your computer and the container. Edit files with your favorite editor on your host machine, and the changes appear instantly in the container.

## Troubleshooting

**Problem**: "Port 8888 already in use"
**Solution**: Change the port in docker-compose.yml or stop whatever is using port 8888

**Problem**: Container won't start
**Solution**: `docker-compose down && docker-compose up --build`

**Problem**: "Permission denied"
**Solution**: Make sure Docker Desktop is running

**Problem**: Everything is broken
**Solution**: Nuclear option: `docker-compose down -v && docker system prune`

## For Course Instructors

Students should use this setup to eliminate environment issues. All course examples will work identically across all platforms.

The container includes:
- All required dependencies
- Development tools
- Jupyter Lab for interactive learning
- Volume mounting for persistent code changes

## Next Steps

Once your container is running, jump directly to [Chapter 2: Modern Web Scraping](chapter-02-preview.md) and start building!

---

*"It works in the container" > "It works on my machine"*
