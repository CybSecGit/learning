# Failure-Driven Development
## *Or: How to Embrace the Chaos and Learn from Every Crash*

> "I have not failed. I've just found 10,000 ways that won't work." - Thomas Edison
> "I've found 10,001." - Every Web Scraper Developer Ever

Welcome to the most honest chapter about software development you'll ever read. We're going to talk about failure - not as something to avoid, but as your most valuable teacher.

## The Great Lie of Programming Tutorials

Most tutorials show you this magical world where:
- Code works on the first try
- Dependencies install perfectly
- Network requests never fail
- Everything is clean and predictable

**This is complete nonsense.**

Real development looks like this:
- Import errors for 20 minutes
- SSL certificate mysteries
- Rate limiting surprises
- "It worked yesterday" syndrome
- Documentation that lies to your face

## Our Philosophy: Fail Fast, Learn Faster

Instead of pretending everything works perfectly, we're going to:

1. **Start with broken code** and debug it together
2. **Intentionally trigger errors** to see how they work
3. **Celebrate each failure** as a learning milestone
4. **Build resilience** through repeated exposure to problems
5. **Develop debugging intuition** through practice

## Chapter 3.1: The Magnificent Seven (Types of Failures)

Let's categorize the beautiful ways your web scraper will fail:

### 1. 💥 The Import Explosion
*"ImportError: No module named 'your_hopes_and_dreams'"*

**What it looks like:**
```python
from changelogger.scraper import BasicScraper
# ImportError: No module named 'changelogger'
```

**Why it happens:**
- Wrong directory
- Virtual environment not activated
- Package not installed
- Python path issues

**The learning opportunity:**
Understanding Python's import system, virtual environments, and package structure.

**How to embrace it:**
```bash
# Intentionally break imports to practice debugging
python -c "from nonexistent_module import everything"
# Now debug: Where are you? What's in sys.path? Is venv active?
```

### 2. 🌐 The Network Nightmare
*"The internet exists, but not for you right now"*

**What it looks like:**
```python
result = await scraper.fetch_url("https://example.com")
# TimeoutError, ConnectionError, SSLError, DNSError...
```

**Why it happens:**
- DNS resolution failures
- SSL certificate issues
- Corporate firewalls
- Server timeouts
- Rate limiting
- The server just doesn't like you today

**The learning opportunity:**
Network protocols, HTTP status codes, debugging connectivity issues.

**How to embrace it:**
```python
# Intentionally cause network failures
urls = [
    "https://this-domain-does-not-exist.invalid",  # DNS failure
    "http://localhost:99999",                      # Connection refused
    "https://httpbin.org/delay/30",               # Timeout
    "https://httpbin.org/status/429",             # Rate limited
]
# Debug each one - what's the specific error? How do you handle it?
```

### 3. 🔧 The Configuration Catastrophe
*"Your settings are technically valid but practically useless"*

**What it looks like:**
```python
config = ScrapingConfig(
    timeout=0,           # Instant timeout
    request_delay=-5,    # Negative delay
    max_concurrent_requests=0  # No requests allowed
)
# Everything fails in creative ways
```

**Why it happens:**
- No input validation
- Extreme edge cases
- Copy-paste errors
- "What could go wrong?" attitude

**The learning opportunity:**
Configuration validation, sensible defaults, edge case handling.

**How to embrace it:**
```python
# Try terrible configurations
bad_configs = [
    ScrapingConfig(timeout=0.001),     # Microscopic timeout
    ScrapingConfig(request_delay=300), # 5-minute delays
    ScrapingConfig(max_concurrent_requests=1000),  # DDOS yourself
]
# What breaks? How? Can you make it fail gracefully?
```

### 4. 🤖 The Async Apocalypse
*"Event loops, coroutines, and timing issues, oh my!"*

**What it looks like:**
```python
# This will fail spectacularly
def not_async_function():
    result = scraper.fetch_url("https://example.com")  # Missing await
    return result

# RuntimeError: coroutine 'fetch_url' was never awaited
```

