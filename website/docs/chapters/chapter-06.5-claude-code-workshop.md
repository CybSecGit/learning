# Chapter 6.5: Claude Code Mastery Workshop
## *Or: Hands-On Practice to Level Up Your AI Pair Programming*

> "Tell me and I forget, teach me and I may remember, involve me and I learn." - Benjamin Franklin (who would have loved Claude Code)

## Workshop Overview

This hands-on workshop is designed to take you from Claude Code beginner to power user through practical exercises. Each exercise builds on the previous one, creating a comprehensive understanding of Claude Code's capabilities.

**Prerequisites:**
- Claude Code installed and configured
- Basic understanding of command line operations
- A project directory for experiments
- Chapter 6 completed (for context)

---

## Exercise 1: CLAUDE.md Mastery
### *Building the Perfect Project Memory*

**Objective:** Create an effective CLAUDE.md file that transforms how Claude Code understands your project.

### Part A: Basic CLAUDE.md Setup

**Task:** Create a CLAUDE.md file for a fictional e-commerce project.

```bash
# Create project structure
mkdir -p ecommerce-workshop/{src,tests,docs}
cd ecommerce-workshop
```

**Your Challenge:**
1. Create a CLAUDE.md that includes:
   - Project overview and architecture
   - Coding standards and conventions
   - Common commands and workflows
   - Testing requirements
   - Security guidelines

**Starter Template:**
```markdown
# E-Commerce Platform

## Project Overview
[Your description here]

## Architecture
- Frontend: React with TypeScript
- Backend: Node.js with Express
- Database: PostgreSQL
- Cache: Redis

## Coding Standards
[Your standards here]

## Common Commands
[Your commands here]

## Testing Requirements
[Your requirements here]

## Security Guidelines
[Your guidelines here]
```

### Part B: Advanced Import Patterns

**Task:** Organize your CLAUDE.md with modular imports.

Create these supporting files:
- `docs/api-standards.md`
- `docs/testing-guide.md`
- `docs/security-checklist.md`

Then update your CLAUDE.md to import them:
```markdown
# E-Commerce Platform

## Standards and Guidelines
@docs/api-standards.md
@docs/testing-guide.md
@docs/security-checklist.md

## Quick Reference
- API endpoints follow RESTful conventions
- All code must have 80% test coverage
- Security review required for auth changes
```

### Part C: Context-Specific Configuration

**Task:** Add environment-specific rules.

```markdown
# Development Environment
When working locally:
- Use Docker Compose for all services
- Mock external APIs with MSW
- Enable debug logging

# Production Deployment
For production releases:
- Run full security audit
- Verify all environment variables
- Check bundle size < 500KB
```

**Self-Assessment Questions:**
1. How does your CLAUDE.md help Claude Code understand project context?
2. What patterns did you use to keep the file concise?
3. How would team members benefit from your configuration?

---

## Exercise 2: Custom Slash Commands
### *Automating Your Workflow*

**Objective:** Create powerful custom commands that accelerate development.

### Part A: Basic Command Creation

**Task:** Create a command to scaffold new API endpoints.

```bash
mkdir -p .claude/commands
```

Create `.claude/commands/create-endpoint.md`:
```markdown
Create a new REST API endpoint for {{resource}}:

1. Create route file: `src/routes/{{resource}}.ts`
2. Create controller: `src/controllers/{{resource}}Controller.ts`
3. Create service: `src/services/{{resource}}Service.ts`
4. Create tests: `tests/{{resource}}.test.ts`
5. Update router index to include new route
6. Add OpenAPI documentation

Follow our REST conventions:
- GET /{{resource}} - List all
- GET /{{resource}}/:id - Get one
- POST /{{resource}} - Create new
- PUT /{{resource}}/:id - Update
- DELETE /{{resource}}/:id - Delete

Include proper error handling and validation.
```

**Test Your Command:**
```bash
# In Claude Code
/create-endpoint products
```

### Part B: Complex Workflow Commands

**Task:** Create a command for comprehensive feature development.

