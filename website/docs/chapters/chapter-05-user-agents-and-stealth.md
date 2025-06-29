# Chapter 5: User Agents and the Art of Not Looking Like a Bot
## *Or: How to Blend In Without Being Evil*

> "The first rule of web scraping is: Don't look like you're web scraping."
> "The second rule of web scraping is: You're always obviously web scraping."

Welcome to the chapter where we learn to be sneaky (but ethical) about our scraping activities. Because nothing gets you blocked faster than a user agent that says "HI I'M A ROBOT PLEASE BLOCK ME."

## The User Agent Problem

### What You're Currently Using (DON'T):
```python
user_agent = "Changelogger/1.0 (Educational Project)"
```

**What servers think when they see this:**
- "Oh look, a well-behaved educational bot!"
- "How refreshingly honest!"
- "Let me block this immediately."

### What You Should Consider Using:
```python
# Modern Chrome (what most humans actually use)
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

# Modern Firefox
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0"

# MacOS Safari
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
```

## The Ethics of User Agent Spoofing

### The Moral Spectrum:

**😇 Perfectly Ethical:**
- Using a normal browser user agent for legitimate research
- Identifying yourself honestly when scraping public data
- Following robots.txt and rate limits

**😐 Morally Gray:**
- Using a browser user agent to avoid bot detection
- Rotating user agents to appear like different users
- Being vague about your identity

**😈 Probably Evil:**
- Pretending to be a specific person
- Bypassing paywalls or authentication
- Ignoring robots.txt and rate limits
- Scraping private or copyrighted content

### Our Approach: Honest But Not Stupid

We'll use realistic browser user agents while still being ethical:

1. ✅ Use realistic user agents that don't scream "BOT"
2. ✅ Respect robots.txt and rate limits
3. ✅ Only scrape public information
4. ✅ Don't overload servers
5. ✅ Have a clear educational purpose

## Chapter 5.1: The Anatomy of a User Agent

### Decoding a Real User Agent:
```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
│           │                            │                  │                 │                    │
│           │                            │                  │                 │                    └─ Safari version (for compatibility)
│           │                            │                  │                 └─ Chrome version and build
│           │                            │                  └─ Rendering engine info
│           │                            └─ Architecture (64-bit x64)
│           └─ Operating system (Windows 10)
└─ Mozilla compatibility (historical reasons)
```

### Why It's So Complicated:
User agents are a mess of historical baggage. Every browser pretends to be every other browser for compatibility reasons. It's like a browser identity crisis that's lasted 30 years.

### What Bot Detection Systems Look For:
- **User agents that are too honest:** "MyBot/1.0"
- **User agents that are too old:** Internet Explorer 6
- **User agents that are obviously fake:** "NotABot/1.0 (Definitely Human)"
- **Missing or inconsistent headers:** User agent says Chrome but no Chrome headers
- **Request patterns:** Too fast, too regular, too perfect

## Chapter 5.2: Realistic User Agent Strategy

### Strategy 1: Use Current Browser Versions
```python
# Good: Current Chrome (as of late 2024)
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

# Bad: Ancient browser
user_agent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
```

### Strategy 2: Match Your Headers to Your User Agent
```python
# If you claim to be Chrome, send Chrome-like headers
chrome_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Ch-Ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Upgrade-Insecure-Requests": "1"
}
```

### Strategy 3: Rotate User Agents (Advanced)
```python
# Pool of realistic user agents
user_agent_pool = [
    # Windows Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    # Windows Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
    # MacOS Chrome
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    # MacOS Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
]

# Use different user agent for each request
import random
user_agent = random.choice(user_agent_pool)
```

## Chapter 5.3: Updating Our Scraper Configuration

Let's update our configuration to use realistic user agents:

### Update .env File:
```bash
# OLD (obviously a bot):
USER_AGENT=Changelogger/1.0 (Educational Project)

# NEW (realistic browser):
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36

# Or use environment-specific:
# Windows user:
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36

# Mac user:
USER_AGENT=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36

# Linux user:
USER_AGENT=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
```

### Update ScrapingConfig:
```python
@dataclass
class ScrapingConfig:
    """Configuration for web scraping operations."""

    # Use realistic browser user agent by default
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    request_delay: float = 1.0
    max_concurrent_requests: int = 5
    timeout: int = 30
    respect_robots_txt: bool = True
```

## Chapter 5.4: Testing User Agent Effectiveness

### Test 1: What Headers Are We Actually Sending?
```python
async def test_our_headers():
    """Test what headers our scraper actually sends."""

    config = ScrapingConfig()
    scraper = BasicScraper(config)

    # httpbin.org/headers shows us exactly what we sent
    result = await scraper.fetch_url("https://httpbin.org/headers")

    if result.is_success():
        response_data = json.loads(result.content)
        sent_headers = response_data["headers"]

        print("📤 Headers we actually sent:")
        for header, value in sent_headers.items():
            print(f"   {header}: {value}")

        # Check if we look like a real browser
        user_agent = sent_headers.get("User-Agent", "")
        if "Chrome" in user_agent and "Mozilla" in user_agent:
            print("✅ User agent looks realistic!")
        else:
            print("⚠️ User agent might look suspicious")
```

### Test 2: Bot Detection Reality Check
```python
async def test_bot_detection():
    """Test against various bot detection mechanisms."""

    config = ScrapingConfig()
    scraper = BasicScraper(config)

    # Test sites with different levels of bot detection
    test_sites = [
        ("Basic site", "https://httpbin.org/get"),
        ("Headers check", "https://httpbin.org/headers"),
        ("User agent check", "https://httpbin.org/user-agent"),
    ]

    for site_name, url in test_sites:
        print(f"🧪 Testing {site_name}: {url}")

        result = await scraper.fetch_url(url)

        if result.is_success():
            print(f"   ✅ Success: {result.status_code}")
        else:
            print(f"   ❌ Failed: {result.status_code} - {result.error}")

        # Small delay to be polite
        await asyncio.sleep(1)
```

