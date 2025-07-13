"""
XSS Security Toolkit - Module 1: Foundations

A comprehensive toolkit for Cross-Site Scripting (XSS) vulnerability detection,
analysis, and prevention. This toolkit provides:

- Payload analysis and categorization
- Comprehensive payload library with bypass techniques
- Reflection-based XSS scanning
- Context-aware vulnerability detection
- Professional reporting capabilities

Usage:
    from xss_toolkit.core.payload_analyzer import PayloadAnalyzer
    from xss_toolkit.payloads.payload_library import PayloadLibrary
    from xss_toolkit.scanners.reflection_scanner import ReflectionScanner

    # Analyze a payload
    analyzer = PayloadAnalyzer()
    analysis = analyzer.analyze_payload('<script>alert("XSS")</script>')
    
    # Get payloads from library
    library = PayloadLibrary()
    basic_payloads = library.get_payloads_by_category(PayloadCategory.BASIC)
    
    # Scan for XSS
    scanner = ReflectionScanner("https://target.example.com")
    results = scanner.scan_url("https://target.example.com/search", ["q"])

Author: Security Learning Lab
License: Educational Use Only - For Learning Purposes
Warning: This toolkit is for educational and authorized security testing only.
         Never use against systems you don't own or have explicit permission to test.
"""

__version__ = "1.0.0"
__author__ = "Security Learning Lab"
__license__ = "Educational Use Only"

# Export main classes for easy importing
from .core.payload_analyzer import PayloadAnalyzer, PayloadAnalysis, XSSType, Context
from .payloads.payload_library import PayloadLibrary, XSSPayload, PayloadCategory
from .scanners.reflection_scanner import ReflectionScanner, XSSTestResult

__all__ = [
    'PayloadAnalyzer',
    'PayloadAnalysis', 
    'XSSType',
    'Context',
    'PayloadLibrary',
    'XSSPayload',
    'PayloadCategory',
    'ReflectionScanner',
    'XSSTestResult'
]