**Why it happens:**
- Forgetting `await`
- Mixing sync and async code
- Event loop confusion
- Timing issues

**The learning opportunity:**
Async programming, coroutines, event loops, concurrency.

**How to embrace it:**
```python
# Common async mistakes to practice fixing
async def async_mistakes():
    # Mistake 1: Forgetting await
    result = scraper.fetch_url("https://example.com")  # Oops

    # Mistake 2: Using sync in async context
    time.sleep(1)  # Should be await asyncio.sleep(1)

    # Mistake 3: Not handling concurrent failures
    tasks = [scraper.fetch_url(url) for url in many_urls]
    results = await asyncio.gather(*tasks)  # One failure kills all
```

### 5. 📊 The Data Disaster
*"You got data, but it's not the data you wanted"*

**What it looks like:**
```python
# Expected JSON, got HTML
response_data = json.loads(result.content)
# JSONDecodeError: Expecting value: line 1 column 1 (char 0)

# Expected text, got bytes
headers = dict(response.headers)  # Bytes keys/values
user_agent = headers["User-Agent"]  # KeyError or encoding error
```

**Why it happens:**
- Content type mismatches
- Encoding issues
- Bytes vs strings confusion
- API format changes

**The learning opportunity:**
Data types, encoding, content negotiation, defensive programming.

**How to embrace it:**
```python
# Test with different content types
test_urls = [
    "https://httpbin.org/json",      # JSON response
    "https://httpbin.org/html",      # HTML response
    "https://httpbin.org/xml",       # XML response
    "https://httpbin.org/image/png", # Binary response
]
# Try to parse each as JSON - what breaks? How do you detect content type?
```

### 6. ⏱️ The Performance Pitfall
*"It works, but glacially slow or suspiciously fast"*

**What it looks like:**
```python
# Sequential processing (slow)
results = []
for url in 1000_urls:
    result = await scraper.fetch_url(url)  # 1000 sequential requests
    results.append(result)
# Takes 30 minutes, gets you banned

# Uncontrolled concurrency (fast but destructive)
tasks = [scraper.fetch_url(url) for url in 1000_urls]
results = await asyncio.gather(*tasks)  # 1000 simultaneous requests
# Takes 3 seconds, definitely gets you banned
```

**Why it happens:**
- No rate limiting
- Poor concurrency management
- Resource exhaustion
- Server overload

**The learning opportunity:**
Performance optimization, rate limiting, concurrency control, resource management.

**How to embrace it:**
```python
# Benchmark different approaches
import time

# Approach 1: Sequential (slow but safe)
start = time.time()
for url in test_urls:
    await scraper.fetch_url(url)
print(f"Sequential: {time.time() - start:.2f}s")

# Approach 2: Unlimited concurrency (fast but dangerous)
start = time.time()
tasks = [scraper.fetch_url(url) for url in test_urls]
await asyncio.gather(*tasks)
print(f"Concurrent: {time.time() - start:.2f}s")

# Which gets better results? Which gets you banned?
```

### 7. 🔒 The Security Surprise
*"Your scraper works, but also accidentally joins a botnet"*

**What it looks like:**
```python
# Logging sensitive data
logger.info(f"Response: {result.content}")  # Logs API keys, tokens
logger.info(f"Headers: {result.headers}")   # Logs auth headers

# Trusting user input
user_url = input("Enter URL: ")
result = await scraper.fetch_url(user_url)  # SSRF vulnerability

# No input validation
config = load_config_from_file(user_file)  # Code injection risk
```

**Why it happens:**
- Security not considered early
- Trusting inputs blindly
- Oversharing in logs
- Copy-paste from tutorials

**The learning opportunity:**
Security mindset, input validation, secure logging, threat modeling.

