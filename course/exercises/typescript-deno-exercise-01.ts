#!/usr/bin/env -S deno run --allow-net --allow-read --allow-write

/**
 * TypeScript/Deno Exercise 01: Type-Safe Web Scraper
 * ==================================================
 * 
 * Learning Objectives:
 * - Practice TypeScript's type system
 * - Use Deno's built-in APIs
 * - Implement type-safe error handling
 * - Work with async/await patterns
 * 
 * Exercise Description:
 * Build a type-safe web scraper using TypeScript and Deno.
 * Focus on leveraging TypeScript's type system to catch errors
 * at compile time and Deno's security model.
 * 
 * Compare this with the Python equivalent:
 * ```python
 * class WebScraper:
 *     def scrape(self, url: str) -> dict:
 *         response = requests.get(url)
 *         return {"status": response.status_code, "content": response.text}
 * ```
 */

// TODO: Define interfaces for type safety
interface ScrapeResult {
    url: string;
    status: number;
    content: string;
    timestamp: Date;
    error?: string;
}

interface ScraperConfig {
    timeout?: number;
    headers?: Record<string, string>;
    retries?: number;
    rateLimit?: number; // requests per second
}

interface CacheEntry {
    result: ScrapeResult;
    expires: Date;
}

// TODO: Implement a type-safe Result type (like Rust)
type Result<T, E = Error> = 
    | { ok: true; value: T }
    | { ok: false; error: E };

// TODO: Create a WebScraper class with TypeScript features
class WebScraper {
    private config: Required<ScraperConfig>;
    private cache: Map<string, CacheEntry> = new Map();
    private lastRequestTime: number = 0;
    
    constructor(config: ScraperConfig = {}) {
        // TODO: Implement default config with type safety
        // Use the nullish coalescing operator (??)
        this.config = {
            timeout: 0, // Fix this
            headers: {}, // Fix this
            retries: 0, // Fix this
            rateLimit: 0, // Fix this
        };
    }
    
    /**
     * Scrape a URL with type-safe error handling
     * TODO: Implement this method
     */
    async scrape(url: string): Promise<Result<ScrapeResult>> {
        // Your implementation here
        // 1. Validate URL
        // 2. Check cache
        // 3. Apply rate limiting
        // 4. Make request with timeout
        // 5. Handle retries
        // 6. Return typed result
        
        return { ok: false, error: new Error("Not implemented") };
    }
    
    /**
     * Validate URL using TypeScript type guards
     * TODO: Implement this type guard
     */
    private isValidUrl(url: string): url is string {
        // Your implementation here
        return false;
    }
    
    /**
     * Check cache with proper typing
     * TODO: Implement cache checking
     */
    private checkCache(url: string): ScrapeResult | null {
        // Your implementation here
        return null;
    }
    
    /**
     * Apply rate limiting
     * TODO: Implement rate limiting logic
     */
    private async applyRateLimit(): Promise<void> {
        // Your implementation here
    }
    
    /**
     * Scrape multiple URLs concurrently with type safety
     * TODO: Implement concurrent scraping
     */
    async scrapeMultiple(urls: string[]): Promise<Result<ScrapeResult>[]> {
        // Your implementation here
        // Use Promise.all or Promise.allSettled
        return [];
    }
    
    /**
     * Get scraping statistics with proper typing
     */
    getStats(): {
        totalRequests: number;
        cachedRequests: number;
        failedRequests: number;
        averageResponseTime: number;
    } {
        // TODO: Implement statistics gathering
        return {
            totalRequests: 0,
            cachedRequests: 0,
            failedRequests: 0,
            averageResponseTime: 0,
        };
    }
}

// TODO: Implement a generic retry function with TypeScript
async function retry<T>(
    fn: () => Promise<T>,
    retries: number,
    delay: number = 1000
): Promise<T> {
    // Your implementation here
    // Use exponential backoff
    throw new Error("Not implemented");
}

// TODO: Create a type-safe HTML parser
interface ParsedData {
    title?: string;
    links: string[];
    images: string[];
    meta: Record<string, string>;
}

function parseHTML(html: string): ParsedData {
    // Simple regex-based parser for exercise
    // In production, use a proper HTML parser
    
    const data: ParsedData = {
        links: [],
        images: [],
        meta: {},
    };
    
    // TODO: Extract title
    // TODO: Extract links (href attributes)
    // TODO: Extract images (src attributes)
    // TODO: Extract meta tags
    
    return data;
}

// Exercise validation
async function validateImplementation() {
    console.log("TypeScript/Deno Exercise 01: Type-Safe Web Scraper");
    console.log("=".repeat(50));
    
    const scraper = new WebScraper({
        timeout: 5000,
        retries: 3,
        rateLimit: 2, // 2 requests per second
    });
    
    // Test 1: Single URL scraping
    console.log("\n1. Testing single URL scraping...");
    const result = await scraper.scrape("https://example.com");
    if (result.ok) {
        console.log("✅ Scraping successful:", result.value.status);
    } else {
        console.log("❌ Scraping failed:", result.error.message);
    }
    
    // Test 2: Invalid URL handling
    console.log("\n2. Testing invalid URL handling...");
    const invalidResult = await scraper.scrape("not-a-url");
    if (!invalidResult.ok) {
        console.log("✅ Invalid URL rejected correctly");
    }
    
    // Test 3: Concurrent scraping
    console.log("\n3. Testing concurrent scraping...");
    const urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net",
    ];
    const results = await scraper.scrapeMultiple(urls);
    const successful = results.filter(r => r.ok).length;
    console.log(`✅ Scraped ${successful}/${urls.length} URLs successfully`);
    
    // Test 4: Statistics
    console.log("\n4. Testing statistics...");
    const stats = scraper.getStats();
    console.log("📊 Stats:", stats);
}

// Additional exercises
function additionalChallenges() {
    console.log("\nAdditional Challenges:");
    console.log("1. Add Zod schema validation for scraped data");
    console.log("2. Implement streaming for large responses");
    console.log("3. Add WebSocket support for real-time scraping");
    console.log("4. Create a CLI with type-safe arguments");
    console.log("5. Export scraped data to different formats (JSON, CSV)");
    
    console.log("\nDeno-Specific Features to Try:");
    console.log("- Use Deno KV for persistent caching");
    console.log("- Implement permissions checking");
    console.log("- Create a web interface with Fresh");
    console.log("- Use Web Workers for parallel processing");
}

// Main execution
if (import.meta.main) {
    await validateImplementation();
    additionalChallenges();
}

// Export for testing
export { WebScraper, parseHTML, retry };
export type { ScrapeResult, ScraperConfig, Result };

/**
 * Key TypeScript/Deno Concepts:
 * 1. Interface definitions for type safety
 * 2. Generic types for reusable code
 * 3. Type guards for runtime validation
 * 4. Union types for error handling
 * 5. Async/await with proper typing
 * 6. Deno's permission model
 * 7. ES modules instead of CommonJS
 * 
 * Solution Hints:
 * - Use URL constructor for validation
 * - Leverage AbortController for timeouts
 * - Use fetch() API (built into Deno)
 * - Remember to handle all error cases
 * - Use const assertions for literal types
 * 
 * Expected Behavior:
 * - Type-safe throughout
 * - No any types
 * - Proper error handling
 * - Cache management
 * - Rate limiting
 */