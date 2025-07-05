# GitHub GraphQL Security Exercises

Practice building security tools with GitHub's GraphQL API through hands-on exercises.

## Exercise 1: Basic Vulnerability Scanner

Build a GitHub GraphQL vulnerability scanner that can authenticate, query repository vulnerabilities, and generate security reports.

### Learning Objectives
- Set up secure GitHub GraphQL authentication
- Write basic GraphQL queries for security data
- Handle API responses and error cases
- Generate actionable security insights

### Exercise File
The exercise is available as a Python script with TODO sections for you to implement:

```python
# Download the exercise file:
# course/exercises/github-graphql-security-exercise-01.py
```

Key features to implement:
- Token validation
- Repository vulnerability scanning
- Vulnerability categorization by severity
- Security report generation

### Prerequisites
- GitHub account with repository access
- Personal access token with `security_events` scope
- Python 3.8+ with requests library

## Exercise 2: Advanced Security Analysis

Build an enterprise-grade security analyzer for GitHub organizations with policy evaluation and executive reporting.

### Learning Objectives
- Advanced GraphQL queries with pagination
- Security policy implementation and evaluation
- Risk assessment and prioritization algorithms
- Executive-level reporting and dashboards

### Exercise File
```python
# Download the exercise file:
# course/exercises/github-graphql-security-exercise-02.py
```

Key features to implement:
- Organization-wide repository discovery
- Custom security policy evaluation
- Risk scoring algorithms
- Executive security reports

### Prerequisites
- Completion of Exercise 1
- GitHub organization access or multiple repositories
- Understanding of security frameworks

## Setting Up Your Environment

### 1. Create GitHub Personal Access Token

Navigate to GitHub Settings → Developer settings → Personal access tokens → Generate new token

Required scopes:
- `repo` - Access to repository data
- `read:org` - Read organization membership
- `security_events` - Read security events

### 2. Set Environment Variables

```bash
# Create .env file
export GITHUB_TOKEN=your_personal_access_token_here
export GITHUB_REPO_OWNER=repository_owner
export GITHUB_REPO_NAME=repository_name
export GITHUB_ORG=organization_name  # For exercise 2
```

### 3. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install requests python-dotenv pydantic
```

## Running the Exercises

### Exercise 1: Basic Scanner
```bash
python course/exercises/github-graphql-security-exercise-01.py
```

Expected output:
- Authentication validation
- Vulnerability scanning progress
- Security report with findings and recommendations

### Exercise 2: Advanced Analysis
```bash
python course/exercises/github-graphql-security-exercise-02.py
```

Expected output:
- Organization repository discovery
- Security policy evaluation results
- Executive security dashboard

## Testing Your Implementation

Run the comprehensive test suite:

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock

# Run all tests
pytest course/tests/test_github_graphql_security_exercises.py -v

# Run with coverage
pytest course/tests/test_github_graphql_security_exercises.py --cov=course.exercises --cov-report=html
```

## Bonus Challenges

### Exercise 1 Extensions
- Add dependency graph analysis
- Implement rate limiting with exponential backoff
- Add filtering by ecosystem (npm, pip, etc.)
- Create a CLI interface with argparse
- Support scanning multiple repositories

### Exercise 2 Extensions
- Add compliance framework mapping (ISO 27001, SOC 2)
- Implement trend analysis with historical data
- Create HTML executive dashboard
- Add integration with security tools (Jira, Slack)
- Implement automated remediation suggestions

## Security Best Practices

When working with these exercises:

1. **Never commit tokens** - Use environment variables or secure vaults
2. **Use least privilege** - Only request necessary API scopes
3. **Handle errors gracefully** - Don't expose sensitive information
4. **Implement rate limiting** - Respect GitHub's API limits
5. **Validate all inputs** - Prevent injection attacks
6. **Log security events** - Maintain audit trails

## Next Steps

After completing these exercises, explore:

1. **GitHub Actions Integration** - Automate security scanning
2. **Security Dashboards** - Build real-time monitoring
3. **Compliance Reporting** - Map to security frameworks
4. **Multi-Source Analysis** - Combine with other security APIs
5. **Machine Learning** - Add anomaly detection

## Resources

- [GitHub GraphQL API Documentation](https://docs.github.com/en/graphql)
- [GitHub Security Features](https://docs.github.com/en/code-security)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [OWASP API Security](https://owasp.org/www-project-api-security/)

## Getting Help

If you get stuck:

1. Check the test files for expected behavior
2. Review the chapter for detailed explanations
3. Use GitHub's GraphQL Explorer to test queries
4. Refer to the troubleshooting section in the main chapter

Happy secure coding! 🔒