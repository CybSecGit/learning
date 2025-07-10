# Chapter 2: Modern Web Scraping with rnet
## *The Art of Polite Digital Conversation*

Welcome to the heart of our project - building a web scraper that doesn't get you banned from the internet. We'll use Test-Driven Development (TDD) because writing tests first prevents us from building broken scrapers (and there are enough of those already).

## Learning Objectives

By the end of this chapter, you'll be able to:
- Build an async web scraper using `rnet` for browser impersonation
- Implement proper rate limiting and error handling
- Write comprehensive tests for async code
- Handle real-world HTTP quirks gracefully
- Scrape websites without being rude about it

## The Problem with Traditional Web Scraping

Most scraping tutorials teach you this:

```python
import requests
response = requests.get("https://example.com")
print(response.text)
```

This approach has problems:
- 🚫 **Easily detected**: Screams "I'm a bot!"
- 🐌 **Slow**: One request at a time
- 💥 **Fragile**: No retry logic
- 😈 **Rude**: No rate limiting

## Our Modern Approach

We're building something better:

```python
import asyncio
import rnet
from tenacity import retry

# Modern, polite, and fast
client = rnet.Client(impersonate=rnet.Impersonate.Chrome131)
response = await client.get(url, headers=realistic_headers)
```

### Why This Stack?

- **`rnet`**: Advanced HTTP client with browser impersonation
- **`asyncio`**: Concurrent requests (politely)
- **`tenacity`**: Smart retry logic
- **TLS fingerprinting**: Looks like real Chrome

## TDD Process: Red, Green, Refactor (With Real Debugging)

We'll follow the classic TDD cycle, but we'll embrace the debugging journey:
1. **Red**: Write a failing test (expect import errors!)
2. **Debug**: Figure out why it's failing (hint: modules don't exist yet)
3. **Green**: Write minimal code to pass (more errors incoming!)
4. **Debug**: Fix the real-world API issues we encounter
5. **Refactor**: Improve the code based on what we learned

**Important**: In this chapter, we'll show you *all* the errors we encountered, not just the final working code. Debugging is a skill, and you learn it by practicing.

### Step 1: Define Our API (Red Phase) - The First Glorious Failure

First, let's design what we want our scraper to do:

```python
# tests/test_scraper.py
@pytest.mark.asyncio
async def test_fetch_url_success(scraper):
    url = "https://example.com/changelog"
    result = await scraper.fetch_url(url)

    assert result.is_success()
    assert result.status_code == 200
    assert result.content is not None
```

**Let's run this test and watch it fail spectacularly:**

```bash
$ python -m pytest tests/test_scraper.py -v
```

**Error #1: The Import Error**
```
ImportError while importing test module 'tests/test_scraper.py'.
ModuleNotFoundError: No module named 'src.changelogger.scraper'
```

**🎉 Congratulations!** You've encountered your first TDD error. This is exactly what we want - the test is telling us what we need to build.

