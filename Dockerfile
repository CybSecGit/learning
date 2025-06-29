# Use Python slim image for smaller size
FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Build essentials
    build-essential \
    # Git for version control
    git \
    # PostgreSQL client
    postgresql-client \
    # Chromium for web scraping
    chromium \
    chromium-driver \
    # Firefox for alternative scraping
    firefox-esr \
    # Required libraries
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    libssl-dev \
    # Useful tools
    curl \
    wget \
    vim \
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -s /bin/bash scraper && \
    mkdir -p /app && \
    chown -R scraper:scraper /app

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt && \
    pip install -r requirements-dev.txt && \
    # Install Playwright browsers
    playwright install chromium firefox

# Copy course content
COPY --chown=scraper:scraper . .

# Switch to non-root user
USER scraper

# Create directories for course work
RUN mkdir -p \
    /app/workspace \
    /app/data \
    /app/logs \
    /app/output

# Set Python path
ENV PYTHONPATH=/app:$PYTHONPATH

# Default command - start interactive shell
CMD ["/bin/bash"]

# Alternative commands (uncomment as needed):
# CMD ["python", "-m", "ipython"]
# CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; import pandas; print('Ready')" || exit 1

# Expose common ports
# 8888 - Jupyter
# 8000 - Web servers
# 5432 - PostgreSQL
EXPOSE 8888 8000 5432

# Labels
LABEL maintainer="Web Scraping Course" \
      version="1.0" \
      description="Complete environment for web scraping course"

# Build instructions:
# docker build -t webscraping-course .
#
# Run instructions:
# docker run -it --rm -v $(pwd):/app/workspace webscraping-course
#
# Run with Jupyter:
# docker run -it --rm -p 8888:8888 -v $(pwd):/app/workspace webscraping-course jupyter notebook --ip=0.0.0.0 --no-browser
#
# Run with specific exercise:
# docker run -it --rm -v $(pwd):/app/workspace webscraping-course python course/exercises/debugging-exercise-01.py