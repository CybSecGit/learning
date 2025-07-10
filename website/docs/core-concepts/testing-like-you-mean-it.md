# Testing Like You Mean It
## *Or: How to Prove Your Code Works (To Yourself and Others)*

> "Testing shows the presence, not the absence of bugs." - Edsger Dijkstra
> "Testing shows your code is broken in ways you never imagined." - Every Developer Ever

Welcome to the chapter where we learn to systematically break our own code before someone else does it for us. Because nothing builds character like discovering your "perfect" scraper crashes when someone enters an emoji in the URL field.

## The Great Testing Reality Check

**What most tutorials tell you about testing:**
- "Write tests to make sure your code works!"
- "Tests give you confidence!"
- "Testing is fun and easy!"

**What testing actually feels like:**
- Spending 3 hours writing a test for 10 lines of code
- Your tests pass but your code still doesn't work
- Discovering your tests were testing the wrong thing entirely
- The eternal question: "Am I testing this right, or just testing that my mocks work?"

**The truth:** Testing is like insurance - boring, expensive, and you only appreciate it when everything goes wrong.

## Chapter 4.1: The Testing Hierarchy of Needs

### Level 1: "Does It Import?" Tests
*Also known as: "Smoke Tests" or "Please Don't Crash Immediately"*

```python
def test_basic_sanity():
    """Test that our code can be imported without Python having a panic attack."""
    from changelogger.scraper import BasicScraper

    # If we get here without an ImportError, we're already winning
    assert True  # The most optimistic assertion in programming
```

**When to use:** Always. This is like checking if your car has wheels before trying to drive.

**When NOT to use:** Never. Always check your imports work.

**Humor level:** Low (but the relief is high)

### Level 2: Unit Tests - "Testing in a Vacuum"
*The art of testing one thing while pretending everything else doesn't exist*

```python
@pytest.mark.asyncio
async def test_fetch_url_with_perfect_mocks():
    """Test our scraper in a fantasy world where everything works perfectly."""

    # Create a beautiful, perfect mock response
    mock_response = AsyncMock()
    mock_response.status_code.as_int.return_value = 200
    mock_response.text.return_value = "<html>Perfect content</html>"
    mock_response.headers.items.return_value = [("content-type", "text/html")]

    # Test in our controlled environment
    with patch('changelogger.scraper.rnet.Client') as mock_client:
        mock_client.return_value.get.return_value = mock_response

        scraper = BasicScraper(ScrapingConfig())
        result = await scraper.fetch_url("http://example.com")

        assert result.is_success()
        assert result.status_code == 200
        # Look ma, no network requests!
```

**When to use:**
- Testing business logic in isolation
- When you want fast feedback
- When external dependencies are unreliable
- When you want to test error conditions without breaking things

**When NOT to use:**
- When you need to verify actual network behavior
- When your mocks become more complex than the real code
- When you're mocking so much that you're basically testing your mocks

**The dirty secret:** Your mocks will lie to you. They'll tell you everything works perfectly while your real code sets fires in production.

### Level 3: Integration Tests - "Welcome to the Real World"
*Where your beautiful unit tests meet cruel reality*

```python
@pytest.mark.asyncio
async def test_real_http_request():
    """Test with actual HTTP requests because we're brave (or foolish)."""

    scraper = BasicScraper(ScrapingConfig())

    # This actually hits the internet - scary!
    result = await scraper.fetch_url("https://httpbin.org/get")

    assert result.is_success()
    assert result.status_code == 200
    assert "httpbin" in result.content.lower()

    # If this passes, our scraper can actually scrape!
    # If it fails, either our code is broken or the internet is broken
    # (Spoiler: it's usually our code)
```

**When to use:**
- Verifying your components actually work together
- Testing against real APIs (with permission!)
- Catching integration bugs that unit tests miss
- Building confidence that your system actually works

**When NOT to use:**
- In CI/CD without external service dependencies
- For testing every edge case (too slow and flaky)
- When external services are unreliable
- When you'll get rate-limited into oblivion

**Pro tip:** Integration tests fail for mysterious reasons at 3 AM. Plan accordingly.

### Level 4: End-to-End Tests - "The Full Monty"
*Testing the complete user journey, including all the parts that will definitely break*

