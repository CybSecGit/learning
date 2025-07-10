# Modern Web Scraping with rnet
## *The Art of Digital Camouflage and Polite Data Extraction*

Web scraping in the 2020s is like being a spy in a world where everyone has motion detectors. The naive approach of "just grab the HTML" stopped working when websites started treating bots like uninvited party crashers. Modern scraping requires finesse, patience, and the right tools.

## The Evolution of Web Scraping

### The Stone Age (Pre-2010)
```python
import urllib2
html = urllib2.urlopen("http://example.com").read()
# Worked great until it didn't
```

### The Bronze Age (2010-2020)
```python
import requests
response = requests.get("https://example.com", headers={'User-Agent': 'Mozilla/5.0'})
# Better, but still obviously a bot
```

### The Modern Era (2020+)
```python
import rnet
client = rnet.Client(impersonate=rnet.Impersonate.Chrome131)
# TLS fingerprinting, HTTP/2, the works
```

## Why Traditional Scraping Fails

Modern websites employ increasingly sophisticated bot detection:

1. **TLS Fingerprinting**: Your SSL handshake reveals you're not a browser
2. **HTTP/2 Implementation Details**: Browsers have specific HTTP/2 behaviors
3. **JavaScript Challenges**: "Prove you're human by solving this puzzle"
4. **Behavioral Analysis**: "Real users don't request 1000 pages in 10 seconds"
5. **IP Reputation**: "This datacenter IP is definitely not grandma checking recipes"

## Enter rnet: Browser Impersonation Done Right

rnet is a Rust-based HTTP client that impersonates browsers at the protocol level. It's like wearing a perfect disguise instead of a fake mustache.

### The Impersonation Stack

```python
# Traditional approach (obvious fake mustache)
headers = {'User-Agent': 'Mozilla/5.0...'}

# rnet approach (complete identity theft)
client = rnet.Client(
    impersonate=rnet.Impersonate.Chrome131,
    timeout=30
)
```

rnet handles:
- **TLS Fingerprint**: Matches exact Chrome implementation
- **HTTP/2 Settings**: Frame priorities, window sizes, etc.
- **Header Order**: Chrome sends headers in specific order
- **Cipher Suites**: Exact match to browser preferences

## Understanding the rnet API Through Trial and Error

Let's explore rnet's API the way developers actually learn—by making mistakes and fixing them.

### Discovery Phase: What Does rnet Actually Have?

```python
import rnet

# First instinct: Look for AsyncClient (spoiler: it doesn't exist)
print(dir(rnet))
# Output: ['Client', 'BlockingClient', 'Impersonate', 'Response', ...]

# Lesson learned: Always explore the API
help(rnet.Client)
```

### The Status Code Surprise

```python
# What you expect:
if response.status_code == 200:
    print("Success!")

# What actually happens:
# TypeError: unsupported operand type(s) for ==: 'StatusCode' and 'int'

# The investigation:
print(type(response.status_code))  # <class 'rnet.StatusCode'>
print(dir(response.status_code))   # ['as_int', 'is_success', ...]

# The solution:
if response.status_code.as_int() == 200:
    print("Success!")
# Or better:
if response.status_code.is_success():
    print("Success!")
```

### The Async Text Method

```python
# Natural assumption:
content = response.text  # Nope, it's a method

# Second attempt:
content = response.text()  # Still nope, it's async

# Final form:
content = await response.text()  # Victory!
```

### Headers: The Bytes vs Strings Saga

```python
# Headers come as bytes because HTTP is a binary protocol
for key, value in response.headers.items():
    print(f"{key}: {value}")
    # Output: b'content-type': b'text/html'

# Converting to a civilized dictionary:
headers = {
    k.decode() if isinstance(k, bytes) else k:
    v.decode() if isinstance(v, bytes) else v
    for k, v in response.headers.items()
}
```

## Building a Polite Web Scraper

### Core Design Principles

1. **Rate Limiting**: Don't be that person who rings the doorbell 100 times
2. **Concurrent Limits**: Multiple polite requests, not a DDoS attack
3. **Error Handling**: Networks fail, servers hiccup, life goes on
4. **Respect robots.txt**: It's not legally binding, but it's polite

### The Configuration Object

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class ScraperConfig:
    """Configuration for polite web scraping."""
    user_agent: str = "PoliteBot/1.0 (https://example.com/bot-info)"
    request_delay: float = 1.0  # Seconds between requests
    max_concurrent: int = 3     # Parallel requests limit
    timeout: int = 30           # Request timeout
    retry_count: int = 3        # Retry failed requests
    respect_robots: bool = True # Follow robots.txt