Create `.claude/commands/feature-flow.md`:
```markdown
Implement complete feature: {{feature_name}}

## Phase 1: Planning
1. Analyze requirements for {{feature_name}}
2. Design data models and API contracts
3. Create technical specification

## Phase 2: Backend Implementation
1. Create database migrations
2. Implement service layer with business logic
3. Create API endpoints with validation
4. Write comprehensive unit tests
5. Add integration tests

## Phase 3: Frontend Implementation
1. Create Redux/Context state management
2. Build UI components with proper typing
3. Implement API integration layer
4. Add component tests
5. Create E2E tests

## Phase 4: Documentation
1. Update API documentation
2. Add user guide to docs/
3. Update README with feature info
4. Create migration guide if needed

## Phase 5: Review Checklist
- [ ] All tests passing
- [ ] Code coverage > 80%
- [ ] No security vulnerabilities
- [ ] Performance benchmarks met
- [ ] Documentation complete
```

### Part C: Debugging Commands

**Task:** Create specialized debugging commands.

Create `.claude/commands/debug-performance.md`:
```markdown
Debug performance issue in {{component}}:

1. Profile current performance:
   - Add performance marks around {{component}}
   - Measure render times
   - Check network waterfall
   - Analyze bundle impact

2. Identify bottlenecks:
   - Look for unnecessary re-renders
   - Check for N+1 queries
   - Find synchronous operations
   - Analyze memory usage

3. Implement optimizations:
   - Add memoization where appropriate
   - Implement lazy loading
   - Optimize database queries
   - Add caching layer

4. Verify improvements:
   - Compare before/after metrics
   - Run load tests
   - Check user experience metrics
   - Document performance gains

Generate performance report with recommendations.
```

**Practice Scenarios:**
1. Use your commands to create a "users" endpoint
2. Implement a "shopping cart" feature
3. Debug a slow product listing page

---

## Exercise 3: Test-Driven Development with Claude
### *Red, Green, Refactor in Action*

**Objective:** Master TDD workflow with Claude Code as your pair programmer.

### Part A: Basic TDD Cycle

**Task:** Implement a pricing calculator using TDD.

**Step 1: Write Failing Tests First**
```bash
# Ask Claude Code
"Create comprehensive tests for a PricingCalculator class that:
- Calculates base price
- Applies percentage discounts
- Handles bulk pricing tiers
- Applies tax based on location
- Handles invalid inputs gracefully"
```

**Step 2: Implement Minimum Code**
```bash
"Now implement the PricingCalculator to make all tests pass"
```

**Step 3: Refactor for Quality**
```bash
"Refactor the PricingCalculator for better maintainability while keeping tests green"
```

### Part B: Advanced TDD Patterns

**Task:** Implement an inventory management system with complex business rules.

**Requirements to Test:**
1. Stock levels with reservations
2. Automatic reordering when low
3. Batch tracking and expiration
4. Multi-warehouse support
5. Real-time availability checks

**Your Workflow:**
```bash
# 1. Start with integration tests
"Write integration tests for inventory management system with the requirements I specified"

# 2. Break down into unit tests
"Create unit tests for each component of the inventory system"

# 3. Implement incrementally
"Implement the stock level tracking with reservations"
"Now add the automatic reordering feature"
"Implement batch tracking and expiration"

# 4. Refactor with patterns
"Refactor using appropriate design patterns while maintaining test coverage"
```

### Part C: Testing Complex Scenarios

**Task:** Test asynchronous operations and error handling.

```bash
"Create tests for an order processing system that:
- Handles concurrent orders
- Manages distributed transactions
- Recovers from payment failures
- Deals with inventory conflicts
- Maintains data consistency"
```

**Key Learning Points:**
- Always write tests first
- One failing test at a time
- Minimum code to pass
- Refactor when green
- Tests document behavior

---

## Exercise 4: Parallel Development Workshop
### *Multiply Your Productivity*

**Objective:** Learn to effectively use multiple Claude Code instances for parallel development.

### Part A: Feature Branch Strategy

**Setup:** Open 4 terminal windows with Claude Code.

**Window 1 - Backend Development:**
```bash
"I'm working on the backend for user authentication. 
Implement JWT-based auth with refresh tokens, 
following our existing patterns in src/auth/"
```

**Window 2 - Frontend Development:**
```bash
"I'm building the frontend for user authentication. 
Create login/register forms with proper validation,
integrate with the auth API being built"
```

**Window 3 - Testing:**
```bash
"Write comprehensive tests for the authentication system.
Cover both backend API tests and frontend component tests.
Include security test cases"
```