```python
@pytest.mark.asyncio
async def test_complete_scraping_workflow():
    """Test the entire scraping process from config to results."""

    # Create configuration
    config = ScrapingConfig(
        user_agent="Test Scraper",
        request_delay=1.0,
        max_concurrent_requests=3
    )

    # Initialize scraper
    scraper = BasicScraper(config)

    # Test multiple URLs with different characteristics
    urls = [
        "https://httpbin.org/get",        # Should work
        "https://httpbin.org/status/404", # Should fail gracefully
        "https://httpbin.org/delay/2",    # Should be slow but work
    ]

    # Run the complete process
    results = await scraper.fetch_multiple_urls(urls)

    # Verify the complete workflow
    assert len(results) == 3
    assert results[0].is_success()  # GET should work
    assert not results[1].is_success()  # 404 should fail
    assert results[2].is_success()  # Slow request should eventually work

    # This test proves our entire scraping pipeline works end-to-end
```

**When to use:**
- Verifying complete user workflows
- Catching bugs that span multiple components
- Building confidence in major releases
- Testing critical business paths

**When NOT to use:**
- For every feature (too slow and complex)
- When you need quick feedback during development
- When the dependencies are too complex to set up
- When debugging becomes a nightmare

## Chapter 4.2: The Art of Test-Driven Development (TDD)

### The TDD Cycle: Red, Green, Refactor, Repeat, Therapy

**Red Phase: Write a Failing Test**
```python
@pytest.mark.asyncio
async def test_scraper_handles_timeout():
    """Test that our scraper gracefully handles timeouts."""

    # This test will fail because we haven't implemented timeout handling yet
    config = ScrapingConfig(timeout=1)  # Very short timeout
    scraper = BasicScraper(config)

    # This should timeout and be handled gracefully
    result = await scraper.fetch_url("https://httpbin.org/delay/10")

    assert not result.is_success()
    assert "timeout" in result.error.lower()
    # This will fail because we haven't written the timeout logic yet
```

**Green Phase: Make It Pass (By Any Means Necessary)**
```python
async def fetch_url(self, url: str) -> ScrapingResult:
    """Fetch a URL with timeout handling."""

    try:
        # Quick and dirty implementation to make the test pass
        client = rnet.Client(timeout=self.config.timeout)
        response = await client.get(url)
        # ... rest of implementation

    except asyncio.TimeoutError:
        # Handle timeout to make our test pass
        return ScrapingResult(
            url=url,
            status_code=0,
            content="",
            headers={},
            error="Request timed out"
        )
```

**Refactor Phase: Make It Pretty (Optional)**
```python
async def fetch_url(self, url: str) -> ScrapingResult:
    """Fetch a URL with proper timeout handling and error messages."""

    try:
        client = rnet.Client(timeout=self.config.timeout)
        response = await client.get(url)
        # ... proper implementation

    except asyncio.TimeoutError:
        return ScrapingResult(
            url=url,
            status_code=0,
            content="",
            headers={},
            error=f"Request timed out after {self.config.timeout}s"
        )
    except Exception as e:
        # Handle other errors too
        return ScrapingResult(
            url=url,
            status_code=0,
            content="",
            headers={},
            error=f"Request failed: {str(e)}"
        )
```

**Therapy Phase: Question Your Life Choices** *(Not officially part of TDD, but recommended)*
- "Why did I think this was a good idea?"
- "Is this test actually testing anything useful?"
- "Should I have just written the code first?"