```

### The Result Object

```python
@dataclass
class ScrapeResult:
    """Result of a scraping attempt."""
    url: str
    status_code: int
    content: str
    headers: dict
    response_time: float
    error: Optional[str] = None
    
    def is_success(self) -> bool:
        """Check if the scrape was successful."""
        return 200 <= self.status_code < 300 and self.error is None
```

### Rate Limiting Implementation

```python
import asyncio
import time

class PoliteScraper:
    def __init__(self, config: ScraperConfig):
        self.config = config
        self._last_request_time = 0
        self._request_lock = asyncio.Lock()
    
    async def _enforce_rate_limit(self):
        """Ensure we don't exceed rate limits."""
        async with self._request_lock:
            elapsed = time.time() - self._last_request_time
            if elapsed < self.config.request_delay:
                await asyncio.sleep(self.config.request_delay - elapsed)
            self._last_request_time = time.time()
```

### Concurrent Request Management

```python
async def fetch_multiple(self, urls: list[str]) -> list[ScrapeResult]:
    """Fetch multiple URLs concurrently with limits."""
    semaphore = asyncio.Semaphore(self.config.max_concurrent)
    
    async def fetch_with_limit(url: str) -> ScrapeResult:
        async with semaphore:
            await self._enforce_rate_limit()
            return await self.fetch_one(url)
    
    tasks = [fetch_with_limit(url) for url in urls]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

### The Complete Scraper

```python
import asyncio
import time
from typing import Optional
import rnet

class ModernScraper:
    def __init__(self, config: ScraperConfig):
        self.config = config
        self.client = rnet.Client(
            impersonate=rnet.Impersonate.Chrome131,
            timeout=config.timeout
        )
        self._last_request_time = 0
        self._request_lock = asyncio.Lock()
    
    async def fetch(self, url: str) -> ScrapeResult:
        """Fetch a single URL politely."""
        start_time = time.time()
        
        try:
            # Rate limiting
            await self._enforce_rate_limit()
            
            # Make the request
            response = await self.client.get(url, headers={
                'User-Agent': self.config.user_agent,
                'Accept': 'text/html,application/xhtml+xml',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            })
            
            # Extract response data
            status = response.status_code.as_int()
            content = await response.text()
            headers = self._convert_headers(response.headers)
            
            return ScrapeResult(
                url=url,
                status_code=status,
                content=content,
                headers=headers,
                response_time=time.time() - start_time
            )
            
        except asyncio.TimeoutError:
            return ScrapeResult(
                url=url,
                status_code=0,
                content="",
                headers={},
                response_time=time.time() - start_time,
                error=f"Timeout after {self.config.timeout}s"
            )
        except Exception as e:
            return ScrapeResult(
                url=url,
                status_code=0,
                content="",
                headers={},
                response_time=time.time() - start_time,
                error=str(e)
            )
    
    def _convert_headers(self, headers) -> dict:
        """Convert rnet headers to dictionary."""
        return {
            k.decode() if isinstance(k, bytes) else str(k):
            v.decode() if isinstance(v, bytes) else str(v)
            for k, v in headers.items()
        }
```

## Testing Async Scrapers

Testing async code requires special considerations. Here's how to do it right:

### Basic Async Test Setup

```python
import pytest
import asyncio
from unittest.mock import AsyncMock, Mock, patch

@pytest.mark.asyncio
async def test_basic_fetch():
    """Test basic URL fetching."""
    config = ScraperConfig(request_delay=0.1)  # Fast for tests
    scraper = ModernScraper(config)
    
    # Mock the rnet client
    with patch.object(scraper, 'client') as mock_client:
        # Create mock response
        mock_response = AsyncMock()
        mock_response.status_code.as_int.return_value = 200
        mock_response.text.return_value = "<html>Test</html>"
        mock_response.headers.items.return_value = [
            (b'content-type', b'text/html')
        ]
        
        mock_client.get.return_value = mock_response
        
        # Test the fetch
        result = await scraper.fetch("https://example.com")
        
        assert result.is_success()
        assert result.status_code == 200
        assert "<html>Test</html>" in result.content
```

### Testing Rate Limiting

```python
@pytest.mark.asyncio
async def test_rate_limiting():
    """Ensure rate limiting works."""
    config = ScraperConfig(request_delay=0.5)
    scraper = ModernScraper(config)
    
    with patch.object(scraper, 'client') as mock_client:
        mock_client.get.return_value = create_mock_response()
        
        # Time two sequential requests
        start = time.time()
        await scraper.fetch("https://example.com/1")
        await scraper.fetch("https://example.com/2")
        elapsed = time.time() - start
        
        # Should take at least 0.5 seconds
        assert elapsed >= 0.5
```

### Testing Concurrent Limits

