# Database Architecture & SQLAlchemy ORM

> "A database is the permanent memory of your application. Design it well, and your application can scale to millions of users. Design it poorly, and it will crash with a hundred."

## Core Concepts

This guide covers:
- Database design principles for data-intensive applications
- SQLAlchemy ORM models with proper relationships
- Database migrations with Alembic
- Schemas that scale from SQLite to PostgreSQL
- Comprehensive database testing strategies
- Common pitfalls and how to avoid them

## Why Databases Matter for Web Scraping

When you're scraping websites and analyzing data, you need somewhere to store:
- **Scraped data**: Raw HTML, parsed content, structured data
- **Analysis results**: AI insights, categorizations, summaries
- **User preferences**: Which tools to monitor, notification settings
- **System metadata**: When data was scraped, processing status, error logs

A well-designed database ensures your scraping operation can:
- **Handle failures gracefully**: Resume from where you left off
- **Scale efficiently**: Process thousands of tools without slowdown
- **Maintain data integrity**: Prevent corruption and ensure consistency
- **Support analytics**: Track trends and generate insights over time

## Real-World Example: Application Database Design

Let's explore a database architecture for a tool that monitors and analyzes external data sources.

### Core Entities and Relationships

```python
# User Model - Who uses the system
class User(Base):
    __tablename__ = "users"
    
    # OAuth-based identification (GitHub, Google, etc.)
    id = Column(String(255), primary_key=True)  # "github|12345"
    email = Column(String(255), unique=True, nullable=False, index=True)
    github_username = Column(String(255), unique=True, nullable=True, index=True)
    
    # User preferences stored as JSON for flexibility
    preferences = Column(JSON, default=dict)
    
    # Relationships
    tools = relationship("Tool", back_populates="owner", cascade="all, delete-orphan")
```

**Key Design Decisions:**
- **UUID Primary Keys**: No collisions across multiple servers
- **OAuth Integration**: Users identified by external provider
- **JSON Preferences**: Flexible storage for user settings
- **Cascade Deletes**: When user is deleted, their tools are too

### Tool Monitoring Model

```python
class Tool(Base):
    __tablename__ = "tools"
    
    # Unique identifier
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Tool identification
    name = Column(String(255), nullable=False, index=True)
    url = Column(Text, nullable=False)
    github_repo = Column(String(255), nullable=True, index=True)  # "facebook/react"
    
    # Monitoring configuration
    is_active = Column(Boolean, default=True, nullable=False)
    check_frequency = Column(String(20), default="daily")
    
    # Ownership
    owner_id = Column(String(255), ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tools")
    
    # Soft delete support
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    updates = relationship("Update", back_populates="tool", cascade="all, delete-orphan")
```

**Why This Design Works:**
- **Soft Deletes**: Keep audit trails when tools are "deleted"
- **Flexible Categories**: Tools can be categorized multiple ways
- **Configurable Monitoring**: Different frequencies per tool
- **GitHub Integration**: Optional repository linking

### Update Tracking Model

```python
class Update(Base):
    __tablename__ = "updates"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tool_id = Column(String(36), ForeignKey("tools.id"), nullable=False)
    
    # Version information
    version = Column(String(255), nullable=False)
    release_date = Column(DateTime(timezone=True), nullable=False)
    
    # Impact assessment
    impact_level = Column(String(20), nullable=False, default="medium")
    has_breaking_changes = Column(Boolean, default=False, nullable=False)
    security_update = Column(Boolean, default=False, nullable=False)
    
    # Content
    summary = Column(Text, nullable=True)
    raw_changelog = Column(Text, nullable=True)
    processed_changelog = Column(JSON, nullable=True)  # Structured data
    
    # Analysis status tracking
    analysis_status = Column(String(20), default="pending")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('impact_level IN ("low", "medium", "high", "critical")', 
                       name='impact_level_valid'),
        Index('idx_update_tool_version', 'tool_id', 'version'),
    )
```