### TDD Advantages:
- Forces you to think about design before implementation
- Ensures your code is testable
- Gives you confidence to refactor
- Provides documentation of how your code should behave
- Makes you write tests (because otherwise you won't)

### TDD Disadvantages:
- Takes longer initially
- Can lead to over-engineering
- Tests might constrain design too much
- You might test the wrong thing
- Requires discipline (humans are bad at discipline)

## Chapter 4.3: Testing Anti-Patterns (What NOT to Do)

### The "Testing the Framework" Anti-Pattern
```python
# DON'T DO THIS
def test_python_dict_works():
    """Test that Python dictionaries work."""
    d = {"key": "value"}
    assert d["key"] == "value"
    # Congratulations, you just tested Python itself
```

**Why it's bad:** You're testing Python/your framework, not your code.
**Fix:** Test your business logic, not the language features.

### The "Testing Implementation Details" Anti-Pattern
```python
# DON'T DO THIS
def test_scraper_calls_rnet_exactly_once():
    """Test that we call rnet.Client().get() exactly once."""
    with patch('changelogger.scraper.rnet.Client') as mock_client:
        scraper = BasicScraper(ScrapingConfig())
        await scraper.fetch_url("http://example.com")

        # Testing HOW it works, not WHAT it does
        assert mock_client.call_count == 1
        assert mock_client.return_value.get.call_count == 1
```

**Why it's bad:** Your tests become brittle and break when you refactor.
**Fix:** Test behavior, not implementation.

### The "Mock Everything" Anti-Pattern
```python
# DON'T DO THIS - Mock Madness
@patch('changelogger.scraper.time.time')
@patch('changelogger.scraper.asyncio.sleep')
@patch('changelogger.scraper.rnet.Client')
@patch('changelogger.scraper.urlparse')
@patch('changelogger.scraper.logging.getLogger')
async def test_everything_mocked(mock_logger, mock_urlparse, mock_client, mock_sleep, mock_time):
    """Test with so many mocks that we're basically testing nothing."""
    # 50 lines of mock setup
    # 2 lines of actual test
    # 0 confidence that anything actually works
```

**Why it's bad:** You're testing your mocks, not your code.
**Fix:** Mock only external dependencies, not everything.

### The "Happy Path Only" Anti-Pattern
```python
# DON'T DO THIS
async def test_scraper_works():
    """Test that the scraper works with perfect input."""
    scraper = BasicScraper(ScrapingConfig())
    result = await scraper.fetch_url("https://httpbin.org/get")

    assert result.is_success()
    # Great! But what happens when things go wrong?
```

**Why it's bad:** Real users will find ways to break your code that you never imagined.
**Fix:** Test error conditions, edge cases, and unhappy paths.

## Chapter 4.4: Web Scraping Testing Challenges

### Challenge 1: Testing Network Code
**The Problem:** Networks are unreliable, servers go down, and responses change.

**Solution 1: Mock External Calls**
```python
@pytest.mark.asyncio
async def test_handle_network_error():
    """Test network error handling without depending on network."""

    with patch('changelogger.scraper.rnet.Client') as mock_client:
        # Simulate a network error
        mock_client.return_value.get.side_effect = ConnectionError("Network unreachable")

        scraper = BasicScraper(ScrapingConfig())
        result = await scraper.fetch_url("http://example.com")

        assert not result.is_success()
        assert "network unreachable" in result.error.lower()
```

**Solution 2: Use Test Doubles (Local Test Server)**
```python
# You could set up a local HTTP server for testing
# But that's probably overkill for most cases
```

**Solution 3: Use Reliable Test Services**
```python
@pytest.mark.integration
async def test_with_httpbin():
    """Test with httpbin.org - a reliable test service."""

    scraper = BasicScraper(ScrapingConfig())
    result = await scraper.fetch_url("https://httpbin.org/status/200")

    assert result.is_success()
    # httpbin.org is designed for testing, so this should be reliable
```

### Challenge 2: Testing Rate Limiting
**The Problem:** Rate limiting involves timing, which is hard to test.

**Solution: Mock Time**
```python
@pytest.mark.asyncio
async def test_rate_limiting():
    """Test that rate limiting actually delays requests."""

    config = ScrapingConfig(request_delay=1.0)
    scraper = BasicScraper(config)

    start_time = time.time()

    # Make two requests
    await scraper.fetch_url("https://httpbin.org/get")
    await scraper.fetch_url("https://httpbin.org/get")

    elapsed = time.time() - start_time

    # Should take at least 1 second due to rate limiting
    assert elapsed >= 1.0
    # This test is flaky and depends on actual timing - be careful!
```

### Challenge 3: Testing Browser Impersonation
**The Problem:** How do you test that you're successfully impersonating a browser?

**Solution: Verify Headers**
```python
@pytest.mark.asyncio
async def test_browser_impersonation():
    """Test that we send browser-like headers."""

    scraper = BasicScraper(ScrapingConfig())
    result = await scraper.fetch_url("https://httpbin.org/headers")

    # Parse the response to see what headers we sent
    response_data = json.loads(result.content)
    sent_headers = response_data["headers"]

    # Verify we sent browser-like headers
    assert "User-Agent" in sent_headers
    assert "Accept" in sent_headers
    assert "Accept-Language" in sent_headers

    # Verify we don't look like a generic script
    user_agent = sent_headers["User-Agent"]
    assert "python" not in user_agent.lower()
    assert "requests" not in user_agent.lower()
```

## Chapter 4.5: Test Organization and Best Practices

### Directory Structure That Won't Drive You Insane
```
tests/
├── unit/                    # Fast, isolated tests
│   ├── test_scraper.py      # Test scraper logic
│   ├── test_config.py       # Test configuration
│   └── test_utils.py        # Test utility functions
├── integration/             # Tests with external dependencies
│   ├── test_http_requests.py  # Real HTTP requests
│   ├── test_rate_limiting.py  # Timing-based tests
│   └── test_browser_headers.py # Browser impersonation
├── performance/             # Performance and load tests
│   ├── test_concurrent_load.py  # Concurrency tests
│   └── test_memory_usage.py     # Memory leak detection
└── conftest.py             # Shared test configuration
```

### Test Naming That Actually Helps
```python
# GOOD: Descriptive test names
def test_fetch_url_returns_error_result_when_domain_does_not_exist():
    """Test that invalid domains return error results instead of crashing."""
    pass

def test_concurrent_requests_respect_max_limit():
    """Test that we don't exceed max concurrent request limits."""
    pass

# BAD: Cryptic test names
def test_fetch_1():
    """Test fetch."""  # Thanks, that's super helpful
    pass

def test_error():
    """Test error."""  # Which error? What condition?
    pass
```

### Fixture Organization (Shared Test Setup)
```python
# conftest.py - Shared fixtures
@pytest.fixture
def basic_config():
    """Provide a basic scraper configuration for tests."""
    return ScrapingConfig(
        request_delay=0.1,  # Faster for tests
        timeout=5,          # Shorter timeout for tests
        max_concurrent_requests=3
    )

@pytest.fixture
async def scraper(basic_config):
    """Provide a configured scraper instance."""
    return BasicScraper(basic_config)

@pytest.fixture
def mock_response():
    """Provide a mock HTTP response for unit tests."""
    response = AsyncMock()
    response.status_code.as_int.return_value = 200
    response.text.return_value = "<html>Test content</html>"
    response.headers.items.return_value = [("content-type", "text/html")]
    return response
```

## Chapter 4.6: Testing Strategies for Different Scenarios

### Strategy 1: Testing Error Conditions
```python
@pytest.mark.asyncio
async def test_all_the_ways_things_can_break():
    """Test error handling for various failure modes."""

    scraper = BasicScraper(ScrapingConfig(timeout=2))

    # Test different types of failures
    test_cases = [
        ("Invalid URL", "not-a-url"),
        ("Non-existent domain", "https://definitely-not-a-real-domain.invalid"),
        ("Timeout", "https://httpbin.org/delay/10"),
        ("HTTP error", "https://httpbin.org/status/500"),
    ]

    for test_name, url in test_cases:
        result = await scraper.fetch_url(url)

        # All should fail gracefully, not crash
        assert not result.is_success()
        assert result.error is not None
        print(f"✅ {test_name}: Failed gracefully with '{result.error[:50]}...'")
```

### Strategy 2: Property-Based Testing (Advanced)
```python
# Using hypothesis for property-based testing
from hypothesis import given, strategies as st

@given(st.text())
async def test_scraper_handles_any_string_input(random_string):
    """Test that our scraper doesn't crash with random string inputs."""

    scraper = BasicScraper(ScrapingConfig())

    # This should not crash, regardless of input
    result = await scraper.fetch_url(random_string)

    # We don't care if it succeeds or fails, just that it doesn't crash
    assert isinstance(result, ScrapingResult)
    # If it fails, it should have an error message
    if not result.is_success():
        assert result.error is not None
```

### Strategy 3: Performance Testing
```python
@pytest.mark.asyncio
async def test_concurrent_performance():
    """Test that concurrent requests are actually faster than sequential."""

    config = ScrapingConfig(request_delay=0.5, max_concurrent_requests=5)
    scraper = BasicScraper(config)

    urls = ["https://httpbin.org/delay/1" for _ in range(5)]

    # Time concurrent execution
    start = time.time()
    results = await scraper.fetch_multiple_urls(urls)
    concurrent_time = time.time() - start

    # Time sequential execution (for comparison)
    start = time.time()
    sequential_results = []
    for url in urls:
        result = await scraper.fetch_url(url)
        sequential_results.append(result)
    sequential_time = time.time() - start

    # Concurrent should be significantly faster
    assert concurrent_time < sequential_time * 0.7
    print(f"Concurrent: {concurrent_time:.2f}s, Sequential: {sequential_time:.2f}s")
```

## Chapter 4.7: When NOT to Test (Yes, Really)

### Don't Test: Third-Party Libraries
```python
# DON'T DO THIS
def test_rnet_library_works():
    """Test that the rnet library can make HTTP requests."""
    client = rnet.Client()
    response = await client.get("https://httpbin.org/get")
    assert response.status_code.as_int() == 200
    # You're testing someone else's code, not yours
```

### Don't Test: Trivial Code
```python
# DON'T TEST THIS
class ScrapingResult:
    def __init__(self, url, status_code, content):
        self.url = url
        self.status_code = status_code
        self.content = content

# Don't write this test:
def test_scraping_result_init():
    result = ScrapingResult("url", 200, "content")
    assert result.url == "url"
    assert result.status_code == 200
    assert result.content == "content"
    # This tests the Python language, not your logic
```

### Don't Test: Configuration Objects (Usually)
```python
# DON'T TEST THIS (unless there's logic)
@dataclass
class ScrapingConfig:
    timeout: int = 30
    request_delay: float = 1.0

# Don't test that defaults work - that's just testing dataclass
```

### DO Test: Your Business Logic
```python
# DO TEST THIS
class ScrapingResult:
    def is_success(self) -> bool:
        """Check if the scraping was successful."""
        return 200 <= self.status_code < 300 and self.error is None

# This has logic, so test it:
def test_is_success_with_200_status():
    result = ScrapingResult(url="test", status_code=200, content="", headers={})
    assert result.is_success()

def test_is_success_with_404_status():
    result = ScrapingResult(url="test", status_code=404, content="", headers={})
    assert not result.is_success()
```

## Chapter 4.8: Testing Philosophy and Mental Health

### The Testing Paradox
- **Not enough tests:** Your code breaks in production and everyone blames you
- **Too many tests:** You spend more time maintaining tests than writing features
- **Wrong tests:** You have 100% coverage but your code still doesn't work
- **Right tests:** You're probably overthinking it

### Test Coverage: The Lying Metric
```bash
# Your test runner says:
Coverage: 100%

# Reality:
- You tested all your lines of code
- But you didn't test any of the ways users will actually break it
- And you mocked all the parts that could actually fail
- So your coverage is 100% and your confidence is 0%
```

**The truth about coverage:**
- 100% coverage doesn't mean your code works
- 50% coverage doesn't mean your code is bad
- Focus on covering the important paths, not every line

### The Testing Zen
- Test behaviors, not implementation
- Test unhappy paths, not just happy ones
- Test with real data when possible
- Mock external dependencies, not your own code
- Write tests that will catch real bugs
- Don't write tests that just exercise code

### Signs You're Testing Wrong
- Your tests are harder to understand than your code
- Your tests break every time you refactor
- You have more test code than production code
- Your tests all pass but your demo crashes
- You're testing getters and setters
- You mock everything including your own code

### Signs You're Testing Right
- Your tests catch real bugs
- Your tests document how your code should behave
- You can refactor confidently
- Your tests fail when your code is broken
- You can understand your tests in 6 months
- Your tests help you design better code

## Chapter Summary: Testing Reality Check

What we learned:

1. **Testing types have different purposes** - Unit tests for speed, integration tests for confidence
2. **TDD is great in theory** - In practice, it requires discipline and experience
3. **Mocking is powerful and dangerous** - Mock external dependencies, not your own code
4. **Coverage is a tool, not a goal** - 100% coverage doesn't guarantee working code
5. **Test behaviors, not implementation** - Tests should survive refactoring
6. **Error testing is crucial** - Happy path tests don't catch production bugs
7. **Don't test everything** - Focus on logic, skip trivial code
8. **Tests are documentation** - Write tests that explain how your code should work

### The Ultimate Testing Truth
Good tests save you time and embarrassment. Bad tests waste your time and give you false confidence. No tests mean you're basically gambling with production.

Choose wisely, test thoughtfully, and remember: the goal isn't perfect tests, it's working code.

---

## Next Chapter Preview

In Chapter 5, we'll add HTML parsing with selectolax, where we'll discover exciting new ways for tests to fail:

- CSS selectors that work in the browser but not in your scraper
- HTML that's malformed in ways you never imagined
- Character encoding adventures
- The joy of testing DOM manipulation
- And the eternal question: "Should I test that my CSS selector is correct?"

But hey, at least you'll know how to test it properly!

---

*"Testing is like flossing - you know you should do it, you feel guilty when you don't, and when you finally do it, you discover problems you didn't know you had."* - Anonymous Developer

*"The best test is the one you write right before your code breaks in production."* - Murphy's Law of Software Testing
