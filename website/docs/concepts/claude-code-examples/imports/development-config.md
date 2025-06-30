# Development Environment Configuration

## Development Settings
- Enable debug mode for detailed error messages
- Use local databases and services
- Mock external APIs when possible
- Verbose logging for debugging

## Development Tools
- Hot reload enabled
- Source maps for debugging
- Development server with CORS disabled
- Test data seeders available

## Quick Commands
```bash
# Start development environment
make dev

# Run with debugging
make debug

# Reset database with test data
make reset-db

# Watch mode for tests
make test-watch
```

## Local Services
- Database: PostgreSQL on localhost:5432
- Cache: Redis on localhost:6379
- API: http://localhost:8000
- Frontend: http://localhost:3000

## Environment Variables
```bash
# .env.development
NODE_ENV=development
DEBUG=true
LOG_LEVEL=debug
DATABASE_URL=postgresql://dev:dev@localhost:5432/dev_db
REDIS_URL=redis://localhost:6379
API_URL=http://localhost:8000
```

## Development Best Practices
- Use feature flags for WIP features
- Keep development data realistic
- Regular dependency updates
- Profile performance regularly