**How to embrace it:**
```python
# Security testing scenarios
dangerous_inputs = [
    "file:///etc/passwd",           # File system access
    "http://localhost:22",          # Port scanning
    "javascript:alert('xss')",     # XSS attempt
    "data:text/html,<script>...</script>",  # Data URL injection
]
# Test your input validation - what gets through? What should be blocked?
```

## Chapter 3.2: The Debugging Mindset

When things go wrong (not if, when), here's how to think:

### 1. 🤔 **"What exactly is breaking?"**
```python
# Bad debugging: "It doesn't work"
# Good debugging: "The HTTP request succeeds but JSON parsing fails with 'expecting value at line 1 column 1'"

# Add debug prints everywhere
print(f"🐛 About to fetch: {url}")
print(f"🐛 Got response: status={response.status}, length={len(content)}")
print(f"🐛 Content preview: {content[:100]}...")
```

### 2. 🔍 **"What did I assume wrongly?"**
```python
# Assumption: "The API returns JSON"
# Reality: "The API returns HTML when there's an error"

# Test your assumptions
print(f"Content type: {response.headers.get('content-type')}")
print(f"Is JSON?: {content.strip().startswith('{')}")
```

### 3. 🧪 **"Can I make a simpler version that works?"**
```python
# Complex (and broken):
async def complex_scraper():
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        # 47 more lines of complex processing

# Simple (and working):
async def simple_scraper():
    result = await scraper.fetch_url("https://httpbin.org/get")
    print(f"Status: {result.status_code}")
    print(f"Success: {result.is_success()}")
```

### 4. 📚 **"What would the error message look like if I designed it?"**
```python
# Cryptic error: "Expecting value: line 1 column 1 (char 0)"
# Helpful error: "Expected JSON response but got HTML. Content-Type: text/html. Status: 404. Server returned error page instead of API response."

# Design better error messages
if not result.is_success():
    print(f"❌ Request failed:")
    print(f"   URL: {result.url}")
    print(f"   Status: {result.status_code}")
    print(f"   Content-Type: {result.headers.get('content-type', 'unknown')}")
    print(f"   Content preview: {result.content[:200]}...")
```

## Chapter 3.3: Hands-On Failure Workshop

Let's practice failing magnificently:

### Exercise 1: The Import Disaster
```python
# Save this as broken_imports.py and run it
from definitely_not_installed import MagicalScraper
from changelogger.wrong_module import NonExistentClass
from ..invalid.relative import SomethingElse

# Your mission: Fix each import error one by one
# Document what you learned from each failure
```

### Exercise 2: The Network Nightmare
```python
# Save this as network_disasters.py
import asyncio
from src.changelogger.scraper import BasicScraper, ScrapingConfig

async def network_failure_tour():
    scraper = BasicScraper(ScrapingConfig(timeout=2))

    # Each of these should fail differently
    test_cases = [
        ("DNS Failure", "https://definitely-not-a-real-domain-12345.invalid"),
        ("Connection Refused", "http://localhost:99999"),
        ("Timeout", "https://httpbin.org/delay/10"),
        ("404 Error", "https://httpbin.org/status/404"),
        ("Rate Limited", "https://httpbin.org/status/429"),
        ("Server Error", "https://httpbin.org/status/500"),
    ]

    for test_name, url in test_cases:
        print(f"\n🧪 Testing: {test_name}")
        try:
            result = await scraper.fetch_url(url)
            print(f"   Status: {result.status_code}")
            print(f"   Success: {result.is_success()}")
            print(f"   Error: {result.error}")
        except Exception as e:
            print(f"   Exception: {type(e).__name__}: {e}")

        # Question: How is each failure different?
        # Question: Which ones should you retry?
        # Question: How would you explain each to a user?

asyncio.run(network_failure_tour())
```