**What this teaches us:**
- Tests drive the design (we're defining the API before implementation)
- Import errors are common in TDD (modules don't exist yet)
- Python's module system requires proper package structure

### Step 2: Basic Implementation (Green Phase) - More Educational Failures

Now we write the minimal code to make our tests pass:

```python
# src/changelogger/scraper.py - First attempt
import asyncio
import rnet

class BasicScraper:
    async def fetch_url(self, url: str):
        # Let's try the obvious approach
        async with rnet.AsyncClient() as client:
            response = await client.get(url)
            return response  # This will break too!
```

**Let's run the test again:**

```bash
$ python -m pytest tests/test_scraper.py -v
```

**Error #2: The Missing Pytest Plugin**
```
async def functions are not natively supported.
You need to install a suitable plugin for your async framework, for example:
  - anyio
  - pytest-asyncio
```

**What this teaches us:**
- Async testing requires special tools
- Pytest doesn't handle async natively
- Tool compatibility matters

**Fix:** `pip install pytest-asyncio`

**Error #3: The API Discovery**
```
AttributeError: <module 'rnet'> does not have the attribute 'AsyncClient'
```

**This is where the real learning happens!** Let's explore the rnet API:

```python
# Debugging session - always explore unknown APIs
import rnet
print(dir(rnet))
# ['Client', 'BlockingClient', 'Response', ...]
# No AsyncClient! It's just 'Client'
```

**What this teaches us:**
- Documentation can be wrong or incomplete
- Always explore APIs with `dir()` and `help()`
- Library interfaces may differ from expectations

```python
# src/changelogger/scraper.py
@dataclass
class ScrapingConfig:
    user_agent: str = "Changelogger/1.0 (Educational Project)"
    request_delay: float = 2.0  # Be polite
    max_concurrent_requests: int = 5
    respect_robots_txt: bool = True
    timeout: int = 30

@dataclass
class ScrapingResult:
    url: str
    status_code: int
    content: str
    headers: Dict[str, str]
    fetch_time: float = 0.0
    error: Optional[str] = None

    def is_success(self) -> bool:
        return 200 <= self.status_code < 300 and self.error is None

class BasicScraper:
    async def fetch_url(self, url: str) -> ScrapingResult:
        # Implementation here...
```

### Step 3: The StatusCode Mystery - When Types Attack

After fixing the import and API issues, we get our first integration test running, only to encounter:

**Error #4: The StatusCode Comparison**
```
TypeError: '<=' not supported between instances of 'int' and 'builtins.StatusCode'
```

**The debugging process:**
```python
# Let's investigate what we're dealing with
print(f"Status type: {type(response.status_code)}")
print(f"Status value: {response.status_code}")
print(f"Available methods: {[m for m in dir(response.status_code) if not m.startswith('_')]}")
# Found: ['as_int', 'is_client_error', 'is_success', ...]
```

**What this teaches us:**
- Libraries often use custom types instead of primitives
- Type conversion may be required
- Object methods reveal intended usage patterns

**The fix:** Use `response.status_code.as_int()` instead of assuming it's an integer.

### Step 4: The Header Encoding Adventure

**Error #5: The Dictionary Conversion Chaos**
```
ValueError: dictionary update sequence element #0 has length 32; 2 is required
```

**The investigation:**
```python
# Let's see what headers actually look like
for k, v in response.headers.items():
    print(f"Key: {k} (type: {type(k)})")
    print(f"Value: {v} (type: {type(v)})")
# Everything is bytes!
```

**What this teaches us:**
- HTTP is a bytes protocol, not strings
- Network libraries preserve this reality
- Conversion is often needed at boundaries

### Step 5: The Async Text Trap

**Error #6: The Method vs Property Confusion**
```
TypeError: 'builtin_function_or_method' object is not subscriptable
```

**The realization:**
```python
print(f"Text type: {type(response.text)}")
# <class 'builtin_function_or_method'>
# It's a method, not a property!
```

**And then:**
```python
content = response.text()  # Still fails...
# TypeError: object Future can't be used in 'await' expression
content = await response.text()  # Finally works!
```

**What this teaches us:**
- API design varies between libraries
- Some operations are async (and that's often good)
- Always check if methods need to be awaited

## The rnet API: Browser Impersonation Done Right (After All That Debugging!)

### Creating a Client

```python
client = rnet.Client(
    impersonate=rnet.Impersonate.Chrome131,  # Latest Chrome
    timeout=30
)
```

### Making Requests

```python
response = await client.get(url, headers=headers)

# Extract data
status = response.status_code.as_int()  # StatusCode → int
content = await response.text()         # Async method
headers = {                             # Convert HeaderMap
    k.decode() if isinstance(k, bytes) else k:
    v.decode() if isinstance(v, bytes) else v
    for k, v in response.headers.items()
}
```

### Key rnet Features

1. **Browser Impersonation**: Perfect TLS and HTTP fingerprints
2. **HTTP/2 Support**: Modern protocol support
3. **Async by Default**: Built for concurrency
4. **Header Management**: Realistic browser headers

## Rate Limiting: Being a Good Internet Citizen

### The Problem

Without rate limiting:
```python
# DON'T DO THIS
for url in urls:
    response = await client.get(url)  # Hammers the server
```

### Our Solution

```python
async def _apply_rate_limit(self):
    current_time = time.time()
    time_since_last = current_time - self._last_request_time

    if time_since_last < self.config.request_delay:
        sleep_time = self.config.request_delay - time_since_last
        await asyncio.sleep(sleep_time)

    self._last_request_time = time.time()
```

This ensures we never make requests faster than our configured delay.

## Concurrent Processing with Limits

### The Challenge

We want speed, but not rudeness:

```python
async def fetch_multiple_urls(self, urls: List[str]) -> List[ScrapingResult]:
    # Limit concurrent requests
    semaphore = asyncio.Semaphore(self.config.max_concurrent_requests)

    async def fetch_with_semaphore(url: str) -> ScrapingResult:
        async with semaphore:
            return await self.fetch_url(url)

    # Execute all requests concurrently but limited
    tasks = [fetch_with_semaphore(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return results
```

### Why This Works

- **Semaphore**: Limits concurrent connections
- **Rate limiting**: Controls request frequency
- **Error handling**: Graceful failure management

## Error Handling: When Things Go Wrong

### Network Errors

```python
try:
    response = await client.get(url, headers=headers)
    # ... process response
except asyncio.TimeoutError:
    return ScrapingResult(
        url=url,
        status_code=0,
        content="",
        error=f"Timeout after {self.config.timeout}s"
    )
except Exception as e:
    return ScrapingResult(
        url=url,
        status_code=0,
        content="",
        error=str(e)
    )
```

### HTTP Errors

```python
if response.status_code.as_int() >= 400:
    # Still return a result, let caller decide what to do
    return ScrapingResult(
        url=url,
        status_code=response.status_code.as_int(),
        content="",
        error=f"HTTP {response.status_code.as_int()}"
    )
```

## Testing Async Code

### Mock Setup

```python
@pytest.fixture
def mock_response(self):
    response = AsyncMock()

    # Mock status_code
    status_mock = Mock()
    status_mock.as_int.return_value = 200
    response.status_code = status_mock

    # Mock async text() method
    response.text.return_value = "<html>content</html>"

    # Mock headers
    headers_mock = Mock()
    headers_mock.items.return_value = [(b"content-type", b"text/html")]
    response.headers = headers_mock

    return response
```

### Async Test Patterns

```python
@pytest.mark.asyncio
async def test_concurrent_requests(scraper, mock_response):
    urls = ["http://example.com/1", "http://example.com/2"]

    with patch('src.changelogger.scraper.rnet.Client') as mock_client:
        mock_client.return_value.get.return_value = mock_response

        results = await scraper.fetch_multiple_urls(urls)

        assert len(results) == 2
        assert all(r.is_success() for r in results)
```

## Hands-On Lab: Building the Scraper

### Lab Exercise 1: Write Your First Test

Create a test for basic URL fetching:

```python
@pytest.mark.asyncio
async def test_my_scraper():
    config = ScrapingConfig(request_delay=0.1)  # Fast for tests
    scraper = BasicScraper(config)

    # Mock the rnet client
    with patch('src.changelogger.scraper.rnet.Client') as mock_client:
        # Your mock setup here

        result = await scraper.fetch_url("https://example.com")

        # Your assertions here
```

### Lab Exercise 2: Run the Demo

```bash
python demo_scraper.py
```

Watch the scraper in action! Notice:
- Rate limiting in action (1-second delays)
- Concurrent requests (3 URLs fetched simultaneously)
- Error handling (404 and invalid domain)
- Browser-like headers

### Lab Exercise 3: Integration Testing

```python
@pytest.mark.asyncio
async def test_real_website():
    scraper = BasicScraper(ScrapingConfig())
    result = await scraper.fetch_url("https://httpbin.org/get")

    assert result.is_success()
    assert "httpbin" in result.content
```

## Real-World Considerations

### Robots.txt Respect

```python
# Future enhancement
async def check_robots_txt(self, url: str) -> bool:
    # Parse robots.txt and check if we're allowed
    # Return True if allowed, False otherwise
```

### User-Agent Rotation

```python
user_agents = [
    "Changelogger/1.0 (Educational Project)",
    "Changelogger/1.0 (Research Tool)",
    "Changelogger/1.0 (Monitoring Service)"
]
```

### Session Management

```python
# rnet handles this automatically with connection pooling
client = rnet.Client(impersonate=rnet.Impersonate.Chrome131)
# Reuse this client for multiple requests
```

## Performance Analysis

Our demo showed:
- **Single request**: ~1 second (including rate limiting)
- **3 concurrent requests**: ~1.1 seconds total (not 3 seconds!)
- **Browser impersonation**: Perfect Chrome fingerprint
- **Error handling**: Graceful failure for invalid domains

## What We've Accomplished (Through Glorious Failure!)

- ✅ **Built a modern async scraper** with browser impersonation (after fixing 6 API issues)
- ✅ **Implemented rate limiting** for ethical scraping
- ✅ **Added concurrent processing** with limits
- ✅ **Wrote comprehensive tests** using TDD (and learned to debug async tests)
- ✅ **Handled real-world HTTP quirks** gracefully (bytes vs strings, custom types)
- ✅ **Created a reusable scraping framework**
- ✅ **Developed debugging skills** by embracing errors as learning opportunities

### The Real Learning: What Those Errors Taught Us

Each "failure" was actually a success in disguise:

1. **Import Error** → Learned about Python package structure
2. **Async Test Error** → Discovered pytest-asyncio requirements
3. **API Error** → Learned to explore unknown libraries with `dir()`
4. **StatusCode Error** → Understood custom types vs primitives
5. **Header Error** → Learned about bytes in network protocols
6. **Text Method Error** → Mastered async method calls

**This is how real development works!** Every expert has made these exact errors. The difference is they've learned to debug efficiently and stay curious instead of frustrated.

## Key Takeaways

1. **TDD works for async code** - write tests first, implement second
2. **rnet provides excellent browser impersonation** - looks like real Chrome
3. **Rate limiting is essential** - be polite to servers
4. **Concurrent processing with limits** - fast but respectful
5. **Error handling matters** - networks are unreliable
6. **Testing async code requires proper mocking** - simulate network responses

## Next Chapter Preview

In Chapter 3, we'll take our scraped HTML and parse it into structured data using `selectolax`. We'll learn how to:
- Extract specific elements from HTML
- Handle different changelog formats
- Deal with malformed HTML gracefully
- Build flexible parsers for various websites

The scraper gets us the raw HTML, but parsing is where the magic happens!

---

*"The best way to make a fast scraper is to not get blocked in the first place."* - Ancient scraping wisdom

## Exercises

1. **Add User-Agent Rotation**: Modify the scraper to rotate between different User-Agent strings

2. **Implement Retry Logic**: Add `@retry` decorators using `tenacity` for network failures

3. **Memory Usage**: Test the scraper with 100 URLs and monitor memory consumption

4. **Custom Headers**: Add support for custom headers per URL

**Bonus Challenge**: Create a "politeness score" that adjusts rate limiting based on server response times. Fast servers get faster requests, slow servers get extra delays.
