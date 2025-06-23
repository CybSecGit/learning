#!/usr/bin/env python3
"""
Testing Workshop: "Learn to Test by Testing Terribly First"

This script demonstrates different testing approaches with our scraper,
showing both good and bad testing practices. Because the best way to
learn good testing is to see how bad testing fails spectacularly.

Educational Philosophy:
- Show bad tests first (they're more entertaining)
- Explain why they're bad
- Show good tests that actually work
- Make testing less intimidating through humor
"""

from __future__ import annotations

import asyncio
import json
import sys
import time
from pathlib import Path
from unittest.mock import AsyncMock, patch

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from changelogger.scraper import BasicScraper, ScrapingConfig, ScrapingResult


class TestingWorkshop:
    """A workshop to learn testing through trial and error (mostly error)."""

    def __init__(self):
        self.demo_count = 0
        self.passed_tests = 0
        self.failed_tests = 0

    def run_demo(self, name, description, demo_func):
        """Run a testing demo with educational commentary."""
        self.demo_count += 1

        print(f"🧪 Demo {self.demo_count}: {name}")
        print("-" * 60)
        print(f"📝 What we're demonstrating: {description}")
        print()

        try:
            demo_func()
            print("✅ Demo completed successfully!")
            self.passed_tests += 1
        except Exception as e:
            print(f"💥 Demo failed: {e}")
            print("💡 This might be intentional for educational purposes!")
            self.failed_tests += 1

        print("\n" + "=" * 70 + "\n")

    async def run_async_demo(self, name, description, demo_func):
        """Run an async testing demo."""
        self.demo_count += 1

        print(f"🧪 Demo {self.demo_count}: {name}")
        print("-" * 60)
        print(f"📝 What we're demonstrating: {description}")
        print()

        try:
            await demo_func()
            print("✅ Demo completed successfully!")
            self.passed_tests += 1
        except Exception as e:
            print(f"💥 Demo failed: {e}")
            print("💡 This might be intentional for educational purposes!")
            self.failed_tests += 1

        print("\n" + "=" * 70 + "\n")


def demo_bad_test_examples():
    """Demonstrate terrible testing practices (don't do these)."""

    print("🚫 BAD TEST EXAMPLE 1: Testing the Framework")
    print("This test verifies that Python dictionaries work (spoiler: they do)")

    def test_python_dict_works():
        """Test that Python dictionaries work."""
        d = {"key": "value"}
        assert d["key"] == "value"
        return True

    result = test_python_dict_works()
    print(f"   Result: {result}")
    print("   🤔 Why this is bad: You're testing Python, not your code!")
    print()

    print("🚫 BAD TEST EXAMPLE 2: Testing Implementation Details")
    print("This test breaks every time you refactor")

    def test_scraper_calls_specific_method():
        """Test that our scraper calls a specific internal method."""
        config = ScrapingConfig()
        scraper = BasicScraper(config)

        # Testing HOW it works, not WHAT it does
        assert hasattr(scraper, "config")
        assert scraper.config == config
        return True

    result = test_scraper_calls_specific_method()
    print(f"   Result: {result}")
    print("   🤔 Why this is bad: Changes if you rename variables or refactor!")
    print()

    print("🚫 BAD TEST EXAMPLE 3: Happy Path Only")
    print("This test only works when everything is perfect")

    def test_perfect_world():
        """Test that everything works in a perfect world."""
        # Only test the case where everything works perfectly
        config = ScrapingConfig()
        scraper = BasicScraper(config)
        assert scraper is not None
        return True

    result = test_perfect_world()
    print(f"   Result: {result}")
    print(
        "   🤔 Why this is bad: Real users will break your code in ways you never imagined!"
    )


def demo_good_test_examples():
    """Demonstrate good testing practices."""

    print("✅ GOOD TEST EXAMPLE 1: Testing Behavior")
    print("This test verifies what your code does, not how it does it")

    def test_scraping_result_success_logic():
        """Test the success/failure logic of ScrapingResult."""

        # Test successful result
        success_result = ScrapingResult(
            url="http://example.com",
            status_code=200,
            content="<html>content</html>",
            headers={"content-type": "text/html"},
        )
        assert success_result.is_success() == True

        # Test failed result
        failed_result = ScrapingResult(
            url="http://example.com",
            status_code=404,
            content="",
            headers={},
            error="Not found",
        )
        assert failed_result.is_success() == False

        return True

    result = test_scraping_result_success_logic()
    print(f"   Result: {result}")
    print("   ✅ Why this is good: Tests business logic that matters to users!")
    print()

    print("✅ GOOD TEST EXAMPLE 2: Testing Edge Cases")
    print("This test tries to break your code on purpose")

    def test_edge_cases():
        """Test edge cases that users might trigger."""

        # Test with empty URL
        result = ScrapingResult(url="", status_code=0, content="", headers={})
        assert not result.is_success()

        # Test with None values
        result = ScrapingResult(url=None, status_code=0, content=None, headers={})
        assert not result.is_success()

        # Test boundary conditions
        result = ScrapingResult(url="test", status_code=199, content="", headers={})
        assert not result.is_success()  # Just below 200

        result = ScrapingResult(url="test", status_code=300, content="", headers={})
        assert not result.is_success()  # Just at 300

        return True

    result = test_edge_cases()
    print(f"   Result: {result}")
    print("   ✅ Why this is good: Catches bugs that happen in the real world!")