### Exercise 3: The Configuration Catastrophe
```python
# Save this as config_disasters.py
from src.changelogger.scraper import BasicScraper, ScrapingConfig

def test_terrible_configs():
    """Test configurations that are technically valid but practically useless."""

    terrible_configs = [
        ("Microscopic Timeout", ScrapingConfig(timeout=0.001)),
        ("Massive Delay", ScrapingConfig(request_delay=60)),
        ("Zero Concurrency", ScrapingConfig(max_concurrent_requests=0)),
        ("Ludicrous Concurrency", ScrapingConfig(max_concurrent_requests=10000)),
        ("Negative Delay", ScrapingConfig(request_delay=-1)),
    ]

    for config_name, config in terrible_configs:
        print(f"\n🧪 Testing: {config_name}")
        try:
            scraper = BasicScraper(config)
            print(f"   ✅ Scraper created (somehow)")

            # Try to use it
            result = await scraper.fetch_url("https://httpbin.org/get")
            print(f"   Status: {result.status_code}")
            print(f"   Time: {result.fetch_time:.3f}s")

        except Exception as e:
            print(f"   💥 Failed: {e}")

        # Question: Should these configurations be allowed?
        # Question: How would you validate inputs?
        # Question: What are sensible defaults?

asyncio.run(test_terrible_configs())
```

## Chapter 3.4: Learning from Production Failures

Here are real failure stories from production web scrapers (names changed to protect the embarrassed):

### The Case of the Midnight Memory Leak
**The failure:** Scraper ran fine during testing, but crashed every night at 2 AM with out-of-memory errors.

**The investigation:**
- Memory usage grew slowly over time
- Only happened with long-running processes
- Only with certain websites

**The root cause:** Not closing HTTP connections properly. Each request left a connection open, slowly exhausting memory.

**The fix:**
```python
# Before (broken):
async def fetch_url(self, url):
    client = rnet.Client()
    response = await client.get(url)
    return response  # Connection never closed!

# After (fixed):
async def fetch_url(self, url):
    client = rnet.Client()
    try:
        response = await client.get(url)
        return response
    finally:
        await client.close()  # Always close connections
```

**The lesson:** Resource management matters. Test with long-running processes.

### The Great Rate Limiting Disaster of 2023
**The failure:** Scraper worked perfectly for weeks, then suddenly all requests started returning 429 errors.

**The investigation:**
- Rate limiting was implemented correctly
- Server wasn't overloaded
- Other scrapers worked fine

**The root cause:** The scraper was so polite that it wasn't using sessions. Each request created a new connection, which the server interpreted as different clients making rapid requests.

**The fix:**
```python
# Before (polite but inefficient):
for url in urls:
    await asyncio.sleep(1)  # Polite delay
    client = rnet.Client()  # New connection every time
    response = await client.get(url)

# After (polite and efficient):
client = rnet.Client()  # One connection for all requests
for url in urls:
    await asyncio.sleep(1)  # Still polite
    response = await client.get(url)  # Reuse connection
```

**The lesson:** Politeness isn't just about delays. Connection reuse matters.

### The SSL Certificate Mystery
**The failure:** Scraper worked on developer machines but failed in production with SSL errors.

**The investigation:**
- Same code, same Python version
- Same target websites
- Different SSL errors in production

**The root cause:** Production environment had outdated CA certificates. The websites had updated their SSL certificates to use newer certificate authorities.

**The fix:**
```python
# Quick fix (not recommended for production):
import ssl
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Better fix: Update CA certificates
# apt-get update && apt-get install ca-certificates
```

**The lesson:** Environment differences are real. Test in production-like environments.

## Chapter 3.5: Building Failure Resilience

How to make your scraper antifragile:

### 1. **Expect Everything to Fail**
```python
async def resilient_fetch(self, url):
    """Fetch URL with the assumption that everything will go wrong."""

    # Validate inputs (because users lie)
    if not url or not isinstance(url, str):
        return ScrapingResult(url="invalid", status_code=0, error="Invalid URL")

    # Set reasonable timeouts (because servers are slow)
    timeout = min(self.config.timeout, 30)  # Never wait more than 30s

    # Try the request (because networks are unreliable)
    try:
        result = await self._do_request(url, timeout)

        # Validate the response (because servers lie)
        if result.status_code == 200 and not result.content:
            return ScrapingResult(url=url, status_code=200, error="Empty response")

        return result

    except Exception as e:
        # Log for debugging (because future you will thank you)
        logger.warning(f"Request failed for {url}: {e}")
        return ScrapingResult(url=url, status_code=0, error=str(e))
```