```python
@pytest.mark.asyncio
async def test_concurrent_limits():
    """Test concurrent request limiting."""
    config = ScraperConfig(
        request_delay=0.1,
        max_concurrent=2
    )
    scraper = ModernScraper(config)
    
    urls = [f"https://example.com/{i}" for i in range(5)]
    
    # Track concurrent requests
    concurrent_count = 0
    max_concurrent = 0
    
    async def mock_get(*args, **kwargs):
        nonlocal concurrent_count, max_concurrent
        concurrent_count += 1
        max_concurrent = max(max_concurrent, concurrent_count)
        await asyncio.sleep(0.2)  # Simulate network delay
        concurrent_count -= 1
        return create_mock_response()
    
    with patch.object(scraper.client, 'get', side_effect=mock_get):
        await scraper.fetch_multiple(urls)
        
    # Should never exceed configured limit
    assert max_concurrent <= 2
```

## Real-World Scraping Patterns

### Handling JavaScript-Heavy Sites

While rnet excels at protocol-level impersonation, some sites require JavaScript execution:

```python
# For JS-heavy sites, consider:
# 1. Find the API endpoints (often easier to scrape)
# 2. Use Playwright/Selenium for full browser automation
# 3. Look for static data in <script> tags

# Example: Finding JSON data in script tags
import json
import re

def extract_json_from_script(html: str, pattern: str) -> dict:
    """Extract JSON data from script tags."""
    match = re.search(pattern, html, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    return {}
```

### Session Management

```python
class SessionScraper(ModernScraper):
    """Scraper with session management."""
    
    async def login(self, username: str, password: str) -> bool:
        """Perform login and store session."""
        response = await self.fetch("https://example.com/login", data={
            'username': username,
            'password': password
        })
        
        # Session cookies are automatically stored by rnet
        return response.is_success()
    
    async def fetch_authenticated(self, url: str) -> ScrapeResult:
        """Fetch URL using stored session."""
        # rnet maintains cookies automatically
        return await self.fetch(url)
```

### Retry Logic with Exponential Backoff

```python
from tenacity import retry, stop_after_attempt, wait_exponential

class ResilientScraper(ModernScraper):
    """Scraper with automatic retry logic."""
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def fetch_with_retry(self, url: str) -> ScrapeResult:
        """Fetch with automatic retry on failure."""
        result = await self.fetch(url)
        
        # Retry on server errors
        if 500 <= result.status_code < 600:
            raise Exception(f"Server error: {result.status_code}")
            
        return result
```

## Performance Optimization

### Connection Pooling

```python
# rnet handles connection pooling automatically
# Reuse the same client instance for multiple requests
scraper = ModernScraper(config)

# Good: Reuses connections
for url in urls:
    await scraper.fetch(url)

# Bad: Creates new connections each time
for url in urls:
    scraper = ModernScraper(config)  # Don't do this
    await scraper.fetch(url)
```

### Memory Management for Large Scrapes

```python
async def scrape_large_dataset(urls: list[str], batch_size: int = 100):
    """Scrape large datasets in batches to manage memory."""
    scraper = ModernScraper(ScraperConfig())
    
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i + batch_size]
        results = await scraper.fetch_multiple(batch)
        
        # Process and save results immediately
        for result in results:
            if result.is_success():
                # Save to database/file
                await save_result(result)
        
        # Results go out of scope, memory is freed
```

## Ethical Scraping Guidelines

### The Golden Rules

1. **Check robots.txt**: Respect the site's scraping preferences
2. **Identify yourself**: Use a descriptive User-Agent with contact info
3. **Rate limit**: No site appreciates being hammered
4. **Cache responses**: Don't re-scrape unchanged data
5. **Handle errors gracefully**: Don't retry failed requests endlessly

### Implementing robots.txt Checking

```python
from urllib.robotparser import RobotFileParser

class EthicalScraper(ModernScraper):
    def __init__(self, config: ScraperConfig):
        super().__init__(config)
        self._robots_cache = {}
    
    async def can_fetch(self, url: str) -> bool:
        """Check if URL can be fetched according to robots.txt."""
        if not self.config.respect_robots:
            return True
            
        from urllib.parse import urlparse
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        if robots_url not in self._robots_cache:
            # Fetch and parse robots.txt
            rp = RobotFileParser()
            rp.set_url(robots_url)
            
            result = await self.fetch(robots_url)
            if result.is_success():
                rp.parse(result.content.splitlines())
            
            self._robots_cache[robots_url] = rp
        
        return self._robots_cache[robots_url].can_fetch(
            self.config.user_agent, url
        )
```

## Common Pitfalls and Solutions