## Chapter 5.5: Advanced Stealth Techniques

### Technique 1: Request Timing Variation
```python
import random

async def human_like_delay():
    """Add human-like variation to request timing."""

    # Humans don't make requests at exact intervals
    base_delay = 2.0
    variation = random.uniform(-0.5, 1.0)  # ±0.5 to +1.0 seconds
    actual_delay = max(0.1, base_delay + variation)

    await asyncio.sleep(actual_delay)
```

### Technique 2: Realistic Browser Behavior
```python
# Browsers send lots of headers - we should too
realistic_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",  # Do Not Track
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0"
}
```

### Technique 3: Session Management
```python
# Use sessions like a real browser
async def scrape_with_session():
    """Scrape multiple pages with a persistent session."""

    # Real browsers maintain sessions across requests
    scraper = BasicScraper(ScrapingConfig())

    # Start with a "landing page" visit
    await scraper.fetch_url("https://example.com")
    await asyncio.sleep(2)  # Human reading time

    # Then visit the actual page we want
    result = await scraper.fetch_url("https://example.com/data")

    return result
```

## Chapter 5.6: When User Agents Aren't Enough

### Red Flags That Give You Away:
1. **Perfect timing:** Requests every exactly 1.000 seconds
2. **No JavaScript:** Missing JS-generated headers/cookies
3. **No images/CSS:** Only requesting HTML, not assets
4. **Perfect behavior:** Never mistyping URLs or following redirects
5. **Superhuman speed:** Reading pages faster than humanly possible

### Advanced Bot Detection Methods:
- **TLS fingerprinting:** Your HTTP library's TLS signature
- **JavaScript challenges:** Requiring JS execution to get content
- **Canvas fingerprinting:** Browser rendering differences
- **Behavioral analysis:** Mouse movements, click patterns
- **IP reputation:** Known bot hosting providers

### When You Need More Than User Agents:
If simple user agent changes don't work, you might need:
- **Browser automation:** Selenium, Playwright
- **Residential proxies:** Different IP addresses
- **JavaScript execution:** Full browser engines
- **CAPTCHA solving:** (ethically questionable territory)

## Chapter 5.7: The Ethical Framework

### Questions to Ask Yourself:
1. **Is this data public?** If it requires login, reconsider
2. **Are you respecting robots.txt?** Basic courtesy
3. **Are you overwhelming the server?** Rate limit appropriately
4. **Do you have permission?** When in doubt, ask
5. **Is this legal in your jurisdiction?** Check local laws
6. **Would you be comfortable explaining this to the site owner?** Gut check

### Ethical User Agent Guidelines:
- ✅ Use realistic user agents for public data scraping
- ✅ Identify yourself when directly asked
- ✅ Respect rate limits and robots.txt
- ✅ Don't pretend to be a specific person
- ❌ Don't bypass authentication or paywalls
- ❌ Don't scrape private or copyrighted content
- ❌ Don't overload servers or cause disruption

## Chapter 5.8: Practical Exercise

Let's update your actual configuration:

### Step 1: Create a Better .env File
```bash
# Copy the example and customize it
cp config/.env.example .env

# Edit .env with realistic settings
nano .env  # or your preferred editor
```

### Step 2: Choose Your User Agent
Pick one that matches your actual system:

```bash
# Windows users:
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

# Mac users:
USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

# Linux users:
USER_AGENT="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
```

### Step 3: Test the Changes
```python
# Run this to test your new user agent
async def test_new_user_agent():
    config = ScrapingConfig()  # Will load from .env
    scraper = BasicScraper(config)

    result = await scraper.fetch_url("https://httpbin.org/headers")

    if result.is_success():
        data = json.loads(result.content)
        user_agent = data["headers"]["User-Agent"]
        print(f"New user agent: {user_agent}")

        if "Chrome" in user_agent and len(user_agent) > 100:
            print("✅ Looks like a real browser!")
        else:
            print("⚠️ Might still look suspicious")
```

## Chapter Summary: Stealth vs. Ethics

What we learned:

1. **User agents matter** - "Bot/1.0" gets you blocked instantly
2. **Realistic is better** - Current browser user agents work best
3. **Consistency matters** - Match your headers to your user agent
4. **Timing matters** - Don't be too perfect or too fast
5. **Ethics still apply** - Stealth doesn't mean evil
6. **Detection is evolving** - User agents are just the beginning
7. **When in doubt, ask** - Permission beats stealth

### The User Agent Paradox:
- **Too honest:** "Educational Bot" → Blocked
- **Too fake:** "NotABot/1.0" → Blocked
- **Just right:** "Realistic browser" → Works (usually)

Remember: The goal isn't to be sneaky, it's to not accidentally trigger bot detection while doing legitimate research.

---

## Next Chapter Preview

In Chapter 6, we'll add HTML parsing with selectolax, where we'll discover:
- CSS selectors that work in browsers but not in scrapers
- The joy of malformed HTML
- Character encoding adventures
- Why websites hate you personally
- The eternal question: "Where did my `<div>` go?"

Plus, we'll learn to test HTML parsing without wanting to throw our computers out the window!

---

*"The best user agent is the one that doesn't make servers suspicious while you're doing perfectly legitimate research."* - Every Ethical Scraper

*"There's a fine line between being sneaky and being respectful. That line is usually in the robots.txt file."* - Web Scraping Wisdom