### 2. **Make Failures Observable**
```python
# Track failure patterns
failure_counts = {}
failure_patterns = {}

def record_failure(url, error):
    """Record failure for pattern analysis."""
    domain = urlparse(url).netloc
    failure_counts[domain] = failure_counts.get(domain, 0) + 1

    error_type = type(error).__name__
    failure_patterns[error_type] = failure_patterns.get(error_type, 0) + 1

    # Alert if failure rate is high
    if failure_counts[domain] > 10:
        logger.error(f"High failure rate for {domain}: {failure_counts[domain]} failures")
```

### 3. **Degrade Gracefully**
```python
async def fetch_with_fallbacks(self, url):
    """Try multiple strategies when things fail."""

    # Try 1: Normal request
    try:
        return await self.fetch_url(url)
    except TimeoutError:
        pass

    # Try 2: Longer timeout
    try:
        old_timeout = self.config.timeout
        self.config.timeout = old_timeout * 2
        return await self.fetch_url(url)
    finally:
        self.config.timeout = old_timeout

    # Try 3: Different user agent
    try:
        old_agent = self.config.user_agent
        self.config.user_agent = "curl/7.68.0"  # Look like curl
        return await self.fetch_url(url)
    finally:
        self.config.user_agent = old_agent

    # Give up gracefully
    return ScrapingResult(url=url, status_code=0, error="All fallback strategies failed")
```

## Chapter 3.6: The Failure Hall of Fame

Let's celebrate some spectacular failures:

### 🏆 Most Creative Import Error
```python
from __future__ import braces
# SyntaxError: not a chance
```

### 🏆 Most Optimistic Timeout
```python
config = ScrapingConfig(timeout=0.00001)  # 10 microseconds
# Narrator: "It was not enough time"
```

### 🏆 Most Honest Error Message
```python
# Real error from a production system:
"Error: Something went wrong. We're not sure what. Good luck debugging this."
```

### 🏆 Most Expensive Mistake
```python
# Accidentally scraped the same page 1 million times
for i in range(1000000):
    await scraper.fetch_url("https://expensive-api.com/data")
# Invoice: $47,000
# Manager's response: "So... about that code review process..."
```

### 🏆 Most Philosophical Error Message
```python
# Real error from a production system:
"Error: Something went wrong. We're not sure what. Good luck debugging this."
# Followed by: "Also, it's probably your fault somehow."
```

### 🏆 Most Passive-Aggressive Timeout
```python
config = ScrapingConfig(timeout=1)  # 1 second
# Later in logs: "Request timed out. Maybe try being more patient next time?"
```

## Chapter Summary: Embrace the Chaos

What we learned from this chapter:

1. **Failure is inevitable** - Plan for it, don't fight it
2. **Every error teaches something** - Collect them like Pokemon
3. **Good error handling** is more important than perfect code
4. **Debug incrementally** - Start simple, add complexity slowly
5. **Test your assumptions** - They're probably wrong
6. **Build observability** - You can't fix what you can't see
7. **Practice failing** - The more you practice, the faster you recover

## Next Chapter Preview

In Chapter 4, we'll take our battle-tested scraper and add HTML parsing with selectolax. Spoiler alert: This will introduce entirely new categories of failures involving:

- Character encoding mysteries
- CSS selector nightmares
- DOM structure assumptions
- JavaScript-rendered content
- And the eternal question: "Why is this `<div>` empty?"

But hey, at least now you know how to fail gracefully!

---

*"The master has failed more times than the beginner has even tried."* - Stephen McCranie

*"The expert debugger has encountered more error types than the novice has ever imagined."* - Anonymous (definitely not chatGPT)
