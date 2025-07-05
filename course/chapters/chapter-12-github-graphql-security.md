# Chapter 12: GitHub GraphQL API Security Mastery
## *Or: How to Query, Scan, and Secure Your Codebase at Scale*

> "The API is the window to your data. Make sure it's bulletproof glass, not tissue paper." - Security Engineer's Mantra

## Table of Contents
- [Introduction: Why GraphQL for Security?](#introduction-why-graphql-for-security)
- [Learning Objectives](#learning-objectives)
- [Foundation: GraphQL Fundamentals](#foundation-graphql-fundamentals)
- [Security-First Authentication](#security-first-authentication)
- [Dependency Vulnerability Scanning](#dependency-vulnerability-scanning)
- [Repository Security Analysis](#repository-security-analysis)
- [Automated Security Monitoring](#automated-security-monitoring)
- [Rate Limiting and Best Practices](#rate-limiting-and-best-practices)
- [Real-World Security Workflows](#real-world-security-workflows)
- [Troubleshooting and Common Issues](#troubleshooting-and-common-issues)
- [Pro Tips and Advanced Techniques](#pro-tips-and-advanced-techniques)

---

## Introduction: Why GraphQL for Security?

GitHub's GraphQL API isn't just another way to query data - it's a powerful security tool that lets you extract comprehensive insights about your repositories, dependencies, and vulnerabilities with surgical precision. Unlike REST APIs where you make dozens of requests to gather security data, GraphQL lets you fetch everything in a single, efficient query.

**What Makes GitHub GraphQL Special for Security:**
- **Comprehensive vulnerability data**: Access to Dependabot alerts, security advisories, and code scanning results
- **Dependency analysis**: Complete dependency trees with vulnerability information
- **Audit capabilities**: Track who has access to what, when changes were made, and security-relevant events
- **Flexible querying**: Get exactly the security data you need without over-fetching
- **Real-time insights**: Access the latest security information as it becomes available

**Key Security Use Cases:**
- Scanning repositories for vulnerable dependencies
- Monitoring security advisories and alerts
- Auditing repository permissions and access
- Tracking security-relevant commits and changes
- Generating compliance reports
- Automating vulnerability response workflows

---

## Learning Objectives

By the end of this chapter, you'll be able to:

1. **🔐 Secure API Authentication**: Set up and manage GitHub tokens with proper scoping
2. **🔍 Dependency Scanning**: Query and analyze repository dependencies for vulnerabilities
3. **📊 Security Reporting**: Generate comprehensive security reports and dashboards
4. **🤖 Automated Monitoring**: Build tools that continuously monitor for security issues
5. **⚡ Performance Optimization**: Use GraphQL efficiently with proper rate limiting
6. **🛡️ Defensive Security**: Implement security-first practices in your workflows

---

## Foundation: GraphQL Fundamentals

### Learning Plan Step 1: Understanding GraphQL Structure

**Objective**: Master the basics of GraphQL queries and GitHub's schema

**Time Investment**: 30 minutes

**What You'll Learn**:
- GraphQL syntax and structure
- GitHub's schema organization
- Query composition and nesting
- Field selection and aliases

### Step 1.1: Your First Security Query

Let's start with a simple query to understand the structure:

```graphql
query BasicSecurityInfo {
  viewer {
    login
    repositories(first: 5, orderBy: {field: UPDATED_AT, direction: DESC}) {
      nodes {
        name
        isPrivate
        primaryLanguage {
          name
        }
        vulnerabilityAlerts(first: 10) {
          totalCount
          nodes {
            createdAt
            securityVulnerability {
              severity
              package {
                name
              }
            }
          }
        }
      }
    }
  }
}
```

**What This Query Does**:
1. Gets your user information (`viewer`)
2. Fetches your 5 most recently updated repositories
3. For each repository, shows:
   - Name and privacy status
   - Primary programming language
   - First 10 vulnerability alerts
   - Severity and package information

### Step 1.2: Setting Up Your Development Environment

**Prerequisites**:
- Python 3.8+ (for our examples)
- A GitHub account with repository access
- Basic understanding of APIs

**Setup Instructions**:

```bash
# Create a new project directory
mkdir github-graphql-security
cd github-graphql-security

# Set up Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install requests python-dotenv pydantic

# Create project structure
mkdir -p src/github_security/{queries,models,utils}
touch src/github_security/__init__.py
touch src/github_security/client.py
touch src/github_security/models/__init__.py
touch src/github_security/queries/__init__.py
touch src/github_security/utils/__init__.py
```

### Step 1.3: Creating a Secure GraphQL Client

**File**: `src/github_security/client.py`

```python
"""
GitHub GraphQL Client with Security Focus
"""
import os
import time
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


@dataclass
class RateLimitInfo:
    """Track GitHub API rate limiting"""
    limit: int
    remaining: int
    reset_at: int
    
    @property
    def reset_time_readable(self) -> str:
        """Convert reset timestamp to readable format"""
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.reset_at))


class GitHubGraphQLClient:
    """
    Secure GitHub GraphQL API client with rate limiting and error handling
    """
    
    def __init__(self, token: str, base_url: str = "https://api.github.com"):
        """
        Initialize the GitHub GraphQL client
        
        Args:
            token: GitHub personal access token
            base_url: GitHub API base URL (for GitHub Enterprise)
        """
        self.token = token
        self.base_url = base_url
        self.graphql_url = urljoin(base_url, "/graphql")
        
        # Configure session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set secure headers
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "GitHub-Security-Scanner/1.0",
            "Accept": "application/vnd.github.v4+json"
        })
        
        # Rate limiting tracking
        self.rate_limit_info: Optional[RateLimitInfo] = None
    
    def execute_query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a GraphQL query with security best practices
        
        Args:
            query: GraphQL query string
            variables: Query variables
            
        Returns:
            Query response data
            
        Raises:
            GraphQLError: If query execution fails
            RateLimitError: If rate limit is exceeded
        """
        # Check rate limit before making request
        if self.rate_limit_info and self.rate_limit_info.remaining < 10:
            wait_time = self.rate_limit_info.reset_at - time.time()
            if wait_time > 0:
                print(f"Rate limit low ({self.rate_limit_info.remaining} remaining). "
                      f"Waiting {wait_time:.0f} seconds...")
                time.sleep(wait_time + 1)
        
        payload = {
            "query": query,
            "variables": variables or {}
        }
        
        try:
            response = self.session.post(
                self.graphql_url,
                json=payload,
                timeout=30
            )
            
            # Update rate limit info
            self._update_rate_limit_info(response.headers)
            
            # Handle HTTP errors
            response.raise_for_status()
            
            result = response.json()
            
            # Handle GraphQL errors
            if "errors" in result:
                raise GraphQLError(f"GraphQL errors: {result['errors']}")
            
            return result.get("data", {})
            
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Request failed: {e}")
    
    def _update_rate_limit_info(self, headers: Dict[str, str]) -> None:
        """Update rate limit information from response headers"""
        try:
            self.rate_limit_info = RateLimitInfo(
                limit=int(headers.get("x-ratelimit-limit", 0)),
                remaining=int(headers.get("x-ratelimit-remaining", 0)),
                reset_at=int(headers.get("x-ratelimit-reset", 0))
            )
        except (ValueError, TypeError):
            pass  # Headers might not be present in all responses
    
    def get_rate_limit_status(self) -> Dict[str, Any]:
        """
        Get current rate limit status
        
        Returns:
            Rate limit information including remaining requests
        """
        query = """
        query {
          rateLimit {
            limit
            remaining
            resetAt
          }
        }
        """
        
        result = self.execute_query(query)
        return result.get("rateLimit", {})


class GraphQLError(Exception):
    """Exception raised for GraphQL query errors"""
    pass


class RateLimitError(Exception):
    """Exception raised when rate limit is exceeded"""
    pass
```

**Key Security Features**:
1. **Token Management**: Secure token handling with proper headers
2. **Rate Limiting**: Built-in rate limit tracking and throttling
3. **Error Handling**: Comprehensive error handling for network and GraphQL errors
4. **Retry Logic**: Automatic retry with exponential backoff
5. **Security Headers**: Proper user agent and content type headers

---

## Security-First Authentication

### Learning Plan Step 2: Secure Token Management

**Objective**: Set up secure authentication with proper token scoping

**Time Investment**: 20 minutes

**What You'll Learn**:
- GitHub token creation and scoping
- Secure token storage and handling
- Permission validation and testing

### Step 2.1: Creating a GitHub Personal Access Token

**Security-First Approach**:

1. **Navigate to GitHub Settings**:
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"

2. **Configure Token Scopes** (principle of least privilege):
   ```
   Essential Scopes for Security Scanning:
   ✅ repo                    # Access to repository data
   ✅ read:org               # Read organization membership
   ✅ read:packages          # Read package information
   ✅ read:project           # Read project boards
   ✅ security_events        # Read security events
   ✅ read:discussion        # Read discussions
   
   Optional Scopes (add only if needed):
   ⚠️  write:packages        # Only if you need to update packages
   ⚠️  admin:repo_hook       # Only if you need webhook management
   ```

3. **Token Storage Best Practices**:

**File**: `.env` (never commit this file!)

```bash
# GitHub API Configuration
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_BASE_URL=https://api.github.com

# Security Configuration
SECURITY_SCAN_ENABLED=true
VULNERABILITY_THRESHOLD=high
NOTIFICATION_EMAIL=security@yourcompany.com
```

**File**: `.env.example` (commit this template)

```bash
# GitHub API Configuration
GITHUB_TOKEN=your_github_token_here
GITHUB_BASE_URL=https://api.github.com

# Security Configuration
SECURITY_SCAN_ENABLED=true
VULNERABILITY_THRESHOLD=high
NOTIFICATION_EMAIL=your-email@example.com
```

### Step 2.2: Secure Configuration Management

**File**: `src/github_security/config.py`

```python
"""
Secure configuration management for GitHub security scanning
"""
import os
from pathlib import Path
from typing import Optional
from enum import Enum

from dotenv import load_dotenv


class VulnerabilityThreshold(Enum):
    """Vulnerability severity thresholds"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class SecurityConfig:
    """
    Secure configuration management with validation
    """
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration from environment variables
        
        Args:
            env_file: Path to .env file (optional)
        """
        if env_file:
            load_dotenv(env_file)
        else:
            # Try to load from standard locations
            for env_path in [".env", Path.home() / ".github-security.env"]:
                if Path(env_path).exists():
                    load_dotenv(env_path)
                    break
        
        self._validate_required_settings()
    
    @property
    def github_token(self) -> str:
        """GitHub API token (required)"""
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        
        # Basic token validation
        if not token.startswith(("ghp_", "gho_", "ghu_", "ghs_", "ghr_")):
            raise ValueError("Invalid GitHub token format")
        
        return token
    
    @property
    def github_base_url(self) -> str:
        """GitHub API base URL"""
        return os.getenv("GITHUB_BASE_URL", "https://api.github.com")
    
    @property
    def vulnerability_threshold(self) -> VulnerabilityThreshold:
        """Minimum vulnerability severity to report"""
        threshold = os.getenv("VULNERABILITY_THRESHOLD", "high").lower()
        try:
            return VulnerabilityThreshold(threshold)
        except ValueError:
            return VulnerabilityThreshold.HIGH
    
    @property
    def security_scan_enabled(self) -> bool:
        """Whether security scanning is enabled"""
        return os.getenv("SECURITY_SCAN_ENABLED", "true").lower() == "true"
    
    @property
    def notification_email(self) -> Optional[str]:
        """Email for security notifications"""
        return os.getenv("NOTIFICATION_EMAIL")
    
    @property
    def max_repositories(self) -> int:
        """Maximum number of repositories to scan in one run"""
        return int(os.getenv("MAX_REPOSITORIES", "100"))
    
    @property
    def rate_limit_buffer(self) -> int:
        """Number of requests to keep in reserve"""
        return int(os.getenv("RATE_LIMIT_BUFFER", "100"))
    
    def _validate_required_settings(self) -> None:
        """Validate that required configuration is present"""
        required_settings = ["github_token"]
        
        for setting in required_settings:
            try:
                getattr(self, setting)
            except ValueError as e:
                raise ValueError(f"Configuration error: {e}")
    
    def __repr__(self) -> str:
        """Safe string representation (no secrets)"""
        return (
            f"SecurityConfig("
            f"github_base_url='{self.github_base_url}', "
            f"vulnerability_threshold={self.vulnerability_threshold.value}, "
            f"security_scan_enabled={self.security_scan_enabled}, "
            f"max_repositories={self.max_repositories}"
            f")"
        )
```

### Step 2.3: Token Validation and Permission Testing

**File**: `src/github_security/utils/auth.py`

```python
"""
Authentication utilities and token validation
"""
from typing import Dict, List, Any

from ..client import GitHubGraphQLClient
from ..config import SecurityConfig


class TokenValidator:
    """
    Validate GitHub token permissions and capabilities
    """
    
    def __init__(self, client: GitHubGraphQLClient):
        self.client = client
    
    def validate_token_permissions(self) -> Dict[str, Any]:
        """
        Validate that the token has required permissions for security scanning
        
        Returns:
            Validation results including permissions and capabilities
        """
        query = """
        query TokenValidation {
          viewer {
            login
            email
            createdAt
            organizations(first: 10) {
              nodes {
                login
                viewerCanAdminister
              }
            }
          }
          rateLimit {
            limit
            remaining
            resetAt
          }
        }
        """
        
        try:
            result = self.client.execute_query(query)
            
            return {
                "valid": True,
                "user": result.get("viewer", {}),
                "rate_limit": result.get("rateLimit", {}),
                "permissions": self._check_permissions(result),
                "errors": []
            }
            
        except Exception as e:
            return {
                "valid": False,
                "user": {},
                "rate_limit": {},
                "permissions": {},
                "errors": [str(e)]
            }
    
    def _check_permissions(self, result: Dict[str, Any]) -> Dict[str, bool]:
        """Check specific permissions needed for security scanning"""
        permissions = {
            "can_read_user": bool(result.get("viewer", {}).get("login")),
            "can_read_orgs": bool(result.get("viewer", {}).get("organizations", {}).get("nodes")),
            "has_rate_limit": bool(result.get("rateLimit", {}).get("limit")),
        }
        
        return permissions
    
    def test_repository_access(self, repo_owner: str, repo_name: str) -> Dict[str, Any]:
        """
        Test access to a specific repository
        
        Args:
            repo_owner: Repository owner (user or organization)
            repo_name: Repository name
            
        Returns:
            Access test results
        """
        query = """
        query TestRepositoryAccess($owner: String!, $name: String!) {
          repository(owner: $owner, name: $name) {
            id
            name
            isPrivate
            viewerCanAdminister
            viewerPermission
            vulnerabilityAlerts(first: 1) {
              totalCount
            }
            dependencyGraphManifests(first: 1) {
              totalCount
            }
          }
        }
        """
        
        variables = {
            "owner": repo_owner,
            "name": repo_name
        }
        
        try:
            result = self.client.execute_query(query, variables)
            repo = result.get("repository", {})
            
            return {
                "accessible": bool(repo.get("id")),
                "repository": repo,
                "can_read_vulnerabilities": repo.get("vulnerabilityAlerts", {}).get("totalCount", 0) >= 0,
                "can_read_dependencies": repo.get("dependencyGraphManifests", {}).get("totalCount", 0) >= 0,
                "viewer_permission": repo.get("viewerPermission"),
                "errors": []
            }
            
        except Exception as e:
            return {
                "accessible": False,
                "repository": {},
                "can_read_vulnerabilities": False,
                "can_read_dependencies": False,
                "viewer_permission": None,
                "errors": [str(e)]
            }


def validate_setup() -> bool:
    """
    Validate that the security scanning setup is correct
    
    Returns:
        True if setup is valid, False otherwise
    """
    try:
        # Load configuration
        config = SecurityConfig()
        
        # Create client
        client = GitHubGraphQLClient(config.github_token, config.github_base_url)
        
        # Validate token
        validator = TokenValidator(client)
        validation_result = validator.validate_token_permissions()
        
        if not validation_result["valid"]:
            print("❌ Token validation failed:")
            for error in validation_result["errors"]:
                print(f"   - {error}")
            return False
        
        # Print validation results
        user = validation_result["user"]
        rate_limit = validation_result["rate_limit"]
        permissions = validation_result["permissions"]
        
        print("✅ GitHub token validation successful!")
        print(f"   User: {user.get('login', 'Unknown')}")
        print(f"   Rate limit: {rate_limit.get('remaining', 0)}/{rate_limit.get('limit', 0)}")
        print(f"   Permissions: {sum(permissions.values())}/{len(permissions)} checks passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup validation failed: {e}")
        return False


if __name__ == "__main__":
    validate_setup()
```

**Testing Your Setup**:

```bash
# Test your authentication setup
python -m src.github_security.utils.auth

# Expected output:
# ✅ GitHub token validation successful!
#    User: your-username
#    Rate limit: 4999/5000
#    Permissions: 3/3 checks passed
```

---

## Dependency Vulnerability Scanning

### Learning Plan Step 3: Repository Dependency Analysis

**Objective**: Build a comprehensive dependency vulnerability scanner

**Time Investment**: 45 minutes

**What You'll Learn**:
- Query repository dependency graphs
- Identify vulnerable dependencies
- Analyze vulnerability severity and impact
- Generate actionable security reports

### Step 3.1: Dependency Graph Queries

**File**: `src/github_security/queries/dependencies.py`

```python
"""
GraphQL queries for dependency analysis and vulnerability scanning
"""

REPOSITORY_DEPENDENCIES_QUERY = """
query RepositoryDependencies($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    id
    name
    isPrivate
    primaryLanguage {
      name
    }
    
    # Dependency graph manifests (package.json, requirements.txt, etc.)
    dependencyGraphManifests(first: 10, after: $cursor) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        id
        filename
        parseable
        
        # Dependencies from this manifest
        dependencies(first: 100) {
          nodes {
            packageName
            packageManager
            requirements
            
            # Vulnerability information
            repository {
              name
              url
            }
          }
        }
      }
    }
    
    # Vulnerability alerts
    vulnerabilityAlerts(first: 100) {
      totalCount
      nodes {
        id
        createdAt
        dismissedAt
        state
        
        # Vulnerability details
        securityVulnerability {
          severity
          package {
            name
            ecosystem
          }
          advisory {
            id
            summary
            description
            severity
            references {
              url
            }
            cvss {
              score
              vectorString
            }
            cwes(first: 10) {
              nodes {
                cweId
                name
                description
              }
            }
          }
          vulnerableVersionRange
          firstPatchedVersion {
            identifier
          }
        }
        
        # Repository-specific details
        repositoryVulnerabilityAlert {
          id
          repository {
            name
            url
          }
        }
      }
    }
  }
}
"""

ORGANIZATION_VULNERABILITY_SUMMARY = """
query OrganizationVulnerabilities($org: String!, $cursor: String) {
  organization(login: $org) {
    login
    repositories(first: 100, after: $cursor) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        name
        isPrivate
        primaryLanguage {
          name
        }
        vulnerabilityAlerts(first: 1) {
          totalCount
        }
        
        # Recent vulnerability alerts
        recentVulnerabilityAlerts: vulnerabilityAlerts(
          first: 10
          orderBy: {field: CREATED_AT, direction: DESC}
        ) {
          nodes {
            createdAt
            state
            securityVulnerability {
              severity
              package {
                name
                ecosystem
              }
            }
          }
        }
      }
    }
  }
}
"""

SECURITY_ADVISORY_QUERY = """
query SecurityAdvisories($cursor: String) {
  securityAdvisories(first: 100, after: $cursor, orderBy: {field: PUBLISHED_AT, direction: DESC}) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      id
      ghsaId
      summary
      description
      severity
      publishedAt
      updatedAt
      
      # Affected packages
      vulnerabilities(first: 10) {
        nodes {
          package {
            name
            ecosystem
          }
          vulnerableVersionRange
          firstPatchedVersion {
            identifier
          }
        }
      }
      
      # CVSS information
      cvss {
        score
        vectorString
      }
      
      # CWE categories
      cwes(first: 10) {
        nodes {
          cweId
          name
          description
        }
      }
      
      # References
      references {
        url
      }
    }
  }
}
"""

DEPENDENCY_INSIGHTS_QUERY = """
query DependencyInsights($owner: String!, $name: String!, $package: String!, $ecosystem: String!) {
  repository(owner: $owner, name: $name) {
    dependencyGraphManifests(first: 10) {
      nodes {
        dependencies(first: 100) {
          nodes {
            packageName
            packageManager
            requirements
            
            # Check if this is the package we're looking for
            repository {
              name
              url
              licenseInfo {
                name
                spdxId
              }
              stargazerCount
              forkCount
              
              # Recent releases
              releases(first: 5, orderBy: {field: CREATED_AT, direction: DESC}) {
                nodes {
                  name
                  tagName
                  createdAt
                  isPrerelease
                }
              }
            }
          }
        }
      }
    }
  }
}
"""
```

### Step 3.2: Vulnerability Analysis Models

**File**: `src/github_security/models/vulnerability.py`

```python
"""
Pydantic models for vulnerability analysis
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

from pydantic import BaseModel, Field, validator


class VulnerabilitySeverity(str, Enum):
    """Vulnerability severity levels"""
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class VulnerabilityState(str, Enum):
    """Vulnerability alert states"""
    OPEN = "OPEN"
    DISMISSED = "DISMISSED"
    FIXED = "FIXED"


class EcosystemType(str, Enum):
    """Package ecosystem types"""
    NPM = "NPM"
    PIP = "PIP"
    RUBYGEMS = "RUBYGEMS"
    NUGET = "NUGET"
    MAVEN = "MAVEN"
    COMPOSER = "COMPOSER"
    GO = "GO"
    RUST = "RUST"


class CVSSScore(BaseModel):
    """CVSS scoring information"""
    score: float = Field(..., ge=0.0, le=10.0)
    vector_string: Optional[str] = Field(None, alias="vectorString")


class CWEReference(BaseModel):
    """Common Weakness Enumeration reference"""
    cwe_id: str = Field(..., alias="cweId")
    name: str
    description: Optional[str] = None


class Package(BaseModel):
    """Package information"""
    name: str
    ecosystem: EcosystemType


class PatchVersion(BaseModel):
    """First patched version information"""
    identifier: str


class SecurityAdvisory(BaseModel):
    """Security advisory information"""
    id: str
    summary: str
    description: Optional[str] = None
    severity: VulnerabilitySeverity
    cvss: Optional[CVSSScore] = None
    cwes: List[CWEReference] = Field(default_factory=list)
    references: List[Dict[str, str]] = Field(default_factory=list)


class SecurityVulnerability(BaseModel):
    """Security vulnerability details"""
    severity: VulnerabilitySeverity
    package: Package
    advisory: SecurityAdvisory
    vulnerable_version_range: str = Field(..., alias="vulnerableVersionRange")
    first_patched_version: Optional[PatchVersion] = Field(None, alias="firstPatchedVersion")


class VulnerabilityAlert(BaseModel):
    """Vulnerability alert information"""
    id: str
    created_at: datetime = Field(..., alias="createdAt")
    dismissed_at: Optional[datetime] = Field(None, alias="dismissedAt")
    state: VulnerabilityState
    security_vulnerability: SecurityVulnerability = Field(..., alias="securityVulnerability")
    
    @validator('created_at', 'dismissed_at', pre=True)
    def parse_datetime(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace('Z', '+00:00'))
        return v


class DependencyInfo(BaseModel):
    """Repository dependency information"""
    package_name: str = Field(..., alias="packageName")
    package_manager: str = Field(..., alias="packageManager")
    requirements: str
    repository_url: Optional[str] = None
    license_info: Optional[str] = None
    star_count: int = 0
    fork_count: int = 0


class ManifestFile(BaseModel):
    """Dependency manifest file information"""
    id: str
    filename: str
    parseable: bool
    dependencies: List[DependencyInfo] = Field(default_factory=list)


class RepositorySecuritySummary(BaseModel):
    """Repository security analysis summary"""
    id: str
    name: str
    is_private: bool = Field(..., alias="isPrivate")
    primary_language: Optional[str] = None
    
    # Dependency information
    manifests: List[ManifestFile] = Field(default_factory=list)
    
    # Vulnerability information
    vulnerability_alerts: List[VulnerabilityAlert] = Field(default_factory=list)
    total_vulnerabilities: int = 0
    
    # Severity breakdown
    critical_count: int = 0
    high_count: int = 0
    moderate_count: int = 0
    low_count: int = 0
    
    def __post_init__(self):
        """Calculate vulnerability statistics"""
        self.total_vulnerabilities = len(self.vulnerability_alerts)
        
        for alert in self.vulnerability_alerts:
            severity = alert.security_vulnerability.severity
            if severity == VulnerabilitySeverity.CRITICAL:
                self.critical_count += 1
            elif severity == VulnerabilitySeverity.HIGH:
                self.high_count += 1
            elif severity == VulnerabilitySeverity.MODERATE:
                self.moderate_count += 1
            elif severity == VulnerabilitySeverity.LOW:
                self.low_count += 1
    
    @property
    def risk_score(self) -> float:
        """Calculate a risk score based on vulnerability severity"""
        return (
            self.critical_count * 10 +
            self.high_count * 7 +
            self.moderate_count * 4 +
            self.low_count * 1
        )
    
    @property
    def has_critical_vulnerabilities(self) -> bool:
        """Check if repository has critical vulnerabilities"""
        return self.critical_count > 0
    
    @property
    def needs_immediate_attention(self) -> bool:
        """Check if repository needs immediate security attention"""
        return self.critical_count > 0 or self.high_count > 5
```

### Step 3.3: Dependency Scanner Implementation

**File**: `src/github_security/scanner.py`

```python
"""
GitHub repository vulnerability scanner
"""
import asyncio
from typing import List, Dict, Any, Optional, Generator
from dataclasses import dataclass
from datetime import datetime, timedelta

from .client import GitHubGraphQLClient
from .config import SecurityConfig, VulnerabilityThreshold
from .models.vulnerability import (
    RepositorySecuritySummary, 
    VulnerabilityAlert, 
    VulnerabilitySeverity,
    VulnerabilityState
)
from .queries.dependencies import (
    REPOSITORY_DEPENDENCIES_QUERY,
    ORGANIZATION_VULNERABILITY_SUMMARY
)


@dataclass
class ScanResult:
    """Results from a security scan"""
    repository: str
    scan_time: datetime
    vulnerability_count: int
    risk_score: float
    summary: RepositorySecuritySummary
    errors: List[str]


class VulnerabilityScanner:
    """
    GitHub repository vulnerability scanner with security focus
    """
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.client = GitHubGraphQLClient(
            config.github_token,
            config.github_base_url
        )
        self.scan_results: List[ScanResult] = []
    
    def scan_repository(self, owner: str, name: str) -> ScanResult:
        """
        Scan a single repository for vulnerabilities
        
        Args:
            owner: Repository owner (user or organization)
            name: Repository name
            
        Returns:
            Scan results with vulnerability analysis
        """
        print(f"🔍 Scanning repository: {owner}/{name}")
        
        errors = []
        scan_time = datetime.now()
        
        try:
            # Execute dependency and vulnerability query
            variables = {"owner": owner, "name": name}
            result = self.client.execute_query(
                REPOSITORY_DEPENDENCIES_QUERY,
                variables
            )
            
            # Parse repository data
            repo_data = result.get("repository", {})
            if not repo_data:
                raise ValueError(f"Repository {owner}/{name} not found or not accessible")
            
            # Convert to security summary
            summary = self._parse_repository_security_summary(repo_data)
            
            # Calculate risk metrics
            risk_score = summary.risk_score
            vulnerability_count = summary.total_vulnerabilities
            
            # Check against thresholds
            if self._exceeds_threshold(summary):
                print(f"⚠️  Repository {owner}/{name} has vulnerabilities above threshold")
                self._log_vulnerability_details(summary)
            
            result = ScanResult(
                repository=f"{owner}/{name}",
                scan_time=scan_time,
                vulnerability_count=vulnerability_count,
                risk_score=risk_score,
                summary=summary,
                errors=errors
            )
            
            self.scan_results.append(result)
            return result
            
        except Exception as e:
            error_msg = f"Error scanning {owner}/{name}: {str(e)}"
            errors.append(error_msg)
            print(f"❌ {error_msg}")
            
            # Return empty result with error
            return ScanResult(
                repository=f"{owner}/{name}",
                scan_time=scan_time,
                vulnerability_count=0,
                risk_score=0.0,
                summary=RepositorySecuritySummary(
                    id="",
                    name=name,
                    isPrivate=False
                ),
                errors=errors
            )
    
    def scan_organization(self, org: str, max_repos: Optional[int] = None) -> List[ScanResult]:
        """
        Scan all repositories in an organization
        
        Args:
            org: Organization name
            max_repos: Maximum number of repositories to scan
            
        Returns:
            List of scan results for all repositories
        """
        print(f"🏢 Scanning organization: {org}")
        
        max_repos = max_repos or self.config.max_repositories
        results = []
        
        try:
            # Get organization repositories
            cursor = None
            scanned_count = 0
            
            while scanned_count < max_repos:
                variables = {"org": org, "cursor": cursor}
                result = self.client.execute_query(
                    ORGANIZATION_VULNERABILITY_SUMMARY,
                    variables
                )
                
                org_data = result.get("organization", {})
                if not org_data:
                    raise ValueError(f"Organization {org} not found or not accessible")
                
                repos = org_data.get("repositories", {}).get("nodes", [])
                page_info = org_data.get("repositories", {}).get("pageInfo", {})
                
                # Scan each repository
                for repo in repos:
                    if scanned_count >= max_repos:
                        break
                    
                    repo_name = repo.get("name")
                    if repo_name:
                        scan_result = self.scan_repository(org, repo_name)
                        results.append(scan_result)
                        scanned_count += 1
                
                # Check if there are more pages
                if not page_info.get("hasNextPage"):
                    break
                
                cursor = page_info.get("endCursor")
            
            print(f"✅ Organization scan complete: {scanned_count} repositories scanned")
            return results
            
        except Exception as e:
            print(f"❌ Error scanning organization {org}: {str(e)}")
            return results
    
    def _parse_repository_security_summary(self, repo_data: Dict[str, Any]) -> RepositorySecuritySummary:
        """Parse repository data into security summary"""
        # Extract basic repository info
        repo_id = repo_data.get("id", "")
        name = repo_data.get("name", "")
        is_private = repo_data.get("isPrivate", False)
        primary_language = repo_data.get("primaryLanguage", {}).get("name")
        
        # Parse vulnerability alerts
        vulnerability_alerts = []
        alerts_data = repo_data.get("vulnerabilityAlerts", {}).get("nodes", [])
        
        for alert_data in alerts_data:
            try:
                alert = VulnerabilityAlert.parse_obj(alert_data)
                vulnerability_alerts.append(alert)
            except Exception as e:
                print(f"⚠️  Error parsing vulnerability alert: {str(e)}")
        
        # Create summary
        summary = RepositorySecuritySummary(
            id=repo_id,
            name=name,
            isPrivate=is_private,
            primary_language=primary_language,
            vulnerability_alerts=vulnerability_alerts
        )
        
        # Calculate severity counts
        summary.total_vulnerabilities = len(vulnerability_alerts)
        for alert in vulnerability_alerts:
            severity = alert.security_vulnerability.severity
            if severity == VulnerabilitySeverity.CRITICAL:
                summary.critical_count += 1
            elif severity == VulnerabilitySeverity.HIGH:
                summary.high_count += 1
            elif severity == VulnerabilitySeverity.MODERATE:
                summary.moderate_count += 1
            elif severity == VulnerabilitySeverity.LOW:
                summary.low_count += 1
        
        return summary
    
    def _exceeds_threshold(self, summary: RepositorySecuritySummary) -> bool:
        """Check if vulnerability count exceeds configured threshold"""
        threshold = self.config.vulnerability_threshold
        
        if threshold == VulnerabilityThreshold.CRITICAL:
            return summary.critical_count > 0
        elif threshold == VulnerabilityThreshold.HIGH:
            return summary.critical_count > 0 or summary.high_count > 0
        elif threshold == VulnerabilityThreshold.MODERATE:
            return (summary.critical_count + summary.high_count + summary.moderate_count) > 0
        else:  # LOW
            return summary.total_vulnerabilities > 0
    
    def _log_vulnerability_details(self, summary: RepositorySecuritySummary) -> None:
        """Log detailed vulnerability information"""
        print(f"   📊 Vulnerability Summary:")
        print(f"      Critical: {summary.critical_count}")
        print(f"      High: {summary.high_count}")
        print(f"      Moderate: {summary.moderate_count}")
        print(f"      Low: {summary.low_count}")
        print(f"      Risk Score: {summary.risk_score}")
        
        # Log critical vulnerabilities
        for alert in summary.vulnerability_alerts:
            if alert.security_vulnerability.severity == VulnerabilitySeverity.CRITICAL:
                vuln = alert.security_vulnerability
                print(f"      🚨 CRITICAL: {vuln.package.name} - {vuln.advisory.summary}")
    
    def generate_security_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive security report
        
        Returns:
            Security report with statistics and recommendations
        """
        if not self.scan_results:
            return {"error": "No scan results available"}
        
        # Calculate overall statistics
        total_repos = len(self.scan_results)
        total_vulnerabilities = sum(result.vulnerability_count for result in self.scan_results)
        total_risk_score = sum(result.risk_score for result in self.scan_results)
        
        # Count repositories by risk level
        high_risk_repos = [r for r in self.scan_results if r.summary.has_critical_vulnerabilities]
        needs_attention_repos = [r for r in self.scan_results if r.summary.needs_immediate_attention]
        
        # Generate recommendations
        recommendations = self._generate_recommendations()
        
        return {
            "scan_summary": {
                "total_repositories": total_repos,
                "total_vulnerabilities": total_vulnerabilities,
                "average_risk_score": total_risk_score / total_repos if total_repos > 0 else 0,
                "high_risk_repositories": len(high_risk_repos),
                "needs_attention_repositories": len(needs_attention_repos)
            },
            "top_vulnerable_repositories": [
                {
                    "repository": result.repository,
                    "vulnerability_count": result.vulnerability_count,
                    "risk_score": result.risk_score,
                    "critical_vulnerabilities": result.summary.critical_count,
                    "high_vulnerabilities": result.summary.high_count
                }
                for result in sorted(self.scan_results, key=lambda r: r.risk_score, reverse=True)[:10]
            ],
            "recommendations": recommendations,
            "scan_metadata": {
                "scan_date": datetime.now().isoformat(),
                "configuration": {
                    "vulnerability_threshold": self.config.vulnerability_threshold.value,
                    "max_repositories": self.config.max_repositories
                }
            }
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate security recommendations based on scan results"""
        recommendations = []
        
        if not self.scan_results:
            return recommendations
        
        # Check for critical vulnerabilities
        critical_repos = [r for r in self.scan_results if r.summary.critical_count > 0]
        if critical_repos:
            recommendations.append(
                f"🚨 URGENT: {len(critical_repos)} repositories have critical vulnerabilities. "
                f"Address these immediately."
            )
        
        # Check for high vulnerability counts
        high_vuln_repos = [r for r in self.scan_results if r.vulnerability_count > 10]
        if high_vuln_repos:
            recommendations.append(
                f"⚠️  {len(high_vuln_repos)} repositories have more than 10 vulnerabilities. "
                f"Consider dependency updates."
            )
        
        # Check for outdated dependencies
        recommendations.append(
            "📋 Regularly update dependencies to latest stable versions"
        )
        
        # Check for security monitoring
        recommendations.append(
            "🔍 Enable Dependabot alerts for automatic vulnerability notifications"
        )
        
        return recommendations


def main():
    """Example usage of the vulnerability scanner"""
    config = SecurityConfig()
    scanner = VulnerabilityScanner(config)
    
    # Example: Scan a single repository
    result = scanner.scan_repository("facebook", "react")
    print(f"Scan result: {result.vulnerability_count} vulnerabilities found")
    
    # Generate report
    report = scanner.generate_security_report()
    print(f"Security report generated with {len(report['top_vulnerable_repositories'])} repositories")


if __name__ == "__main__":
    main()
```

**Testing the Scanner**:

```bash
# Test the vulnerability scanner
python -m src.github_security.scanner

# Expected output:
# 🔍 Scanning repository: facebook/react
# ✅ Scan result: 0 vulnerabilities found
# Security report generated with 1 repositories
```

---

## Repository Security Analysis

### Learning Plan Step 4: Advanced Security Queries

**Objective**: Build advanced security analysis capabilities

**Time Investment**: 40 minutes

**What You'll Learn**:
- Query security events and audit logs
- Analyze code scanning results
- Monitor repository access and permissions
- Track security-relevant changes

### Step 4.1: Security Events and Audit Queries

**File**: `src/github_security/queries/security_events.py`

```python
"""
GraphQL queries for security events and audit analysis
"""

REPOSITORY_SECURITY_EVENTS_QUERY = """
query RepositorySecurityEvents($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    id
    name
    isPrivate
    
    # Security and analysis settings
    hasVulnerabilityAlertsEnabled
    hasDiscussionsEnabled
    
    # Code scanning alerts
    codeScanning: object(expression: "HEAD") {
      ... on Commit {
        statusCheckRollup {
          contexts(first: 10) {
            nodes {
              ... on CheckRun {
                name
                status
                conclusion
                detailsUrl
              }
              ... on StatusContext {
                state
                description
                context
                targetUrl
              }
            }
          }
        }
      }
    }
    
    # Recent commits with security relevance
    defaultBranchRef {
      target {
        ... on Commit {
          history(first: 50) {
            nodes {
              oid
              message
              author {
                name
                email
                date
              }
              additions
              deletions
              changedFiles
              
              # Check for security-related keywords
              messageHeadline
              messageBody
            }
          }
        }
      }
    }
    
    # Repository collaborators and permissions
    collaborators(first: 100) {
      nodes {
        login
        name
        permission
      }
    }
    
    # Branch protection rules
    branchProtectionRules(first: 10) {
      nodes {
        pattern
        requiresApprovingReviews
        requiredApprovingReviewCount
        dismissesStaleReviews
        requiresCodeOwnerReviews
        requiresStatusChecks
        requiresStrictStatusChecks
        requiresConversationResolution
        allowsForcePushes
        allowsDeletions
        isAdminEnforced
      }
    }
    
    # Deploy keys
    deployKeys(first: 10) {
      nodes {
        id
        title
        readOnly
        verified
        createdAt
      }
    }
  }
}
"""

ORGANIZATION_SECURITY_OVERVIEW_QUERY = """
query OrganizationSecurityOverview($org: String!, $cursor: String) {
  organization(login: $org) {
    login
    
    # Organization security settings
    samlIdentityProvider {
      ssoUrl
      issuer
    }
    
    # Two-factor authentication requirement
    requiresTwoFactorAuthentication
    
    # Member privileges
    membersCanCreateRepositories
    membersCanCreateInternalRepositories
    membersCanCreatePrivateRepositories
    
    # Security policies
    ipAllowListEnabled
    ipAllowListForInstalledAppsEnabled
    
    # Repositories with security issues
    repositories(first: 100, after: $cursor) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        name
        isPrivate
        visibility
        
        # Security settings
        hasVulnerabilityAlertsEnabled
        hasDiscussionsEnabled
        
        # Vulnerability summary
        vulnerabilityAlerts(first: 1) {
          totalCount
        }
        
        # Recent security-related activity
        pushedAt
        updatedAt
        
        # Archive status
        isArchived
        isDisabled
        
        # Admin access
        viewerCanAdminister
        viewerPermission
      }
    }
    
    # Organization members
    membersWithRole(first: 100) {
      nodes {
        login
        name
        role
        
        # Two-factor authentication status
        hasTwoFactorEnabled
      }
    }
  }
}
"""

SECURITY_ADVISORY_IMPACT_QUERY = """
query SecurityAdvisoryImpact($ghsaId: String!) {
  securityAdvisory(ghsaId: $ghsaId) {
    id
    ghsaId
    summary
    description
    severity
    publishedAt
    updatedAt
    
    # CVSS scoring
    cvss {
      score
      vectorString
    }
    
    # Affected packages and versions
    vulnerabilities(first: 20) {
      nodes {
        package {
          name
          ecosystem
        }
        vulnerableVersionRange
        firstPatchedVersion {
          identifier
        }
      }
    }
    
    # Common weakness enumerations
    cwes(first: 10) {
      nodes {
        cweId
        name
        description
      }
    }
    
    # External references
    references {
      url
    }
    
    # Related repositories (if available)
    origin
  }
}
"""

DEPENDENCY_SECURITY_QUERY = """
query DependencySecurityAnalysis($owner: String!, $name: String!, $manifestPath: String!) {
  repository(owner: $owner, name: $name) {
    id
    name
    
    # Specific manifest file
    dependencyGraphManifests(first: 10, withDependencies: true) {
      nodes {
        id
        filename
        parseable
        
        # All dependencies from this manifest
        dependencies(first: 100) {
          nodes {
            packageName
            packageManager
            requirements
            
            # Security information for each dependency
            repository {
              name
              url
              description
              
              # Repository health indicators
              stargazerCount
              forkCount
              isArchived
              isDisabled
              
              # License information
              licenseInfo {
                name
                spdxId
                url
              }
              
              # Recent activity
              pushedAt
              updatedAt
              
              # Security settings
              hasVulnerabilityAlertsEnabled
              
              # Recent releases
              releases(first: 5, orderBy: {field: CREATED_AT, direction: DESC}) {
                nodes {
                  name
                  tagName
                  createdAt
                  isPrerelease
                  isDraft
                }
              }
            }
          }
        }
      }
    }
  }
}
"""
```

### Step 4.2: Security Analysis Engine

**File**: `src/github_security/analysis/security_engine.py`

```python
"""
Advanced security analysis engine for GitHub repositories
"""
import re
from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timedelta
from dataclasses import dataclass

from ..client import GitHubGraphQLClient
from ..queries.security_events import (
    REPOSITORY_SECURITY_EVENTS_QUERY,
    ORGANIZATION_SECURITY_OVERVIEW_QUERY,
    DEPENDENCY_SECURITY_QUERY
)


@dataclass
class SecurityFinding:
    """Security finding or issue detected during analysis"""
    severity: str  # "critical", "high", "medium", "low", "info"
    category: str  # "vulnerability", "configuration", "access", "dependency"
    title: str
    description: str
    recommendation: str
    affected_component: str
    evidence: Dict[str, Any]
    
    def __post_init__(self):
        """Validate severity level"""
        valid_severities = {"critical", "high", "medium", "low", "info"}
        if self.severity not in valid_severities:
            raise ValueError(f"Invalid severity: {self.severity}")


@dataclass
class SecurityScore:
    """Security score calculation for a repository"""
    total_score: float  # 0-100
    vulnerability_score: float
    configuration_score: float
    access_control_score: float
    dependency_hygiene_score: float
    activity_score: float
    
    @property
    def grade(self) -> str:
        """Get letter grade based on score"""
        if self.total_score >= 90:
            return "A"
        elif self.total_score >= 80:
            return "B"
        elif self.total_score >= 70:
            return "C"
        elif self.total_score >= 60:
            return "D"
        else:
            return "F"


class SecurityAnalysisEngine:
    """
    Advanced security analysis engine for GitHub repositories
    """
    
    def __init__(self, client: GitHubGraphQLClient):
        self.client = client
        self.security_keywords = {
            "vulnerability", "security", "cve", "exploit", "malware", "backdoor",
            "injection", "xss", "csrf", "authentication", "authorization", "password",
            "secret", "token", "key", "credential", "leak", "breach", "attack"
        }
        
        # Patterns for security-relevant commits
        self.security_patterns = [
            r"(?i)(fix|patch|security|vuln|cve-\d{4}-\d{4,})",
            r"(?i)(password|secret|token|key|credential)",
            r"(?i)(auth|login|session|cookie)",
            r"(?i)(injection|xss|csrf|sql|ldap)",
            r"(?i)(encrypt|decrypt|hash|salt|crypto)"
        ]
    
    def analyze_repository_security(self, owner: str, name: str) -> Dict[str, Any]:
        """
        Perform comprehensive security analysis of a repository
        
        Args:
            owner: Repository owner
            name: Repository name
            
        Returns:
            Complete security analysis report
        """
        print(f"🔍 Analyzing repository security: {owner}/{name}")
        
        findings = []
        
        try:
            # Query repository security events
            variables = {"owner": owner, "name": name}
            result = self.client.execute_query(
                REPOSITORY_SECURITY_EVENTS_QUERY,
                variables
            )
            
            repo_data = result.get("repository", {})
            if not repo_data:
                raise ValueError(f"Repository {owner}/{name} not found")
            
            # Analyze different security aspects
            findings.extend(self._analyze_security_configuration(repo_data))
            findings.extend(self._analyze_access_control(repo_data))
            findings.extend(self._analyze_commit_security(repo_data))
            findings.extend(self._analyze_branch_protection(repo_data))
            findings.extend(self._analyze_deploy_keys(repo_data))
            
            # Calculate security score
            security_score = self._calculate_security_score(repo_data, findings)
            
            # Generate recommendations
            recommendations = self._generate_security_recommendations(findings)
            
            return {
                "repository": f"{owner}/{name}",
                "analysis_date": datetime.now().isoformat(),
                "security_score": security_score,
                "findings": [self._finding_to_dict(f) for f in findings],
                "recommendations": recommendations,
                "metadata": {
                    "total_findings": len(findings),
                    "critical_findings": len([f for f in findings if f.severity == "critical"]),
                    "high_findings": len([f for f in findings if f.severity == "high"]),
                    "medium_findings": len([f for f in findings if f.severity == "medium"]),
                    "low_findings": len([f for f in findings if f.severity == "low"])
                }
            }
            
        except Exception as e:
            return {
                "repository": f"{owner}/{name}",
                "analysis_date": datetime.now().isoformat(),
                "error": str(e),
                "findings": [],
                "recommendations": []
            }
    
    def _analyze_security_configuration(self, repo_data: Dict[str, Any]) -> List[SecurityFinding]:
        """Analyze repository security configuration"""
        findings = []
        
        # Check vulnerability alerts
        if not repo_data.get("hasVulnerabilityAlertsEnabled"):
            findings.append(SecurityFinding(
                severity="medium",
                category="configuration",
                title="Vulnerability Alerts Disabled",
                description="Repository does not have vulnerability alerts enabled",
                recommendation="Enable vulnerability alerts to receive notifications about security issues",
                affected_component="Repository Settings",
                evidence={"hasVulnerabilityAlertsEnabled": False}
            ))
        
        # Check if repository is private vs public
        if not repo_data.get("isPrivate"):
            findings.append(SecurityFinding(
                severity="info",
                category="configuration",
                title="Public Repository",
                description="Repository is publicly accessible",
                recommendation="Review if repository should be private to protect sensitive code",
                affected_component="Repository Visibility",
                evidence={"isPrivate": False}
            ))
        
        return findings
    
    def _analyze_access_control(self, repo_data: Dict[str, Any]) -> List[SecurityFinding]:
        """Analyze repository access control"""
        findings = []
        
        collaborators = repo_data.get("collaborators", {}).get("nodes", [])
        
        # Check for admin access
        admin_count = len([c for c in collaborators if c.get("permission") == "ADMIN"])
        if admin_count > 5:
            findings.append(SecurityFinding(
                severity="medium",
                category="access",
                title="Excessive Admin Access",
                description=f"Repository has {admin_count} administrators",
                recommendation="Review admin access and follow principle of least privilege",
                affected_component="Repository Permissions",
                evidence={"admin_count": admin_count, "collaborators": collaborators}
            ))
        
        # Check for collaborators without recent activity
        # This would require additional API calls to get user activity
        
        return findings
    
    def _analyze_commit_security(self, repo_data: Dict[str, Any]) -> List[SecurityFinding]:
        """Analyze recent commits for security relevance"""
        findings = []
        
        # Get commit history
        default_branch = repo_data.get("defaultBranchRef", {})
        target = default_branch.get("target", {})
        history = target.get("history", {}).get("nodes", [])
        
        security_commits = []
        potential_secrets = []
        
        for commit in history:
            message = commit.get("message", "")
            headline = commit.get("messageHeadline", "")
            
            # Check for security-related commits
            for pattern in self.security_patterns:
                if re.search(pattern, message):
                    security_commits.append({
                        "oid": commit.get("oid"),
                        "message": headline,
                        "author": commit.get("author", {}).get("name"),
                        "date": commit.get("author", {}).get("date")
                    })
                    break
            
            # Check for potential secrets in commit messages
            if any(keyword in message.lower() for keyword in ["password", "secret", "token", "key"]):
                potential_secrets.append({
                    "oid": commit.get("oid"),
                    "message": headline,
                    "author": commit.get("author", {}).get("name")
                })
        
        # Generate findings
        if security_commits:
            findings.append(SecurityFinding(
                severity="info",
                category="activity",
                title="Security-Related Commits",
                description=f"Found {len(security_commits)} security-related commits",
                recommendation="Review security commits for proper implementation",
                affected_component="Git History",
                evidence={"security_commits": security_commits}
            ))
        
        if potential_secrets:
            findings.append(SecurityFinding(
                severity="high",
                category="vulnerability",
                title="Potential Secrets in Commit Messages",
                description=f"Found {len(potential_secrets)} commits with potential secrets",
                recommendation="Review commit messages and remove any exposed secrets",
                affected_component="Git History",
                evidence={"potential_secrets": potential_secrets}
            ))
        
        return findings
    
    def _analyze_branch_protection(self, repo_data: Dict[str, Any]) -> List[SecurityFinding]:
        """Analyze branch protection rules"""
        findings = []
        
        protection_rules = repo_data.get("branchProtectionRules", {}).get("nodes", [])
        
        if not protection_rules:
            findings.append(SecurityFinding(
                severity="medium",
                category="configuration",
                title="No Branch Protection Rules",
                description="Repository has no branch protection rules configured",
                recommendation="Configure branch protection rules for main/master branch",
                affected_component="Branch Protection",
                evidence={"protection_rules_count": 0}
            ))
        else:
            # Analyze each protection rule
            for rule in protection_rules:
                pattern = rule.get("pattern", "")
                
                issues = []
                if not rule.get("requiresApprovingReviews"):
                    issues.append("No required reviews")
                if rule.get("allowsForcePushes"):
                    issues.append("Force pushes allowed")
                if rule.get("allowsDeletions"):
                    issues.append("Branch deletions allowed")
                if not rule.get("requiresStatusChecks"):
                    issues.append("No status checks required")
                
                if issues:
                    findings.append(SecurityFinding(
                        severity="medium",
                        category="configuration",
                        title=f"Weak Branch Protection: {pattern}",
                        description=f"Branch protection rule has issues: {', '.join(issues)}",
                        recommendation="Strengthen branch protection rules",
                        affected_component="Branch Protection",
                        evidence={"pattern": pattern, "issues": issues, "rule": rule}
                    ))
        
        return findings
    
    def _analyze_deploy_keys(self, repo_data: Dict[str, Any]) -> List[SecurityFinding]:
        """Analyze deploy keys"""
        findings = []
        
        deploy_keys = repo_data.get("deployKeys", {}).get("nodes", [])
        
        for key in deploy_keys:
            if not key.get("readOnly"):
                findings.append(SecurityFinding(
                    severity="medium",
                    category="access",
                    title="Write-Access Deploy Key",
                    description=f"Deploy key '{key.get('title')}' has write access",
                    recommendation="Use read-only deploy keys when possible",
                    affected_component="Deploy Keys",
                    evidence={"deploy_key": key}
                ))
            
            if not key.get("verified"):
                findings.append(SecurityFinding(
                    severity="low",
                    category="access",
                    title="Unverified Deploy Key",
                    description=f"Deploy key '{key.get('title')}' is not verified",
                    recommendation="Verify deploy key ownership",
                    affected_component="Deploy Keys",
                    evidence={"deploy_key": key}
                ))
        
        return findings
    
    def _calculate_security_score(self, repo_data: Dict[str, Any], findings: List[SecurityFinding]) -> SecurityScore:
        """Calculate comprehensive security score"""
        
        # Base scores (start at 100, deduct for issues)
        vulnerability_score = 100.0
        configuration_score = 100.0
        access_control_score = 100.0
        dependency_hygiene_score = 100.0
        activity_score = 100.0
        
        # Deduct points for findings
        for finding in findings:
            deduction = 0
            if finding.severity == "critical":
                deduction = 20
            elif finding.severity == "high":
                deduction = 10
            elif finding.severity == "medium":
                deduction = 5
            elif finding.severity == "low":
                deduction = 2
            
            # Apply deduction to appropriate category
            if finding.category == "vulnerability":
                vulnerability_score = max(0, vulnerability_score - deduction)
            elif finding.category == "configuration":
                configuration_score = max(0, configuration_score - deduction)
            elif finding.category == "access":
                access_control_score = max(0, access_control_score - deduction)
            elif finding.category == "dependency":
                dependency_hygiene_score = max(0, dependency_hygiene_score - deduction)
            elif finding.category == "activity":
                activity_score = max(0, activity_score - deduction)
        
        # Calculate weighted total score
        total_score = (
            vulnerability_score * 0.3 +
            configuration_score * 0.25 +
            access_control_score * 0.2 +
            dependency_hygiene_score * 0.15 +
            activity_score * 0.1
        )
        
        return SecurityScore(
            total_score=total_score,
            vulnerability_score=vulnerability_score,
            configuration_score=configuration_score,
            access_control_score=access_control_score,
            dependency_hygiene_score=dependency_hygiene_score,
            activity_score=activity_score
        )
    
    def _generate_security_recommendations(self, findings: List[SecurityFinding]) -> List[str]:
        """Generate prioritized security recommendations"""
        recommendations = []
        
        # Group findings by severity
        critical_findings = [f for f in findings if f.severity == "critical"]
        high_findings = [f for f in findings if f.severity == "high"]
        medium_findings = [f for f in findings if f.severity == "medium"]
        
        # Generate recommendations based on findings
        if critical_findings:
            recommendations.append(
                f"🚨 CRITICAL: Address {len(critical_findings)} critical security issues immediately"
            )
        
        if high_findings:
            recommendations.append(
                f"⚠️ HIGH: Resolve {len(high_findings)} high-severity security issues"
            )
        
        if medium_findings:
            recommendations.append(
                f"📋 MEDIUM: Review {len(medium_findings)} medium-severity security issues"
            )
        
        # Add specific recommendations
        recommendations.extend([
            "✅ Enable vulnerability alerts for all repositories",
            "🔐 Implement strong branch protection rules",
            "👥 Review and minimize admin access",
            "🔍 Regularly audit deploy keys and access tokens",
            "📊 Monitor repository activity for suspicious changes"
        ])
        
        return recommendations
    
    def _finding_to_dict(self, finding: SecurityFinding) -> Dict[str, Any]:
        """Convert SecurityFinding to dictionary"""
        return {
            "severity": finding.severity,
            "category": finding.category,
            "title": finding.title,
            "description": finding.description,
            "recommendation": finding.recommendation,
            "affected_component": finding.affected_component,
            "evidence": finding.evidence
        }


def main():
    """Example usage of the security analysis engine"""
    from ..config import SecurityConfig
    
    config = SecurityConfig()
    client = GitHubGraphQLClient(config.github_token)
    engine = SecurityAnalysisEngine(client)
    
    # Analyze a repository
    analysis = engine.analyze_repository_security("octocat", "Hello-World")
    
    print(f"Security Analysis Complete!")
    print(f"Score: {analysis['security_score'].total_score:.1f}/100 (Grade: {analysis['security_score'].grade})")
    print(f"Findings: {analysis['metadata']['total_findings']}")
    print(f"Critical: {analysis['metadata']['critical_findings']}")


if __name__ == "__main__":
    main()
```

---

## Automated Security Monitoring

### Learning Plan Step 5: Building Continuous Security Monitoring

**Objective**: Create automated systems for continuous security monitoring

**Time Investment**: 35 minutes

**What You'll Learn**:
- Build automated vulnerability scanning workflows
- Set up security alerting and notifications
- Create security dashboards and reports
- Implement continuous monitoring patterns

### Step 5.1: Automated Vulnerability Monitor

**File**: `src/github_security/monitor/vulnerability_monitor.py`

```python
"""
Automated vulnerability monitoring system for GitHub repositories
"""
import json
import time
import smtplib
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from pathlib import Path

from ..client import GitHubGraphQLClient
from ..config import SecurityConfig
from ..scanner import VulnerabilityScanner, ScanResult
from ..models.vulnerability import VulnerabilitySeverity


class SecurityMonitor:
    """
    Automated security monitoring system
    """
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.scanner = VulnerabilityScanner(config)
        self.results_cache = {}
        self.alert_history = []
        
        # Monitoring configuration
        self.check_interval_hours = 24  # Daily checks
        self.alert_threshold = VulnerabilitySeverity.HIGH
        self.max_alerts_per_day = 10
        
        # Storage paths
        self.cache_file = Path("security_cache.json")
        self.alerts_file = Path("security_alerts.json")
    
    def start_monitoring(self, repositories: List[Dict[str, str]], max_runs: Optional[int] = None):
        """
        Start continuous monitoring of repositories
        
        Args:
            repositories: List of {"owner": "name", "name": "repo"} dictionaries
            max_runs: Maximum number of monitoring cycles (None for infinite)
        """
        print(f"🚀 Starting security monitoring for {len(repositories)} repositories")
        print(f"📊 Check interval: {self.check_interval_hours} hours")
        print(f"⚠️  Alert threshold: {self.alert_threshold.value}")
        
        run_count = 0
        
        try:
            while max_runs is None or run_count < max_runs:
                print(f"\n🔄 Monitoring cycle {run_count + 1} started at {datetime.now()}")
                
                # Scan all repositories
                cycle_results = []
                for repo in repositories:
                    try:
                        result = self.scanner.scan_repository(repo["owner"], repo["name"])
                        cycle_results.append(result)
                        
                        # Check for new vulnerabilities
                        self._check_for_new_vulnerabilities(result)
                        
                    except Exception as e:
                        print(f"❌ Error scanning {repo['owner']}/{repo['name']}: {e}")
                
                # Update cache and generate reports
                self._update_results_cache(cycle_results)
                self._generate_monitoring_report(cycle_results)
                
                # Send alerts if needed
                if self.config.notification_email:
                    self._send_alert_notifications()
                
                run_count += 1
                
                # Wait for next cycle (unless this is the last run)
                if max_runs is None or run_count < max_runs:
                    print(f"⏸️  Waiting {self.check_interval_hours} hours until next scan...")
                    time.sleep(self.check_interval_hours * 3600)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        except Exception as e:
            print(f"❌ Monitoring error: {e}")
        
        print(f"✅ Monitoring completed after {run_count} cycles")
    
    def _check_for_new_vulnerabilities(self, current_result: ScanResult) -> None:
        """Check for new vulnerabilities compared to previous scan"""
        repo_key = current_result.repository
        
        # Load previous results
        previous_result = self.results_cache.get(repo_key)
        if not previous_result:
            print(f"   📋 First scan for {repo_key}")
            return
        
        # Compare vulnerability counts
        current_count = current_result.vulnerability_count
        previous_count = previous_result.get("vulnerability_count", 0)
        
        if current_count > previous_count:
            new_vulns = current_count - previous_count
            print(f"   🚨 NEW VULNERABILITIES: {new_vulns} new vulnerabilities found in {repo_key}")
            
            # Create alert
            alert = {
                "timestamp": datetime.now().isoformat(),
                "repository": repo_key,
                "type": "new_vulnerabilities",
                "severity": "high",
                "message": f"{new_vulns} new vulnerabilities detected",
                "current_count": current_count,
                "previous_count": previous_count,
                "details": {
                    "critical": current_result.summary.critical_count,
                    "high": current_result.summary.high_count,
                    "medium": current_result.summary.moderate_count,
                    "low": current_result.summary.low_count
                }
            }
            
            self.alert_history.append(alert)
            print(f"   📬 Alert created for {repo_key}")
        
        elif current_count < previous_count:
            fixed_vulns = previous_count - current_count
            print(f"   ✅ VULNERABILITIES FIXED: {fixed_vulns} vulnerabilities resolved in {repo_key}")
    
    def _update_results_cache(self, results: List[ScanResult]) -> None:
        """Update the results cache with latest scan data"""
        for result in results:
            self.results_cache[result.repository] = {
                "scan_time": result.scan_time.isoformat(),
                "vulnerability_count": result.vulnerability_count,
                "risk_score": result.risk_score,
                "summary": {
                    "critical": result.summary.critical_count,
                    "high": result.summary.high_count,
                    "medium": result.summary.moderate_count,
                    "low": result.summary.low_count
                }
            }
        
        # Save cache to file
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.results_cache, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save cache: {e}")
    
    def _generate_monitoring_report(self, results: List[ScanResult]) -> None:
        """Generate monitoring cycle report"""
        if not results:
            return
        
        total_repos = len(results)
        total_vulns = sum(r.vulnerability_count for r in results)
        high_risk_repos = len([r for r in results if r.summary.has_critical_vulnerabilities])
        
        print(f"\n📊 Monitoring Cycle Summary:")
        print(f"   Repositories scanned: {total_repos}")
        print(f"   Total vulnerabilities: {total_vulns}")
        print(f"   High-risk repositories: {high_risk_repos}")
        print(f"   Average risk score: {sum(r.risk_score for r in results) / total_repos:.1f}")
        
        # Top 3 highest risk repositories
        top_risk = sorted(results, key=lambda r: r.risk_score, reverse=True)[:3]
        if top_risk:
            print(f"   Top risk repositories:")
            for i, repo in enumerate(top_risk, 1):
                print(f"     {i}. {repo.repository} (Score: {repo.risk_score:.1f})")
    
    def _send_alert_notifications(self) -> None:
        """Send email notifications for security alerts"""
        # Get recent alerts (last 24 hours)
        recent_alerts = [
            alert for alert in self.alert_history
            if datetime.fromisoformat(alert["timestamp"]) > datetime.now() - timedelta(hours=24)
        ]
        
        if not recent_alerts:
            return
        
        # Limit alerts per day
        if len(recent_alerts) > self.max_alerts_per_day:
            print(f"⚠️  Too many alerts ({len(recent_alerts)}), limiting to {self.max_alerts_per_day}")
            recent_alerts = recent_alerts[:self.max_alerts_per_day]
        
        try:
            self._send_email_alert(recent_alerts)
            print(f"📧 Sent {len(recent_alerts)} security alerts to {self.config.notification_email}")
        except Exception as e:
            print(f"❌ Failed to send email alerts: {e}")
    
    def _send_email_alert(self, alerts: List[Dict[str, Any]]) -> None:
        """Send email alert with security findings"""
        if not self.config.notification_email:
            return
        
        # Create email content
        subject = f"GitHub Security Alert: {len(alerts)} new issues detected"
        
        body = f"""
Security Monitoring Alert

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Alerts: {len(alerts)}

Alert Details:
"""
        
        for alert in alerts:
            body += f"""
Repository: {alert['repository']}
Type: {alert['type']}
Severity: {alert['severity']}
Message: {alert['message']}
Timestamp: {alert['timestamp']}
---
"""
        
        body += """

This is an automated security alert from your GitHub repository monitoring system.
Please review the security issues and take appropriate action.

Best regards,
GitHub Security Monitor
"""
        
        # For demonstration, just print the email content
        # In a real implementation, you would configure SMTP settings
        print(f"📧 Email Alert Content:")
        print(f"To: {self.config.notification_email}")
        print(f"Subject: {subject}")
        print(body)
    
    def load_cache(self) -> None:
        """Load previous scan results from cache"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    self.results_cache = json.load(f)
                print(f"📋 Loaded cache with {len(self.results_cache)} repositories")
        except Exception as e:
            print(f"⚠️  Could not load cache: {e}")
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring status and statistics"""
        if not self.results_cache:
            return {"status": "no_data", "repositories": 0}
        
        total_repos = len(self.results_cache)
        total_vulns = sum(repo.get("vulnerability_count", 0) for repo in self.results_cache.values())
        
        # Recent alerts (last 7 days)
        recent_alerts = [
            alert for alert in self.alert_history
            if datetime.fromisoformat(alert["timestamp"]) > datetime.now() - timedelta(days=7)
        ]
        
        return {
            "status": "active",
            "repositories": total_repos,
            "total_vulnerabilities": total_vulns,
            "recent_alerts": len(recent_alerts),
            "last_scan": max(
                (datetime.fromisoformat(repo["scan_time"]) for repo in self.results_cache.values()),
                default=None
            ).isoformat() if self.results_cache else None
        }


class SecurityDashboard:
    """
    Security monitoring dashboard generator
    """
    
    def __init__(self, monitor: SecurityMonitor):
        self.monitor = monitor
    
    def generate_html_dashboard(self, output_file: str = "security_dashboard.html") -> None:
        """Generate HTML security dashboard"""
        status = self.monitor.get_monitoring_status()
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>GitHub Security Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background: #f4f4f4; padding: 20px; border-radius: 5px; }}
        .metric {{ display: inline-block; margin: 20px; padding: 15px; 
                  background: #e8f4fd; border-radius: 5px; min-width: 150px; }}
        .alert {{ background: #ffebee; border-left: 4px solid #f44336; padding: 15px; margin: 20px 0; }}
        .success {{ background: #e8f5e8; border-left: 4px solid #4caf50; padding: 15px; margin: 20px 0; }}
        .repo-list {{ margin: 20px 0; }}
        .repo-item {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        .high-risk {{ background: #ffebee; }}
        .medium-risk {{ background: #fff3e0; }}
        .low-risk {{ background: #e8f5e8; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔐 GitHub Security Dashboard</h1>
        <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="metrics">
        <div class="metric">
            <h3>Repositories</h3>
            <p style="font-size: 24px; margin: 0;">{status.get('repositories', 0)}</p>
        </div>
        <div class="metric">
            <h3>Total Vulnerabilities</h3>
            <p style="font-size: 24px; margin: 0; color: #f44336;">{status.get('total_vulnerabilities', 0)}</p>
        </div>
        <div class="metric">
            <h3>Recent Alerts</h3>
            <p style="font-size: 24px; margin: 0; color: #ff9800;">{status.get('recent_alerts', 0)}</p>
        </div>
    </div>
    
    <div class="repo-list">
        <h2>Repository Status</h2>
"""
        
        # Add repository details
        for repo_name, repo_data in self.monitor.results_cache.items():
            risk_score = repo_data.get("risk_score", 0)
            vuln_count = repo_data.get("vulnerability_count", 0)
            
            if risk_score > 50:
                risk_class = "high-risk"
                risk_label = "High Risk"
            elif risk_score > 20:
                risk_class = "medium-risk"
                risk_label = "Medium Risk"
            else:
                risk_class = "low-risk"
                risk_label = "Low Risk"
            
            html_content += f"""
        <div class="repo-item {risk_class}">
            <h3>{repo_name}</h3>
            <p>Risk Score: {risk_score:.1f} ({risk_label})</p>
            <p>Vulnerabilities: {vuln_count}</p>
            <p>Last Scan: {repo_data.get('scan_time', 'Never')}</p>
        </div>
"""
        
        html_content += """
    </div>
    
    <script>
        // Auto-refresh every 5 minutes
        setTimeout(function() {
            location.reload();
        }, 300000);
    </script>
</body>
</html>
"""
        
        # Write dashboard to file
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        print(f"📊 Security dashboard generated: {output_file}")


def main():
    """Example usage of the security monitor"""
    config = SecurityConfig()
    monitor = SecurityMonitor(config)
    
    # Load previous cache
    monitor.load_cache()
    
    # Example repositories to monitor
    repositories = [
        {"owner": "facebook", "name": "react"},
        {"owner": "microsoft", "name": "vscode"},
        {"owner": "octocat", "name": "Hello-World"}
    ]
    
    # Start monitoring (run once for demo)
    monitor.start_monitoring(repositories, max_runs=1)
    
    # Generate dashboard
    dashboard = SecurityDashboard(monitor)
    dashboard.generate_html_dashboard()


if __name__ == "__main__":
    main()
```

### Step 5.2: GitHub Actions Security Workflow

**File**: `.github/workflows/security-scan.yml`

```yaml
name: Automated Security Scanning

on:
  schedule:
    # Run daily at 6 AM UTC
    - cron: '0 6 * * *'
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  security-scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
      
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests python-dotenv pydantic
        
    - name: Run vulnerability scan
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        VULNERABILITY_THRESHOLD: high
        SECURITY_SCAN_ENABLED: true
      run: |
        python -m src.github_security.scanner
        
    - name: Generate security report
      run: |
        python -c "
        from src.github_security.config import SecurityConfig
        from src.github_security.scanner import VulnerabilityScanner
        import json
        
        config = SecurityConfig()
        scanner = VulnerabilityScanner(config)
        
        # Scan current repository
        import os
        repo_owner = os.environ.get('GITHUB_REPOSITORY_OWNER')
        repo_name = os.environ.get('GITHUB_REPOSITORY').split('/')[-1]
        
        result = scanner.scan_repository(repo_owner, repo_name)
        report = scanner.generate_security_report()
        
        # Save report as artifact
        with open('security-report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f'Security scan complete: {result.vulnerability_count} vulnerabilities found')
        "
        
    - name: Upload security report
      uses: actions/upload-artifact@v3
      with:
        name: security-report
        path: security-report.json
        
    - name: Comment on PR with results
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v7
      with:
        script: |
          const fs = require('fs');
          
          try {
            const report = JSON.parse(fs.readFileSync('security-report.json', 'utf8'));
            const summary = report.scan_summary;
            
            const comment = `## 🔐 Security Scan Results
            
            - **Repositories Scanned**: ${summary.total_repositories}
            - **Total Vulnerabilities**: ${summary.total_vulnerabilities}
            - **High Risk Repositories**: ${summary.high_risk_repositories}
            - **Average Risk Score**: ${summary.average_risk_score.toFixed(1)}
            
            ${summary.high_risk_repositories > 0 ? '⚠️ **Action Required**: High-risk vulnerabilities detected!' : '✅ **All Clear**: No high-risk vulnerabilities detected.'}
            
            <details>
            <summary>📊 Detailed Results</summary>
            
            ### Top Vulnerable Repositories
            ${report.top_vulnerable_repositories.slice(0, 5).map(repo => 
              `- **${repo.repository}**: ${repo.vulnerability_count} vulnerabilities (Risk: ${repo.risk_score.toFixed(1)})`
            ).join('\n')}
            
            ### Recommendations
            ${report.recommendations.map(rec => `- ${rec}`).join('\n')}
            </details>
            `;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
          } catch (error) {
            console.log('Could not create comment:', error);
          }
          
    - name: Fail on critical vulnerabilities
      run: |
        python -c "
        import json
        with open('security-report.json', 'r') as f:
            report = json.load(f)
        
        critical_repos = len([r for r in report['top_vulnerable_repositories'] 
                             if r['critical_vulnerabilities'] > 0])
        
        if critical_repos > 0:
            print(f'❌ FAILING: {critical_repos} repositories have critical vulnerabilities')
            exit(1)
        else:
            print('✅ PASSING: No critical vulnerabilities detected')
        "
```

---

## Rate Limiting and Best Practices

### Learning Plan Step 6: Efficient API Usage

**Objective**: Master GitHub GraphQL rate limiting and optimization

**Time Investment**: 25 minutes

**What You'll Learn**:
- Understand GitHub's rate limiting model
- Implement efficient query patterns
- Optimize API usage for large-scale scanning
- Handle rate limits gracefully

### Step 6.1: Rate Limiting Strategy

**File**: `src/github_security/utils/rate_limit.py`

```python
"""
Advanced rate limiting and API optimization utilities
"""
import time
import math
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta

from ..client import GitHubGraphQLClient


@dataclass
class QueryCost:
    """GraphQL query cost analysis"""
    estimated_cost: int
    actual_cost: Optional[int] = None
    execution_time: Optional[float] = None
    
    @property
    def efficiency_ratio(self) -> Optional[float]:
        """Calculate efficiency ratio (actual vs estimated cost)"""
        if self.actual_cost and self.estimated_cost:
            return self.actual_cost / self.estimated_cost
        return None


class RateLimitManager:
    """
    Advanced rate limit management for GitHub GraphQL API
    """
    
    def __init__(self, client: GitHubGraphQLClient, buffer_points: int = 100):
        self.client = client
        self.buffer_points = buffer_points  # Points to keep in reserve
        self.query_costs: List[QueryCost] = []
        self.optimization_enabled = True
        
        # Rate limit state
        self.current_limit = 5000
        self.current_remaining = 5000
        self.current_reset_at = None
        
        # Query optimization tracking
        self.query_patterns = {}
        self.performance_metrics = {}
    
    def check_rate_limit(self) -> Dict[str, Any]:
        """
        Check current rate limit status
        
        Returns:
            Current rate limit information
        """
        query = """
        query {
          rateLimit {
            limit
            remaining
            resetAt
            used
          }
        }
        """
        
        result = self.client.execute_query(query)
        rate_limit = result.get("rateLimit", {})
        
        # Update internal state
        self.current_limit = rate_limit.get("limit", 5000)
        self.current_remaining = rate_limit.get("remaining", 5000)
        reset_at_str = rate_limit.get("resetAt")
        
        if reset_at_str:
            self.current_reset_at = datetime.fromisoformat(reset_at_str.replace('Z', '+00:00'))
        
        return {
            "limit": self.current_limit,
            "remaining": self.current_remaining,
            "used": rate_limit.get("used", 0),
            "reset_at": reset_at_str,
            "buffer_points": self.buffer_points,
            "safe_remaining": max(0, self.current_remaining - self.buffer_points)
        }
    
    def estimate_query_cost(self, query: str, variables: Optional[Dict[str, Any]] = None) -> int:
        """
        Estimate the cost of a GraphQL query
        
        Args:
            query: GraphQL query string
            variables: Query variables
            
        Returns:
            Estimated query cost in points
        """
        # Basic cost estimation based on query complexity
        base_cost = 1
        
        # Count expensive operations
        query_lower = query.lower()
        
        # Field multipliers
        if "nodes" in query_lower:
            base_cost += query.count("nodes") * 2
        if "edges" in query_lower:
            base_cost += query.count("edges") * 2
        if "pageinfo" in query_lower:
            base_cost += 1
        
        # Pagination costs
        if variables:
            first_val = variables.get("first", 0)
            if first_val:
                base_cost += math.ceil(first_val / 10)  # Rough estimate
        
        # Repository queries are more expensive
        if "repository" in query_lower:
            base_cost += 3
        if "organization" in query_lower:
            base_cost += 5
        
        # Vulnerability queries
        if "vulnerability" in query_lower:
            base_cost += 10
        if "dependencygraph" in query_lower:
            base_cost += 15
        
        return min(base_cost, 1000)  # Cap at reasonable maximum
    
    def can_execute_query(self, estimated_cost: int) -> bool:
        """
        Check if a query can be executed within rate limits
        
        Args:
            estimated_cost: Estimated cost of the query
            
        Returns:
            True if query can be executed safely
        """
        safe_remaining = max(0, self.current_remaining - self.buffer_points)
        return safe_remaining >= estimated_cost
    
    def wait_for_rate_limit_reset(self, required_points: int) -> None:
        """
        Wait for rate limit reset if needed
        
        Args:
            required_points: Points needed for next operation
        """
        if not self.can_execute_query(required_points):
            if self.current_reset_at:
                wait_time = (self.current_reset_at - datetime.now()).total_seconds()
                if wait_time > 0:
                    print(f"⏳ Rate limit exceeded. Waiting {wait_time:.0f} seconds for reset...")
                    time.sleep(wait_time + 1)  # Add 1 second buffer
                    
                    # Refresh rate limit status
                    self.check_rate_limit()
    
    def execute_with_rate_limiting(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute query with automatic rate limiting
        
        Args:
            query: GraphQL query
            variables: Query variables
            
        Returns:
            Query result
        """
        start_time = time.time()
        estimated_cost = self.estimate_query_cost(query, variables)
        
        # Check rate limits before execution
        self.check_rate_limit()
        
        # Wait if necessary
        if not self.can_execute_query(estimated_cost):
            self.wait_for_rate_limit_reset(estimated_cost)
        
        # Execute query
        result = self.client.execute_query(query, variables)
        execution_time = time.time() - start_time
        
        # Record performance metrics
        cost_info = QueryCost(
            estimated_cost=estimated_cost,
            execution_time=execution_time
        )
        self.query_costs.append(cost_info)
        
        # Update rate limit info after execution
        self.check_rate_limit()
        
        return result
    
    def batch_execute_queries(self, queries: List[Dict[str, Any]], max_batch_size: int = 5) -> List[Dict[str, Any]]:
        """
        Execute multiple queries in batches with rate limiting
        
        Args:
            queries: List of {"query": str, "variables": dict} dictionaries
            max_batch_size: Maximum queries per batch
            
        Returns:
            List of query results
        """
        results = []
        total_queries = len(queries)
        
        print(f"🔄 Executing {total_queries} queries in batches of {max_batch_size}")
        
        for i in range(0, total_queries, max_batch_size):
            batch = queries[i:i + max_batch_size]
            batch_start = time.time()
            
            print(f"   📦 Batch {i//max_batch_size + 1}: Processing queries {i+1}-{min(i+max_batch_size, total_queries)}")
            
            # Calculate total estimated cost for batch
            total_estimated_cost = sum(
                self.estimate_query_cost(q["query"], q.get("variables"))
                for q in batch
            )
            
            # Check if we can execute the entire batch
            self.check_rate_limit()
            if not self.can_execute_query(total_estimated_cost):
                self.wait_for_rate_limit_reset(total_estimated_cost)
            
            # Execute batch
            batch_results = []
            for query_info in batch:
                try:
                    result = self.execute_with_rate_limiting(
                        query_info["query"],
                        query_info.get("variables")
                    )
                    batch_results.append(result)
                except Exception as e:
                    print(f"   ❌ Query failed: {e}")
                    batch_results.append({"error": str(e)})
            
            results.extend(batch_results)
            
            batch_time = time.time() - batch_start
            print(f"   ✅ Batch completed in {batch_time:.1f} seconds")
            
            # Brief pause between batches
            if i + max_batch_size < total_queries:
                time.sleep(1)
        
        print(f"✅ All {total_queries} queries completed")
        return results
    
    def optimize_pagination_query(self, base_query: str, variables: Dict[str, Any], max_pages: int = 10) -> List[Dict[str, Any]]:
        """
        Optimize paginated queries with smart page sizing
        
        Args:
            base_query: Base GraphQL query with pagination
            variables: Initial variables
            max_pages: Maximum pages to fetch
            
        Returns:
            List of all paginated results
        """
        results = []
        current_variables = variables.copy()
        page_count = 0
        
        # Start with conservative page size
        optimal_page_size = min(variables.get("first", 50), 50)
        current_variables["first"] = optimal_page_size
        
        while page_count < max_pages:
            # Execute query
            result = self.execute_with_rate_limiting(base_query, current_variables)
            
            if "errors" in result or not result:
                break
            
            results.append(result)
            page_count += 1
            
            # Check for next page
            page_info = self._extract_page_info(result)
            if not page_info or not page_info.get("hasNextPage"):
                break
            
            # Update cursor for next page
            current_variables["cursor"] = page_info.get("endCursor")
            
            # Optimize page size based on performance
            if self.optimization_enabled:
                optimal_page_size = self._calculate_optimal_page_size(optimal_page_size)
                current_variables["first"] = optimal_page_size
        
        print(f"📄 Paginated query completed: {page_count} pages fetched")
        return results
    
    def _extract_page_info(self, result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract pageInfo from nested GraphQL result"""
        # This is a simplified extraction - you might need to adapt for specific queries
        for key, value in result.items():
            if isinstance(value, dict):
                if "pageInfo" in value:
                    return value["pageInfo"]
                # Recursively search nested objects
                nested_page_info = self._extract_page_info(value)
                if nested_page_info:
                    return nested_page_info
        return None
    
    def _calculate_optimal_page_size(self, current_size: int) -> int:
        """Calculate optimal page size based on recent performance"""
        if not self.query_costs:
            return current_size
        
        # Analyze recent query performance
        recent_costs = self.query_costs[-10:]  # Last 10 queries
        avg_efficiency = sum(
            cost.efficiency_ratio for cost in recent_costs 
            if cost.efficiency_ratio
        ) / len([cost for cost in recent_costs if cost.efficiency_ratio])
        
        if avg_efficiency and avg_efficiency < 0.5:
            # Queries are more expensive than expected, reduce page size
            return max(10, int(current_size * 0.8))
        elif avg_efficiency and avg_efficiency > 0.8:
            # Queries are efficient, can increase page size
            return min(100, int(current_size * 1.2))
        
        return current_size
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance and rate limiting report"""
        if not self.query_costs:
            return {"message": "No query performance data available"}
        
        total_queries = len(self.query_costs)
        total_estimated_cost = sum(cost.estimated_cost for cost in self.query_costs)
        avg_execution_time = sum(
            cost.execution_time for cost in self.query_costs if cost.execution_time
        ) / len([cost for cost in self.query_costs if cost.execution_time])
        
        efficiency_ratios = [
            cost.efficiency_ratio for cost in self.query_costs if cost.efficiency_ratio
        ]
        avg_efficiency = sum(efficiency_ratios) / len(efficiency_ratios) if efficiency_ratios else None
        
        return {
            "total_queries_executed": total_queries,
            "total_estimated_cost": total_estimated_cost,
            "average_execution_time_seconds": avg_execution_time,
            "average_efficiency_ratio": avg_efficiency,
            "current_rate_limit": self.check_rate_limit(),
            "optimization_recommendations": self._generate_optimization_recommendations()
        }
    
    def _generate_optimization_recommendations(self) -> List[str]:
        """Generate optimization recommendations based on usage patterns"""
        recommendations = []
        
        if not self.query_costs:
            return recommendations
        
        # Analyze query patterns
        avg_cost = sum(cost.estimated_cost for cost in self.query_costs) / len(self.query_costs)
        
        if avg_cost > 50:
            recommendations.append("Consider reducing query complexity or implementing pagination")
        
        if self.current_remaining < self.current_limit * 0.2:
            recommendations.append("Rate limit usage is high - consider implementing query caching")
        
        execution_times = [cost.execution_time for cost in self.query_costs if cost.execution_time]
        if execution_times and sum(execution_times) / len(execution_times) > 5:
            recommendations.append("Slow query performance detected - review query complexity")
        
        return recommendations


def main():
    """Example usage of rate limit manager"""
    from ..config import SecurityConfig
    
    config = SecurityConfig()
    client = GitHubGraphQLClient(config.github_token)
    rate_manager = RateLimitManager(client)
    
    # Check current rate limit
    status = rate_manager.check_rate_limit()
    print(f"Rate limit status: {status['remaining']}/{status['limit']}")
    
    # Example query with rate limiting
    query = """
    query {
      viewer {
        login
        repositories(first: 10) {
          nodes {
            name
            vulnerabilityAlerts(first: 5) {
              totalCount
            }
          }
        }
      }
    }
    """
    
    result = rate_manager.execute_with_rate_limiting(query)
    print(f"Query executed successfully: {len(result)} fields returned")
    
    # Generate performance report
    report = rate_manager.get_performance_report()
    print(f"Performance report: {report['total_queries_executed']} queries executed")


if __name__ == "__main__":
    main()
```

---

## Real-World Security Workflows

### Learning Plan Step 7: Production Security Workflows

**Objective**: Build production-ready security workflows and integrations

**Time Investment**: 50 minutes

**What You'll Learn**:
- Create comprehensive security pipelines
- Integrate with security tools and platforms
- Build security reporting and alerting systems
- Implement compliance and audit workflows

### Step 7.1: Enterprise Security Pipeline

**File**: `src/github_security/enterprise/security_pipeline.py`

```python
"""
Enterprise-grade security pipeline for GitHub organizations
"""
import json
import csv
import asyncio
from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict

from ..client import GitHubGraphQLClient
from ..config import SecurityConfig
from ..scanner import VulnerabilityScanner
from ..analysis.security_engine import SecurityAnalysisEngine
from ..monitor.vulnerability_monitor import SecurityMonitor


@dataclass
class ComplianceReport:
    """Compliance report structure"""
    organization: str
    report_date: datetime
    total_repositories: int
    compliant_repositories: int
    non_compliant_repositories: int
    critical_findings: int
    high_findings: int
    compliance_score: float
    findings_by_category: Dict[str, int]
    action_items: List[str]


@dataclass
class SecurityMetrics:
    """Security metrics for dashboards"""
    timestamp: datetime
    total_vulnerabilities: int
    critical_vulnerabilities: int
    high_vulnerabilities: int
    mean_time_to_resolution: float
    vulnerability_trend: str  # "increasing", "decreasing", "stable"
    coverage_percentage: float


class EnterpriseSecurityPipeline:
    """
    Enterprise-grade security pipeline for GitHub organizations
    """
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.client = GitHubGraphQLClient(config.github_token)
        self.scanner = VulnerabilityScanner(config)
        self.analysis_engine = SecurityAnalysisEngine(self.client)
        self.monitor = SecurityMonitor(config)
        
        # Pipeline configuration
        self.compliance_standards = {
            "pci_dss": self._check_pci_compliance,
            "sox": self._check_sox_compliance,
            "hipaa": self._check_hipaa_compliance,
            "iso27001": self._check_iso27001_compliance
        }
        
        # Output directories
        self.reports_dir = Path("security_reports")
        self.reports_dir.mkdir(exist_ok=True)
        
        # Metrics storage
        self.metrics_history: List[SecurityMetrics] = []
    
    def run_full_security_pipeline(self, organization: str, compliance_frameworks: List[str] = None) -> Dict[str, Any]:
        """
        Run complete security pipeline for an organization
        
        Args:
            organization: GitHub organization name
            compliance_frameworks: List of compliance frameworks to check
            
        Returns:
            Complete pipeline results
        """
        print(f"🚀 Starting enterprise security pipeline for: {organization}")
        pipeline_start = datetime.now()
        
        # Default compliance frameworks
        if compliance_frameworks is None:
            compliance_frameworks = ["iso27001"]
        
        results = {
            "organization": organization,
            "pipeline_start": pipeline_start,
            "stages": {}
        }
        
        try:
            # Stage 1: Repository Discovery and Classification
            print("📋 Stage 1: Repository Discovery")
            repos = self._discover_repositories(organization)
            results["stages"]["discovery"] = {
                "total_repositories": len(repos),
                "repositories": repos
            }
            
            # Stage 2: Vulnerability Scanning
            print("🔍 Stage 2: Vulnerability Scanning")
            scan_results = self._scan_repositories(repos)
            results["stages"]["vulnerability_scan"] = {
                "scan_results": scan_results,
                "total_vulnerabilities": sum(r.vulnerability_count for r in scan_results)
            }
            
            # Stage 3: Security Analysis
            print("🔍 Stage 3: Security Analysis")
            analysis_results = self._analyze_repository_security(repos)
            results["stages"]["security_analysis"] = analysis_results
            
            # Stage 4: Compliance Assessment
            print("📊 Stage 4: Compliance Assessment")
            compliance_results = self._assess_compliance(repos, scan_results, compliance_frameworks)
            results["stages"]["compliance"] = compliance_results
            
            # Stage 5: Risk Assessment and Prioritization
            print("⚠️  Stage 5: Risk Assessment")
            risk_assessment = self._assess_organizational_risk(scan_results, analysis_results)
            results["stages"]["risk_assessment"] = risk_assessment
            
            # Stage 6: Report Generation
            print("📝 Stage 6: Report Generation")
            reports = self._generate_enterprise_reports(
                organization, results, compliance_frameworks
            )
            results["stages"]["reports"] = reports
            
            # Stage 7: Metrics and Monitoring
            print("📊 Stage 7: Metrics Collection")
            metrics = self._collect_security_metrics(scan_results, analysis_results)
            results["stages"]["metrics"] = metrics
            
            results["pipeline_end"] = datetime.now()
            results["pipeline_duration"] = (results["pipeline_end"] - pipeline_start).total_seconds()
            results["status"] = "completed"
            
            print(f"✅ Pipeline completed in {results['pipeline_duration']:.1f} seconds")
            return results
            
        except Exception as e:
            results["error"] = str(e)
            results["status"] = "failed"
            print(f"❌ Pipeline failed: {e}")
            return results
    
    def _discover_repositories(self, organization: str) -> List[Dict[str, Any]]:
        """Discover and classify repositories in organization"""
        query = """
        query DiscoverRepositories($org: String!, $cursor: String) {
          organization(login: $org) {
            repositories(first: 100, after: $cursor) {
              pageInfo {
                hasNextPage
                endCursor
              }
              nodes {
                name
                isPrivate
                visibility
                primaryLanguage {
                  name
                }
                createdAt
                updatedAt
                pushedAt
                isArchived
                isDisabled
                isFork
                stargazerCount
                forkCount
                
                # Security settings
                hasVulnerabilityAlertsEnabled
                hasDiscussionsEnabled
                
                # Repository topics for classification
                repositoryTopics(first: 10) {
                  nodes {
                    topic {
                      name
                    }
                  }
                }
                
                # Recent activity
                defaultBranchRef {
                  target {
                    ... on Commit {
                      history(first: 1) {
                        nodes {
                          committedDate
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
        """
        
        repositories = []
        cursor = None
        
        while True:
            variables = {"org": organization, "cursor": cursor}
            result = self.client.execute_query(query, variables)
            
            org_data = result.get("organization", {})
            if not org_data:
                break
            
            repos_data = org_data.get("repositories", {})
            repos = repos_data.get("nodes", [])
            
            for repo in repos:
                # Classify repository
                classification = self._classify_repository(repo)
                repo["classification"] = classification
                repositories.append(repo)
            
            # Check for next page
            page_info = repos_data.get("pageInfo", {})
            if not page_info.get("hasNextPage"):
                break
            
            cursor = page_info.get("endCursor")
        
        print(f"   📚 Discovered {len(repositories)} repositories")
        return repositories
    
    def _classify_repository(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Classify repository by type and risk level"""
        classification = {
            "type": "unknown",
            "risk_level": "medium",
            "business_critical": False,
            "contains_sensitive_data": False,
            "customer_facing": False,
            "regulatory_scope": []
        }
        
        name = repo_data.get("name", "").lower()
        topics = [
            topic["topic"]["name"].lower() 
            for topic in repo_data.get("repositoryTopics", {}).get("nodes", [])
        ]
        language = repo_data.get("primaryLanguage", {}).get("name", "").lower()
        
        # Classify by type
        if any(keyword in name for keyword in ["api", "service", "server"]):
            classification["type"] = "backend_service"
            classification["risk_level"] = "high"
        elif any(keyword in name for keyword in ["web", "app", "ui", "frontend"]):
            classification["type"] = "frontend_application"
            classification["customer_facing"] = True
        elif any(keyword in name for keyword in ["lib", "sdk", "package"]):
            classification["type"] = "library"
        elif any(keyword in name for keyword in ["doc", "guide", "example"]):
            classification["type"] = "documentation"
            classification["risk_level"] = "low"
        elif language in ["dockerfile", "shell", "makefile"]:
            classification["type"] = "infrastructure"
            classification["risk_level"] = "high"
        
        # Check for sensitive data indicators
        sensitive_keywords = ["auth", "payment", "billing", "user", "customer", "personal"]
        if any(keyword in name for keyword in sensitive_keywords):
            classification["contains_sensitive_data"] = True
            classification["risk_level"] = "high"
        
        # Check for business criticality indicators
        if repo_data.get("stargazerCount", 0) > 100 or "prod" in name or "main" in name:
            classification["business_critical"] = True
        
        # Regulatory scope based on topics and content
        if any(topic in ["finance", "payment", "banking"] for topic in topics):
            classification["regulatory_scope"].append("pci_dss")
        if any(topic in ["healthcare", "medical", "hipaa"] for topic in topics):
            classification["regulatory_scope"].append("hipaa")
        if any(topic in ["sox", "audit", "compliance"] for topic in topics):
            classification["regulatory_scope"].append("sox")
        
        return classification
    
    def _scan_repositories(self, repositories: List[Dict[str, Any]]) -> List[Any]:
        """Scan repositories for vulnerabilities"""
        scan_results = []
        
        # Prioritize critical repositories
        sorted_repos = sorted(
            repositories,
            key=lambda r: (
                r["classification"]["business_critical"],
                r["classification"]["risk_level"] == "high",
                r.get("stargazerCount", 0)
            ),
            reverse=True
        )
        
        for repo in sorted_repos[:self.config.max_repositories]:
            if repo.get("isArchived") or repo.get("isDisabled"):
                continue
            
            try:
                result = self.scanner.scan_repository(
                    repo["owner"]["login"] if "owner" in repo else "unknown",
                    repo["name"]
                )
                result.classification = repo["classification"]
                scan_results.append(result)
            except Exception as e:
                print(f"   ❌ Failed to scan {repo['name']}: {e}")
        
        return scan_results
    
    def _analyze_repository_security(self, repositories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform detailed security analysis"""
        analysis_results = {
            "total_analyzed": 0,
            "security_scores": [],
            "findings_summary": {},
            "recommendations": []
        }
        
        for repo in repositories:
            if repo.get("isArchived"):
                continue
            
            try:
                analysis = self.analysis_engine.analyze_repository_security(
                    repo["owner"]["login"] if "owner" in repo else "unknown",
                    repo["name"]
                )
                
                analysis_results["total_analyzed"] += 1
                
                if "security_score" in analysis:
                    analysis_results["security_scores"].append(analysis["security_score"])
                
                # Aggregate findings
                for finding in analysis.get("findings", []):
                    category = finding.get("category", "unknown")
                    severity = finding.get("severity", "unknown")
                    
                    key = f"{category}_{severity}"
                    analysis_results["findings_summary"][key] = (
                        analysis_results["findings_summary"].get(key, 0) + 1
                    )
                
            except Exception as e:
                print(f"   ❌ Failed to analyze {repo['name']}: {e}")
        
        return analysis_results
    
    def _assess_compliance(self, repositories: List[Dict[str, Any]], scan_results: List[Any], 
                          frameworks: List[str]) -> Dict[str, Any]:
        """Assess compliance with regulatory frameworks"""
        compliance_results = {}
        
        for framework in frameworks:
            if framework in self.compliance_standards:
                check_function = self.compliance_standards[framework]
                compliance_results[framework] = check_function(repositories, scan_results)
        
        return compliance_results
    
    def _check_iso27001_compliance(self, repositories: List[Dict[str, Any]], scan_results: List[Any]) -> Dict[str, Any]:
        """Check ISO 27001 compliance requirements"""
        findings = []
        
        # A.12.2.1 - Controls against malware
        repos_without_security_scanning = [
            repo for repo in repositories 
            if not repo.get("hasVulnerabilityAlertsEnabled", False)
        ]
        if repos_without_security_scanning:
            findings.append({
                "control": "A.12.2.1",
                "description": "Controls against malware",
                "finding": f"{len(repos_without_security_scanning)} repositories lack vulnerability scanning",
                "severity": "medium"
            })
        
        # A.12.6.1 - Management of technical vulnerabilities
        high_risk_vulnerabilities = sum(
            result.summary.critical_count + result.summary.high_count 
            for result in scan_results
        )
        if high_risk_vulnerabilities > 0:
            findings.append({
                "control": "A.12.6.1",
                "description": "Management of technical vulnerabilities",
                "finding": f"{high_risk_vulnerabilities} high/critical vulnerabilities found",
                "severity": "high"
            })
        
        # A.9.2.1 - User registration and de-registration
        # This would require additional API calls to check user access
        
        compliance_score = max(0, 100 - len(findings) * 10)
        
        return {
            "framework": "ISO 27001",
            "compliance_score": compliance_score,
            "findings": findings,
            "compliant": compliance_score >= 80
        }
    
    def _check_pci_compliance(self, repositories: List[Dict[str, Any]], scan_results: List[Any]) -> Dict[str, Any]:
        """Check PCI DSS compliance requirements"""
        # Implementation would include PCI DSS specific checks
        return {"framework": "PCI DSS", "status": "not_implemented"}
    
    def _check_sox_compliance(self, repositories: List[Dict[str, Any]], scan_results: List[Any]) -> Dict[str, Any]:
        """Check SOX compliance requirements"""
        # Implementation would include SOX specific checks
        return {"framework": "SOX", "status": "not_implemented"}
    
    def _check_hipaa_compliance(self, repositories: List[Dict[str, Any]], scan_results: List[Any]) -> Dict[str, Any]:
        """Check HIPAA compliance requirements"""
        # Implementation would include HIPAA specific checks
        return {"framework": "HIPAA", "status": "not_implemented"}
    
    def _assess_organizational_risk(self, scan_results: List[Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall organizational security risk"""
        total_repos = len(scan_results)
        if total_repos == 0:
            return {"risk_level": "unknown", "score": 0}
        
        # Calculate risk metrics
        critical_vulns = sum(result.summary.critical_count for result in scan_results)
        high_vulns = sum(result.summary.high_count for result in scan_results)
        total_vulns = sum(result.vulnerability_count for result in scan_results)
        
        # Risk scoring algorithm
        risk_score = (
            critical_vulns * 10 +
            high_vulns * 5 +
            total_vulns * 1
        ) / total_repos
        
        # Determine risk level
        if risk_score > 50:
            risk_level = "critical"
        elif risk_score > 20:
            risk_level = "high"
        elif risk_score > 10:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        # Business impact assessment
        critical_repos = [
            result for result in scan_results 
            if getattr(result, 'classification', {}).get('business_critical', False)
        ]
        
        critical_risk_repos = [
            result for result in critical_repos 
            if result.summary.has_critical_vulnerabilities
        ]
        
        return {
            "overall_risk_level": risk_level,
            "risk_score": risk_score,
            "total_repositories": total_repos,
            "vulnerable_repositories": len([r for r in scan_results if r.vulnerability_count > 0]),
            "critical_business_repos_at_risk": len(critical_risk_repos),
            "recommendations": self._generate_risk_recommendations(risk_level, scan_results)
        }
    
    def _generate_risk_recommendations(self, risk_level: str, scan_results: List[Any]) -> List[str]:
        """Generate risk-based recommendations"""
        recommendations = []
        
        if risk_level == "critical":
            recommendations.extend([
                "🚨 IMMEDIATE ACTION REQUIRED: Critical vulnerabilities detected",
                "🛑 Consider emergency patching procedures",
                "📞 Notify security incident response team",
                "🔒 Implement additional monitoring and access controls"
            ])
        elif risk_level == "high":
            recommendations.extend([
                "⚠️  HIGH PRIORITY: Address vulnerabilities within 48 hours",
                "🔍 Increase security monitoring frequency",
                "👥 Review access controls and permissions"
            ])
        elif risk_level == "medium":
            recommendations.extend([
                "📋 MEDIUM PRIORITY: Address vulnerabilities within 1 week",
                "🔄 Review and update security policies",
                "📊 Implement regular security assessments"
            ])
        
        # Universal recommendations
        recommendations.extend([
            "✅ Enable Dependabot alerts for all repositories",
            "🏗️  Implement security-focused development practices",
            "📚 Provide security training for development teams",
            "🔐 Regular security audits and penetration testing"
        ])
        
        return recommendations
    
    def _generate_enterprise_reports(self, organization: str, pipeline_results: Dict[str, Any], 
                                   compliance_frameworks: List[str]) -> Dict[str, str]:
        """Generate comprehensive enterprise security reports"""
        reports = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Executive Summary Report
        exec_report_path = self.reports_dir / f"executive_summary_{organization}_{timestamp}.json"
        exec_summary = self._create_executive_summary(organization, pipeline_results)
        with open(exec_report_path, 'w') as f:
            json.dump(exec_summary, f, indent=2, default=str)
        reports["executive_summary"] = str(exec_report_path)
        
        # Detailed Technical Report
        tech_report_path = self.reports_dir / f"technical_report_{organization}_{timestamp}.json"
        with open(tech_report_path, 'w') as f:
            json.dump(pipeline_results, f, indent=2, default=str)
        reports["technical_report"] = str(tech_report_path)
        
        # CSV Export for spreadsheet analysis
        csv_report_path = self.reports_dir / f"vulnerability_summary_{organization}_{timestamp}.csv"
        self._export_vulnerabilities_csv(pipeline_results, csv_report_path)
        reports["csv_export"] = str(csv_report_path)
        
        # Compliance Report
        if compliance_frameworks:
            compliance_report_path = self.reports_dir / f"compliance_report_{organization}_{timestamp}.json"
            compliance_data = pipeline_results.get("stages", {}).get("compliance", {})
            with open(compliance_report_path, 'w') as f:
                json.dump(compliance_data, f, indent=2, default=str)
            reports["compliance_report"] = str(compliance_report_path)
        
        print(f"   📁 Reports generated in: {self.reports_dir}")
        return reports
    
    def _create_executive_summary(self, organization: str, pipeline_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create executive summary for leadership"""
        stages = pipeline_results.get("stages", {})
        
        # Extract key metrics
        discovery = stages.get("discovery", {})
        vulnerability_scan = stages.get("vulnerability_scan", {})
        risk_assessment = stages.get("risk_assessment", {})
        compliance = stages.get("compliance", {})
        
        scan_results = vulnerability_scan.get("scan_results", [])
        total_vulns = sum(result.vulnerability_count for result in scan_results)
        critical_vulns = sum(result.summary.critical_count for result in scan_results)
        high_vulns = sum(result.summary.high_count for result in scan_results)
        
        return {
            "organization": organization,
            "report_date": datetime.now().isoformat(),
            "executive_summary": {
                "total_repositories": discovery.get("total_repositories", 0),
                "repositories_scanned": len(scan_results),
                "total_vulnerabilities": total_vulns,
                "critical_vulnerabilities": critical_vulns,
                "high_vulnerabilities": high_vulns,
                "overall_risk_level": risk_assessment.get("overall_risk_level", "unknown"),
                "risk_score": risk_assessment.get("risk_score", 0)
            },
            "key_findings": [
                f"Total of {total_vulns} vulnerabilities found across {len(scan_results)} repositories",
                f"{critical_vulns} critical and {high_vulns} high severity vulnerabilities require immediate attention",
                f"Overall organizational risk level: {risk_assessment.get('overall_risk_level', 'unknown')}"
            ],
            "recommendations": risk_assessment.get("recommendations", [])[:5],  # Top 5
            "compliance_status": {
                framework: result.get("compliant", False)
                for framework, result in compliance.items()
            }
        }
    
    def _export_vulnerabilities_csv(self, pipeline_results: Dict[str, Any], output_path: Path) -> None:
        """Export vulnerability data to CSV for analysis"""
        scan_results = pipeline_results.get("stages", {}).get("vulnerability_scan", {}).get("scan_results", [])
        
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = [
                'repository', 'total_vulnerabilities', 'critical_count', 'high_count',
                'medium_count', 'low_count', 'risk_score', 'classification_type',
                'business_critical', 'scan_time'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in scan_results:
                classification = getattr(result, 'classification', {})
                writer.writerow({
                    'repository': result.repository,
                    'total_vulnerabilities': result.vulnerability_count,
                    'critical_count': result.summary.critical_count,
                    'high_count': result.summary.high_count,
                    'medium_count': result.summary.moderate_count,
                    'low_count': result.summary.low_count,
                    'risk_score': result.risk_score,
                    'classification_type': classification.get('type', 'unknown'),
                    'business_critical': classification.get('business_critical', False),
                    'scan_time': result.scan_time.isoformat()
                })
    
    def _collect_security_metrics(self, scan_results: List[Any], analysis_results: Dict[str, Any]) -> SecurityMetrics:
        """Collect security metrics for monitoring and trending"""
        total_vulns = sum(result.vulnerability_count for result in scan_results)
        critical_vulns = sum(result.summary.critical_count for result in scan_results)
        high_vulns = sum(result.summary.high_count for result in scan_results)
        
        # Calculate trend (simplified - would need historical data)
        trend = "stable"  # Would compare with previous metrics
        
        metrics = SecurityMetrics(
            timestamp=datetime.now(),
            total_vulnerabilities=total_vulns,
            critical_vulnerabilities=critical_vulns,
            high_vulnerabilities=high_vulns,
            mean_time_to_resolution=0.0,  # Would need issue tracking integration
            vulnerability_trend=trend,
            coverage_percentage=100.0 if scan_results else 0.0
        )
        
        self.metrics_history.append(metrics)
        return metrics


def main():
    """Example usage of enterprise security pipeline"""
    config = SecurityConfig()
    pipeline = EnterpriseSecurityPipeline(config)
    
    # Run full pipeline for an organization
    results = pipeline.run_full_security_pipeline(
        organization="octocat",
        compliance_frameworks=["iso27001"]
    )
    
    print(f"Pipeline Status: {results['status']}")
    if results["status"] == "completed":
        risk = results["stages"]["risk_assessment"]
        print(f"Overall Risk Level: {risk['overall_risk_level']}")
        print(f"Risk Score: {risk['risk_score']:.1f}")


if __name__ == "__main__":
    main()
```

---

## Troubleshooting and Common Issues

### Learning Plan Step 8: Common Pitfalls and Solutions

**Objective**: Master troubleshooting GitHub GraphQL security implementations

**Time Investment**: 20 minutes

**What You'll Learn**:
- Common API errors and their solutions
- Performance troubleshooting techniques
- Security-specific GraphQL gotchas
- Debugging and monitoring strategies

### Common Issue 1: Rate Limit Exceeded

**Problem**: Hitting GitHub's GraphQL rate limits during large-scale scanning

**Symptoms**:
```
GraphQLError: Rate limit exceeded. Reset at 2024-01-15T15:30:00Z
```

**Solutions**:

```python
# Solution 1: Implement exponential backoff
def handle_rate_limit_error(error_response):
    """Handle rate limit with exponential backoff"""
    reset_time = error_response.get('extensions', {}).get('rateLimitReset')
    if reset_time:
        wait_time = datetime.fromisoformat(reset_time) - datetime.now()
        backoff_time = min(wait_time.total_seconds(), 60)  # Max 1 minute
        
        print(f"Rate limited. Waiting {backoff_time:.0f} seconds...")
        time.sleep(backoff_time)
        return True
    return False

# Solution 2: Query cost estimation
def estimate_and_batch_queries(queries, max_cost_per_batch=1000):
    """Batch queries based on estimated cost"""
    batches = []
    current_batch = []
    current_cost = 0
    
    for query in queries:
        estimated_cost = estimate_query_cost(query)
        
        if current_cost + estimated_cost > max_cost_per_batch:
            if current_batch:
                batches.append(current_batch)
                current_batch = []
                current_cost = 0
        
        current_batch.append(query)
        current_cost += estimated_cost
    
    if current_batch:
        batches.append(current_batch)
    
    return batches
```

### Common Issue 2: Permission Denied Errors

**Problem**: Token lacks necessary permissions for security queries

**Symptoms**:
```
GraphQLError: Resource not accessible by integration
```

**Solutions**:

```python
def diagnose_permission_issues(client):
    """Diagnose and fix permission issues"""
    
    # Test basic permissions
    test_queries = {
        "viewer": "query { viewer { login } }",
        "repositories": "query { viewer { repositories(first: 1) { totalCount } } }",
        "vulnerabilities": """
        query { 
          viewer { 
            repositories(first: 1) { 
              nodes { 
                vulnerabilityAlerts(first: 1) { totalCount } 
              } 
            } 
          } 
        }""",
        "organizations": "query { viewer { organizations(first: 1) { totalCount } } }"
    }
    
    results = {}
    for test_name, query in test_queries.items():
        try:
            result = client.execute_query(query)
            results[test_name] = "✅ Success"
        except Exception as e:
            results[test_name] = f"❌ Failed: {str(e)}"
    
    # Generate recommendations
    recommendations = []
    if "Failed" in results.get("viewer", ""):
        recommendations.append("Token may be invalid or expired")
    if "Failed" in results.get("repositories", ""):
        recommendations.append("Need 'repo' scope for repository access")
    if "Failed" in results.get("vulnerabilities", ""):
        recommendations.append("Need 'security_events' scope for vulnerability data")
    if "Failed" in results.get("organizations", ""):
        recommendations.append("Need 'read:org' scope for organization data")
    
    return results, recommendations

# Usage example
def validate_token_permissions():
    """Validate and fix token permissions"""
    client = GitHubGraphQLClient(config.github_token)
    results, recommendations = diagnose_permission_issues(client)
    
    print("Permission Test Results:")
    for test, result in results.items():
        print(f"  {test}: {result}")
    
    if recommendations:
        print("\nRecommendations:")
        for rec in recommendations:
            print(f"  • {rec}")
```

### Common Issue 3: Large Query Timeouts

**Problem**: Complex security queries timing out

**Symptoms**:
```
requests.exceptions.Timeout: HTTPSConnectionPool timeout
```

**Solutions**:

```python
def optimize_large_queries():
    """Strategies for handling large, complex queries"""
    
    # Strategy 1: Break down into smaller queries
    def scan_organization_incrementally(org_name, batch_size=20):
        """Scan organization repositories in smaller batches"""
        repositories = []
        cursor = None
        
        while True:
            query = """
            query GetRepos($org: String!, $cursor: String, $first: Int!) {
              organization(login: $org) {
                repositories(first: $first, after: $cursor) {
                  pageInfo {
                    hasNextPage
                    endCursor
                  }
                  nodes {
                    name
                    isPrivate
                    # Minimal fields to reduce query complexity
                  }
                }
              }
            }
            """
            
            variables = {"org": org_name, "cursor": cursor, "first": batch_size}
            result = client.execute_query(query, variables)
            
            org_data = result.get("organization", {})
            repos_data = org_data.get("repositories", {})
            repos = repos_data.get("nodes", [])
            
            repositories.extend(repos)
            
            page_info = repos_data.get("pageInfo", {})
            if not page_info.get("hasNextPage"):
                break
                
            cursor = page_info.get("endCursor")
        
        return repositories
    
    # Strategy 2: Parallel processing with threading
    import concurrent.futures
    
    def scan_repositories_parallel(repositories, max_workers=5):
        """Scan repositories in parallel"""
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_repo = {
                executor.submit(scan_single_repository, repo): repo 
                for repo in repositories
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_repo):
                repo = future_to_repo[future]
                try:
                    result = future.result(timeout=30)  # 30 second timeout per repo
                    results.append(result)
                except Exception as e:
                    print(f"Failed to scan {repo['name']}: {e}")
        
        return results
```

### Common Issue 4: Incomplete Vulnerability Data

**Problem**: Missing or incomplete vulnerability information

**Symptoms**:
- Empty vulnerability alerts for repositories with known issues
- Missing CVSS scores or security advisories

**Solutions**:

```python
def verify_vulnerability_data_completeness(repo_owner, repo_name):
    """Verify and enhance vulnerability data collection"""
    
    # Primary vulnerability query
    primary_query = """
    query PrimaryVulnCheck($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        vulnerabilityAlerts(first: 100) {
          totalCount
          nodes {
            id
            state
            createdAt
            securityVulnerability {
              severity
              package {
                name
                ecosystem
              }
              advisory {
                ghsaId
                summary
              }
            }
          }
        }
      }
    }
    """
    
    # Backup: Check security advisories directly
    advisory_query = """
    query SecurityAdvisories($cursor: String) {
      securityAdvisories(first: 100, after: $cursor) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          ghsaId
          summary
          severity
          vulnerabilities(first: 10) {
            nodes {
              package {
                name
                ecosystem
              }
            }
          }
        }
      }
    }
    """
    
    variables = {"owner": repo_owner, "name": repo_name}
    
    try:
        # Try primary method
        result = client.execute_query(primary_query, variables)
        alerts = result.get("repository", {}).get("vulnerabilityAlerts", {}).get("nodes", [])
        
        if alerts:
            return alerts, "primary"
        
        # Fallback to advisory search
        print(f"No direct alerts found for {repo_owner}/{repo_name}, checking security advisories...")
        
        # This would require additional logic to match advisories to the repository
        # based on dependencies, which is more complex
        
        return [], "none"
        
    except Exception as e:
        print(f"Error checking vulnerabilities for {repo_owner}/{repo_name}: {e}")
        return [], "error"

def enhance_vulnerability_scanning():
    """Enhanced vulnerability scanning with multiple data sources"""
    
    def cross_reference_vulnerabilities(repo_data, external_sources=None):
        """Cross-reference GitHub data with external vulnerability databases"""
        
        github_vulns = repo_data.get("vulnerability_alerts", [])
        
        # Add external vulnerability data sources
        if external_sources:
            for source in external_sources:
                if source == "osv":
                    # Query OSV (Open Source Vulnerabilities) database
                    osv_vulns = query_osv_database(repo_data)
                    github_vulns.extend(osv_vulns)
                elif source == "snyk":
                    # Query Snyk database (would require API key)
                    snyk_vulns = query_snyk_database(repo_data)
                    github_vulns.extend(snyk_vulns)
        
        return github_vulns
    
    def query_osv_database(repo_data):
        """Query OSV database for additional vulnerability data"""
        # Implementation would make HTTP requests to OSV API
        # https://osv.dev/docs/
        return []  # Placeholder
    
    def query_snyk_database(repo_data):
        """Query Snyk database for additional vulnerability data"""
        # Implementation would use Snyk API
        return []  # Placeholder
```

### Common Issue 5: Memory Issues with Large Datasets

**Problem**: Running out of memory when processing large organizations

**Solutions**:

```python
def memory_efficient_scanning():
    """Memory-efficient scanning strategies"""
    
    class StreamingVulnerabilityScanner:
        """Process repositories one at a time to minimize memory usage"""
        
        def __init__(self, config):
            self.config = config
            self.client = GitHubGraphQLClient(config.github_token)
        
        def scan_organization_streaming(self, org_name, output_file=None):
            """Scan organization with streaming processing"""
            
            processed_count = 0
            total_vulnerabilities = 0
            
            # Open output file for streaming results
            with open(output_file or f"{org_name}_scan_results.jsonl", 'w') as f:
                
                for repo in self.get_repositories_generator(org_name):
                    try:
                        # Process one repository at a time
                        result = self.scan_single_repository(repo)
                        
                        # Write result immediately and free memory
                        f.write(json.dumps(result, default=str) + '\n')
                        f.flush()  # Ensure data is written
                        
                        processed_count += 1
                        total_vulnerabilities += result.get('vulnerability_count', 0)
                        
                        # Progress reporting
                        if processed_count % 10 == 0:
                            print(f"Processed {processed_count} repositories, "
                                  f"found {total_vulnerabilities} vulnerabilities")
                        
                        # Clear any caches or temporary data
                        del result
                        
                    except Exception as e:
                        print(f"Error processing {repo.get('name', 'unknown')}: {e}")
            
            return {
                "processed_repositories": processed_count,
                "total_vulnerabilities": total_vulnerabilities,
                "output_file": output_file
            }
        
        def get_repositories_generator(self, org_name):
            """Generator that yields repositories one at a time"""
            cursor = None
            
            while True:
                query = """
                query GetRepos($org: String!, $cursor: String) {
                  organization(login: $org) {
                    repositories(first: 50, after: $cursor) {
                      pageInfo {
                        hasNextPage
                        endCursor
                      }
                      nodes {
                        name
                        isPrivate
                        primaryLanguage { name }
                      }
                    }
                  }
                }
                """
                
                variables = {"org": org_name, "cursor": cursor}
                result = self.client.execute_query(query, variables)
                
                org_data = result.get("organization", {})
                repos_data = org_data.get("repositories", {})
                repos = repos_data.get("nodes", [])
                
                # Yield each repository
                for repo in repos:
                    yield repo
                
                # Check for next page
                page_info = repos_data.get("pageInfo", {})
                if not page_info.get("hasNextPage"):
                    break
                    
                cursor = page_info.get("endCursor")
```

---

## Pro Tips and Advanced Techniques

### Learning Plan Step 9: Master-Level GraphQL Security

**Objective**: Advanced techniques for expert-level GitHub GraphQL security

**Time Investment**: 30 minutes

**What You'll Learn**:
- Advanced query optimization techniques
- Security automation patterns
- Integration with external security tools
- Custom security rule engines

### Pro Tip 1: Custom Security Rule Engine

Build a flexible rule engine for custom security policies:

```python
"""
Advanced security rule engine for custom policies
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Callable
from dataclasses import dataclass
from enum import Enum

class RuleSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class SecurityRule:
    """Define a custom security rule"""
    id: str
    name: str
    description: str
    severity: RuleSeverity
    category: str
    check_function: Callable[[Dict[str, Any]], bool]
    recommendation: str

class SecurityRuleEngine:
    """Advanced security rule engine"""
    
    def __init__(self):
        self.rules: List[SecurityRule] = []
        self.custom_rules: Dict[str, SecurityRule] = {}
    
    def register_rule(self, rule: SecurityRule):
        """Register a new security rule"""
        self.rules.append(rule)
        self.custom_rules[rule.id] = rule
    
    def create_vulnerability_rules(self):
        """Create comprehensive vulnerability-based rules"""
        
        # Rule: Critical vulnerabilities in production repositories
        self.register_rule(SecurityRule(
            id="critical_vulns_prod",
            name="Critical Vulnerabilities in Production",
            description="Production repositories with critical vulnerabilities",
            severity=RuleSeverity.CRITICAL,
            category="vulnerability",
            check_function=lambda repo: (
                repo.get("classification", {}).get("type") == "backend_service" and
                repo.get("vulnerability_summary", {}).get("critical_count", 0) > 0
            ),
            recommendation="Immediately patch critical vulnerabilities in production services"
        ))
        
        # Rule: High vulnerability count
        self.register_rule(SecurityRule(
            id="high_vuln_count",
            name="High Vulnerability Count",
            description="Repositories with excessive vulnerability counts",
            severity=RuleSeverity.HIGH,
            category="vulnerability",
            check_function=lambda repo: repo.get("vulnerability_count", 0) > 50,
            recommendation="Review dependency management and update vulnerable packages"
        ))
        
        # Rule: Stale vulnerabilities
        self.register_rule(SecurityRule(
            id="stale_vulnerabilities",
            name="Stale Vulnerabilities",
            description="Vulnerabilities older than 90 days",
            severity=RuleSeverity.MEDIUM,
            category="vulnerability",
            check_function=lambda repo: self._has_stale_vulnerabilities(repo, days=90),
            recommendation="Establish SLA for vulnerability remediation"
        ))
    
    def create_configuration_rules(self):
        """Create configuration-based security rules"""
        
        # Rule: Missing vulnerability alerts
        self.register_rule(SecurityRule(
            id="missing_vuln_alerts",
            name="Missing Vulnerability Alerts",
            description="Repositories without vulnerability alerts enabled",
            severity=RuleSeverity.MEDIUM,
            category="configuration",
            check_function=lambda repo: not repo.get("hasVulnerabilityAlertsEnabled", False),
            recommendation="Enable vulnerability alerts for all repositories"
        ))
        
        # Rule: Public repositories with sensitive data indicators
        self.register_rule(SecurityRule(
            id="public_sensitive_data",
            name="Public Repository with Sensitive Data",
            description="Public repositories containing sensitive data indicators",
            severity=RuleSeverity.HIGH,
            category="configuration",
            check_function=lambda repo: (
                not repo.get("isPrivate", True) and
                repo.get("classification", {}).get("contains_sensitive_data", False)
            ),
            recommendation="Review repository privacy settings and data classification"
        ))
    
    def create_access_control_rules(self):
        """Create access control rules"""
        
        # Rule: Excessive admin access
        self.register_rule(SecurityRule(
            id="excessive_admin_access",
            name="Excessive Admin Access",
            description="Too many users with admin access",
            severity=RuleSeverity.MEDIUM,
            category="access",
            check_function=lambda repo: len(repo.get("admin_users", [])) > 5,
            recommendation="Review admin access and apply principle of least privilege"
        ))
        
        # Rule: Weak branch protection
        self.register_rule(SecurityRule(
            id="weak_branch_protection",
            name="Weak Branch Protection",
            description="Main branch lacks adequate protection",
            severity=RuleSeverity.MEDIUM,
            category="access",
            check_function=lambda repo: not self._has_strong_branch_protection(repo),
            recommendation="Implement strong branch protection rules"
        ))
    
    def evaluate_repository(self, repo_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluate all rules against a repository"""
        violations = []
        
        for rule in self.rules:
            try:
                if rule.check_function(repo_data):
                    violations.append({
                        "rule_id": rule.id,
                        "rule_name": rule.name,
                        "description": rule.description,
                        "severity": rule.severity.value,
                        "category": rule.category,
                        "recommendation": rule.recommendation,
                        "repository": repo_data.get("name", "unknown")
                    })
            except Exception as e:
                print(f"Error evaluating rule {rule.id}: {e}")
        
        return violations
    
    def _has_stale_vulnerabilities(self, repo: Dict[str, Any], days: int) -> bool:
        """Check if repository has vulnerabilities older than specified days"""
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for alert in repo.get("vulnerability_alerts", []):
            created_at = alert.get("createdAt")
            if created_at:
                alert_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                if alert_date < cutoff_date:
                    return True
        
        return False
    
    def _has_strong_branch_protection(self, repo: Dict[str, Any]) -> bool:
        """Check if repository has strong branch protection"""
        protection_rules = repo.get("branchProtectionRules", [])
        
        for rule in protection_rules:
            if (rule.get("requiresApprovingReviews") and
                rule.get("requiredApprovingReviewCount", 0) >= 2 and
                rule.get("requiresStatusChecks") and
                not rule.get("allowsForcePushes", True)):
                return True
        
        return False
    
    def generate_policy_report(self, scan_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive policy compliance report"""
        all_violations = []
        violation_summary = {}
        
        for repo_data in scan_results:
            violations = self.evaluate_repository(repo_data)
            all_violations.extend(violations)
            
            # Count violations by severity
            for violation in violations:
                severity = violation["severity"]
                violation_summary[severity] = violation_summary.get(severity, 0) + 1
        
        # Generate policy recommendations
        policy_recommendations = []
        if violation_summary.get("critical", 0) > 0:
            policy_recommendations.append("Establish emergency response procedures for critical violations")
        if violation_summary.get("high", 0) > 5:
            policy_recommendations.append("Implement automated policy enforcement")
        if violation_summary.get("medium", 0) > 20:
            policy_recommendations.append("Review and strengthen security policies")
        
        return {
            "total_violations": len(all_violations),
            "violation_summary": violation_summary,
            "violations_by_category": self._group_violations_by_category(all_violations),
            "policy_recommendations": policy_recommendations,
            "detailed_violations": all_violations
        }
    
    def _group_violations_by_category(self, violations: List[Dict[str, Any]]) -> Dict[str, int]:
        """Group violations by category"""
        categories = {}
        for violation in violations:
            category = violation["category"]
            categories[category] = categories.get(category, 0) + 1
        return categories

# Usage example
def implement_custom_security_policies():
    """Example of implementing custom security policies"""
    
    # Initialize rule engine
    rule_engine = SecurityRuleEngine()
    
    # Register built-in rules
    rule_engine.create_vulnerability_rules()
    rule_engine.create_configuration_rules()
    rule_engine.create_access_control_rules()
    
    # Add custom organizational rules
    rule_engine.register_rule(SecurityRule(
        id="fintech_compliance",
        name="FinTech Compliance Requirements",
        description="Financial repositories must meet specific security requirements",
        severity=RuleSeverity.HIGH,
        category="compliance",
        check_function=lambda repo: (
            "finance" in repo.get("classification", {}).get("regulatory_scope", []) and
            (repo.get("vulnerability_count", 0) > 0 or 
             not repo.get("hasVulnerabilityAlertsEnabled", False))
        ),
        recommendation="Ensure zero vulnerabilities and enabled monitoring for financial services"
    ))
    
    # Evaluate repositories
    scan_results = [...]  # Your scan results
    policy_report = rule_engine.generate_policy_report(scan_results)
    
    print(f"Policy Violations: {policy_report['total_violations']}")
    print(f"Critical: {policy_report['violation_summary'].get('critical', 0)}")
    print(f"High: {policy_report['violation_summary'].get('high', 0)}")
```

### Pro Tip 2: GraphQL Query Optimization Patterns

Advanced query patterns for maximum efficiency:

```python
"""
Advanced GraphQL query optimization patterns
"""

class GraphQLQueryOptimizer:
    """Advanced query optimization techniques"""
    
    def __init__(self, client):
        self.client = client
        self.query_cache = {}
        self.fragment_library = {}
    
    def create_fragment_library(self):
        """Create reusable GraphQL fragments"""
        
        self.fragment_library = {
            "repositoryBasics": """
            fragment RepositoryBasics on Repository {
              id
              name
              isPrivate
              primaryLanguage {
                name
              }
              createdAt
              updatedAt
            }
            """,
            
            "vulnerabilityDetails": """
            fragment VulnerabilityDetails on RepositoryVulnerabilityAlert {
              id
              createdAt
              state
              securityVulnerability {
                severity
                package {
                  name
                  ecosystem
                }
                advisory {
                  ghsaId
                  summary
                  cvss {
                    score
                  }
                }
              }
            }
            """,
            
            "securitySettings": """
            fragment SecuritySettings on Repository {
              hasVulnerabilityAlertsEnabled
              hasDiscussionsEnabled
              branchProtectionRules(first: 5) {
                nodes {
                  pattern
                  requiresApprovingReviews
                  requiredApprovingReviewCount
                }
              }
            }
            """
        }
    
    def build_optimized_query(self, query_type: str, variables: Dict[str, Any]) -> str:
        """Build optimized queries using fragments"""
        
        if query_type == "comprehensive_security_scan":
            return f"""
            {self.fragment_library['repositoryBasics']}
            {self.fragment_library['vulnerabilityDetails']}
            {self.fragment_library['securitySettings']}
            
            query ComprehensiveSecurityScan($owner: String!, $name: String!) {{
              repository(owner: $owner, name: $name) {{
                ...RepositoryBasics
                ...SecuritySettings
                
                vulnerabilityAlerts(first: 100) {{
                  totalCount
                  nodes {{
                    ...VulnerabilityDetails
                  }}
                }}
                
                dependencyGraphManifests(first: 10) {{
                  nodes {{
                    filename
                    dependencies(first: 50) {{
                      nodes {{
                        packageName
                        requirements
                      }}
                    }}
                  }}
                }}
              }}
            }}
            """
        
        elif query_type == "organization_overview":
            return f"""
            {self.fragment_library['repositoryBasics']}
            
            query OrganizationOverview($org: String!, $cursor: String) {{
              organization(login: $org) {{
                repositories(first: 100, after: $cursor) {{
                  pageInfo {{
                    hasNextPage
                    endCursor
                  }}
                  nodes {{
                    ...RepositoryBasics
                    vulnerabilityAlerts(first: 1) {{
                      totalCount
                    }}
                  }}
                }}
              }}
            }}
            """
    
    def execute_with_caching(self, query: str, variables: Dict[str, Any], cache_ttl: int = 300) -> Dict[str, Any]:
        """Execute query with intelligent caching"""
        import hashlib
        import time
        
        # Create cache key
        cache_key = hashlib.md5(f"{query}{str(variables)}".encode()).hexdigest()
        
        # Check cache
        if cache_key in self.query_cache:
            cached_result, timestamp = self.query_cache[cache_key]
            if time.time() - timestamp < cache_ttl:
                print(f"Cache hit for query {cache_key[:8]}...")
                return cached_result
        
        # Execute query
        result = self.client.execute_query(query, variables)
        
        # Cache result
        self.query_cache[cache_key] = (result, time.time())
        
        return result
    
    def parallel_query_execution(self, queries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute multiple queries in parallel"""
        import concurrent.futures
        import threading
        
        results = []
        lock = threading.Lock()
        
        def execute_single_query(query_info):
            try:
                result = self.execute_with_caching(
                    query_info["query"],
                    query_info.get("variables", {})
                )
                with lock:
                    results.append({
                        "id": query_info.get("id", "unknown"),
                        "result": result,
                        "error": None
                    })
            except Exception as e:
                with lock:
                    results.append({
                        "id": query_info.get("id", "unknown"),
                        "result": None,
                        "error": str(e)
                    })
        
        # Execute queries in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(execute_single_query, query) for query in queries]
            concurrent.futures.wait(futures)
        
        return results
```

### Pro Tip 3: Integration with External Security Tools

Integrate GitHub GraphQL with popular security tools:

```python
"""
Integration patterns with external security tools
"""

class SecurityToolIntegration:
    """Integrate GitHub security data with external tools"""
    
    def __init__(self, github_client):
        self.github_client = github_client
    
    def export_to_splunk(self, scan_results: List[Dict[str, Any]], splunk_config: Dict[str, str]):
        """Export security data to Splunk for analysis"""
        import requests
        
        splunk_url = splunk_config["hec_url"]
        splunk_token = splunk_config["hec_token"]
        
        headers = {
            "Authorization": f"Splunk {splunk_token}",
            "Content-Type": "application/json"
        }
        
        for result in scan_results:
            # Format for Splunk
            splunk_event = {
                "time": result.get("scan_time"),
                "sourcetype": "github:security:scan",
                "event": {
                    "repository": result.get("repository"),
                    "vulnerability_count": result.get("vulnerability_count", 0),
                    "risk_score": result.get("risk_score", 0),
                    "vulnerabilities": result.get("vulnerability_details", [])
                }
            }
            
            # Send to Splunk
            try:
                response = requests.post(
                    splunk_url,
                    headers=headers,
                    json=splunk_event,
                    timeout=30
                )
                response.raise_for_status()
            except Exception as e:
                print(f"Failed to send data to Splunk: {e}")
    
    def create_jira_security_tickets(self, high_severity_findings: List[Dict[str, Any]], jira_config: Dict[str, str]):
        """Create JIRA tickets for high-severity security findings"""
        from atlassian import Jira
        
        jira = Jira(
            url=jira_config["url"],
            username=jira_config["username"],
            password=jira_config["api_token"]
        )
        
        for finding in high_severity_findings:
            if finding.get("severity") in ["critical", "high"]:
                
                # Create ticket
                issue_dict = {
                    "project": {"key": jira_config["project_key"]},
                    "summary": f"Security Issue: {finding.get('title', 'Unknown')}",
                    "description": self._format_jira_description(finding),
                    "issuetype": {"name": "Bug"},
                    "priority": {"name": "High" if finding.get("severity") == "high" else "Highest"},
                    "labels": ["security", "github", finding.get("category", "unknown")]
                }
                
                try:
                    issue = jira.create_issue(fields=issue_dict)
                    print(f"Created JIRA ticket: {issue['key']}")
                except Exception as e:
                    print(f"Failed to create JIRA ticket: {e}")
    
    def _format_jira_description(self, finding: Dict[str, Any]) -> str:
        """Format security finding for JIRA description"""
        return f"""
h2. Security Finding Details

*Repository:* {finding.get('repository', 'Unknown')}
*Severity:* {finding.get('severity', 'Unknown')}
*Category:* {finding.get('category', 'Unknown')}

h3. Description
{finding.get('description', 'No description available')}

h3. Recommendation
{finding.get('recommendation', 'No recommendation available')}

h3. Evidence
{{code}}
{json.dumps(finding.get('evidence', {}), indent=2)}
{{code}}

*Generated by GitHub Security Scanner*
        """
    
    def integrate_with_sonarqube(self, repo_data: Dict[str, Any], sonar_config: Dict[str, str]):
        """Integrate security findings with SonarQube"""
        import requests
        
        # SonarQube API integration
        sonar_url = sonar_config["url"]
        sonar_token = sonar_config["token"]
        project_key = repo_data.get("name", "unknown")
        
        headers = {
            "Authorization": f"Bearer {sonar_token}",
            "Content-Type": "application/json"
        }
        
        # Get SonarQube security issues
        try:
            response = requests.get(
                f"{sonar_url}/api/issues/search",
                headers=headers,
                params={
                    "componentKeys": project_key,
                    "types": "VULNERABILITY,SECURITY_HOTSPOT",
                    "severities": "CRITICAL,HIGH"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                sonar_issues = response.json().get("issues", [])
                
                # Combine with GitHub security data
                combined_analysis = {
                    "repository": repo_data.get("name"),
                    "github_vulnerabilities": repo_data.get("vulnerabilities", []),
                    "sonarqube_issues": sonar_issues,
                    "total_security_issues": len(repo_data.get("vulnerabilities", [])) + len(sonar_issues)
                }
                
                return combined_analysis
                
        except Exception as e:
            print(f"Failed to integrate with SonarQube: {e}")
            return None
```

### Pro Tip 4: Advanced Security Metrics and Dashboards

Create sophisticated security metrics:

```python
"""
Advanced security metrics and dashboard generation
"""

class SecurityMetricsDashboard:
    """Generate advanced security metrics and dashboards"""
    
    def __init__(self, scan_data: List[Dict[str, Any]]):
        self.scan_data = scan_data
    
    def calculate_security_kpis(self) -> Dict[str, Any]:
        """Calculate key security performance indicators"""
        
        total_repos = len(self.scan_data)
        if total_repos == 0:
            return {}
        
        # Vulnerability metrics
        total_vulns = sum(repo.get("vulnerability_count", 0) for repo in self.scan_data)
        critical_vulns = sum(repo.get("critical_count", 0) for repo in self.scan_data)
        high_vulns = sum(repo.get("high_count", 0) for repo in self.scan_data)
        
        # Coverage metrics
        repos_with_alerts_enabled = len([r for r in self.scan_data if r.get("hasVulnerabilityAlertsEnabled")])
        coverage_percentage = (repos_with_alerts_enabled / total_repos) * 100
        
        # Risk distribution
        risk_distribution = {
            "critical": len([r for r in self.scan_data if r.get("risk_level") == "critical"]),
            "high": len([r for r in self.scan_data if r.get("risk_level") == "high"]),
            "medium": len([r for r in self.scan_data if r.get("risk_level") == "medium"]),
            "low": len([r for r in self.scan_data if r.get("risk_level") == "low"])
        }
        
        # Time-based metrics (would need historical data)
        mttr = self._calculate_mean_time_to_resolution()
        vulnerability_velocity = self._calculate_vulnerability_velocity()
        
        return {
            "total_repositories": total_repos,
            "total_vulnerabilities": total_vulns,
            "critical_vulnerabilities": critical_vulns,
            "high_vulnerabilities": high_vulns,
            "vulnerability_density": total_vulns / total_repos,
            "coverage_percentage": coverage_percentage,
            "risk_distribution": risk_distribution,
            "mean_time_to_resolution_days": mttr,
            "vulnerability_velocity_per_week": vulnerability_velocity,
            "security_score": self._calculate_overall_security_score()
        }
    
    def _calculate_mean_time_to_resolution(self) -> float:
        """Calculate mean time to resolve vulnerabilities"""
        # This would require historical data tracking
        # Placeholder implementation
        return 7.5  # days
    
    def _calculate_vulnerability_velocity(self) -> float:
        """Calculate rate of new vulnerabilities discovered"""
        # This would require time-series data
        # Placeholder implementation
        return 2.3  # vulnerabilities per week
    
    def _calculate_overall_security_score(self) -> float:
        """Calculate overall organizational security score (0-100)"""
        if not self.scan_data:
            return 0.0
        
        total_score = 0
        for repo in self.scan_data:
            repo_score = 100  # Start with perfect score
            
            # Deduct for vulnerabilities
            vuln_count = repo.get("vulnerability_count", 0)
            critical_count = repo.get("critical_count", 0)
            high_count = repo.get("high_count", 0)
            
            repo_score -= (critical_count * 20)  # -20 per critical
            repo_score -= (high_count * 10)     # -10 per high
            repo_score -= (vuln_count * 1)      # -1 per total vuln
            
            # Deduct for missing security features
            if not repo.get("hasVulnerabilityAlertsEnabled"):
                repo_score -= 15
            
            # Bonus for good practices
            if repo.get("has_branch_protection"):
                repo_score += 5
            
            repo_score = max(0, min(100, repo_score))  # Clamp to 0-100
            total_score += repo_score
        
        return total_score / len(self.scan_data)
    
    def generate_executive_dashboard_html(self, output_file: str = "security_executive_dashboard.html"):
        """Generate executive-level security dashboard"""
        
        kpis = self.calculate_security_kpis()
        
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Security Executive Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background-color: #f5f5f5; 
        }
        .dashboard-header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 30px; 
            border-radius: 10px; 
            margin-bottom: 30px; 
            text-align: center;
        }
        .kpi-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px; 
        }
        .kpi-card { 
            background: white; 
            padding: 25px; 
            border-radius: 10px; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
            text-align: center;
        }
        .kpi-value { 
            font-size: 2.5em; 
            font-weight: bold; 
            margin: 15px 0; 
        }
        .kpi-label { 
            font-size: 0.9em; 
            color: #666; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
        }
        .chart-container { 
            background: white; 
            padding: 30px; 
            border-radius: 10px; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
            margin-bottom: 20px; 
        }
        .critical { color: #e74c3c; }
        .high { color: #f39c12; }
        .medium { color: #f1c40f; }
        .good { color: #27ae60; }
    </style>
</head>
<body>
    <div class="dashboard-header">
        <h1>🔐 Security Executive Dashboard</h1>
        <p>Last Updated: {last_updated}</p>
    </div>
    
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Total Repositories</div>
            <div class="kpi-value">{total_repositories}</div>
        </div>
        
        <div class="kpi-card">
            <div class="kpi-label">Critical Vulnerabilities</div>
            <div class="kpi-value critical">{critical_vulnerabilities}</div>
        </div>
        
        <div class="kpi-card">
            <div class="kpi-label">Security Score</div>
            <div class="kpi-value {score_class}">{security_score:.1f}%</div>
        </div>
        
        <div class="kpi-card">
            <div class="kpi-label">Coverage</div>
            <div class="kpi-value good">{coverage_percentage:.1f}%</div>
        </div>
        
        <div class="kpi-card">
            <div class="kpi-label">Vulnerability Density</div>
            <div class="kpi-value medium">{vulnerability_density:.1f}</div>
        </div>
        
        <div class="kpi-card">
            <div class="kpi-label">Mean Time to Resolution</div>
            <div class="kpi-value">{mttr:.1f} days</div>
        </div>
    </div>
    
    <div class="chart-container">
        <h3>Risk Distribution</h3>
        <canvas id="riskChart" width="400" height="200"></canvas>
    </div>
    
    <script>
        // Risk distribution chart
        const ctx = document.getElementById('riskChart').getContext('2d');
        new Chart(ctx, {{
            type: 'doughnut',
            data: {{
                labels: ['Critical', 'High', 'Medium', 'Low'],
                datasets: [{{
                    data: [{risk_critical}, {risk_high}, {risk_medium}, {risk_low}],
                    backgroundColor: ['#e74c3c', '#f39c12', '#f1c40f', '#27ae60']
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
        """.format(
            last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_repositories=kpis["total_repositories"],
            critical_vulnerabilities=kpis["critical_vulnerabilities"],
            security_score=kpis["security_score"],
            score_class="critical" if kpis["security_score"] < 50 else "medium" if kpis["security_score"] < 80 else "good",
            coverage_percentage=kpis["coverage_percentage"],
            vulnerability_density=kpis["vulnerability_density"],
            mttr=kpis["mean_time_to_resolution_days"],
            risk_critical=kpis["risk_distribution"]["critical"],
            risk_high=kpis["risk_distribution"]["high"],
            risk_medium=kpis["risk_distribution"]["medium"],
            risk_low=kpis["risk_distribution"]["low"]
        )
        
        with open(output_file, 'w') as f:
            f.write(html_template)
        
        print(f"Executive dashboard generated: {output_file}")
        return output_file
```

---

## Conclusion

You've now mastered GitHub GraphQL for security! This comprehensive learning plan has taken you from basic GraphQL concepts to advanced enterprise security pipelines. You can now:

- **🔐 Secure Authentication**: Implement robust token management and scoping
- **🔍 Vulnerability Scanning**: Build comprehensive dependency and vulnerability scanners
- **📊 Security Analysis**: Perform deep security analysis with custom rule engines
- **🤖 Automated Monitoring**: Create continuous security monitoring systems
- **⚡ Optimization**: Handle rate limits and optimize large-scale queries
- **🏢 Enterprise Integration**: Build production-ready security workflows
- **🛠️ Troubleshooting**: Solve common issues and implement advanced techniques

### Next Steps for Continued Learning

1. **Expand Integrations**: Connect with more security tools (SIEM, vulnerability scanners)
2. **Machine Learning**: Add ML-based security anomaly detection
3. **Compliance Automation**: Automate compliance reporting for multiple frameworks
4. **Custom Security Rules**: Develop organization-specific security policies
5. **API Extensions**: Explore GitHub's REST API for additional security data

### Real-World Applications

This knowledge enables you to build:
- **Enterprise Security Dashboards** for executive reporting
- **Automated Vulnerability Management** systems
- **Compliance Monitoring** for regulatory requirements
- **Security CI/CD Integration** for DevSecOps workflows
- **Custom Security Tools** tailored to your organization

### Security Best Practices Reminder

- Always use least-privilege token scoping
- Implement proper rate limiting and error handling
- Never hardcode secrets or credentials
- Regularly audit and rotate access tokens
- Monitor for suspicious API usage patterns
- Keep dependencies updated and scan for vulnerabilities

**Happy secure coding!** 🔒✨

---

**Related Chapters:**
- [Chapter 4: Testing Like You Mean It](./chapter-04-testing-like-you-mean-it.md) - For testing your security tools
- [Chapter 6: Mastering Claude Code](./chapter-06-mastering-claude-code.md) - For AI-powered development workflows
- [Chapter 7: Database Architecture](./chapter-07-database-architecture.md) - For storing security data
- [Chapter 10: Playwright MCP Mastery](./chapter-10-playwright-mcp-mastery.md) - For automated security testing