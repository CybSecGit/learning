package main

/*
Go Exercise 01: From Python to Go - Basic Syntax and Types
=========================================================

Learning Objectives:
- Translate Python concepts to Go syntax
- Understand Go's type system
- Practice error handling without exceptions
- Learn Go's approach to functions and methods

Exercise Description:
You're converting a Python web scraper utility to Go. This exercise
focuses on translating Python patterns to idiomatic Go code.

Python Code to Translate:
```python
class WebScraper:
    def __init__(self, base_url, timeout=30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.scraped_urls = set()
    
    def scrape_page(self, path):
        url = self.base_url + path
        if url in self.scraped_urls:
            return None, "Already scraped"
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            self.scraped_urls.add(url)
            return response.text, None
        except requests.RequestException as e:
            return None, str(e)
    
    def extract_links(self, html):
        # Extract all links from HTML
        links = []
        # ... parsing logic ...
        return links
```
*/

import (
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"
)

// TODO: Define the WebScraper struct
// Hint: Go doesn't have classes, use a struct
// Remember: Go doesn't have sets, consider using map[string]bool
type WebScraper struct {
	// Your fields here
}

// TODO: Create a constructor function (Go doesn't have __init__)
// Convention: Name it NewWebScraper
// Return (*WebScraper, error) to handle initialization errors
func NewWebScraper(baseURL string, timeout int) (*WebScraper, error) {
	// Your implementation here
	// Validate the baseURL
	// Create HTTP client with timeout
	// Initialize the scraped URLs map
	return nil, nil
}

// TODO: Implement ScrapePage method
// Note: Go methods are defined outside the struct
// Return (string, error) instead of using exceptions
func (ws *WebScraper) ScrapePage(path string) (string, error) {
	// Your implementation here
	// 1. Build full URL
	// 2. Check if already scraped
	// 3. Make HTTP request
	// 4. Read response body
	// 5. Mark URL as scraped
	// 6. Return content or error
	return "", nil
}

// TODO: Implement ExtractLinks method
// Parse HTML and extract all href links
func (ws *WebScraper) ExtractLinks(html string) []string {
	// Your implementation here
	// Simple implementation: find all href=" patterns
	// In real code, use golang.org/x/net/html package
	links := []string{}
	return links
}

// TODO: Implement a method to get scraping statistics
func (ws *WebScraper) GetStats() map[string]interface{} {
	// Return a map with:
	// - "total_scraped": number of scraped URLs
	// - "base_url": the base URL
	// - "timeout_seconds": timeout in seconds
	stats := make(map[string]interface{})
	return stats
}

// Helper function to validate URL
func isValidURL(url string) bool {
	// Simple validation - starts with http:// or https://
	return strings.HasPrefix(url, "http://") || strings.HasPrefix(url, "https://")
}

// Exercise validation functions
func validateScraper(ws *WebScraper) {
	fmt.Println("Validating WebScraper implementation...")
	
	// Test 1: Check if struct has required fields
	if ws == nil {
		fmt.Println("❌ WebScraper is nil")
		return
	}
	
	// Test 2: Try scraping a page
	content, err := ws.ScrapePage("/test")
	if err != nil {
		fmt.Printf("⚠️  Scraping returned error: %v\n", err)
	} else if content != "" {
		fmt.Println("✅ ScrapePage method implemented")
	}
	
	// Test 3: Check stats
	stats := ws.GetStats()
	if len(stats) > 0 {
		fmt.Println("✅ GetStats method implemented")
		fmt.Printf("   Stats: %+v\n", stats)
	}
}

func main() {
	fmt.Println("Go Exercise 01: From Python to Go")
	fmt.Println("==================================")
	
	// Test your implementation
	scraper, err := NewWebScraper("https://example.com", 30)
	if err != nil {
		fmt.Printf("Error creating scraper: %v\n", err)
		return
	}
	
	// Validate the implementation
	validateScraper(scraper)
	
	// Additional exercises
	fmt.Println("\nAdditional Challenges:")
	fmt.Println("1. Add retry logic with exponential backoff")
	fmt.Println("2. Implement concurrent scraping with goroutines")
	fmt.Println("3. Add rate limiting to prevent overwhelming servers")
	fmt.Println("4. Create a channel-based progress reporter")
	fmt.Println("5. Implement graceful shutdown with context")
	
	// Example of Go-specific patterns to try
	fmt.Println("\nGo Patterns to Explore:")
	fmt.Println("- Use channels for communication between goroutines")
	fmt.Println("- Implement the Worker Pool pattern")
	fmt.Println("- Use context for cancellation")
	fmt.Println("- Apply the functional options pattern")
}

/*
Key Differences from Python:
1. No classes - use structs and methods
2. No __init__ - use NewXXX constructor functions
3. No exceptions - return errors explicitly
4. No sets - use map[string]bool
5. Explicit error handling required
6. Methods defined outside struct
7. Public vs private: Capitalized = public

Solution Hints:
- Use http.Client with Timeout field
- Check errors immediately after function calls
- Use defer to ensure resources are cleaned up
- Consider using sync.Map for thread-safe scraped URLs
- Remember to close response bodies

Expected Output:
A working WebScraper that:
- Validates URLs before scraping
- Tracks scraped URLs to avoid duplicates
- Handles errors gracefully
- Returns proper statistics
*/