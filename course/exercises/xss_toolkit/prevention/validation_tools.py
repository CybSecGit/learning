"""
Module 7: XSS Prevention Validation Tools

This module provides comprehensive tools for validating and testing XSS prevention mechanisms:
- Input sanitization testing and validation
- Output encoding verification
- CSP policy effectiveness testing
- WAF rule validation and bypass testing
- Security header analysis
- Framework-specific protection testing

The tools help developers and security teams verify that their XSS prevention
measures are working correctly and identify weaknesses in their defenses.
"""

import re
import html
import urllib.parse
import json
import base64
from typing import List, Dict, Set, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class PreventionMechanism(Enum):
    """Types of XSS prevention mechanisms"""
    INPUT_SANITIZATION = "input_sanitization"          # Input cleaning/filtering
    OUTPUT_ENCODING = "output_encoding"                # HTML/URL/JS encoding
    CSP_POLICY = "csp_policy"                         # Content Security Policy
    WAF_RULES = "waf_rules"                           # Web Application Firewall
    FRAMEWORK_PROTECTION = "framework_protection"     # Built-in framework protections
    SECURITY_HEADERS = "security_headers"             # HTTP security headers
    TEMPLATE_ENGINE = "template_engine"               # Auto-escaping templates
    VALIDATION_RULES = "validation_rules"             # Input validation rules


class SanitizationTechnique(Enum):
    """Input sanitization techniques"""
    WHITELIST_TAGS = "whitelist_tags"                 # Allow only safe HTML tags
    BLACKLIST_TAGS = "blacklist_tags"                 # Block dangerous HTML tags
    ATTRIBUTE_FILTERING = "attribute_filtering"        # Filter dangerous attributes
    CONTENT_FILTERING = "content_filtering"           # Filter dangerous content
    ENCODING_ONLY = "encoding_only"                   # Just encode, don't filter
    STRIP_TAGS = "strip_tags"                         # Remove all HTML tags
    ESCAPE_ENTITIES = "escape_entities"               # Escape HTML entities


class EncodingType(Enum):
    """Output encoding types"""
    HTML_ENCODING = "html_encoding"                   # &lt; &gt; &quot; etc.
    ATTRIBUTE_ENCODING = "attribute_encoding"         # Encoding for HTML attributes
    URL_ENCODING = "url_encoding"                     # %3C %3E %22 etc.
    JAVASCRIPT_ENCODING = "javascript_encoding"       # \\x3C \\x3E \\x22 etc.
    CSS_ENCODING = "css_encoding"                     # CSS-specific encoding
    JSON_ENCODING = "json_encoding"                   # JSON string encoding


@dataclass
class SanitizationTest:
    """Test case for input sanitization"""
    test_name: str                                    # Name of the test
    input_payload: str                               # Malicious input to test
    expected_safe_output: str                        # Expected sanitized output
    description: str                                 # What this test validates
    attack_type: str                                 # Type of attack (script, event, etc.)
    context: str                                     # Where this would be injected
    severity: str                                    # Critical/High/Medium/Low


@dataclass
class EncodingTest:
    """Test case for output encoding"""
    test_name: str                                    # Name of the test
    raw_input: str                                   # Raw input that needs encoding
    encoding_type: EncodingType                      # Type of encoding to apply
    expected_encoded: str                            # Expected encoded output
    context: str                                     # HTML/Attribute/URL/JS context
    bypass_attempt: str                              # Payload that tries to bypass


@dataclass
class PreventionTestResult:
    """Result of a prevention mechanism test"""
    mechanism: PreventionMechanism                   # Which mechanism was tested
    test_name: str                                   # Name of the specific test
    passed: bool                                     # Whether the test passed
    input_payload: str                               # Input that was tested
    actual_output: str                               # Actual output received
    expected_output: str                             # Expected safe output
    bypass_detected: bool                            # Whether bypass was detected
    risk_level: str                                  # Risk if this fails
    remediation: str                                 # How to fix the issue