**Data Integrity Features:**
- **Check Constraints**: Validate enum values at database level
- **Composite Indexes**: Fast queries on tool + version
- **JSON Storage**: Flexible structured data storage
- **Status Tracking**: Monitor processing pipeline

## Database Performance Patterns

### 1. Strategic Indexing

```python
class Tool(Base):
    # Single column indexes for common queries
    name = Column(String(255), nullable=False, index=True)
    github_repo = Column(String(255), nullable=True, index=True)
    
    # Composite indexes for complex queries
    __table_args__ = (
        Index('idx_tool_owner_active', 'owner_id', 'is_active'),
        Index('idx_tool_category_language', 'category', 'language'),
    )
```

**Index Strategy:**
- **Query Patterns**: Index columns you filter/sort on
- **Composite Indexes**: For multi-column WHERE clauses
- **Avoid Over-Indexing**: Each index slows down writes

### 2. Avoiding N+1 Query Problems

```python
# ❌ This triggers N+1 queries (1 query for users + N queries for tools)
users = session.query(User).all()
for user in users:
    print(f"{user.email} has {len(user.tools)} tools")  # Database hit per user!

# ✅ Eager loading - single query with JOIN
users = session.query(User).options(joinedload(User.tools)).all()
for user in users:
    print(f"{user.email} has {len(user.tools)} tools")  # No additional queries
```

### 3. Query Optimization

```python
# ❌ Loads everything unnecessarily
all_tools = session.query(Tool).all()

# ✅ Filter and limit appropriately
active_tools = (session.query(Tool)
               .filter(Tool.is_active == True)
               .filter(Tool.deleted_at.is_(None))
               .limit(100)
               .all())

# ✅ Select only needed columns
tool_names = session.query(Tool.name, Tool.url).filter(Tool.is_active == True).all()
```

## Database Testing Strategy

### In-Memory Testing for Speed

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def db_session():
    """Create a test database session using in-memory SQLite."""
    # In-memory database - super fast, completely isolated
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()

def test_user_tool_relationship(db_session):
    """Test that user-tool relationships work correctly."""
    user = User(id="test-user", email="test@example.com")
    tool = Tool(name="React", url="https://reactjs.org", owner_id=user.id)
    
    db_session.add_all([user, tool])
    db_session.commit()
    
    # Test relationship works both ways
    assert len(user.tools) == 1
    assert tool.owner == user
    assert user.tools[0].name == "React"
```

### Testing Data Constraints

```python
def test_impact_level_constraint(db_session):
    """Test that invalid impact levels are rejected."""
    user = User(id="test-user", email="test@example.com")
    tool = Tool(name="React", url="https://reactjs.org", owner_id=user.id)
    db_session.add_all([user, tool])
    db_session.commit()
    
    # This should fail due to check constraint
    with pytest.raises(IntegrityError):
        invalid_update = Update(
            tool_id=tool.id,
            version="1.0.0",
            release_date=datetime.now(UTC),
            impact_level="INVALID_LEVEL"  # Not in allowed values
        )
        db_session.add(invalid_update)
        db_session.commit()
```

## Migration Strategy: SQLite to PostgreSQL

### Development with SQLite

```python
# For local development - zero setup
DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(DATABASE_URL)
```

**SQLite Benefits:**
- No installation required
- Perfect for development and testing
- Same SQL syntax as PostgreSQL for most operations
- File-based - easy backups and sharing

### Production with PostgreSQL

```python
# For production - better concurrency and features
DATABASE_URL = "postgresql://user:password@host:port/database"

engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True
)
```

**PostgreSQL Benefits:**
- Better concurrency (multiple users)
- Advanced JSON operations
- Full-text search capabilities
- Better performance at scale
- Cloud hosting support

### Same Code, Different Database

```python
class User(Base):
    # This model works with both SQLite and PostgreSQL
    preferences = Column(JSON, default=dict)
    
    # SQLite: Stores as TEXT, parsed as JSON
    # PostgreSQL: Native JSONB type with indexing
