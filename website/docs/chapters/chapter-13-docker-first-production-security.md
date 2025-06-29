# Chapter 13: Docker-First Production Security
## *Or: How to Stop Your Containers from Becoming the Digital Equivalent of a House with No Locks*

> "Using the default Docker setup in production is like leaving your front door open with a sign that says 'Rob me, I have good stuff inside.'" - Every Security Professional After Their First Container Breach

## Table of Contents
- [The Container Security Wake-Up Call](#the-container-security-wake-up-call)
- [Chainguard/Wolfi: The Hero We Actually Need](#chainguardwolfi-the-hero-we-actually-need)
- [Multi-Stage Builds That Don't Suck](#multi-stage-builds-that-dont-suck)
- [Supply Chain Security for Containers](#supply-chain-security-for-containers)
- [Runtime Security and Monitoring](#runtime-security-and-monitoring)
- [Secrets Management That Actually Works](#secrets-management-that-actually-works)
- [Network Security and Isolation](#network-security-and-isolation)
- [Compliance and Audit Patterns](#compliance-and-audit-patterns)
- [Container Registry Security](#container-registry-security)
- [The Production-Ready Container Stack](#the-production-ready-container-stack)

---

## The Container Security Wake-Up Call

### Why Your Current Docker Setup is Probably Terrible

Let me paint you a picture of what most production Docker setups look like from a security perspective:

**The "Oops, We're Pwned" Starter Pack:**
```dockerfile
# What 90% of production Dockerfiles look like
FROM ubuntu:latest

# Run everything as root because convenience
USER root

# Install everything under the sun
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    vim \
    htop \
    python3 \
    python3-pip \
    nodejs \
    npm \
    # probably 47 other things

# Copy your entire project (including .git, .env, etc.)
COPY . /app

# Expose all the ports
EXPOSE 80 443 3000 5432 6379 8080 9000

# Run with maximum privileges
RUN chmod 777 /app
WORKDIR /app

# Start everything as root
CMD ["python3", "app.py"]
```

**What This Actually Means:**
- Attack surface larger than Texas
- Running as root = game over if compromised
- Base image with 847 known vulnerabilities
- Secrets probably hardcoded in the image
- No network isolation
- Supply chain security? What's that?

**The Reality Check:**
```bash
# What happens when you scan that image
$ docker scan my-app:latest

Testing my-app:latest...

Organization:      your-company
Package manager:   deb
Project name:      docker-image|my-app
Docker image:      my-app:latest
Platform:          linux/amd64
Base image:        ubuntu:latest

✗ High severity vulnerability found in base image
  Introduced by your base image (ubuntu:latest)
  From: ubuntu:latest
  Fixed in: actually-secure-distro:latest

✗ 1,247 vulnerabilities found
  - 127 high
  - 456 medium  
  - 664 low

Base image is 847 days out of date
```

### The Hidden Costs of Insecure Containers

**What Happens When (Not If) You Get Breached:**

**Immediate Costs:**
- Production downtime: $50,000-$500,000 per hour
- Incident response team: $200,000-$2M
- Customer notification: $100,000+
- Legal fees: $500,000+

**Long-term Costs:**
- Customer churn: 20-40% 
- Regulatory fines: $1M-$50M (GDPR, SOX, HIPAA)
- Reputation damage: Priceless (and not in a good way)
- Insurance premium increases: 200-500%

**The Really Fun Part:**
Most container breaches happen because of preventable misconfigurations that take 5 minutes to fix but cost millions to clean up.

---

## Chainguard/Wolfi: The Hero We Actually Need

### Why Chainguard Images Are Like Body Armor for Your Apps

Let me explain why Chainguard base images are the best thing to happen to container security since someone invented the concept of "not running everything as root."

**Traditional Base Images vs. Chainguard:**

```dockerfile
# Traditional approach (the "hope and pray" method)
FROM ubuntu:latest  # 1,200+ packages, 847 vulnerabilities
RUN apt-get update && apt-get install -y python3 python3-pip
# Now you have Python + 1,199 other packages you don't need

# Chainguard approach (the "actually secure" method)
FROM cgr.dev/chainguard/python:latest  # 47 packages, 0 known vulnerabilities
# You have Python. That's it. That's the whole point.
```

**The Chainguard Difference:**

**1. Minimal Attack Surface**
```bash
# Traditional Python image
$ docker run ubuntu:latest dpkg -l | wc -l
1,247 packages

# Chainguard Python image  
$ docker run cgr.dev/chainguard/python:latest apk list | wc -l
47 packages

# Which one do you think has more vulnerabilities?
```

**2. Always Up-to-Date**
- Updated daily (not "whenever we feel like it")
- CVE fixes within hours, not months
- No deprecated packages lingering around like bad code

**3. Provenance and Supply Chain Security**
- Every package signed and verified
- Complete build transparency
- SLSA Level 3 compliance
- No mystery meat in your container

### Real-World Chainguard Implementation

**The Production-Ready Python App:**
```dockerfile
# Multi-stage build with Chainguard
FROM cgr.dev/chainguard/python:latest-dev AS builder

# Install build dependencies
WORKDIR /app
COPY requirements.txt .

# Build virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM cgr.dev/chainguard/python:latest

# Copy only what we need
COPY --from=builder /app/venv /app/venv
COPY src/ /app/src/

# Create non-root user (Chainguard images often include this)
USER nonroot

# Set secure environment
ENV PATH="/app/venv/bin:$PATH"
ENV PYTHONPATH="/app/src"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**The Secure Node.js App:**
```dockerfile
FROM cgr.dev/chainguard/node:latest-dev AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production && npm cache clean --force

# Production stage
FROM cgr.dev/chainguard/node:latest

# Copy application
COPY --from=builder /app/node_modules /app/node_modules
COPY --chown=nonroot:nonroot src/ /app/src/

USER nonroot
WORKDIR /app

# Security headers and settings
ENV NODE_ENV=production
ENV NODE_OPTIONS="--max-old-space-size=512"

EXPOSE 3000
CMD ["node", "src/server.js"]
```

**The Bulletproof Go App:**
```dockerfile
# Build stage
FROM cgr.dev/chainguard/go:latest-dev AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Production stage - use the distroless-like Chainguard static image
FROM cgr.dev/chainguard/static:latest

# Copy only the binary
COPY --from=builder /app/main /main

# Run as non-root
USER nonroot

EXPOSE 8080
ENTRYPOINT ["/main"]
```

### Chainguard Ecosystem Integration

**Container Scanning with Chainguard:**
```bash
#!/bin/bash
# scan_chainguard.sh

# Scan your current image
echo "Scanning current image..."
docker scout cves your-app:latest

# Compare with Chainguard equivalent
echo "Scanning Chainguard-based image..."
docker scout cves your-app:chainguard

# The difference will make you cry (tears of joy)
```

**Automated Updates:**
```yaml
# .github/workflows/chainguard-updates.yml
name: Chainguard Base Image Updates

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:

jobs:
  update-base-images:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check for Chainguard updates
        run: |
          # Get latest digest
          LATEST_DIGEST=$(docker manifest inspect cgr.dev/chainguard/python:latest | jq -r '.manifests[0].digest')
          CURRENT_DIGEST=$(grep "cgr.dev/chainguard/python" Dockerfile | sed 's/.*@//' | cut -d' ' -f1)
          
          if [ "$LATEST_DIGEST" != "$CURRENT_DIGEST" ]; then
            echo "New Chainguard image available!"
            echo "UPDATE_AVAILABLE=true" >> $GITHUB_ENV
          fi
      
      - name: Update Dockerfile
        if: env.UPDATE_AVAILABLE == 'true'
        run: |
          sed -i "s|cgr.dev/chainguard/python:.*|cgr.dev/chainguard/python:latest@${LATEST_DIGEST}|g" Dockerfile
      
      - name: Create PR for update
        if: env.UPDATE_AVAILABLE == 'true'
        uses: peter-evans/create-pull-request@v5
        with:
          title: "Update Chainguard base image"
          body: "Automated update to latest Chainguard base image"
          branch: "chainguard-update"
```

---

## Multi-Stage Builds That Don't Suck

### The Art of Building Secure, Minimal Images

Multi-stage builds are like Marie Kondo for containers - only keep what sparks joy (and actually works).

**The Wrong Way (Single-Stage Disaster):**
```dockerfile
# Everything in one stage = everything in production
FROM node:18

# Install build tools (that stay in production)
RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    make \
    g++ \
    git

# Install dependencies (including devDependencies)
COPY package*.json ./
RUN npm install  # Installs EVERYTHING

# Copy source
COPY . .

# Build (but keep all the build tools)
RUN npm run build

# Run (with 500MB of unnecessary crap)
CMD ["npm", "start"]
```

**The Right Way (Multi-Stage Mastery):**
```dockerfile
# Stage 1: Build environment
FROM cgr.dev/chainguard/node:latest-dev AS builder

WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install ALL dependencies (dev + prod)
RUN npm ci

# Copy source code
COPY src/ ./src/
COPY public/ ./public/
COPY tsconfig.json ./

# Build the application
RUN npm run build

# Stage 2: Dependency pruning
FROM cgr.dev/chainguard/node:latest-dev AS deps

WORKDIR /app
COPY package*.json ./

# Install ONLY production dependencies
RUN npm ci --only=production && npm cache clean --force

# Stage 3: Production runtime
FROM cgr.dev/chainguard/node:latest

WORKDIR /app

# Copy only production dependencies
COPY --from=deps /app/node_modules ./node_modules

# Copy only built application
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

# Security: Don't run as root
USER nonroot

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD node healthcheck.js

EXPOSE 3000
CMD ["node", "dist/server.js"]
```

**Advanced Multi-Stage Pattern for Complex Apps:**
```dockerfile
# Stage 1: Base with common dependencies
FROM cgr.dev/chainguard/python:latest-dev AS base

WORKDIR /app
COPY requirements.txt requirements-dev.txt ./

# Install system dependencies once
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Development/testing stage
FROM base AS development

RUN pip install --no-cache-dir -r requirements-dev.txt
COPY . .
RUN python -m pytest
RUN python -m mypy src/
RUN python -m bandit -r src/

# Stage 3: Build/compile stage
FROM base AS builder

COPY src/ ./src/
# Compile Python to bytecode for faster startup
RUN python -m compileall src/

# Create wheel for faster installs
RUN pip wheel --no-deps --wheel-dir /wheels .

# Stage 4: Security scanning
FROM base AS security

COPY --from=builder /wheels /wheels
RUN pip install /wheels/*.whl

# Run security scans
RUN python -m safety check
RUN python -m bandit -r /app

# Stage 5: Production runtime
FROM cgr.dev/chainguard/python:latest AS production

# Copy only what's needed for runtime
COPY --from=builder /wheels /tmp/wheels
RUN pip install --no-cache-dir /tmp/wheels/*.whl && rm -rf /tmp/wheels

# Copy compiled application
COPY --from=builder /app/src /app/src

# Security: non-root user
USER nonroot

# Minimal environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app/src"

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Size Optimization Techniques

**Before and After Comparison:**
```bash
# Traditional single-stage build
$ docker images my-app:traditional
REPOSITORY   TAG           SIZE
my-app       traditional   1.2GB

# Multi-stage Chainguard build
$ docker images my-app:secure
REPOSITORY   TAG           SIZE  
my-app       secure        145MB

# That's 89% smaller with better security
```

**The .dockerignore That Actually Matters:**
```dockerignore
# .dockerignore - because copying everything is stupid

# Git
.git
.gitignore
.gitattributes

# CI/CD
.github
.gitlab-ci.yml
Jenkinsfile

# Documentation
README.md
docs/
*.md

# Development files
.env
.env.local
.env.development
.vscode/
.idea/

# Dependencies (let the Dockerfile handle these)
node_modules/
__pycache__/
*.pyc
.pytest_cache/

# Build artifacts
dist/
build/
target/

# Logs
*.log
logs/

# Security scanning results
.trivyignore
scan-results/

# Docker files (except the one we're using)
Dockerfile.dev
docker-compose.override.yml

# Testing
coverage/
.coverage
test-results/

# Package managers
.npm
.yarn
pip-cache/

# OS generated files
.DS_Store
Thumbs.db
```

---

## Supply Chain Security for Containers

### Protecting Against the "Someone Poisoned My Dependencies" Attack

Supply chain attacks are like someone switching your coffee with decaf - you don't notice until it's too late, and the damage to your productivity is irreversible.

**The Modern Threat Landscape:**
```bash
# What your typical dependency tree looks like
$ npm ls --depth=0
your-app@1.0.0
├── express@4.18.2
├── lodash@4.17.21
├── axios@1.6.0
└── react@18.2.0

# What your actual dependency tree looks like
$ npm ls
your-app@1.0.0
├── express@4.18.2
│   ├── accepts@1.3.8
│   │   ├── mime-types@2.1.35
│   │   │   └── mime-db@1.52.0
│   │   └── negotiator@0.6.3
│   ├── array-flatten@1.1.1
│   # ... 847 more packages
│   # Any one of which could be compromised
│   # And you'd never know
```

**SLSA (Supply-chain Levels for Software Artifacts) Implementation:**
```dockerfile
# SLSA Level 3 compliant Dockerfile
FROM cgr.dev/chainguard/python:latest-dev AS builder

# Verify image provenance
LABEL org.opencontainers.image.source="https://github.com/your-org/your-app"
LABEL org.opencontainers.image.revision="${GIT_COMMIT}"
LABEL org.opencontainers.image.created="${BUILD_DATE}"

WORKDIR /app

# Use locked dependency files with cryptographic hashes
COPY requirements.txt requirements.lock ./

# Verify dependency integrity
RUN pip install --require-hashes -r requirements.lock

# Build with reproducible settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV SOURCE_DATE_EPOCH=1640995200

COPY src/ ./src/

# Build with verification
RUN python -m build --wheel --outdir /wheels

# Verify the build
RUN python -m twine check /wheels/*

# Production stage with minimal attack surface
FROM cgr.dev/chainguard/python:latest

# Copy verified artifacts
COPY --from=builder /wheels /tmp/wheels
RUN pip install --no-deps /tmp/wheels/*.whl && rm -rf /tmp/wheels

# Runtime verification
COPY --from=builder /app/src /app/src

USER nonroot
HEALTHCHECK CMD python -c "import main; print('OK')"

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0"]
```

**Software Bill of Materials (SBOM) Generation:**
```bash
#!/bin/bash
# generate_sbom.sh

# Generate SBOM for your container
docker sbom your-app:latest --format spdx-json > sbom.json

# Scan SBOM for vulnerabilities
grype sbom:sbom.json

# Verify provenance
cosign verify-attestation \
  --type https://slsa.dev/provenance/v0.2 \
  --certificate-identity-regexp '^https://github\.com/your-org/your-app/\.github/workflows/.+@refs/heads/main$' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  your-app:latest
```

**Dependency Pinning with Verification:**
```python
# requirements.lock - Every hash verified
wheel==0.41.2 --hash=sha256:0c5ac5ff2afb79ac23ab82bab027a0be7b5dbcf2e54dc50efe4bf507de1f7985
setuptools==68.2.2 --hash=sha256:4ac1475276d2f1c48684874089fefcd83bd7162ddaafb81fac866ba0db282a87
pip==23.2.1 --hash=sha256:7ccf472345f20d35bdc9d1841ff5f313260c2c33fe417f48c30ac46cccabf5be

# Any tampering with these dependencies will fail the install
```

**Container Registry with Cosign Signing:**
```bash
#!/bin/bash
# secure_push.sh

IMAGE="your-registry.com/your-app:${VERSION}"

# Build the image
docker build -t "${IMAGE}" .

# Scan for vulnerabilities before pushing
trivy image "${IMAGE}" --exit-code 1

# Push to registry
docker push "${IMAGE}"

# Sign the image
cosign sign "${IMAGE}" \
  --key env://COSIGN_PRIVATE_KEY \
  --annotation "org.example.version=${VERSION}" \
  --annotation "org.example.builder=github-actions"

# Generate and attach SBOM
syft packages "${IMAGE}" -o spdx-json | \
  cosign attest --predicate - "${IMAGE}"

# Verify the signature (for testing)
cosign verify "${IMAGE}" \
  --key env://COSIGN_PUBLIC_KEY \
  --certificate-identity-regexp '^https://github\.com/your-org/your-app/\.github/workflows/.+@refs/heads/main$' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

### Automated Dependency Updates with Security

**Dependabot with Security Gates:**
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "daily"
    reviewers:
      - "security-team"
    open-pull-requests-limit: 5
    
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "daily"
    allow:
      - dependency-type: "all"
    ignore:
      # Ignore major version updates for critical dependencies
      - dependency-name: "django"
        update-types: ["version-update:semver-major"]
```

**Security-First Update Workflow:**
```yaml
# .github/workflows/dependency-update.yml
name: Secure Dependency Updates

on:
  pull_request:
    paths:
      - 'requirements.txt'
      - 'package.json'
      - 'Dockerfile'

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build updated image
        run: |
          docker build -t test-image:latest .
      
      - name: Scan for vulnerabilities
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'test-image:latest'
          format: 'sarif'
          output: 'trivy-results.sarif'
          exit-code: '1'  # Fail on HIGH/CRITICAL
      
      - name: Upload scan results
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'
      
      - name: License compliance check
        run: |
          pip-licenses --format=json > licenses.json
          python scripts/check_license_compliance.py
      
      - name: Performance regression test
        run: |
          docker run --rm test-image:latest python -m pytest tests/performance/
      
      - name: Security unit tests
        run: |
          docker run --rm test-image:latest python -m pytest tests/security/
```

---

## Runtime Security and Monitoring

### Keeping Watch While Your Containers Do Their Thing

Runtime security is like having a bouncer for your containers - someone who watches for trouble and kicks out the bad actors before they can cause damage.

**Falco for Runtime Monitoring:**
```yaml
# falco-rules.yaml
- rule: Unexpected Network Connection from Container
  desc: Detect unexpected network connections from containers
  condition: >
    (inbound_outbound) and container and
    not proc.name in (known_network_processes) and
    not fd.net.cip in (allowed_ips)
  output: >
    Unexpected network connection from container
    (user=%user.name container=%container.name 
     image=%container.image.repository:%container.image.tag
     connection=%fd.net.cip:%fd.net.cport->%fd.net.sip:%fd.net.sport)
  priority: WARNING

- rule: Container with Sensitive Mount
  desc: Detect containers with sensitive filesystem mounts
  condition: >
    container and
    (fd.name startswith /etc/shadow or
     fd.name startswith /etc/passwd or
     fd.name startswith /root/.ssh)
  output: >
    Container accessing sensitive files
    (user=%user.name container=%container.name
     file=%fd.name)
  priority: CRITICAL

- rule: Cryptocurrency Mining Activity
  desc: Detect potential cryptocurrency mining
  condition: >
    spawned_process and
    (proc.name in (cryptominers) or
     proc.cmdline contains "stratum" or
     proc.cmdline contains "xmrig")
  output: >
    Cryptocurrency mining detected
    (user=%user.name container=%container.name
     command=%proc.cmdline)
  priority: CRITICAL
```

**Container Resource Limits and Security:**
```yaml
# docker-compose.yml with security constraints
version: '3.8'

services:
  web-app:
    image: your-app:secure
    
    # Resource limits (prevent resource exhaustion attacks)
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
    
    # Security context
    user: "1000:1000"  # Non-root user
    
    # Read-only root filesystem
    read_only: true
    
    # Temporary filesystem for writes
    tmpfs:
      - /tmp:size=100M,uid=1000,gid=1000,mode=1777
      - /var/cache:size=50M,uid=1000,gid=1000,mode=755
    
    # Security options
    security_opt:
      - no-new-privileges:true
      - seccomp:./seccomp-profile.json
    
    # Capabilities (drop all, add only what's needed)
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if binding to port 80/443
    
    # Network isolation
    networks:
      - app-network
    
    # Environment variables from secrets
    environment:
      - DATABASE_URL_FILE=/run/secrets/database_url
    
    secrets:
      - database_url
    
    # Health check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

networks:
  app-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

secrets:
  database_url:
    external: true
```

**Custom Seccomp Profile:**
```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {
      "names": [
        "accept",
        "accept4", 
        "access",
        "bind",
        "brk",
        "chdir",
        "close",
        "connect",
        "dup",
        "dup2",
        "epoll_create",
        "epoll_ctl",
        "epoll_wait",
        "exit",
        "exit_group",
        "fchdir",
        "fcntl",
        "fstat",
        "futex",
        "getcwd",
        "getdents",
        "getpid",
        "gettimeofday",
        "listen",
        "lseek",
        "mmap",
        "munmap",
        "open",
        "openat",
        "poll",
        "read",
        "recv",
        "recvfrom",
        "rt_sigaction",
        "rt_sigprocmask",
        "rt_sigreturn",
        "send",
        "sendto",
        "set_thread_area",
        "socket",
        "stat",
        "write"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

**AppArmor Profile for Container:**
```apparmor
# /etc/apparmor.d/docker-default-secure
#include <tunables/global>

profile docker-default-secure flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  # Deny dangerous capabilities
  deny capability mac_admin,
  deny capability mac_override,
  deny capability sys_admin,
  deny capability sys_module,
  deny capability sys_rawio,
  deny capability sys_time,
  deny capability syslog,

  # Allow necessary network access
  network inet tcp,
  network inet udp,

  # File system access
  /app/** r,
  /tmp/** rw,
  /var/cache/** rw,
  /etc/passwd r,
  /etc/group r,
  /etc/hosts r,
  /etc/resolv.conf r,

  # Deny access to sensitive files
  deny /etc/shadow r,
  deny /etc/sudoers r,
  deny /root/.ssh/** r,
  deny /home/*/.ssh/** r,

  # Deny access to system directories
  deny /sys/** w,
  deny /proc/sys/** w,
  deny /proc/sysrq-trigger w,

  # Allow process execution only in app directory
  /app/** ix,
  /usr/bin/python3 ix,
  /bin/sh ix,

  # Deny dangerous executables
  deny /bin/su x,
  deny /usr/bin/sudo x,
  deny /usr/bin/ssh x,
}
```

### Real-Time Threat Detection

**Custom Monitoring Agent:**
```python
# container_monitor.py
import docker
import psutil
import json
import time
from datetime import datetime
from typing import Dict, List, Any

class ContainerSecurityMonitor:
    """
    Real-time container security monitoring
    
    Because knowing your containers are misbehaving 
    AFTER they've misbehaved is not a security strategy
    """
    
    def __init__(self):
        self.client = docker.from_env()
        self.baseline_metrics = {}
        self.alert_thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'network_connections': 100,
            'file_descriptors': 1000
        }
        
    def monitor_containers(self):
        """Monitor all running containers"""
        while True:
            try:
                containers = self.client.containers.list()
                
                for container in containers:
                    metrics = self.collect_metrics(container)
                    threats = self.analyze_threats(container, metrics)
                    
                    if threats:
                        self.send_alert(container, threats)
                    
                    self.update_baseline(container.id, metrics)
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.log_error(f"Monitoring error: {e}")
                time.sleep(60)
    
    def collect_metrics(self, container) -> Dict[str, Any]:
        """Collect container metrics"""
        try:
            stats = container.stats(stream=False)
            
            # CPU metrics
            cpu_percent = self.calculate_cpu_percent(stats)
            
            # Memory metrics
            memory_stats = stats['memory_stats']
            memory_usage = memory_stats.get('usage', 0)
            memory_limit = memory_stats.get('limit', 0)
            memory_percent = (memory_usage / memory_limit * 100) if memory_limit > 0 else 0
            
            # Network metrics
            network_stats = stats.get('networks', {})
            total_network_io = sum(
                net['rx_bytes'] + net['tx_bytes'] 
                for net in network_stats.values()
            )
            
            # Process information
            top_output = container.top()
            process_count = len(top_output.get('Processes', []))
            
            return {
                'timestamp': datetime.utcnow(),
                'cpu_percent': cpu_percent,
                'memory_usage': memory_usage,
                'memory_percent': memory_percent,
                'network_io': total_network_io,
                'process_count': process_count,
                'container_id': container.id,
                'image': container.image.tags[0] if container.image.tags else 'unknown'
            }
            
        except Exception as e:
            self.log_error(f"Metrics collection error for {container.id}: {e}")
            return {}
    
    def analyze_threats(self, container, metrics: Dict[str, Any]) -> List[str]:
        """Analyze metrics for potential threats"""
        threats = []
        
        if not metrics:
            return threats
        
        # Resource exhaustion detection
        if metrics['cpu_percent'] > self.alert_thresholds['cpu_percent']:
            threats.append(f"High CPU usage: {metrics['cpu_percent']:.1f}%")
        
        if metrics['memory_percent'] > self.alert_thresholds['memory_percent']:
            threats.append(f"High memory usage: {metrics['memory_percent']:.1f}%")
        
        # Anomaly detection based on baseline
        baseline = self.baseline_metrics.get(container.id, {})
        if baseline:
            # Network activity anomaly
            if metrics['network_io'] > baseline.get('network_io', 0) * 5:
                threats.append("Unusual network activity detected")
            
            # Process count anomaly
            if metrics['process_count'] > baseline.get('process_count', 0) * 2:
                threats.append("Unusual process activity detected")
        
        # Container behavior analysis
        threats.extend(self.check_container_behavior(container))
        
        return threats
    
    def check_container_behavior(self, container) -> List[str]:
        """Check for suspicious container behavior"""
        threats = []
        
        try:
            # Check for unexpected network connections
            exec_result = container.exec_run("netstat -tuln")
            if exec_result.exit_code == 0:
                connections = exec_result.output.decode()
                
                # Look for suspicious ports
                suspicious_ports = ['4444', '5555', '6666', '7777', '31337']
                for port in suspicious_ports:
                    if port in connections:
                        threats.append(f"Suspicious port {port} detected")
            
            # Check for cryptocurrency mining indicators
            exec_result = container.exec_run("ps aux")
            if exec_result.exit_code == 0:
                processes = exec_result.output.decode().lower()
                
                mining_indicators = ['xmrig', 'cryptonight', 'stratum', 'monero']
                for indicator in mining_indicators:
                    if indicator in processes:
                        threats.append(f"Cryptocurrency mining indicator: {indicator}")
            
            # Check for privilege escalation attempts
            exec_result = container.exec_run("find /tmp -name '*sudo*' -o -name '*su*'")
            if exec_result.exit_code == 0 and exec_result.output:
                threats.append("Privilege escalation tools found in /tmp")
            
        except Exception as e:
            # Don't log every exec error, just note it happened
            pass
        
        return threats
    
    def send_alert(self, container, threats: List[str]):
        """Send security alert"""
        alert = {
            'timestamp': datetime.utcnow().isoformat(),
            'container_id': container.id[:12],
            'container_name': container.name,
            'image': container.image.tags[0] if container.image.tags else 'unknown',
            'threats': threats,
            'severity': 'HIGH' if any('mining' in t.lower() for t in threats) else 'MEDIUM'
        }
        
        # Log to file
        with open('/var/log/container-security.log', 'a') as f:
            f.write(json.dumps(alert) + '\n')
        
        # Send to SIEM/monitoring system
        self.send_to_siem(alert)
        
        print(f"🚨 SECURITY ALERT: {container.name}")
        for threat in threats:
            print(f"  • {threat}")
    
    def send_to_siem(self, alert: Dict[str, Any]):
        """Send alert to SIEM system"""
        try:
            # This would integrate with your SIEM system
            # Example: Splunk, ELK Stack, etc.
            pass
        except Exception as e:
            self.log_error(f"SIEM integration error: {e}")
    
    def calculate_cpu_percent(self, stats) -> float:
        """Calculate CPU percentage from Docker stats"""
        try:
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                       stats['precpu_stats']['cpu_usage']['total_usage']
            system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                          stats['precpu_stats']['system_cpu_usage']
            
            if system_delta > 0:
                cpu_percent = (cpu_delta / system_delta) * 100.0
                return min(cpu_percent, 100.0)
        except (KeyError, ZeroDivisionError):
            pass
        
        return 0.0
    
    def update_baseline(self, container_id: str, metrics: Dict[str, Any]):
        """Update baseline metrics for anomaly detection"""
        if container_id not in self.baseline_metrics:
            self.baseline_metrics[container_id] = metrics
        else:
            # Simple moving average
            baseline = self.baseline_metrics[container_id]
            for key in ['cpu_percent', 'memory_percent', 'network_io', 'process_count']:
                if key in metrics and key in baseline:
                    baseline[key] = (baseline[key] * 0.9) + (metrics[key] * 0.1)
    
    def log_error(self, message: str):
        """Log error message"""
        with open('/var/log/container-monitor-errors.log', 'a') as f:
            f.write(f"{datetime.utcnow().isoformat()}: {message}\n")

if __name__ == "__main__":
    monitor = ContainerSecurityMonitor()
    monitor.monitor_containers()
```

---

## Secrets Management That Actually Works

### Because Hardcoding Passwords is Not a Security Strategy

Secrets management in containers is like keeping your house keys - you need them to get in, but you don't want to leave them under the doormat for everyone to find.

**The Hall of Shame (Don't Do This):**
```dockerfile
# What nightmares are made of
FROM ubuntu:latest

# Secrets directly in the Dockerfile (visible to anyone)
ENV DATABASE_PASSWORD="super_secret_password_123"
ENV API_KEY="sk-definitely-not-my-openai-key-456789"

# Secrets in the image layers (accessible via docker history)
RUN echo "password123" > /app/.env

# Secrets as build args (visible in build logs)
ARG SECRET_TOKEN=abc123def456

# Copy .env file into image (secrets in final image)
COPY .env /app/.env
```

**Docker Secrets (The Right Way):**
```yaml
# docker-compose.yml with proper secrets management
version: '3.8'

services:
  web-app:
    image: your-app:secure
    environment:
      # Reference secrets, don't hardcode values
      - DATABASE_URL_FILE=/run/secrets/database_url
      - API_KEY_FILE=/run/secrets/api_key
      - JWT_SECRET_FILE=/run/secrets/jwt_secret
    
    secrets:
      - database_url
      - api_key
      - jwt_secret
    
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure

secrets:
  database_url:
    external: true
    name: production_database_url_v2
  
  api_key:
    external: true
    name: production_api_key_v1
  
  jwt_secret:
    external: true
    name: production_jwt_secret_v3
```

**Application Code for Secrets:**
```python
# secrets_manager.py
import os
from pathlib import Path
from typing import Optional, Dict
from dataclasses import dataclass
import json

@dataclass
class Secret:
    """A secret value with metadata"""
    value: str
    name: str
    version: Optional[str] = None
    expires_at: Optional[str] = None

class SecretsManager:
    """
    Secure secrets management for containers
    
    Because environment variables are visible to 
    anyone who can run 'docker inspect'
    """
    
    def __init__(self):
        self.secrets_cache: Dict[str, Secret] = {}
        self.secrets_dir = Path("/run/secrets")
        
    def get_secret(self, secret_name: str, required: bool = True) -> Optional[str]:
        """Get secret value safely"""
        
        # Check cache first
        if secret_name in self.secrets_cache:
            return self.secrets_cache[secret_name].value
        
        # Try Docker secrets first (production)
        secret_file = self.secrets_dir / secret_name
        if secret_file.exists():
            try:
                secret_value = secret_file.read_text().strip()
                
                # Cache the secret
                self.secrets_cache[secret_name] = Secret(
                    value=secret_value,
                    name=secret_name
                )
                
                return secret_value
                
            except Exception as e:
                if required:
                    raise RuntimeError(f"Failed to read secret {secret_name}: {e}")
                return None
        
        # Fallback to environment variable file (development)
        env_file_var = f"{secret_name.upper()}_FILE"
        env_file_path = os.getenv(env_file_var)
        
        if env_file_path and Path(env_file_path).exists():
            try:
                secret_value = Path(env_file_path).read_text().strip()
                
                self.secrets_cache[secret_name] = Secret(
                    value=secret_value,
                    name=secret_name
                )
                
                return secret_value
                
            except Exception as e:
                if required:
                    raise RuntimeError(f"Failed to read secret file {env_file_path}: {e}")
                return None
        
        # Last resort: environment variable (not recommended for production)
        env_value = os.getenv(secret_name.upper())
        if env_value:
            self.secrets_cache[secret_name] = Secret(
                value=env_value,
                name=secret_name
            )
            return env_value
        
        if required:
            raise RuntimeError(f"Secret {secret_name} not found")
        
        return None
    
    def get_database_url(self) -> str:
        """Get database URL from secrets"""
        return self.get_secret("database_url")
    
    def get_api_key(self, service_name: str) -> str:
        """Get API key for specific service"""
        return self.get_secret(f"{service_name}_api_key")
    
    def get_jwt_secret(self) -> str:
        """Get JWT signing secret"""
        return self.get_secret("jwt_secret")
    
    def rotate_secret(self, secret_name: str):
        """Remove secret from cache to force reload"""
        if secret_name in self.secrets_cache:
            del self.secrets_cache[secret_name]
    
    def health_check(self) -> bool:
        """Check if all required secrets are available"""
        required_secrets = [
            "database_url",
            "jwt_secret"
        ]
        
        try:
            for secret_name in required_secrets:
                if not self.get_secret(secret_name, required=False):
                    return False
            return True
        except:
            return False

# Usage in your application
secrets = SecretsManager()

# Database connection
DATABASE_URL = secrets.get_database_url()

# API keys
OPENAI_API_KEY = secrets.get_api_key("openai")

# JWT secret for authentication
JWT_SECRET = secrets.get_jwt_secret()
```

**Kubernetes Secrets Integration:**
```yaml
# k8s-secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: production
type: Opaque
data:
  # Base64 encoded values (not secure by themselves)
  database-url: <base64-encoded-database-url>
  api-key: <base64-encoded-api-key>
  jwt-secret: <base64-encoded-jwt-secret>

---
# Deployment with secrets mounted as files
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
    spec:
      containers:
      - name: app
        image: your-registry.com/your-app:secure
        
        # Mount secrets as files (not environment variables)
        volumeMounts:
        - name: secrets-volume
          mountPath: /run/secrets
          readOnly: true
        
        # Security context
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
        
        # Resource limits
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
          requests:
            memory: "256Mi"
            cpu: "250m"
        
        # Liveness and readiness probes
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
      
      volumes:
      - name: secrets-volume
        secret:
          secretName: app-secrets
```

**HashiCorp Vault Integration:**
```python
# vault_secrets.py
import hvac
import os
from typing import Dict, Optional

class VaultSecretsManager:
    """
    HashiCorp Vault integration for container secrets
    
    Because proper secret rotation is not optional
    """
    
    def __init__(self):
        self.vault_addr = os.getenv("VAULT_ADDR", "https://vault.internal:8200")
        self.vault_token = self._get_vault_token()
        
        self.client = hvac.Client(
            url=self.vault_addr,
            token=self.vault_token
        )
        
        if not self.client.is_authenticated():
            raise RuntimeError("Failed to authenticate with Vault")
    
    def _get_vault_token(self) -> str:
        """Get Vault token from file (mounted by Vault agent)"""
        token_file = Path("/var/run/secrets/vault/token")
        
        if token_file.exists():
            return token_file.read_text().strip()
        
        # Fallback to environment variable (not recommended)
        token = os.getenv("VAULT_TOKEN")
        if not token:
            raise RuntimeError("Vault token not found")
        
        return token
    
    def get_secret(self, path: str, key: str) -> str:
        """Get secret from Vault"""
        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point="secret"
            )
            
            secret_data = response['data']['data']
            return secret_data[key]
            
        except Exception as e:
            raise RuntimeError(f"Failed to read secret {path}/{key}: {e}")
    
    def get_database_credentials(self) -> Dict[str, str]:
        """Get dynamic database credentials"""
        try:
            response = self.client.secrets.database.generate_credentials(
                name="postgres-app-role"
            )
            
            return {
                'username': response['data']['username'],
                'password': response['data']['password'],
                'lease_id': response['lease_id']
            }
            
        except Exception as e:
            raise RuntimeError(f"Failed to get database credentials: {e}")
    
    def renew_lease(self, lease_id: str):
        """Renew a Vault lease"""
        try:
            self.client.sys.renew_lease(lease_id)
        except Exception as e:
            print(f"Failed to renew lease {lease_id}: {e}")
```

**Secret Rotation Automation:**
```bash
#!/bin/bash
# rotate_secrets.sh

set -euo pipefail

# Script to rotate secrets in production
NAMESPACE=${NAMESPACE:-production}
SECRET_NAME=${SECRET_NAME:-app-secrets}

echo "Starting secret rotation for ${SECRET_NAME} in ${NAMESPACE}"

# Generate new secrets
NEW_JWT_SECRET=$(openssl rand -base64 32)
NEW_API_KEY=$(uuidgen)

# Create new secret version
kubectl create secret generic "${SECRET_NAME}-new" \
  --namespace="${NAMESPACE}" \
  --from-literal=jwt-secret="${NEW_JWT_SECRET}" \
  --from-literal=api-key="${NEW_API_KEY}" \
  --from-file=database-url=/run/secrets/database_url

# Update deployment to use new secret
kubectl patch deployment secure-app \
  --namespace="${NAMESPACE}" \
  --patch='{"spec":{"template":{"spec":{"volumes":[{"name":"secrets-volume","secret":{"secretName":"'${SECRET_NAME}'-new"}}]}}}}'

# Wait for rollout to complete
kubectl rollout status deployment/secure-app --namespace="${NAMESPACE}"

# Verify deployment health
kubectl wait --for=condition=available --timeout=300s deployment/secure-app --namespace="${NAMESPACE}"

# Clean up old secret
kubectl delete secret "${SECRET_NAME}" --namespace="${NAMESPACE}" || true

# Rename new secret to original name
kubectl get secret "${SECRET_NAME}-new" --namespace="${NAMESPACE}" -o yaml | \
  sed "s/${SECRET_NAME}-new/${SECRET_NAME}/" | \
  kubectl apply -f -

kubectl delete secret "${SECRET_NAME}-new" --namespace="${NAMESPACE}"

echo "Secret rotation completed successfully"
```

---

## Network Security and Isolation

### Building Digital Moats Around Your Containers

Network security for containers is like designing a castle - you want multiple layers of defense, and you definitely don't want to leave the drawbridge down.

**The Wrong Way (Welcome to Hack City):**
```yaml
# docker-compose.yml - The "Please Hack Me" Edition
version: '3.8'

services:
  web:
    image: my-app:latest
    ports:
      - "80:80"        # Exposed to the world
      - "443:443"      # Also exposed
      - "3000:3000"    # Debug port exposed (oops)
      - "5432:5432"    # Database port exposed (double oops)
      - "6379:6379"    # Redis exposed (triple oops)
    
    # No network isolation
    network_mode: "host"  # Shares host network (nightmare fuel)
```

**The Right Way (Fort Knox for Containers):**
```yaml
# docker-compose.yml - The "Actually Secure" Edition
version: '3.8'

services:
  # Web tier (only thing exposed to internet)
  nginx:
    image: cgr.dev/chainguard/nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/ssl:ro
    networks:
      - frontend
    depends_on:
      - web-app
    
    # Security hardening
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    read_only: true
    tmpfs:
      - /var/cache/nginx:size=100M
      - /var/run:size=50M

  # Application tier (internal only)
  web-app:
    image: your-app:secure
    # No external ports exposed
    expose:
      - "8000"
    networks:
      - frontend
      - backend
    environment:
      - DATABASE_URL_FILE=/run/secrets/database_url
    secrets:
      - database_url
    
    # Security context
    user: "1000:1000"
    cap_drop:
      - ALL
    read_only: true
    tmpfs:
      - /tmp:size=100M,uid=1000,gid=1000

  # Database tier (most restricted)
  postgres:
    image: cgr.dev/chainguard/postgres:latest
    # Only accessible from backend network
    expose:
      - "5432"
    networks:
      - backend
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password
    secrets:
      - postgres_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    
    # Ultra-restricted security
    user: "70:70"  # postgres user
    cap_drop:
      - ALL
    read_only: true
    tmpfs:
      - /tmp:size=50M
      - /run:size=50M

  # Redis (cache tier)
  redis:
    image: cgr.dev/chainguard/redis:latest
    expose:
      - "6379"
    networks:
      - backend
    command: ["redis-server", "--appendonly", "yes", "--requirepass", "$(cat /run/secrets/redis_password)"]
    secrets:
      - redis_password
    
    user: "999:999"  # redis user
    cap_drop:
      - ALL
    read_only: true
    tmpfs:
      - /tmp:size=50M

# Network isolation (the moat around your castle)
networks:
  frontend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/24
    driver_opts:
      com.docker.network.bridge.enable_icc: "false"  # Disable inter-container communication
  
  backend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.21.0.0/24
    internal: true  # No internet access
    driver_opts:
      com.docker.network.bridge.enable_icc: "true"   # Allow backend communication

volumes:
  postgres_data:
    driver: local

secrets:
  database_url:
    external: true
  postgres_password:
    external: true
  redis_password:
    external: true
```

**Nginx Security Configuration:**
```nginx
# nginx.conf - The "Not Getting Pwned Today" Edition
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    # Security headers (because security is not optional)
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Hide nginx version (security through obscurity is still obscurity)
    server_tokens off;
    
    # DDoS protection
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
    limit_req_zone $binary_remote_addr zone=api:10m rate=100r/m;
    limit_req_zone $binary_remote_addr zone=general:10m rate=200r/m;
    
    # Connection limits
    limit_conn_zone $binary_remote_addr zone=conn_limit_per_ip:10m;
    
    # Basic security settings
    client_max_body_size 10M;
    client_body_timeout 60s;
    client_header_timeout 60s;
    keepalive_timeout 65s;
    send_timeout 60s;
    
    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    'rt=$request_time uct="$upstream_connect_time" '
                    'uht="$upstream_header_time" urt="$upstream_response_time"';
    
    access_log /var/log/nginx/access.log main;

    # Main application
    upstream app_backend {
        server web-app:8000 max_fails=3 fail_timeout=30s;
        keepalive 32;
    }

    server {
        listen 80;
        server_name _;
        
        # Redirect HTTP to HTTPS
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;
        
        # SSL configuration
        ssl_certificate /etc/ssl/cert.pem;
        ssl_certificate_key /etc/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
        ssl_prefer_server_ciphers off;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;
        
        # Rate limiting
        limit_req zone=general burst=20 nodelay;
        limit_conn conn_limit_per_ip 10;
        
        # Block common attack patterns
        location ~ /\. {
            deny all;
            access_log off;
            log_not_found off;
        }
        
        location ~ \.(htaccess|htpasswd|ini|log|sh|inc|bak)$ {
            deny all;
            access_log off;
            log_not_found off;
        }
        
        # API endpoints with stricter rate limiting
        location /api/ {
            limit_req zone=api burst=50 nodelay;
            
            proxy_pass http://app_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Timeouts
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
        }
        
        # Login endpoints with very strict rate limiting
        location /auth/login {
            limit_req zone=login burst=3 nodelay;
            
            proxy_pass http://app_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Static files
        location /static/ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
        
        # Main application
        location / {
            limit_req zone=general burst=20 nodelay;
            
            proxy_pass http://app_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Security timeouts
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
        }
    }
}
```

### Container Network Policies

**Kubernetes Network Policies (The Firewall Rules for Containers):**
```yaml
# network-policies.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-default
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  # Default deny all (whitelist approach)

---
# Allow frontend to access backend
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-to-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      tier: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          tier: frontend
    ports:
    - protocol: TCP
      port: 8000

---
# Allow backend to access database
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-to-database
  namespace: production
spec:
  podSelector:
    matchLabels:
      tier: database
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          tier: backend
    ports:
    - protocol: TCP
      port: 5432

---
# Allow egress to external APIs (DNS, etc.)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-external-egress
  namespace: production
spec:
  podSelector:
    matchLabels:
      tier: backend
  policyTypes:
  - Egress
  egress:
  # Allow DNS
  - to: []
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
  
  # Allow HTTPS to specific external services
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: TCP
      port: 443
  
  # Block everything else by default
```

**Service Mesh with Istio (Next-Level Security):**
```yaml
# istio-security.yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: strict-mtls
  namespace: production
spec:
  mtls:
    mode: STRICT  # Enforce mutual TLS for all communication

---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: frontend-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: web-app
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/nginx"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*", "/health"]
  - when:
    - key: source.ip
      values: ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]

---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: database-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: postgres
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/web-app"]
    to:
    - operation:
        ports: ["5432"]
  # Deny all other access
```

---

## The Production-Ready Container Stack

### Putting It All Together (The "Actually Works in Production" Edition)

Now let's build a complete, production-ready container stack that incorporates all the security practices we've covered.

**Complete Production Stack:**
```yaml
# docker-compose.production.yml
version: '3.8'

services:
  # Load Balancer / Reverse Proxy
  nginx:
    image: cgr.dev/chainguard/nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/ssl:ro
    networks:
      - frontend
    depends_on:
      - web-app
    restart: unless-stopped
    
    # Security hardening
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    read_only: true
    tmpfs:
      - /var/cache/nginx:size=100M
      - /var/run:size=50M
    
    # Resource limits
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.5'
        reservations:
          memory: 128M
          cpus: '0.25'
    
    # Health check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Application Layer
  web-app:
    image: your-registry.com/your-app:${VERSION:-latest}
    expose:
      - "8000"
    networks:
      - frontend
      - backend
    environment:
      - DATABASE_URL_FILE=/run/secrets/database_url
      - REDIS_URL_FILE=/run/secrets/redis_url
      - JWT_SECRET_FILE=/run/secrets/jwt_secret
      - ENVIRONMENT=production
    secrets:
      - database_url
      - redis_url
      - jwt_secret
    
    # Security context
    user: "1000:1000"
    cap_drop:
      - ALL
    read_only: true
    tmpfs:
      - /tmp:size=100M,uid=1000,gid=1000,mode=1777
      - /var/cache:size=50M,uid=1000,gid=1000,mode=755
    
    # Resource limits
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
        reservations:
          memory: 512M
          cpus: '0.5'
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
    
    # Health checks
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Database
  postgres:
    image: cgr.dev/chainguard/postgres:latest
    expose:
      - "5432"
    networks:
      - backend
    environment:
      - POSTGRES_DB=app_db
      - POSTGRES_USER=app_user
      - POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password
      - POSTGRES_INITDB_ARGS=--auth-host=scram-sha-256
    secrets:
      - postgres_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgres/postgresql.conf:/etc/postgresql/postgresql.conf:ro
      - ./postgres/pg_hba.conf:/etc/postgresql/pg_hba.conf:ro
    
    # Security hardening
    user: "70:70"
    cap_drop:
      - ALL
    read_only: true
    tmpfs:
      - /tmp:size=100M
      - /run:size=100M
      - /run/postgresql:size=100M
    
    # Resource limits
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.5'
        reservations:
          memory: 1G
          cpus: '0.75'
    
    # Health check
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app_user -d app_db"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Cache Layer
  redis:
    image: cgr.dev/chainguard/redis:latest
    expose:
      - "6379"
    networks:
      - backend
    command: [
      "redis-server",
      "--appendonly", "yes",
      "--requirepass", "$(cat /run/secrets/redis_password)",
      "--maxmemory", "256mb",
      "--maxmemory-policy", "allkeys-lru"
    ]
    secrets:
      - redis_password
    volumes:
      - redis_data:/data
    
    # Security
    user: "999:999"
    cap_drop:
      - ALL
    read_only: true
    tmpfs:
      - /tmp:size=50M
    
    # Resource limits
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
    
    # Health check
    healthcheck:
      test: ["CMD", "redis-cli", "--pass", "$(cat /run/secrets/redis_password)", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Security Monitoring
  security-monitor:
    image: your-registry.com/security-monitor:${VERSION:-latest}
    networks:
      - monitoring
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /var/log:/var/log:ro
    environment:
      - ALERT_WEBHOOK_URL_FILE=/run/secrets/alert_webhook_url
    secrets:
      - alert_webhook_url
    
    # Security context
    user: "1001:1001"
    cap_drop:
      - ALL
    read_only: true
    tmpfs:
      - /tmp:size=50M
    
    # Resource limits
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.25'

# Secure Networks
networks:
  frontend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/24
    driver_opts:
      com.docker.network.bridge.enable_icc: "false"
  
  backend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.21.0.0/24
    internal: true
    driver_opts:
      com.docker.network.bridge.enable_icc: "true"
  
  monitoring:
    driver: bridge
    ipam:
      config:
        - subnet: 172.22.0.0/24
    internal: true

# Persistent Volumes
volumes:
  postgres_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /var/lib/docker/volumes/postgres_data
  
  redis_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /var/lib/docker/volumes/redis_data

# Secrets (managed externally)
secrets:
  database_url:
    external: true
    name: production_database_url_v2
  
  postgres_password:
    external: true
    name: production_postgres_password_v3
  
  redis_url:
    external: true
    name: production_redis_url_v1
  
  redis_password:
    external: true
    name: production_redis_password_v2
  
  jwt_secret:
    external: true
    name: production_jwt_secret_v4
  
  alert_webhook_url:
    external: true
    name: production_alert_webhook_url_v1
```

**Production Deployment Script:**
```bash
#!/bin/bash
# deploy.sh - Production deployment with security checks

set -euo pipefail

VERSION=${1:-latest}
ENVIRONMENT=${2:-production}

echo "🚀 Starting secure deployment of version ${VERSION} to ${ENVIRONMENT}"

# Pre-deployment security checks
echo "🔍 Running pre-deployment security checks..."

# 1. Scan container images
echo "  📊 Scanning container images for vulnerabilities..."
trivy image "your-registry.com/your-app:${VERSION}" --exit-code 1 --severity HIGH,CRITICAL

# 2. Verify image signatures
echo "  ✍️  Verifying image signatures..."
cosign verify "your-registry.com/your-app:${VERSION}" \
  --certificate-identity-regexp '^https://github\.com/your-org/your-app/\.github/workflows/.+@refs/heads/main$' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com

# 3. Check secrets exist
echo "  🔐 Verifying secrets exist..."
required_secrets=(
  "production_database_url_v2"
  "production_postgres_password_v3"
  "production_redis_url_v1"
  "production_redis_password_v2"
  "production_jwt_secret_v4"
  "production_alert_webhook_url_v1"
)

for secret in "${required_secrets[@]}"; do
  if ! docker secret inspect "${secret}" >/dev/null 2>&1; then
    echo "❌ Secret ${secret} not found"
    exit 1
  fi
done

# 4. Check network requirements
echo "  🌐 Verifying network setup..."
if ! docker network inspect production_frontend >/dev/null 2>&1; then
  echo "Creating frontend network..."
  docker network create production_frontend
fi

# 5. Backup databases
echo "  💾 Creating database backup..."
docker-compose -f docker-compose.production.yml exec -T postgres \
  pg_dump -U app_user app_db | \
  gzip > "backup-$(date +%Y%m%d-%H%M%S).sql.gz"

# Deploy with rolling update
echo "🔄 Starting rolling deployment..."

# Export version for docker-compose
export VERSION="${VERSION}"

# Pull latest images
docker-compose -f docker-compose.production.yml pull

# Start new services
docker-compose -f docker-compose.production.yml up -d --remove-orphans

# Wait for health checks
echo "⏳ Waiting for services to be healthy..."
for service in nginx web-app postgres redis; do
  echo "  Checking ${service}..."
  timeout 300 bash -c "until docker-compose -f docker-compose.production.yml ps ${service} | grep -q 'healthy'; do sleep 5; done"
done

# Run post-deployment tests
echo "🧪 Running post-deployment tests..."

# 1. Health check endpoints
curl -f "https://your-domain.com/health" || exit 1

# 2. Database connectivity
docker-compose -f docker-compose.production.yml exec -T postgres \
  psql -U app_user -d app_db -c "SELECT 1;" >/dev/null || exit 1

# 3. Redis connectivity
docker-compose -f docker-compose.production.yml exec -T redis \
  redis-cli --pass "$(docker secret inspect production_redis_password_v2 --format '{{.Spec.Data}}')" ping | grep -q PONG || exit 1

# 4. Security headers check
if ! curl -sI "https://your-domain.com" | grep -q "Strict-Transport-Security"; then
  echo "❌ Security headers missing"
  exit 1
fi

# Clean up old images
echo "🧹 Cleaning up old images..."
docker image prune -f --filter "until=24h"

echo "✅ Deployment completed successfully!"
echo "📊 Deployment summary:"
echo "  Version: ${VERSION}"
echo "  Environment: ${ENVIRONMENT}"
echo "  Services: $(docker-compose -f docker-compose.production.yml ps --services | wc -l)"
echo "  Healthy containers: $(docker-compose -f docker-compose.production.yml ps | grep -c healthy)"

# Send notification
curl -X POST "${SLACK_WEBHOOK_URL}" \
  -H 'Content-type: application/json' \
  --data "{\"text\":\"🚀 Production deployment of ${VERSION} completed successfully!\"}" || true
```

**Container Security Monitoring Dashboard:**
```python
# monitoring_dashboard.py
import docker
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class SecurityMetric:
    container_id: str
    container_name: str
    image: str
    vulnerability_count: int
    last_updated: datetime
    running_as_root: bool
    privileged: bool
    network_mode: str
    security_score: float

class SecurityDashboard:
    """
    Real-time security dashboard for production containers
    
    Because ignorance is not bliss when it comes to security
    """
    
    def __init__(self):
        self.client = docker.from_env()
        self.metrics_history: List[SecurityMetric] = []
    
    def generate_security_report(self) -> Dict:
        """Generate comprehensive security report"""
        
        containers = self.client.containers.list()
        metrics = []
        
        for container in containers:
            metric = self.analyze_container_security(container)
            metrics.append(metric)
        
        # Calculate overall security score
        overall_score = sum(m.security_score for m in metrics) / len(metrics) if metrics else 0
        
        # Identify critical issues
        critical_issues = [
            m for m in metrics 
            if m.security_score < 50 or m.running_as_root or m.privileged
        ]
        
        # Generate recommendations
        recommendations = self.generate_recommendations(metrics)
        
        report = {
            'timestamp': datetime.utcnow().isoformat(),
            'overall_security_score': round(overall_score, 2),
            'total_containers': len(metrics),
            'critical_issues': len(critical_issues),
            'containers': [
                {
                    'name': m.container_name,
                    'image': m.image,
                    'security_score': m.security_score,
                    'vulnerabilities': m.vulnerability_count,
                    'running_as_root': m.running_as_root,
                    'privileged': m.privileged
                }
                for m in metrics
            ],
            'critical_containers': [
                {
                    'name': m.container_name,
                    'issues': self.get_container_issues(m)
                }
                for m in critical_issues
            ],
            'recommendations': recommendations
        }
        
        # Store in history
        self.metrics_history.extend(metrics)
        
        # Keep only last 24 hours
        cutoff = datetime.utcnow() - timedelta(hours=24)
        self.metrics_history = [
            m for m in self.metrics_history 
            if m.last_updated > cutoff
        ]
        
        return report
    
    def analyze_container_security(self, container) -> SecurityMetric:
        """Analyze security of a single container"""
        
        # Get container configuration
        config = container.attrs['Config']
        host_config = container.attrs['HostConfig']
        
        # Check if running as root
        user = config.get('User', '')
        running_as_root = not user or user == 'root' or user == '0'
        
        # Check if privileged
        privileged = host_config.get('Privileged', False)
        
        # Get network mode
        network_mode = host_config.get('NetworkMode', 'default')
        
        # Calculate security score
        security_score = self.calculate_security_score(
            running_as_root=running_as_root,
            privileged=privileged,
            network_mode=network_mode,
            config=config,
            host_config=host_config
        )
        
        # Get vulnerability count (placeholder - would integrate with scanner)
        vulnerability_count = self.get_vulnerability_count(container.image)
        
        return SecurityMetric(
            container_id=container.id[:12],
            container_name=container.name,
            image=container.image.tags[0] if container.image.tags else 'unknown',
            vulnerability_count=vulnerability_count,
            last_updated=datetime.utcnow(),
            running_as_root=running_as_root,
            privileged=privileged,
            network_mode=network_mode,
            security_score=security_score
        )
    
    def calculate_security_score(self, **kwargs) -> float:
        """Calculate security score (0-100)"""
        score = 100.0
        
        # Major penalties
        if kwargs['running_as_root']:
            score -= 30
        
        if kwargs['privileged']:
            score -= 40
        
        if kwargs['network_mode'] == 'host':
            score -= 25
        
        # Minor penalties
        host_config = kwargs['host_config']
        
        # Check for dangerous capabilities
        cap_add = host_config.get('CapAdd', [])
        if cap_add and 'ALL' in cap_add:
            score -= 20
        
        # Check for dangerous volumes
        binds = host_config.get('Binds', [])
        dangerous_mounts = ['/var/run/docker.sock', '/etc', '/root', '/home']
        for bind in binds:
            for dangerous in dangerous_mounts:
                if dangerous in bind:
                    score -= 15
                    break
        
        # Check for read-only filesystem
        if not host_config.get('ReadonlyRootfs', False):
            score -= 10
        
        return max(0.0, score)
    
    def get_vulnerability_count(self, image) -> int:
        """Get vulnerability count for image (placeholder)"""
        # This would integrate with Trivy, Clair, or other scanner
        # For now, return random number for demo
        import random
        return random.randint(0, 50)
    
    def get_container_issues(self, metric: SecurityMetric) -> List[str]:
        """Get list of security issues for container"""
        issues = []
        
        if metric.running_as_root:
            issues.append("Running as root user")
        
        if metric.privileged:
            issues.append("Running in privileged mode")
        
        if metric.network_mode == 'host':
            issues.append("Using host network mode")
        
        if metric.vulnerability_count > 10:
            issues.append(f"{metric.vulnerability_count} known vulnerabilities")
        
        if metric.security_score < 50:
            issues.append("Overall security score below threshold")
        
        return issues
    
    def generate_recommendations(self, metrics: List[SecurityMetric]) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        # Check for common issues
        root_containers = [m for m in metrics if m.running_as_root]
        if root_containers:
            recommendations.append(
                f"Configure {len(root_containers)} containers to run as non-root user"
            )
        
        privileged_containers = [m for m in metrics if m.privileged]
        if privileged_containers:
            recommendations.append(
                f"Remove privileged mode from {len(privileged_containers)} containers"
            )
        
        host_network_containers = [m for m in metrics if m.network_mode == 'host']
        if host_network_containers:
            recommendations.append(
                f"Use bridge networking instead of host mode for {len(host_network_containers)} containers"
            )
        
        vulnerable_containers = [m for m in metrics if m.vulnerability_count > 5]
        if vulnerable_containers:
            recommendations.append(
                f"Update base images for {len(vulnerable_containers)} containers with high vulnerability counts"
            )
        
        low_score_containers = [m for m in metrics if m.security_score < 70]
        if low_score_containers:
            recommendations.append(
                f"Review security configuration for {len(low_score_containers)} containers with low security scores"
            )
        
        return recommendations
    
    def export_report(self, report: Dict, format: str = 'json'):
        """Export report in various formats"""
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        
        if format == 'json':
            filename = f'security_report_{timestamp}.json'
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
        
        elif format == 'html':
            filename = f'security_report_{timestamp}.html'
            html_content = self.generate_html_report(report)
            with open(filename, 'w') as f:
                f.write(html_content)
        
        return filename
    
    def generate_html_report(self, report: Dict) -> str:
        """Generate HTML report"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Container Security Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .critical {{ color: red; }}
                .warning {{ color: orange; }}
                .good {{ color: green; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>Container Security Report</h1>
            <p><strong>Generated:</strong> {report['timestamp']}</p>
            <p><strong>Overall Security Score:</strong> 
                <span class="{'good' if report['overall_security_score'] > 80 else 'warning' if report['overall_security_score'] > 60 else 'critical'}">
                    {report['overall_security_score']}/100
                </span>
            </p>
            
            <h2>Summary</h2>
            <ul>
                <li>Total Containers: {report['total_containers']}</li>
                <li>Critical Issues: {report['critical_issues']}</li>
            </ul>
            
            <h2>Container Details</h2>
            <table>
                <tr>
                    <th>Container</th>
                    <th>Image</th>
                    <th>Security Score</th>
                    <th>Vulnerabilities</th>
                    <th>Running as Root</th>
                    <th>Privileged</th>
                </tr>
        """
        
        for container in report['containers']:
            score_class = 'good' if container['security_score'] > 80 else 'warning' if container['security_score'] > 60 else 'critical'
            html += f"""
                <tr>
                    <td>{container['name']}</td>
                    <td>{container['image']}</td>
                    <td class="{score_class}">{container['security_score']}</td>
                    <td>{container['vulnerabilities']}</td>
                    <td>{'Yes' if container['running_as_root'] else 'No'}</td>
                    <td>{'Yes' if container['privileged'] else 'No'}</td>
                </tr>
            """
        
        html += """
            </table>
            
            <h2>Recommendations</h2>
            <ul>
        """
        
        for rec in report['recommendations']:
            html += f"<li>{rec}</li>"
        
        html += """
            </ul>
        </body>
        </html>
        """
        
        return html

if __name__ == "__main__":
    dashboard = SecurityDashboard()
    report = dashboard.generate_security_report()
    
    print("Container Security Report")
    print("=" * 50)
    print(f"Overall Security Score: {report['overall_security_score']}/100")
    print(f"Total Containers: {report['total_containers']}")
    print(f"Critical Issues: {report['critical_issues']}")
    
    if report['critical_containers']:
        print("\nCritical Issues:")
        for container in report['critical_containers']:
            print(f"  {container['name']}:")
            for issue in container['issues']:
                print(f"    - {issue}")
    
    if report['recommendations']:
        print("\nRecommendations:")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"  {i}. {rec}")
    
    # Export reports
    json_file = dashboard.export_report(report, 'json')
    html_file = dashboard.export_report(report, 'html')
    
    print(f"\nReports exported:")
    print(f"  JSON: {json_file}")
    print(f"  HTML: {html_file}")
```

---

## The Bottom Line

Container security isn't rocket science, but it's also not "set it and forget it." It's more like "set it up right once, then continuously monitor it because the internet is a hostile place full of people who want to steal your stuff."

**The Container Security Hierarchy of Needs:**

1. **Basic Hygiene**: Use minimal base images, don't run as root
2. **Supply Chain**: Verify what you're installing, sign what you're deploying  
3. **Runtime Protection**: Monitor, limit, and isolate your containers
4. **Network Security**: Build proper firewalls between your services
5. **Secrets Management**: Handle sensitive data like it's actually sensitive
6. **Continuous Monitoring**: Watch for threats in real-time

**Remember:**
- Security is not a feature you add at the end - it's the foundation you build on
- The best security is the kind you don't have to think about because it's built into your process
- A container that's compromised in 5 minutes is not "faster to deploy"
- If your security depends on hoping attackers won't find you, you're already compromised

**Your Mission:**
Build containers that are secure by default, monitored by design, and updated automatically. Because manual security is an oxymoron, and insecure containers are just expensive ways to get pwned.

Now go forth and containerize responsibly. The internet is watching, and some of it wants to steal your lunch money.

---

*"The best container security is the kind that works even when you're asleep, on vacation, or having an existential crisis about whether Kubernetes was a mistake."* - Ancient DevOps Wisdom