### The Cloudflare Wall
**Problem**: "Checking your browser" infinite loop  
**Solution**: Use undetected-chromedriver or Playwright with stealth plugin

### The Rate Limit Ban
**Problem**: 429 Too Many Requests after 10 requests  
**Solution**: Exponential backoff, respect Retry-After headers

### The Honeypot Trap
**Problem**: Hidden links that only bots would follow  
**Solution**: Parse visibility, don't follow display:none links

### The Session Timeout
**Problem**: Login expires mid-scrape  
**Solution**: Implement session refresh logic, monitor auth status

## Advanced Techniques

### Distributed Scraping

```python
# Using Redis for distributed rate limiting
import redis
import asyncio

class DistributedScraper(ModernScraper):
    def __init__(self, config: ScraperConfig, redis_url: str):
        super().__init__(config)
        self.redis = redis.from_url(redis_url)
    
    async def _enforce_rate_limit(self):
        """Distributed rate limiting using Redis."""
        key = f"scraper:last_request:{self.config.user_agent}"
        
        while True:
            last_request = self.redis.get(key)
            now = time.time()
            
            if not last_request:
                self.redis.setex(key, 60, str(now))
                break
                
            elapsed = now - float(last_request)
            if elapsed >= self.config.request_delay:
                self.redis.setex(key, 60, str(now))
                break
                
            await asyncio.sleep(self.config.request_delay - elapsed)
```

### Proxy Rotation

```python
class ProxyScraper(ModernScraper):
    def __init__(self, config: ScraperConfig, proxies: list[str]):
        super().__init__(config)
        self.proxies = proxies
        self._proxy_index = 0
    
    async def fetch(self, url: str) -> ScrapeResult:
        """Fetch using rotating proxies."""
        proxy = self.proxies[self._proxy_index]
        self._proxy_index = (self._proxy_index + 1) % len(self.proxies)
        
        # Note: rnet proxy support varies by version
        # This is pseudocode for the concept
        client = rnet.Client(
            impersonate=rnet.Impersonate.Chrome131,
            proxy=proxy
        )
        
        # ... rest of fetch logic
```

## Debugging Real Scraping Issues

### The Request Inspector

```python
class DebugScraper(ModernScraper):
    async def fetch(self, url: str) -> ScrapeResult:
        """Fetch with detailed debugging."""
        print(f"🔍 Fetching: {url}")
        print(f"⏱️  Rate limit delay: {self.config.request_delay}s")
        
        result = await super().fetch(url)
        
        print(f"📊 Status: {result.status_code}")
        print(f"⏱️  Response time: {result.response_time:.2f}s")
        print(f"📦 Content length: {len(result.content)}")
        
        if result.error:
            print(f"❌ Error: {result.error}")
        else:
            print(f"✅ Success!")
            
        return result
```

### Response Analysis

```python
def analyze_response(result: ScrapeResult):
    """Analyze scraping response for issues."""
    indicators = {
        'cloudflare': 'Checking your browser',
        'rate_limit': '429 Too Many Requests',
        'bot_detection': 'detected unusual activity',
        'captcha': 'Please complete the security check',
        'login_required': 'Please sign in',
        'geo_blocked': 'not available in your country'
    }
    
    for key, indicator in indicators.items():
        if indicator.lower() in result.content.lower():
            print(f"⚠️  Detected: {key}")
            return key
            
    return None
```

## Conclusion

Modern web scraping is an arms race between scrapers and anti-bot systems. The key to success is not trying to break down the door, but rather knocking politely and looking like you belong. rnet provides the perfect disguise, but it's up to you to act the part.

Remember: With great scraping power comes great responsibility. The sites you scrape are someone's servers, bandwidth, and money. Scrape responsibly, cache aggressively, and always ask yourself: "Would I be okay if someone scraped my site like this?"

---

*"The best scraper is indistinguishable from a regular user."* - Ancient web scraping proverb (coined last Tuesday)

## Practical Exercises

1. **Build a Polite Scraper**: Create a scraper that respects robots.txt, implements exponential backoff on errors, and identifies itself properly. Test it on your own website first.

2. **Performance Challenge**: Scrape 1000 URLs while maintaining a 1-second rate limit. Optimize to complete in under 6 minutes (hint: concurrency is your friend).

3. **Detection Evasion**: Set up a test site with basic bot detection (User-Agent checking, rate limiting). Build a scraper that bypasses it ethically.

4. **Memory Profiler**: Create a scraper that processes 10,000 URLs without exceeding 100MB of memory usage. Use generators and streaming where possible.

5. **The Ultimate Test**: Build a scraper for a site you actually need data from. Handle all edge cases, errors, and implement proper monitoring. Deploy it to production (with the site owner's permission).