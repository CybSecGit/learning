# Use Python slim image for smaller size
FROM python:3.12-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    postgresql-client \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    libssl-dev \
    curl \
    wget \
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -s /bin/bash learning && \
    mkdir -p /app && \
    chown -R learning:learning /app

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./ 

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt && \
    pip install -r requirements-dev.txt

# Copy project content
COPY --chown=learning:learning . .

# Switch to non-root user
USER learning

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

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; import os; sys.exit(os.system('python -c \'import requests; print(\'Ready\')\''))" || exit 1

# Expose common ports
# 8888 - Jupyter
# 8000 - Web servers
# 5432 - PostgreSQL
EXPOSE 8888 8000 5432

# Labels
LABEL maintainer="Development Skills Laboratory" \
      version="1.0" \
      description="Complete environment for Development Skills Laboratory"

# Build instructions:
# docker build -t learning-platform .
#
# Run instructions:
# docker run -it --rm -v $(pwd):/app/workspace learning-platform
#
# Run with Jupyter:
# docker run -it --rm -p 8888:8888 -v $(pwd):/app/workspace learning-platform jupyter notebook --ip=0.0.0.0 --no-browser
#
# Run with specific exercise:
# docker run -it --rm -v $(pwd):/app/workspace learning-platform python website/docs/exercises/debugging-exercise.md