```

## Alembic Migrations

### Setting Up Migrations

```bash
# Initialize Alembic
alembic init alembic

# Generate first migration
alembic revision --autogenerate -m "Initial database schema"

# Apply migration
alembic upgrade head
```

### Migration Best Practices

```python
# alembic/env.py
from src.api.database.base import Base
from src.api.database.models import User, Tool, Update, AIInsight

# This tells Alembic about your models
target_metadata = Base.metadata

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
```

### Safe Migration Workflow

```bash
# 1. Always review generated migrations
alembic revision --autogenerate -m "Add user preferences"
# Check the generated file before applying!

# 2. Test on copy of production data first
alembic upgrade head

# 3. Can rollback if needed
alembic downgrade -1
```

## Common Database Pitfalls

### 1. Forgetting to Commit

```python
# ❌ Data is not saved!
user = User(email="test@example.com")
session.add(user)
# Missing: session.commit()

# ✅ Explicitly commit changes
user = User(email="test@example.com")
session.add(user)
session.commit()
```

### 2. Session Leaks

```python
# ❌ Session never closed - memory leak
def get_user(email):
    session = Session()
    user = session.query(User).filter(User.email == email).first()
    return user  # Session still open!

# ✅ Always clean up sessions
def get_user(email):
    session = Session()
    try:
        user = session.query(User).filter(User.email == email).first()
        return user
    finally:
        session.close()

# ✅ Even better - use context manager
def get_user(email):
    with Session() as session:
        user = session.query(User).filter(User.email == email).first()
        return user  # Session automatically closed
```

### 3. Race Conditions

```python
# ❌ Two processes might create duplicate users
existing = session.query(User).filter(User.email == email).first()
if not existing:
    # Another process might create user here!
    user = User(email=email)
    session.add(user)
    session.commit()

# ✅ Use database constraints + exception handling
try:
    user = User(email=email)  # email has UNIQUE constraint
    session.add(user)
    session.commit()
except IntegrityError:
    session.rollback()
    user = session.query(User).filter(User.email == email).first()
```

## Exercise: Build Your Own Data Collection Database

Create a database schema for a web scraping project that monitors e-commerce prices:

```python
class Product(Base):
    """Product being monitored for price changes."""
    # TODO: Add fields for:
    # - product_id (UUID)
    # - name, url, category
    # - target_price (when to alert)
    # - is_active
    # - created_at, updated_at

class PriceCheck(Base):
    """Individual price check result."""
    # TODO: Add fields for:
    # - price_check_id (UUID)
    # - product_id (foreign key)
    # - price, currency
    # - availability (in_stock, out_of_stock, etc.)
    # - scraped_at timestamp
    # - raw_html (for debugging)

class PriceAlert(Base):
    """Alert when price drops below target."""
    # TODO: Add fields for:
    # - alert_id (UUID)
    # - price_check_id (foreign key)
    # - alert_type (price_drop, back_in_stock)
    # - sent_at timestamp
```

**Your Tasks:**
1. Define the complete schema with proper relationships
2. Add appropriate indexes for common queries
3. Write tests for the relationships
4. Create migration scripts
5. Implement a price tracking service

## Key Takeaways

1. **Design for Scale Early**: Use UUIDs, proper indexes, and constraints
2. **Test Everything**: Database relationships, constraints, and edge cases
3. **Plan Migrations**: Use Alembic for safe schema evolution
4. **Monitor Performance**: Watch for N+1 queries and missing indexes
5. **Handle Failures Gracefully**: Use transactions and proper error handling

## Next Steps

- **Practice**: Build database schemas for your own scraping projects
- **Advanced Topics**: Study database sharding, read replicas, and caching
- **Monitoring**: Learn database performance monitoring and optimization
- **Security**: Implement proper access controls and data encryption

Remember: A well-designed database is the foundation that enables everything else in your application to work reliably at scale.