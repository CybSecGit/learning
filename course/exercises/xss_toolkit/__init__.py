"""
XSS Mastery Toolkit - The Complete Web Security Testing Suite

A comprehensive, production-quality XSS security testing toolkit that demonstrates
mastery of web application security through practical, working implementations.

This toolkit implements 8 progressive modules:
1. Payload Analyzer & Library (Foundation)
2. DOM XSS Detective (JavaScript Analysis)  
3. Context-Aware Fuzzer (Intelligent Testing)
4. Stored XSS Framework (Persistence Testing)
5. CSP Bypass Analyzer (Policy Analysis)
6. Advanced Polyglot Engine (Multi-Context Payloads)
7. Prevention Validator (Security Controls Testing)
8. Enterprise Integration (Production Workflows)

Usage:
    from xss_toolkit import PayloadAnalyzer, PayloadLibrary
    from xss_toolkit import JavaScriptParser, ContextAwareFuzzer
    from xss_toolkit import CSPBypassAnalyzer, AdvancedPolyglotEngine
    
    # Basic payload analysis
    analyzer = PayloadAnalyzer()
    analysis = analyzer.analyze_payload('<script>alert("XSS")</script>')
    
    # DOM XSS analysis
    js_parser = JavaScriptParser()
    sources, sinks, flows = js_parser.analyze_javascript(js_code)
    
    # CSP bypass analysis
    csp_analyzer = CSPBypassAnalyzer()
    result = csp_analyzer.analyze_csp("script-src 'self' 'unsafe-inline'")

Author: XSS Mastery Toolkit
License: Educational Use Only - For Learning Purposes
Warning: This toolkit is for educational and authorized security testing only.
         Never use against systems you don't own or have explicit permission to test.
"""

__version__ = "1.0.0"
__author__ = "XSS Mastery Toolkit"
__license__ = "Educational Use Only"

# Module 1: Foundation & Analysis
from .core.payload_analyzer import PayloadAnalyzer, PayloadAnalysis, XSSType, Context
from .payloads.payload_library import PayloadLibrary, XSSPayload, PayloadCategory
from .scanners.reflection_scanner import ReflectionScanner, XSSTestResult

# Module 2: DOM XSS Analysis
from .dom.javascript_parser import JavaScriptParser, JavaScriptSource, JavaScriptSink, DataFlowPath

# Module 3: Context-Aware Fuzzing
from .fuzzing.context_fuzzer import ContextAwareFuzzer, InjectionContext, FuzzingResult

# Module 4: Stored XSS Testing
from .persistence.stored_xss_framework import StoredXSSFramework, StoredPayload, PersistenceResult

# Module 5: CSP Analysis
from .csp.bypass_analyzer import CSPBypassAnalyzer, CSPAnalysisResult, CSPBypassPayload

# Module 6: Advanced Payloads
from .polyglot.advanced_engine import AdvancedPolyglotEngine, PolyglotPayload, PolyglotContext

# Module 7: Security Validation
from .prevention.validation_tools import XSSPreventionValidator, PreventionTestResult, SecurityAssessment

# Module 8: Enterprise Integration
from .enterprise.integration_suite import EnterpriseIntegrationSuite, VulnerabilityFinding, ScanSession

__all__ = [
    # Core analysis (Module 1)
    'PayloadAnalyzer', 'PayloadAnalysis', 'XSSType', 'Context',
    'PayloadLibrary', 'XSSPayload', 'PayloadCategory',
    'ReflectionScanner', 'XSSTestResult',
    
    # DOM XSS analysis (Module 2)
    'JavaScriptParser', 'JavaScriptSource', 'JavaScriptSink', 'DataFlowPath',
    
    # Context-aware fuzzing (Module 3)
    'ContextAwareFuzzer', 'InjectionContext', 'FuzzingResult',
    
    # Stored XSS testing (Module 4)
    'StoredXSSFramework', 'StoredPayload', 'PersistenceResult',
    
    # CSP analysis (Module 5)
    'CSPBypassAnalyzer', 'CSPAnalysisResult', 'CSPBypassPayload',
    
    # Advanced payloads (Module 6)
    'AdvancedPolyglotEngine', 'PolyglotPayload', 'PolyglotContext',
    
    # Security validation (Module 7)
    'XSSPreventionValidator', 'PreventionTestResult', 'SecurityAssessment',
    
    # Enterprise integration (Module 8)
    'EnterpriseIntegrationSuite', 'VulnerabilityFinding', 'ScanSession'
]