# Security Guidelines

## Security First Principles
- Never trust user input
- Principle of least privilege
- Defense in depth
- Fail securely

## Common Vulnerabilities to Prevent

### Input Validation
- Validate all inputs on the server side
- Use allowlists, not denylists
- Sanitize data for the output context
- Validate data types, ranges, and formats

### Authentication & Authorization
- Use established libraries (don't roll your own crypto)
- Implement proper session management
- Use MFA where appropriate
- Check authorization on every request

### Data Protection
```python
# Never store passwords in plain text
from werkzeug.security import generate_password_hash, check_password_hash

# Use environment variables for secrets
import os
API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY not configured")

# Parameterized queries to prevent SQL injection
cursor.execute(
    "SELECT * FROM users WHERE id = %s",
    (user_id,)  # Parameters are safely escaped
)
```

### OWASP Top 10 Checklist
- [ ] Injection prevention (SQL, NoSQL, LDAP, etc.)
- [ ] Broken authentication checks
- [ ] Sensitive data exposure audit
- [ ] XML external entities (XXE) prevention
- [ ] Broken access control review
- [ ] Security misconfiguration scan
- [ ] Cross-site scripting (XSS) prevention
- [ ] Insecure deserialization checks
- [ ] Components with known vulnerabilities
- [ ] Insufficient logging & monitoring

## Security Tools
- SAST: Semgrep, Bandit (Python), gosec (Go)
- Dependency scanning: safety, npm audit, go mod audit
- Container scanning: Trivy, Grype
- Secret scanning: git-secrets, truffleHog

## Incident Response
1. Identify and contain the issue
2. Assess the impact
3. Notify stakeholders
4. Fix the vulnerability
5. Document lessons learned
6. Update security practices