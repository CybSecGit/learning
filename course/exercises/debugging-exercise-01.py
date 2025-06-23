#!/usr/bin/env python3
"""
Debugging Exercise 1: Fix the Broken Scraper

This file contains several intentional bugs that mirror the real issues
we encountered while building the scraper. Your job is to debug them!

Run this file and fix each error as it appears. Each error teaches you
something important about Python, async programming, or the rnet library.

Expected errors (in order):
1. Import error
2. Async testing issue
3. rnet API confusion
4. StatusCode type error
5. Header conversion problem
6. Async method call issue

Ready? Let's break some code! 🐛
"""

from __future__ import annotations

import asyncio

import pytest

# Import the modules (this will fail first)
from src.changelogger.scraper import BasicScraper, ScrapingConfig


# Exercise 1: The Import Mystery
def test_import_works():
    """This test will fail with an import error. Fix the import path!"""
    config = ScrapingConfig()
    scraper = BasicScraper(config)
    assert scraper is not None
    print("✅ Import exercise passed!")


# Exercise 2: The Async Test Trap
@pytest.mark.asyncio
async def test_async_scraping():
    """This test needs special async support. What's missing?"""
    config = ScrapingConfig(request_delay=0.1)
    scraper = BasicScraper(config)

    # This will fail with async testing issues
    result = await scraper.fetch_url("https://httpbin.org/get")
    assert result is not None
    print("✅ Async test exercise passed!")


# Exercise 3: The rnet API Explorer
async def explore_rnet_api():
    """Figure out the correct rnet API by exploring it."""
    import rnet

    # This line is wrong - fix it!
    # Hint: Use dir(rnet) to see what's available
    client = rnet.AsyncClient(impersonate="chrome")

    response = await client.get("https://httpbin.org/get")
    print(f"Response: {response}")
    print("✅ rnet API exercise passed!")


# Exercise 4: The StatusCode Detective
async def debug_status_code():
    """Fix the status code comparison issue."""
    import rnet

    client = rnet.Client(impersonate=rnet.Impersonate.Chrome131)
    response = await client.get("https://httpbin.org/get")

    # This comparison will fail - why?
    if response.status_code >= 200:  # This line breaks!
        print("Success!")
    else:
        print("Failed!")

    print("✅ StatusCode exercise passed!")


# Exercise 5: The Header Decoder
async def decode_headers():
    """Fix the header conversion problem."""
    import rnet

    client = rnet.Client(impersonate=rnet.Impersonate.Chrome131)
    response = await client.get("https://httpbin.org/headers")

    # This will fail - headers aren't what you expect!
    headers_dict = dict(response.headers)  # This line breaks!
    print(f"Headers: {headers_dict}")
    print("✅ Header decoding exercise passed!")


# Exercise 6: The Text Content Puzzle
async def extract_text():
    """Fix the text extraction issue."""
    import rnet

    client = rnet.Client(impersonate=rnet.Impersonate.Chrome131)
    response = await client.get("https://httpbin.org/get")

    # This is wrong in two ways - fix both!
    content = response.text  # Issue 1: method vs property
    # content = response.text()  # Issue 2: missing await

    print(f"Content length: {len(content)}")
    print("✅ Text extraction exercise passed!")


# Main debugging session
async def main():
    """Run all debugging exercises."""
    print("🐛 Welcome to the Debugging Bootcamp!")
    print("=" * 50)
    print("Each function will fail. Fix them one by one!")
    print()

    try:
        print("🔍 Exercise 1: Import Mystery")
        test_import_works()
    except Exception as e:
        print(f"💥 Error: {e}")
        print("💡 Hint: Check the import path. Does the module exist?")
        return

    try:
        print("\n🔍 Exercise 2: Async Test Trap")
        await test_async_scraping()
    except Exception as e:
        print(f"💥 Error: {e}")
        print("💡 Hint: Async tests need special support. What plugin is missing?")
        return

    try:
        print("\n🔍 Exercise 3: rnet API Explorer")
        await explore_rnet_api()
    except Exception as e:
        print(f"💥 Error: {e}")
        print("💡 Hint: Use print(dir(rnet)) to see available classes")
        return

    try:
        print("\n🔍 Exercise 4: StatusCode Detective")
        await debug_status_code()
    except Exception as e:
        print(f"💥 Error: {e}")
        print("💡 Hint: Check the type of response.status_code. Is it an int?")
        return

    try:
        print("\n🔍 Exercise 5: Header Decoder")
        await decode_headers()
    except Exception as e:
        print(f"💥 Error: {e}")
        print("💡 Hint: HTTP headers come as bytes. Check the types!")
        return

    try:
        print("\n🔍 Exercise 6: Text Content Puzzle")
        await extract_text()
    except Exception as e:
        print(f"💥 Error: {e}")
        print("💡 Hint: Is .text a property or method? Is it async?")
        return

    print("\n🎉 Congratulations! You've debugged all the exercises!")
    print("You now have the skills to debug real-world async scraping code.")


if __name__ == "__main__":
    # Run the debugging exercises
    asyncio.run(main())
