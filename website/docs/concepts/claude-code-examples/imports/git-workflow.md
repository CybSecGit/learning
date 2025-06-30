# Git Workflow Standards

## Branch Strategy
- `main` - production-ready code
- `develop` - integration branch
- `feature/*` - new features
- `bugfix/*` - bug fixes
- `hotfix/*` - urgent production fixes

## Commit Messages
- Use conventional commits format
- Types: feat, fix, docs, style, refactor, test, chore
- Format: `type(scope): description`
- Examples:
  - `feat(auth): add OAuth2 integration`
  - `fix(api): handle null response in user endpoint`
  - `docs(readme): update installation instructions`

## Pull Request Process
1. Create feature branch from develop
2. Make atomic commits
3. Write comprehensive PR description
4. Ensure CI passes
5. Request review from team members
6. Address feedback promptly
7. Squash merge when approved

## Code Review Guidelines
- Review for correctness, security, and performance
- Suggest improvements, don't demand perfection
- Use "nit:" prefix for minor issues
- Approve when code is better than before