**Window 4 - Documentation:**
```bash
"Document the authentication system implementation.
Update API docs, create user guides, and add 
security considerations to our documentation"
```

### Part B: Coordination Patterns

**Task:** Implement a real-time notification system across multiple instances.

**Instance Roles:**
1. **WebSocket Server**: Implement real-time server
2. **Client Library**: Build client-side integration
3. **Admin Dashboard**: Create monitoring interface
4. **Infrastructure**: Set up Redis pub/sub

**Coordination Commands:**
```bash
# Instance 1
"Implement WebSocket server for notifications.
Use Socket.io with Redis adapter.
Support rooms and acknowledgments"

# Instance 2
"Create React hooks for WebSocket notifications.
Include connection management and retry logic.
Coordinate with the server implementation"

# Instance 3
"Build admin dashboard to monitor active connections
and send broadcast notifications"

# Instance 4
"Set up Redis configuration for pub/sub.
Create Docker compose for local development"
```

### Part C: Merge Strategy

**Task:** Coordinate the merge of parallel work.

```bash
# In main instance after parallel work
"Review and integrate the work from:
1. Authentication backend (branch: feat/auth-backend)
2. Authentication frontend (branch: feat/auth-frontend)
3. Test suite (branch: test/auth-system)
4. Documentation (branch: docs/auth-guide)

Resolve any conflicts and ensure all parts work together"
```

---

## Exercise 5: Advanced Debugging Techniques
### *Sherlock Holmes Mode*

**Objective:** Master systematic debugging with Claude Code.

### Part A: Mystery Bug Hunt

**Setup:** Create a buggy application:

```javascript
// bug-hunt.js
class ShoppingCart {
  constructor() {
    this.items = [];
    this.discounts = [];
  }

  addItem(product, quantity) {
    const existing = this.items.find(i => i.product.id = product.id);
    if (existing) {
      existing.quantity += quantity;
    } else {
      this.items.push({ product, quantity });
    }
  }

  applyDiscount(code) {
    // Bug: Discounts stack infinitely
    this.discounts.push(code);
  }

  calculateTotal() {
    let total = 0;
    for (let item of this.items) {
      total += item.product.price * item.quantity;
    }
    
    // Bug: Discount calculation is wrong
    for (let discount of this.discounts) {
      total = total - (total * discount.percentage);
    }
    
    return total;
  }
}
```

**Debugging Session:**
```bash
"There are several bugs in this shopping cart implementation.
Use systematic debugging to find and fix all issues.
Add comprehensive tests to prevent regression"
```

### Part B: Performance Detective

**Task:** Debug performance issues in a slow API.

```bash
"This API endpoint is taking 5+ seconds to respond:
GET /api/products?category=electronics&inStock=true

Use profiling and analysis to find the bottlenecks.
Look for:
- N+1 queries
- Missing indexes
- Unnecessary computations
- Memory leaks
- Inefficient algorithms"
```

### Part C: Concurrency Challenges

**Task:** Debug race conditions and deadlocks.

```bash
"Users report intermittent failures when placing orders.
Sometimes inventory is oversold, sometimes orders disappear.
Debug the concurrent order processing system.
Add proper locking and transaction handling"
```

---

## Exercise 6: Real-World Project Simulation
### *Putting It All Together*

**Objective:** Complete a mini-project using all Claude Code techniques.

### The Challenge: Build a Task Management API

**Requirements:**
1. User authentication and authorization
2. CRUD operations for tasks
3. Task assignment and collaboration
4. Due date notifications
5. Activity tracking
6. Real-time updates
7. Full test coverage
8. Production-ready code

### Phase 1: Project Setup (30 minutes)

```bash
# With Claude Code
"Set up a new Node.js project for a task management API.
Initialize with TypeScript, Express, and PostgreSQL.
Create the project structure and initial configuration.
Set up testing framework and development environment"
```

### Phase 2: Core Implementation (2 hours)

**Use parallel instances:**
- Instance 1: Authentication system
- Instance 2: Task CRUD operations
- Instance 3: Database schema and migrations
- Instance 4: Test suite development

### Phase 3: Advanced Features (1 hour)

```bash
"Implement real-time updates using WebSockets.
Add task assignment with email notifications.
Create activity tracking for audit logs"
```