async def demo_mocking_done_right():
    """Demonstrate proper mocking techniques."""

    print("🎭 MOCKING EXAMPLE 1: Mock External Dependencies Only")
    print("Mock the network, not your own code")

    # Create a proper mock response
    mock_response = AsyncMock()
    mock_response.status_code.as_int.return_value = 200
    mock_response.text.return_value = "<html>Test content</html>"
    mock_response.headers.items.return_value = [("content-type", "text/html")]

    with patch("changelogger.scraper.rnet.Client") as mock_client:
        mock_client.return_value.get.return_value = mock_response

        config = ScrapingConfig()
        scraper = BasicScraper(config)

        result = await scraper.fetch_url("http://example.com")

        print(
            f"   Mock result: Success={result.is_success()}, Status={result.status_code}"
        )
        print("   ✅ This mocks the external network dependency (rnet)")
        print("   ✅ But still tests our scraper's logic")
        return True


async def demo_integration_testing():
    """Demonstrate integration testing with real requests."""

    print("🌐 INTEGRATION TEST: Real Network Requests")
    print("Testing with actual HTTP requests to verify everything works together")

    config = ScrapingConfig(request_delay=0.5)  # Be polite
    scraper = BasicScraper(config)

    # Test with a reliable test service
    result = await scraper.fetch_url("https://httpbin.org/json")

    print(f"   Real request result: Success={result.is_success()}")
    print(f"   Status code: {result.status_code}")
    print(f"   Content length: {len(result.content)} bytes")
    print(f"   Fetch time: {result.fetch_time:.3f}s")

    if result.is_success():
        # Verify the content is actually JSON
        try:
            data = json.loads(result.content)
            print(f"   ✅ Response is valid JSON with {len(data)} keys")
        except json.JSONDecodeError:
            print("   ❌ Response is not valid JSON")
            return False

    print("   ✅ This tests the complete system working together")
    print("   ✅ Catches integration bugs that unit tests miss")
    return True


async def demo_error_condition_testing():
    """Demonstrate testing error conditions."""

    print("💥 ERROR CONDITION TESTING: Making Things Fail On Purpose")
    print("Testing how your code handles various failure modes")

    config = ScrapingConfig(timeout=2)
    scraper = BasicScraper(config)

    # Test different error conditions
    error_tests = [
        ("Invalid URL", "not-a-valid-url"),
        ("Non-existent domain", "https://this-domain-does-not-exist-12345.invalid"),
        ("HTTP error", "https://httpbin.org/status/404"),
        ("Timeout", "https://httpbin.org/delay/5"),  # Will timeout with 2s limit
    ]

    passed_error_tests = 0

    for test_name, url in error_tests:
        print(f"   🧪 Testing {test_name}...")

        try:
            result = await scraper.fetch_url(url)

            if not result.is_success():
                print(f"      ✅ Failed gracefully: {result.error[:50]}...")
                passed_error_tests += 1
            else:
                print(f"      🤔 Unexpectedly succeeded: {result.status_code}")

        except Exception as e:
            print(f"      ❌ Crashed with exception: {e}")

    print(f"   📊 Error handling tests passed: {passed_error_tests}/{len(error_tests)}")
    print("   ✅ Good error handling means graceful failures, not crashes")

    return passed_error_tests > 0


async def demo_performance_testing():
    """Demonstrate basic performance testing."""

    print("⚡ PERFORMANCE TESTING: Is Concurrent Actually Faster?")
    print("Testing that our concurrent implementation actually improves performance")

    config = ScrapingConfig(request_delay=0.3, max_concurrent_requests=3)
    scraper = BasicScraper(config)

    # URLs that will take some time to respond
    test_urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
    ]

    # Test concurrent execution
    print("   🚀 Testing concurrent execution...")
    start_time = time.time()
    concurrent_results = await scraper.fetch_multiple_urls(test_urls)
    concurrent_time = time.time() - start_time

    # Test sequential execution
    print("   🐌 Testing sequential execution...")
    start_time = time.time()
    sequential_results = []
    for url in test_urls:
        result = await scraper.fetch_url(url)
        sequential_results.append(result)
    sequential_time = time.time() - start_time

    print(f"   📊 Concurrent time: {concurrent_time:.2f}s")
    print(f"   📊 Sequential time: {sequential_time:.2f}s")
    print(f"   📊 Speedup: {sequential_time / concurrent_time:.1f}x")

    if concurrent_time < sequential_time * 0.8:
        print("   ✅ Concurrency is working - significant speedup achieved!")
        return True
    print("   🤔 Concurrency might not be working as expected")
    return False