@dataclass
class SecurityAssessment:
    """Overall security assessment results"""
    total_tests: int                                 # Total number of tests run
    passed_tests: int                                # Number of tests that passed
    failed_tests: int                                # Number of tests that failed
    critical_failures: int                           # Number of critical failures
    security_score: float                            # Overall score (0.0-10.0)
    prevention_coverage: Dict[PreventionMechanism, float]  # Coverage per mechanism
    recommendations: List[str]                       # Security recommendations
    test_results: List[PreventionTestResult]         # Detailed test results


class XSSPreventionValidator:
    """
    Comprehensive validator for XSS prevention mechanisms.
    
    This validator tests various prevention techniques to ensure they
    properly protect against XSS attacks. It includes tests for:
    - Input sanitization effectiveness
    - Output encoding correctness
    - CSP policy enforcement
    - WAF rule validation
    - Framework protection verification
    
    Example:
        validator = XSSPreventionValidator()
        
        # Test a sanitization function
        def my_sanitizer(input_text):
            return html.escape(input_text)
        
        results = validator.test_sanitization(my_sanitizer)
        assessment = validator.generate_assessment(results)
    """
    
    def __init__(self):
        # Initialize test cases for different prevention mechanisms
        self.sanitization_tests = self._create_sanitization_tests()
        self.encoding_tests = self._create_encoding_tests()
        self.csp_tests = self._create_csp_tests()
        self.waf_tests = self._create_waf_tests()
        
        # Common XSS vectors for testing
        self.xss_vectors = [
            # Basic script injection
            '<script>alert("XSS")</script>',
            '<img src=x onerror=alert("XSS")>',
            '<svg onload=alert("XSS")>',
            
            # Event handler injection
            '" onmouseover=alert("XSS") "',
            "' onclick=alert('XSS') '",
            '<div onload="alert(\'XSS\')">',
            
            # JavaScript protocol
            'javascript:alert("XSS")',
            'JaVaScRiPt:alert("XSS")',
            
            # Encoded variants
            '%3Cscript%3Ealert("XSS")%3C/script%3E',
            '&lt;script&gt;alert("XSS")&lt;/script&gt;',
            '\\u003cscript\\u003ealert("XSS")\\u003c/script\\u003e',
            
            # Advanced vectors
            '<iframe src="javascript:alert(\'XSS\')">',
            '<object data="javascript:alert(\'XSS\')">',
            '<meta http-equiv="refresh" content="0;url=javascript:alert(\'XSS\')">',
            
            # Framework-specific
            '{{constructor.constructor("alert(\'XSS\')")()}}',
            '${alert("XSS")}',
            '#{alert("XSS")}',
            
            # Filter bypass attempts
            '<scr<script>ipt>alert("XSS")</script>',
            '<svg/onload=alert("XSS")>',
            '<img src=x onerror="alert`XSS`">',
            'eval(String.fromCharCode(97,108,101,114,116,40,34,88,83,83,34,41))',
        ]
        
        # Expected safe outputs for different encoding types
        self.safe_encodings = {
            EncodingType.HTML_ENCODING: {
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#x27;',
                '&': '&amp;'
            },
            EncodingType.URL_ENCODING: {
                '<': '%3C',
                '>': '%3E',
                '"': '%22',
                "'": '%27',
                '&': '%26'
            },
            EncodingType.JAVASCRIPT_ENCODING: {
                '<': '\\x3C',
                '>': '\\x3E',
                '"': '\\x22',
                "'": '\\x27',
                '&': '\\x26'
            }
        }
    
    def _create_sanitization_tests(self) -> List[SanitizationTest]:
        """Create comprehensive sanitization test cases"""
        tests = []
        
        # Basic script tag tests
        tests.append(SanitizationTest(
            test_name="basic_script_tag",
            input_payload='<script>alert("XSS")</script>',
            expected_safe_output='&lt;script&gt;alert("XSS")&lt;/script&gt;',
            description="Basic script tag should be encoded or removed",
            attack_type="script_injection",
            context="html_content",
            severity="critical"
        ))
        
        # Event handler tests
        tests.append(SanitizationTest(
            test_name="img_onerror_event",
            input_payload='<img src=x onerror=alert("XSS")>',
            expected_safe_output='<img src="x">',  # Event handler removed
            description="Event handlers should be stripped from tags",
            attack_type="event_handler",
            context="html_content",
            severity="high"
        ))
        
        # Attribute injection tests
        tests.append(SanitizationTest(
            test_name="attribute_breaking",
            input_payload='" onmouseover=alert("XSS") "',
            expected_safe_output='&quot; onmouseover=alert(&quot;XSS&quot;) &quot;',
            description="Attribute breaking attempts should be encoded",
            attack_type="attribute_injection",
            context="html_attribute",
            severity="high"
        ))
        
        # JavaScript protocol tests
        tests.append(SanitizationTest(
            test_name="javascript_protocol",
            input_payload='javascript:alert("XSS")',
            expected_safe_output='',  # Should be completely removed
            description="JavaScript protocol should be blocked",
            attack_type="protocol_injection",
            context="url_parameter",
            severity="medium"
        ))
        
        # Encoding bypass tests
        tests.append(SanitizationTest(
            test_name="url_encoded_bypass",
            input_payload='%3Cscript%3Ealert("XSS")%3C/script%3E',
            expected_safe_output='%3Cscript%3Ealert("XSS")%3C/script%3E',  # Should remain encoded
            description="URL encoded payloads should not be decoded before sanitization",
            attack_type="encoding_bypass",
            context="url_parameter",
            severity="medium"
        ))
        
        # Advanced HTML5 tests
        tests.append(SanitizationTest(
            test_name="svg_onload",
            input_payload='<svg onload=alert("XSS")>',
            expected_safe_output='<svg>',  # Event handler removed
            description="SVG onload events should be stripped",
            attack_type="html5_injection",
            context="html_content",
            severity="high"
        ))
        
        # Template injection tests
        tests.append(SanitizationTest(
            test_name="angular_template",
            input_payload='{{constructor.constructor("alert(\\"XSS\\")")()}}',
            expected_safe_output='{{constructor.constructor("alert(\\"XSS\\")")()}}',  # Should be treated as text
            description="Template injection syntax should be treated as plain text",
            attack_type="template_injection",
            context="html_content",
            severity="medium"
        ))
        
        return tests
    
    def _create_encoding_tests(self) -> List[EncodingTest]:
        """Create comprehensive encoding test cases"""
        tests = []
        
        # HTML context encoding
        tests.append(EncodingTest(
            test_name="html_context_encoding",
            raw_input='<script>alert("XSS")</script>',
            encoding_type=EncodingType.HTML_ENCODING,
            expected_encoded='&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;',
            context="html_content",
            bypass_attempt='&lt;script&gt;alert("XSS")&lt;/script&gt;'
        ))
        
        # Attribute context encoding
        tests.append(EncodingTest(
            test_name="attribute_context_encoding",
            raw_input='" onmouseover=alert("XSS") "',
            encoding_type=EncodingType.ATTRIBUTE_ENCODING,
            expected_encoded='&quot; onmouseover=alert(&quot;XSS&quot;) &quot;',
            context="html_attribute",
            bypass_attempt='" onmouseover=alert("XSS") "'
        ))
        
        # URL context encoding
        tests.append(EncodingTest(
            test_name="url_context_encoding",
            raw_input='javascript:alert("XSS")',
            encoding_type=EncodingType.URL_ENCODING,
            expected_encoded='javascript%3Aalert%28%22XSS%22%29',
            context="url_parameter",
            bypass_attempt='javascript:alert("XSS")'
        ))
        
        # JavaScript context encoding
        tests.append(EncodingTest(
            test_name="javascript_context_encoding",
            raw_input='"; alert("XSS"); //',
            encoding_type=EncodingType.JAVASCRIPT_ENCODING,
            expected_encoded='\\x22; alert(\\x22XSS\\x22); //',
            context="javascript_string",
            bypass_attempt='"; alert("XSS"); //'
        ))
        
        return tests
    
    def _create_csp_tests(self) -> List[Dict[str, Any]]:
        """Create CSP effectiveness test cases"""
        return [
            {
                'test_name': 'unsafe_inline_detection',
                'csp_policy': "script-src 'self' 'unsafe-inline'",
                'payload': '<script>alert("CSP Test")</script>',
                'should_block': False,  # unsafe-inline allows this
                'description': "'unsafe-inline' should allow inline scripts"
            },
            {
                'test_name': 'strict_policy_enforcement',
                'csp_policy': "script-src 'self'",
                'payload': '<script>alert("CSP Test")</script>',
                'should_block': True,  # Should block inline scripts
                'description': "Strict CSP should block inline scripts"
            },
            {
                'test_name': 'nonce_validation',
                'csp_policy': "script-src 'nonce-test123'",
                'payload': '<script nonce="test123">alert("CSP Test")</script>',
                'should_block': False,  # Valid nonce should allow
                'description': "Valid nonce should allow script execution"
            }
        ]
    
    def _create_waf_tests(self) -> List[Dict[str, Any]]:
        """Create WAF rule test cases"""
        return [
            {
                'test_name': 'basic_script_blocking',
                'payload': '<script>alert("WAF Test")</script>',
                'should_block': True,
                'rule_type': 'script_injection',
                'description': 'Basic script tags should be blocked'
            },
            {
                'test_name': 'event_handler_blocking',
                'payload': '<img src=x onerror=alert("WAF Test")>',
                'should_block': True,
                'rule_type': 'event_handler',
                'description': 'Event handlers should be blocked'
            },
            {
                'test_name': 'encoded_bypass_attempt',
                'payload': '%3Cscript%3Ealert("WAF Test")%3C/script%3E',
                'should_block': True,
                'rule_type': 'encoding_bypass',
                'description': 'URL encoded scripts should be blocked'
            },
            {
                'test_name': 'case_variation_bypass',
                'payload': '<ScRiPt>alert("WAF Test")</ScRiPt>',
                'should_block': True,
                'rule_type': 'case_bypass',
                'description': 'Case variations should be blocked'
            }
        ]
    
    def test_sanitization(self, sanitizer_function: Callable[[str], str]) -> List[PreventionTestResult]:
        """
        Test a sanitization function against various XSS vectors.
        
        Args:
            sanitizer_function: Function that takes input and returns sanitized output
            
        Returns:
            List of test results
        """
        results = []
        
        for test_case in self.sanitization_tests:
            try:
                # Apply the sanitization function
                actual_output = sanitizer_function(test_case.input_payload)
                
                # Check if the output is safe
                passed = self._is_output_safe(actual_output, test_case.expected_safe_output)
                
                # Check for bypass attempts
                bypass_detected = self._check_sanitization_bypass(actual_output)
                
                # Determine risk level
                risk_level = test_case.severity if not passed else "low"
                
                # Generate remediation advice
                remediation = self._generate_sanitization_remediation(test_case, actual_output)
                
                result = PreventionTestResult(
                    mechanism=PreventionMechanism.INPUT_SANITIZATION,
                    test_name=test_case.test_name,
                    passed=passed,
                    input_payload=test_case.input_payload,
                    actual_output=actual_output,
                    expected_output=test_case.expected_safe_output,
                    bypass_detected=bypass_detected,
                    risk_level=risk_level,
                    remediation=remediation
                )
                results.append(result)
                
            except Exception as e:
                # Handle sanitization function errors
                result = PreventionTestResult(
                    mechanism=PreventionMechanism.INPUT_SANITIZATION,
                    test_name=test_case.test_name,
                    passed=False,
                    input_payload=test_case.input_payload,
                    actual_output=f"ERROR: {str(e)}",
                    expected_output=test_case.expected_safe_output,
                    bypass_detected=True,
                    risk_level="critical",
                    remediation="Fix sanitization function error"
                )
                results.append(result)
        
        return results
    
    def test_encoding(self, encoder_function: Callable[[str, str], str]) -> List[PreventionTestResult]:
        """
        Test an encoding function against various contexts.
        
        Args:
            encoder_function: Function that takes (input, context) and returns encoded output
            
        Returns:
            List of test results
        """
        results = []
        
        for test_case in self.encoding_tests:
            try:
                # Apply the encoding function
                actual_output = encoder_function(test_case.raw_input, test_case.context)
                
                # Check if encoding is correct
                passed = self._is_encoding_correct(actual_output, test_case.expected_encoded, test_case.encoding_type)
                
                # Check for bypass potential
                bypass_detected = self._check_encoding_bypass(actual_output, test_case.bypass_attempt)
                
                # Determine risk level
                risk_level = "high" if not passed else "low"
                
                # Generate remediation advice
                remediation = self._generate_encoding_remediation(test_case, actual_output)
                
                result = PreventionTestResult(
                    mechanism=PreventionMechanism.OUTPUT_ENCODING,
                    test_name=test_case.test_name,
                    passed=passed,
                    input_payload=test_case.raw_input,
                    actual_output=actual_output,
                    expected_output=test_case.expected_encoded,
                    bypass_detected=bypass_detected,
                    risk_level=risk_level,
                    remediation=remediation
                )
                results.append(result)
                
            except Exception as e:
                result = PreventionTestResult(
                    mechanism=PreventionMechanism.OUTPUT_ENCODING,
                    test_name=test_case.test_name,
                    passed=False,
                    input_payload=test_case.raw_input,
                    actual_output=f"ERROR: {str(e)}",
                    expected_output=test_case.expected_encoded,
                    bypass_detected=True,
                    risk_level="critical",
                    remediation="Fix encoding function error"
                )
                results.append(result)
        
        return results
    
    def test_csp_policy(self, csp_policy: str) -> List[PreventionTestResult]:
        """
        Test CSP policy effectiveness against various attacks.
        
        Args:
            csp_policy: Content-Security-Policy header value
            
        Returns:
            List of test results
        """
        results = []
        
        for test_case in self.csp_tests:
            # Simulate CSP policy evaluation
            would_block = self._simulate_csp_enforcement(csp_policy, test_case['payload'])
            
            # Check if result matches expectation
            passed = (would_block == test_case['should_block'])
            
            # Determine bypass detection
            bypass_detected = not would_block and test_case['should_block']
            
            # Risk level based on policy effectiveness
            risk_level = "high" if bypass_detected else "low"
            
            # Generate remediation
            remediation = self._generate_csp_remediation(csp_policy, test_case)
            
            result = PreventionTestResult(
                mechanism=PreventionMechanism.CSP_POLICY,
                test_name=test_case['test_name'],
                passed=passed,
                input_payload=test_case['payload'],
                actual_output=f"Blocked: {would_block}",
                expected_output=f"Should block: {test_case['should_block']}",
                bypass_detected=bypass_detected,
                risk_level=risk_level,
                remediation=remediation
            )
            results.append(result)
        
        return results
    
    def test_waf_rules(self, waf_function: Callable[[str], bool]) -> List[PreventionTestResult]:
        """
        Test WAF rules against various bypass attempts.
        
        Args:
            waf_function: Function that takes payload and returns True if blocked
            
        Returns:
            List of test results
        """
        results = []
        
        for test_case in self.waf_tests:
            try:
                # Test if WAF blocks the payload
                was_blocked = waf_function(test_case['payload'])
                
                # Check if result matches expectation
                passed = (was_blocked == test_case['should_block'])
                
                # Detect bypasses
                bypass_detected = not was_blocked and test_case['should_block']
                
                # Risk assessment
                risk_level = "high" if bypass_detected else "low"
                
                # Remediation advice
                remediation = self._generate_waf_remediation(test_case, was_blocked)
                
                result = PreventionTestResult(
                    mechanism=PreventionMechanism.WAF_RULES,
                    test_name=test_case['test_name'],
                    passed=passed,
                    input_payload=test_case['payload'],
                    actual_output=f"Blocked: {was_blocked}",
                    expected_output=f"Should block: {test_case['should_block']}",
                    bypass_detected=bypass_detected,
                    risk_level=risk_level,
                    remediation=remediation
                )
                results.append(result)
                
            except Exception as e:
                result = PreventionTestResult(
                    mechanism=PreventionMechanism.WAF_RULES,
                    test_name=test_case['test_name'],
                    passed=False,
                    input_payload=test_case['payload'],
                    actual_output=f"ERROR: {str(e)}",
                    expected_output=f"Should block: {test_case['should_block']}",
                    bypass_detected=True,
                    risk_level="critical",
                    remediation="Fix WAF function error"
                )
                results.append(result)
        
        return results
    
    def _is_output_safe(self, actual_output: str, expected_output: str) -> bool:
        """Check if sanitized output is safe"""
        # Check for dangerous patterns that should be removed/encoded
        dangerous_patterns = [
            r'<script[^>]*>',           # Script tags
            r'on\w+\s*=',               # Event handlers
            r'javascript:',             # JavaScript protocol
            r'<iframe[^>]*>',           # Iframe tags
            r'<object[^>]*>',           # Object tags
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, actual_output, re.IGNORECASE):
                # Check if it's properly encoded
                if not self._is_properly_encoded(actual_output):
                    return False
        
        return True
    
    def _is_properly_encoded(self, output: str) -> bool:
        """Check if dangerous characters are properly encoded"""
        # Look for unencoded dangerous characters
        dangerous_chars = ['<', '>', '"', "'"]
        
        for char in dangerous_chars:
            if char in output:
                # Check if there's a pattern suggesting it's part of an attack
                if char == '<' and re.search(r'<\s*\w+', output):
                    return False  # Looks like an HTML tag
                if char in ['"', "'"] and re.search(r'on\w+\s*=\s*["\']', output):
                    return False  # Looks like an event handler
        
        return True
    
    def _check_sanitization_bypass(self, output: str) -> bool:
        """Check if output contains potential bypass indicators"""
        bypass_indicators = [
            r'javascript:',                           # JavaScript protocol
            r'on\w+\s*=\s*[^"\s>]+',                 # Unquoted event handlers
            r'<\s*script[^>]*>',                     # Script tags
            r'eval\s*\(',                            # Eval function
            r'expression\s*\(',                      # CSS expressions
        ]
        
        for indicator in bypass_indicators:
            if re.search(indicator, output, re.IGNORECASE):
                return True
        
        return False
    
    def _is_encoding_correct(self, actual: str, expected: str, encoding_type: EncodingType) -> bool:
        """Check if encoding is applied correctly"""
        # For this example, we'll do a simple comparison
        # In practice, you might want more sophisticated checking
        return actual == expected
    
    def _check_encoding_bypass(self, encoded_output: str, original_payload: str) -> bool:
        """Check if encoded output could still be exploited"""
        # If the encoded output is the same as original, encoding failed
        if encoded_output == original_payload:
            return True
        
        # Check for incomplete encoding
        dangerous_chars = ['<', '>', '"', "'", '&']
        for char in dangerous_chars:
            if char in encoded_output and char in original_payload:
                return True
        
        return False
    
    def _simulate_csp_enforcement(self, csp_policy: str, payload: str) -> bool:
        """Simulate CSP policy enforcement (simplified)"""
        # This is a simplified simulation
        # In practice, you'd need a full CSP parser
        
        # Check for unsafe-inline
        if "'unsafe-inline'" in csp_policy:
            if '<script>' in payload:
                return False  # Would not block inline scripts
        
        # Check for script-src restrictions
        if 'script-src' in csp_policy:
            if "'self'" in csp_policy and 'javascript:' in payload:
                return True  # Would block javascript: URLs
            if "'none'" in csp_policy and '<script>' in payload:
                return True  # Would block all scripts
        
        # Default behavior
        if '<script>' in payload and 'script-src' not in csp_policy:
            return False  # No script-src means default-src or allow all
        
        return True  # Default to blocking
    
    def _generate_sanitization_remediation(self, test_case: SanitizationTest, actual_output: str) -> str:
        """Generate remediation advice for sanitization failures"""
        if test_case.attack_type == "script_injection":
            return "Use HTML encoding or remove <script> tags completely"
        elif test_case.attack_type == "event_handler":
            return "Strip all event handler attributes (on*) from HTML tags"
        elif test_case.attack_type == "attribute_injection":
            return "Properly encode quotes and other special characters in attributes"
        elif test_case.attack_type == "protocol_injection":
            return "Block or remove javascript:, data:, and vbscript: protocols"
        else:
            return "Apply context-appropriate encoding and filtering"
    
    def _generate_encoding_remediation(self, test_case: EncodingTest, actual_output: str) -> str:
        """Generate remediation advice for encoding failures"""
        return f"Apply proper {test_case.encoding_type.value} to all user input in {test_case.context} context"
    
    def _generate_csp_remediation(self, csp_policy: str, test_case: Dict[str, Any]) -> str:
        """Generate remediation advice for CSP failures"""
        if "'unsafe-inline'" in csp_policy:
            return "Remove 'unsafe-inline' and use nonces or hashes for legitimate inline scripts"
        elif not test_case.get('should_block', True):
            return "Review CSP policy for proper script-src restrictions"
        else:
            return "CSP policy is working correctly"
    
    def _generate_waf_remediation(self, test_case: Dict[str, Any], was_blocked: bool) -> str:
        """Generate remediation advice for WAF failures"""
        if not was_blocked and test_case['should_block']:
            return f"Add or improve WAF rules for {test_case['rule_type']} attacks"
        else:
            return "WAF rule is working correctly"
    
    def generate_assessment(self, all_results: List[PreventionTestResult]) -> SecurityAssessment:
        """Generate overall security assessment from test results"""
        if not all_results:
            return SecurityAssessment(
                total_tests=0, passed_tests=0, failed_tests=0, critical_failures=0,
                security_score=0.0, prevention_coverage={}, recommendations=[], test_results=[]
            )
        
        # Calculate basic metrics
        total_tests = len(all_results)
        passed_tests = sum(1 for r in all_results if r.passed)
        failed_tests = total_tests - passed_tests
        critical_failures = sum(1 for r in all_results if r.risk_level == "critical")
        
        # Calculate security score (0.0 to 10.0)
        if total_tests > 0:
            pass_rate = passed_tests / total_tests
            # Start with pass rate, reduce for critical failures
            security_score = pass_rate * 10.0
            security_score -= critical_failures * 2.0  # Penalty for critical failures
            security_score = max(0.0, min(10.0, security_score))
        else:
            security_score = 0.0
        
        # Calculate prevention coverage per mechanism
        prevention_coverage = {}
        for mechanism in PreventionMechanism:
            mechanism_results = [r for r in all_results if r.mechanism == mechanism]
            if mechanism_results:
                mechanism_pass_rate = sum(1 for r in mechanism_results if r.passed) / len(mechanism_results)
                prevention_coverage[mechanism] = mechanism_pass_rate
            else:
                prevention_coverage[mechanism] = 0.0
        
        # Generate recommendations
        recommendations = self._generate_security_recommendations(all_results)
        
        return SecurityAssessment(
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            critical_failures=critical_failures,
            security_score=security_score,
            prevention_coverage=prevention_coverage,
            recommendations=recommendations,
            test_results=all_results
        )
    
    def _generate_security_recommendations(self, results: List[PreventionTestResult]) -> List[str]:
        """Generate security recommendations based on test results"""
        recommendations = []
        
        # Check for critical failures
        critical_failures = [r for r in results if r.risk_level == "critical"]
        if critical_failures:
            recommendations.append(f"URGENT: Fix {len(critical_failures)} critical security issues immediately")
        
        # Check for mechanism-specific issues
        sanitization_failures = [r for r in results if r.mechanism == PreventionMechanism.INPUT_SANITIZATION and not r.passed]
        if sanitization_failures:
            recommendations.append("Improve input sanitization to handle script injection and event handlers")
        
        encoding_failures = [r for r in results if r.mechanism == PreventionMechanism.OUTPUT_ENCODING and not r.passed]
        if encoding_failures:
            recommendations.append("Implement proper context-aware output encoding")
        
        csp_failures = [r for r in results if r.mechanism == PreventionMechanism.CSP_POLICY and not r.passed]
        if csp_failures:
            recommendations.append("Strengthen Content Security Policy configuration")
        
        waf_failures = [r for r in results if r.mechanism == PreventionMechanism.WAF_RULES and not r.passed]
        if waf_failures:
            recommendations.append("Update WAF rules to catch advanced bypass techniques")
        
        # General recommendations
        bypass_detected = any(r.bypass_detected for r in results)
        if bypass_detected:
            recommendations.append("Implement defense-in-depth with multiple prevention layers")
        
        # If mostly passing, suggest advanced measures
        pass_rate = sum(1 for r in results if r.passed) / len(results) if results else 0
        if pass_rate > 0.8:
            recommendations.append("Consider implementing advanced security measures like SRI and trusted types")
        
        return recommendations
    
    def generate_prevention_report(self, assessment: SecurityAssessment) -> str:
        """Generate a comprehensive prevention validation report"""
        report = "XSS Prevention Validation Report\n"
        report += "=" * 50 + "\n\n"
        
        # Executive summary
        report += "EXECUTIVE SUMMARY\n"
        report += "-" * 20 + "\n"
        report += f"Security Score: {assessment.security_score:.1f}/10.0\n"
        report += f"Tests Passed: {assessment.passed_tests}/{assessment.total_tests} ({assessment.passed_tests/assessment.total_tests*100:.1f}%)\n"
        report += f"Critical Failures: {assessment.critical_failures}\n\n"
        
        # Prevention coverage breakdown
        report += "PREVENTION MECHANISM COVERAGE\n"
        report += "-" * 35 + "\n"
        for mechanism, coverage in assessment.prevention_coverage.items():
            if coverage > 0:  # Only show tested mechanisms
                report += f"{mechanism.value.replace('_', ' ').title()}: {coverage*100:.1f}%\n"
        report += "\n"
        
        # Critical issues
        critical_results = [r for r in assessment.test_results if r.risk_level == "critical"]
        if critical_results:
            report += "CRITICAL ISSUES\n"
            report += "-" * 15 + "\n"
            for result in critical_results:
                report += f"❌ {result.test_name}\n"
                report += f"   Input: {result.input_payload[:50]}...\n"
                report += f"   Issue: {result.remediation}\n\n"
        
        # High-risk issues
        high_risk_results = [r for r in assessment.test_results if r.risk_level == "high" and not r.passed]
        if high_risk_results:
            report += "HIGH-RISK ISSUES\n"
            report += "-" * 15 + "\n"
            for result in high_risk_results[:5]:  # Show first 5
                report += f"⚠️  {result.test_name}\n"
                report += f"   Input: {result.input_payload[:50]}...\n"
                report += f"   Fix: {result.remediation}\n\n"
        
        # Recommendations
        if assessment.recommendations:
            report += "SECURITY RECOMMENDATIONS\n"
            report += "-" * 25 + "\n"
            for i, rec in enumerate(assessment.recommendations, 1):
                report += f"{i}. {rec}\n"
            report += "\n"
        
        # Detailed test results summary
        report += "TEST RESULTS SUMMARY\n"
        report += "-" * 20 + "\n"
        
        mechanism_stats = {}
        for result in assessment.test_results:
            mech = result.mechanism.value
            if mech not in mechanism_stats:
                mechanism_stats[mech] = {'total': 0, 'passed': 0, 'failed': 0}
            
            mechanism_stats[mech]['total'] += 1
            if result.passed:
                mechanism_stats[mech]['passed'] += 1
            else:
                mechanism_stats[mech]['failed'] += 1
        
        for mechanism, stats in mechanism_stats.items():
            pass_rate = (stats['passed'] / stats['total']) * 100 if stats['total'] > 0 else 0
            report += f"{mechanism.replace('_', ' ').title()}: {stats['passed']}/{stats['total']} ({pass_rate:.1f}%)\n"
        
        return report