### Phase 4: Production Preparation (30 minutes)

```bash
"Prepare the application for production:
- Add comprehensive error handling
- Implement rate limiting
- Add security headers
- Create Dockerfile
- Set up CI/CD pipeline
- Generate API documentation"
```

### Phase 5: Review and Refactor (30 minutes)

```bash
"Review the entire codebase for:
- Code quality and consistency
- Security vulnerabilities
- Performance optimizations
- Test coverage gaps
- Documentation completeness"
```

---

## Exercise 7: MCP Server Integration
### *Extending Claude Code's Capabilities*

**Objective:** Learn to leverage MCP servers for enhanced functionality.

### Part A: Playwright Testing

**Task:** Use Playwright MCP for E2E testing.

```bash
"Use the Playwright MCP server to:
1. Test our login flow on localhost:3000
2. Verify task creation and editing
3. Check responsive design on mobile
4. Test error states and edge cases
5. Generate visual regression tests"
```

### Part B: Documentation Integration

**Task:** Use Context7 MCP for research.

```bash
"Use Context7 MCP to research:
1. Best practices for JWT refresh token rotation
2. PostgreSQL performance optimization for our schema
3. WebSocket scaling strategies
4. Current security recommendations for APIs"
```

### Part C: Custom MCP Development

**Task:** Design a custom MCP for your project.

```bash
"Design an MCP server that:
1. Analyzes our codebase for code smells
2. Suggests refactoring opportunities
3. Checks for security vulnerabilities
4. Generates performance reports"
```

---

## Final Challenge: The Claude Code Kata
### *Daily Practice for Mastery*

Create a daily practice routine with these katas:

### Monday: Refactoring Kata
```bash
"Find a complex function in our codebase and refactor it
for better readability and maintainability.
Ensure tests still pass"
```

### Tuesday: Testing Kata
```bash
"Find a component with < 80% test coverage.
Write comprehensive tests to reach 100% coverage.
Include edge cases and error scenarios"
```

### Wednesday: Performance Kata
```bash
"Profile the application and find one performance issue.
Implement a fix and measure the improvement"
```

### Thursday: Security Kata
```bash
"Audit one module for security vulnerabilities.
Fix any issues found and add preventive tests"
```

### Friday: Documentation Kata
```bash
"Find undocumented code and add comprehensive docs.
Update examples and add to learning concepts"
```

---

## Workshop Completion Checklist

**Core Skills Mastered:**
- [ ] Created effective CLAUDE.md files
- [ ] Built custom slash commands
- [ ] Practiced TDD with Claude Code
- [ ] Used parallel development effectively
- [ ] Debugged complex issues systematically
- [ ] Integrated MCP servers
- [ ] Completed real-world project

**Advanced Techniques Learned:**
- [ ] Memory optimization strategies
- [ ] Headless mode automation
- [ ] CI/CD integration
- [ ] Security best practices
- [ ] Performance optimization
- [ ] Team collaboration patterns

**Next Steps:**
1. Apply these techniques to your real projects
2. Share your custom commands with your team
3. Create project-specific MCP servers
4. Contribute to the Claude Code community
5. Keep practicing with daily katas

---

## Resources and References

### Official Documentation
- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [MCP Protocol Spec](https://modelcontextprotocol.com)
- [Best Practices Guide](https://anthropic.com/claude-code-best-practices)

### Community Resources
- [Awesome Claude Code](https://github.com/awesome-claude-code)
- [Claude Code Patterns](https://claude-code-patterns.dev)
- [Community Commands](https://claude-commands.org)

### Practice Projects
- [Claude Code Challenges](https://github.com/claude-code-challenges)
- [TDD with Claude](https://tdd-claude.dev)
- [Open Source with Claude](https://opensource-claude.org)

---

## Congratulations!

You've completed the Claude Code Mastery Workshop! You now have hands-on experience with advanced Claude Code techniques that will dramatically improve your development workflow. Remember: the key to mastery is consistent practice and experimentation.

**Final Tip:** Every project is an opportunity to discover new ways to leverage Claude Code. Stay curious, share your learnings, and keep pushing the boundaries of what's possible with AI-assisted development.

> "The expert in anything was once a beginner who never gave up." 

Happy coding with Claude! 🤖✨