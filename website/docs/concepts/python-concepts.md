# Python Learning Concepts

This is a comprehensive guide to Python programming concepts, explained using the Feynman technique - making complex ideas simple enough for anyone to understand.

## About This Guide

The full Python concepts guide is available at: [`learning_concepts.md`](https://github.com/YOUR_USERNAME/learning/blob/main/learning_concepts.md)

This guide covers:

### 🐍 Python Language Guide
- Basic syntax and structure
- Functions and classes
- Python naming conventions
- Control flow and data structures
- Exception handling
- Decorators and context managers
- Import system

### 🔤 Python Type System
- Type hints for beginners
- Optional types
- Collection types
- Modern Python style (3.10+)
- Type checking tools

### 📚 Core Programming Concepts
- Async/await programming
- Web scraping with rate limiting
- Error handling in async code
- Service layer architecture

### 🛠️ Development Tools & Setup
- Package management (uv vs pip)
- Virtual environments
- Code formatting and linting
- Testing with pytest
- Security analysis

### 🧪 Testing Guide
- Understanding software testing
- Unit tests vs integration tests
- Mocking and test doubles
- Test-driven development (TDD)

### 🧩 Design Patterns
- Factory pattern
- Singleton pattern
- Abstract base classes
- Dependency injection

## Quick Python Reference

### Variables and Types
```python
# Dynamic typing
name = "Alice"  # str
age = 30        # int
height = 5.6    # float
is_student = False  # bool

# Type hints (Python 3.5+)
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

### Control Flow
```python
# If statements
if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teenager")
else:
    print("Child")

# Loops
for i in range(5):
    print(i)

# List comprehension
squares = [x**2 for x in range(10)]
```

### Functions
```python
# Basic function
def add(a: int, b: int) -> int:
    return a + b

# Default arguments
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

# *args and **kwargs
def flexible_function(*args, **kwargs):
    print(f"Args: {args}")
    print(f"Kwargs: {kwargs}")
```

### Classes
```python
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
    
    def __str__(self) -> str:
        return f"User({self.name})"
    
    def send_email(self, message: str) -> None:
        print(f"Sending '{message}' to {self.email}")
```

### Error Handling
```python
try:
    result = risky_operation()
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
else:
    print("Success!")
finally:
    cleanup()
```

### Async Programming
```python
import asyncio

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Run async function
data = asyncio.run(fetch_data("https://api.example.com"))
```

## Learning Path

1. **Start with basics** - Variables, functions, control flow
2. **Learn data structures** - Lists, dicts, sets, tuples
3. **Understand OOP** - Classes, inheritance, methods
4. **Master error handling** - Try/except, custom exceptions
5. **Explore async** - For web scraping and I/O operations
6. **Add type hints** - Make code more maintainable

## Best Practices

- **PEP 8** - Follow Python style guide
- **Type hints** - Use them for better code clarity
- **Virtual environments** - Always isolate dependencies
- **Testing** - Write tests for your code
- **Documentation** - Document your functions and classes

For the complete guide with detailed explanations and examples, see the full [learning_concepts.md](https://github.com/YOUR_USERNAME/learning/blob/main/learning_concepts.md) file.

Happy Python coding! 🐍