async def demo_test_driven_development():
    """Demonstrate the TDD cycle with a simple example."""

    print("🔴 TDD DEMO: Red-Green-Refactor Cycle")
    print("Demonstrating Test-Driven Development with a simple feature")

    print("\n🔴 RED PHASE: Write a failing test first")
    print("Let's say we want to add a feature to count successful requests")

    def test_scraper_counts_successful_requests():
        """Test that scraper tracks successful request count."""
        scraper = BasicScraper(ScrapingConfig())

        # This will fail because we haven't implemented counter yet
        try:
            assert hasattr(scraper, "successful_requests")
            assert scraper.successful_requests == 0
            return True
        except AttributeError:
            print("   ❌ Test fails - no successful_requests attribute")
            return False

    # Run the failing test
    print("   Running test...")
    result = test_scraper_counts_successful_requests()
    print(f"   Result: {result} (expected to fail)")

    print("\n🟢 GREEN PHASE: Make the test pass (minimal implementation)")
    print("Add just enough code to make the test pass")

    # Monkey patch the BasicScraper class to add the counter
    # (In real TDD, you'd modify the actual class file)
    original_init = BasicScraper.__init__

    def new_init(self, config):
        original_init(self, config)
        self.successful_requests = 0  # Add the counter

    BasicScraper.__init__ = new_init

    # Test again
    print("   Running test after minimal implementation...")
    result = test_scraper_counts_successful_requests()
    print(f"   Result: {result} (should now pass)")

    print("\n🔵 REFACTOR PHASE: Improve the implementation")
    print("Now we could refactor to make it better, add more features, etc.")
    print("But the test ensures we don't break the basic functionality")

    # Restore original init
    BasicScraper.__init__ = original_init

    return True


async def main():
    """Run the complete testing workshop."""

    print("🎓 TESTING WORKSHOP: From Bad Tests to Good Tests")
    print("=" * 70)
    print("Welcome to the most honest testing tutorial you'll ever encounter!")
    print("We'll start with terrible tests and work our way up to good ones.")
    print()

    workshop = TestingWorkshop()

    # Demo bad testing practices
    workshop.run_demo(
        "Bad Testing Practices",
        "Demonstrating what NOT to do when writing tests",
        demo_bad_test_examples,
    )

    # Demo good testing practices
    workshop.run_demo(
        "Good Testing Practices",
        "Demonstrating proper testing approaches",
        demo_good_test_examples,
    )

    # Demo mocking
    await workshop.run_async_demo(
        "Proper Mocking",
        "How to mock external dependencies without testing your mocks",
        demo_mocking_done_right,
    )

    # Demo integration testing
    await workshop.run_async_demo(
        "Integration Testing",
        "Testing with real external dependencies",
        demo_integration_testing,
    )

    # Demo error testing
    await workshop.run_async_demo(
        "Error Condition Testing",
        "Testing how your code handles various failure modes",
        demo_error_condition_testing,
    )

    # Demo performance testing
    await workshop.run_async_demo(
        "Performance Testing",
        "Verifying that optimizations actually work",
        demo_performance_testing,
    )

    # Demo TDD
    await workshop.run_async_demo(
        "Test-Driven Development",
        "The red-green-refactor cycle in action",
        demo_test_driven_development,
    )

    # Final summary
    print("🏁 TESTING WORKSHOP COMPLETE!")
    print("=" * 50)
    print(f"📊 Demos run: {workshop.demo_count}")
    print(f"✅ Successful: {workshop.passed_tests}")
    print(f"💥 Failed: {workshop.failed_tests}")

    success_rate = workshop.passed_tests / workshop.demo_count * 100

    if success_rate >= 80:
        print(f"\n🎉 Excellent! {success_rate:.1f}% success rate!")
        print("You've seen testing done right (and wrong).")
    elif success_rate >= 60:
        print(f"\n👍 Good! {success_rate:.1f}% success rate!")
        print("Most things worked - you're getting the hang of testing.")
    else:
        print(f"\n🤔 Hmm... {success_rate:.1f}% success rate.")
        print("That's actually educational! Failures teach us more than successes.")

    print("\n📚 Key takeaways:")
    print("   1. 🎯 Test behaviors, not implementation details")
    print("   2. 💥 Test error conditions, not just happy paths")
    print("   3. 🎭 Mock external dependencies, not your own code")
    print("   4. 🌐 Use integration tests to verify the whole system works")
    print("   5. ⚡ Test performance claims with actual measurements")
    print("   6. 🔴🟢🔵 TDD helps design better, more testable code")
    print("   7. 😄 Testing can be fun when you embrace the failures!")

    print("\n🎯 Next steps:")
    print("   1. Run pytest tests/ to see our real test suite")
    print("   2. Try writing your own tests for new features")
    print("   3. Break things intentionally and see if your tests catch it")
    print("   4. Read Chapter 4 in docs/course/ for more testing wisdom")

    print(
        "\n💡 Remember: The best test is the one that saves you from embarrassment in production!"
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(
            "\n\n👋 Workshop interrupted! Testing is like exercise - it's never fun to stop."
        )
    except Exception as e:
        print(f"\n\n💥 Workshop crashed: {e}")
        print(
            "💡 Ironically, this is a great example of why we need error handling tests!"
        )
        import traceback

        traceback.print_exc()
