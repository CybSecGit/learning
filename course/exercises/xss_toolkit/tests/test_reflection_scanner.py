#!/usr/bin/env python3
"""
Tests for XSS Reflection Scanner

This test suite validates the reflection scanner functionality including
URL scanning, payload injection, response analysis, and result reporting.
Uses mocked HTTP responses to avoid making real network requests.

Test Categories:
- Unit tests for individual scanner methods
- Integration tests for complete scanning workflows
- Mock HTTP response testing
- Report generation and export testing
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import requests

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanners.reflection_scanner import (
    ReflectionScanner, ScanResult, ScanStatus
)


class TestReflectionScanner:
    """Test cases for the ReflectionScanner class"""
    
    @pytest.fixture
    def scanner(self):
        """Create a ReflectionScanner instance for testing"""
        return ReflectionScanner(timeout=5, delay=0)  # No delay for tests
    
    @pytest.fixture
    def mock_response(self):
        """Create a mock HTTP response"""
        response = Mock()
        response.status_code = 200
        response.text = '<html><body>Hello <script>alert("XSS")</script> World</body></html>'
        response.headers = {'Content-Type': 'text/html'}
        return response
    
    def test_scanner_initialization(self, scanner):
        """Test that the scanner initializes correctly"""
        assert scanner.timeout == 5
        assert scanner.delay == 0
        assert scanner.user_agent.startswith("Mozilla/5.0")
        assert scanner.payload_library is not None
        assert scanner.payload_analyzer is not None
        assert hasattr(scanner, 'session')
        assert len(scanner.execution_patterns) > 0
        assert len(scanner.blocked_patterns) > 0
    
    def test_build_test_url(self, scanner):
        """Test URL building with injected payloads"""
        base_url = "https://example.com/search?q=test&page=1"
        parameter = "q"
        payload = '<script>alert("XSS")</script>'
        
        test_url = scanner._build_test_url(base_url, parameter, payload)
        
        assert "example.com" in test_url
        assert "search" in test_url
        assert payload in test_url or "%3Cscript%3E" in test_url  # URL encoded
        assert "page=1" in test_url  # Other parameters preserved
    
    def test_check_reflection_direct(self, scanner):
        """Test direct payload reflection detection"""
        payload = '<script>alert("XSS")</script>'
        
        # Test direct reflection
        response_with_payload = f'<html><body>User input: {payload}</body></html>'
        assert scanner._check_reflection(response_with_payload, payload) is True
        
        # Test no reflection
        response_without_payload = '<html><body>No user input here</body></html>'
        assert scanner._check_reflection(response_without_payload, payload) is False
    
    def test_check_reflection_encoded(self, scanner):
        """Test encoded payload reflection detection"""
        payload = '<script>alert("XSS")</script>'
        
        # Test URL encoded reflection
        import urllib.parse
        url_encoded = urllib.parse.quote(payload)
        response_url_encoded = f'<html><body>Input: {url_encoded}</body></html>'
        assert scanner._check_reflection(response_url_encoded, payload) is True
        
        # Test HTML encoded reflection
        import html
        html_encoded = html.escape(payload)
        response_html_encoded = f'<html><body>Input: {html_encoded}</body></html>'
        assert scanner._check_reflection(response_html_encoded, payload) is True
    
    def test_check_reflection_partial(self, scanner):
        """Test partial payload reflection detection"""
        payload = '<script>alert("XSS")</script>'
        
        # Test partial reflection (should still detect)
        partial_response = '<html><body>Found: script>alert("XSS")</body></html>'
        assert scanner._check_reflection(partial_response, payload) is True
        
        # Test very small partial (should not detect)
        tiny_partial = '<html><body>Found: ><</body></html>'
        assert scanner._check_reflection(tiny_partial, payload) is False
    
    def test_check_execution_script_tags(self, scanner):
        """Test execution detection in script tags"""
        payload = 'alert("XSS")'
        
        # Test execution within script tags
        script_response = f'<html><head><script>{payload}</script></head></html>'
        assert scanner._check_execution(script_response, payload) is True
        
        # Test execution within inline event handlers
        event_response = f'<html><body><img onclick="{payload}"></body></html>'
        assert scanner._check_execution(event_response, payload) is True
        
        # Test no execution context
        safe_response = f'<html><body>Text: {payload}</body></html>'
        assert scanner._check_execution(safe_response, payload) is False
    
    def test_determine_status_success(self, scanner):
        """Test status determination for successful responses"""
        # Test successful response
        success_response = Mock()
        success_response.status_code = 200
        success_response.text = '<html><body>Normal response</body></html>'
        assert scanner._determine_status(success_response) == ScanStatus.SUCCESS
        
        # Test other 2xx responses
        for code in [201, 202, 204]:
            response = Mock()
            response.status_code = code
            response.text = 'Success'
            assert scanner._determine_status(response) == ScanStatus.SUCCESS
    
    def test_determine_status_blocked(self, scanner):
        """Test status determination for blocked responses"""
        # Test blocked status codes
        for code in [403, 406, 429]:
            blocked_response = Mock()
            blocked_response.status_code = code
            blocked_response.text = 'Blocked'
            assert scanner._determine_status(blocked_response) == ScanStatus.BLOCKED
        
        # Test blocked content detection
        waf_response = Mock()
        waf_response.status_code = 200
        waf_response.text = 'Request blocked by Web Application Firewall'
        assert scanner._determine_status(waf_response) == ScanStatus.BLOCKED
    
    def test_determine_status_failed(self, scanner):
        """Test status determination for failed responses"""
        # Test 4xx and 5xx errors
        for code in [400, 404, 500, 502]:
            error_response = Mock()
            error_response.status_code = code
            error_response.text = 'Error'
            assert scanner._determine_status(error_response) == ScanStatus.FAILED
    
    def test_calculate_confidence(self, scanner):
        """Test confidence score calculation"""
        response = Mock()
        response.status_code = 200
        response.text = '<html><body>Normal</body></html>'
        payload = '<script>alert(1)</script>'
        
        # Test high confidence (reflected and executed)
        high_conf = scanner._calculate_confidence(True, True, response, payload)
        assert high_conf >= 0.8
        
        # Test medium confidence (reflected but not executed)
        med_conf = scanner._calculate_confidence(True, False, response, payload)
        assert 0.3 <= med_conf < 0.8
        
        # Test low confidence (not reflected)
        low_conf = scanner._calculate_confidence(False, False, response, payload)
        assert low_conf < 0.5
        
        # Test filtered response (should reduce confidence)
        filtered_response = Mock()
        filtered_response.status_code = 200
        filtered_response.text = '<html><body>Input filtered</body></html>'
        filtered_conf = scanner._calculate_confidence(True, False, filtered_response, payload)
        normal_conf = scanner._calculate_confidence(True, False, response, payload)
        assert filtered_conf < normal_conf
    
    def test_extract_snippet(self, scanner):
        """Test response snippet extraction"""
        payload = 'alert("XSS")'
        response_text = f'<html><body>Before {payload} After</body></html>'
        
        snippet = scanner._extract_snippet(response_text, payload, context_length=10)
        
        assert snippet is not None
        assert payload in snippet
        assert 'Before' in snippet
        assert 'After' in snippet
        
        # Test payload not found
        no_snippet = scanner._extract_snippet('No payload here', payload)
        assert no_snippet is None
    
    def test_get_common_parameters(self, scanner):
        """Test common parameter generation"""
        params = scanner._get_common_parameters()
        
        assert isinstance(params, dict)
        assert len(params) > 10
        
        # Check for common parameter names
        expected_params = ['q', 'search', 'query', 'input', 'data']
        for param in expected_params:
            assert param in params
            assert isinstance(params[param], list)
    
    @patch('requests.Session.get')
    def test_test_parameter_success(self, mock_get, scanner):
        """Test successful parameter testing"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>Hello <script>alert("XSS")</script></body></html>'
        mock_get.return_value = mock_response
        
        url = "https://example.com/search?q=test"
        parameter = "q"
        payload = '<script>alert("XSS")</script>'
        
        result = scanner._test_parameter(url, parameter, payload)
        
        assert isinstance(result, ScanResult)
        assert result.parameter == parameter
        assert result.payload == payload
        assert result.status == ScanStatus.SUCCESS
        assert result.response_code == 200
        assert result.reflected is True
        assert result.executed is True
        assert result.confidence > 0.7
        assert result.payload_analysis is not None
    
    @patch('requests.Session.get')
    def test_test_parameter_timeout(self, mock_get, scanner):
        """Test parameter testing with timeout"""
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        url = "https://example.com/search?q=test"
        parameter = "q"
        payload = '<script>alert("XSS")</script>'
        
        result = scanner._test_parameter(url, parameter, payload)
        
        assert result.status == ScanStatus.TIMEOUT
        assert result.reflected is False
        assert result.executed is False
        assert result.error_message == "Request timeout"
    
    @patch('requests.Session.get')
    def test_test_parameter_error(self, mock_get, scanner):
        """Test parameter testing with network error"""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        url = "https://example.com/search?q=test"
        parameter = "q"
        payload = '<script>alert("XSS")</script>'
        
        result = scanner._test_parameter(url, parameter, payload)
        
        assert result.status == ScanStatus.ERROR
        assert result.reflected is False
        assert result.executed is False
        assert "Connection failed" in result.error_message
    
    @patch('requests.Session.get')
    def test_scan_url_basic(self, mock_get, scanner):
        """Test basic URL scanning"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>Search results for: <script>alert("XSS")</script></body></html>'
        mock_get.return_value = mock_response
        
        url = "https://example.com/search?q=test&category=all"
        results = scanner.scan_url(url)
        
        assert isinstance(results, list)
        assert len(results) > 0
        
        # Should test multiple payloads on available parameters
        assert len(results) >= 2  # At least 2 parameters * some payloads
        
        # All results should be ScanResult objects
        for result in results:
            assert isinstance(result, ScanResult)
            assert result.parameter in ["q", "category"]
    
    @patch('requests.Session.get')
    def test_scan_url_with_custom_payloads(self, mock_get, scanner):
        """Test URL scanning with custom payloads"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>Test</body></html>'
        mock_get.return_value = mock_response
        
        url = "https://example.com/search?q=test"
        custom_payloads = ['<script>alert(1)</script>', '<img src=x onerror=alert(1)>']
        
        results = scanner.scan_url(url, payloads=custom_payloads)
        
        assert len(results) >= len(custom_payloads)
        
        # Should use our custom payloads
        used_payloads = [r.payload for r in results]
        for payload in custom_payloads:
            assert payload in used_payloads
    
    @patch('requests.Session.get')
    def test_scan_url_with_custom_parameters(self, mock_get, scanner):
        """Test URL scanning with specific parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>Test</body></html>'
        mock_get.return_value = mock_response
        
        url = "https://example.com/search?q=test&category=all&sort=date"
        custom_parameters = ["q", "sort"]
        
        results = scanner.scan_url(url, parameters=custom_parameters)
        
        # Should only test specified parameters
        tested_params = set(r.parameter for r in results)
        assert tested_params.issubset(set(custom_parameters))
        assert "category" not in tested_params
    
    @patch('requests.Session.get')
    def test_scan_advanced(self, mock_get, scanner):
        """Test advanced scanning with polyglots and bypass payloads"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>Test</body></html>'
        mock_get.return_value = mock_response
        
        url = "https://example.com/search?q=test"
        
        # Test with polyglots and bypass payloads
        results = scanner.scan_advanced(url, use_polyglots=True, use_bypass_payloads=True)
        
        assert isinstance(results, list)
        assert len(results) > 0
        
        # Should include various payload types
        used_payloads = [r.payload for r in results]
        assert len(set(used_payloads)) > 10  # Should have diverse payloads
    
    def test_generate_report_empty(self, scanner):
        """Test report generation with no results"""
        report = scanner.generate_report([])
        assert "No scan results to report." in report
    
    def test_generate_report_with_results(self, scanner):
        """Test report generation with actual results"""
        # Create mock results
        results = [
            ScanResult(
                url="https://example.com/test?q=payload1",
                parameter="q",
                payload='<script>alert(1)</script>',
                status=ScanStatus.SUCCESS,
                reflected=True,
                executed=True,
                response_code=200,
                response_time=0.5,
                response_length=1000,
                confidence=0.9
            ),
            ScanResult(
                url="https://example.com/test?q=payload2",
                parameter="q",
                payload='<img src=x onerror=alert(1)>',
                status=ScanStatus.SUCCESS,
                reflected=True,
                executed=False,
                response_code=200,
                response_time=0.3,
                response_length=1000,
                confidence=0.6
            ),
            ScanResult(
                url="https://example.com/test?q=payload3",
                parameter="search",
                payload='javascript:alert(1)',
                status=ScanStatus.BLOCKED,
                reflected=False,
                executed=False,
                response_code=403,
                response_time=0.1,
                response_length=500,
                confidence=0.1
            )
        ]
        
        report = scanner.generate_report(results)
        
        assert "XSS REFLECTION SCAN REPORT" in report
        assert "Total Tests: 3" in report
        assert "Payloads Reflected: 2" in report
        assert "Likely Executed: 1" in report
        assert "Blocked Requests: 1" in report
        assert "HIGH CONFIDENCE FINDINGS" in report
        assert "PARAMETER ANALYSIS" in report
        assert "RECOMMENDATIONS" in report
        
        # Should indicate high risk due to executed payload
        assert "HIGH" in report or "CRITICAL" in report
    
    def test_generate_report_low_risk(self, scanner):
        """Test report generation for low risk scenarios"""
        # Create results with no reflection/execution
        results = [
            ScanResult(
                url="https://example.com/test?q=payload",
                parameter="q",
                payload='<script>alert(1)</script>',
                status=ScanStatus.SUCCESS,
                reflected=False,
                executed=False,
                response_code=200,
                response_time=0.5,
                response_length=1000,
                confidence=0.1
            )
        ]
        
        report = scanner.generate_report(results)
        
        assert "OVERALL RISK LEVEL: LOW" in report
        assert "No obvious XSS vulnerabilities detected" in report
    
    def test_save_results_json(self, scanner, tmp_path):
        """Test saving results in JSON format"""
        # Create mock results
        results = [
            ScanResult(
                url="https://example.com/test?q=payload",
                parameter="q",
                payload='<script>alert(1)</script>',
                status=ScanStatus.SUCCESS,
                reflected=True,
                executed=True,
                response_code=200,
                response_time=0.5,
                response_length=1000,
                confidence=0.9
            )
        ]
        
        output_file = tmp_path / "test_results.json"
        scanner.save_results(results, str(output_file), format_type="json")
        
        assert output_file.exists()
        
        # Verify JSON content
        import json
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["url"] == "https://example.com/test?q=payload"
        assert data[0]["parameter"] == "q"
        assert data[0]["reflected"] is True
        assert data[0]["executed"] is True
    
    def test_save_results_csv(self, scanner, tmp_path):
        """Test saving results in CSV format"""
        results = [
            ScanResult(
                url="https://example.com/test?q=payload",
                parameter="q",
                payload='<script>alert(1)</script>',
                status=ScanStatus.SUCCESS,
                reflected=True,
                executed=True,
                response_code=200,
                response_time=0.5,
                response_length=1000,
                confidence=0.9
            )
        ]
        
        output_file = tmp_path / "test_results.csv"
        scanner.save_results(results, str(output_file), format_type="csv")
        
        assert output_file.exists()
        
        # Verify CSV content
        import csv
        with open(output_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        assert len(rows) == 2  # Header + 1 data row
        assert "URL" in rows[0]  # Header
        assert "Parameter" in rows[0]
        assert "https://example.com/test?q=payload" in rows[1]  # Data
    
    def test_scanner_session_management(self, scanner):
        """Test session management and cleanup"""
        # Check that session exists
        assert hasattr(scanner, 'session')
        assert isinstance(scanner.session, requests.Session)
        
        # Check session headers
        assert 'User-Agent' in scanner.session.headers
        assert scanner.user_agent in scanner.session.headers['User-Agent']
        
        # Test cleanup
        scanner.close()
        # Session should still exist but be closed
        assert hasattr(scanner, 'session')
    
    def test_execution_pattern_matching(self, scanner):
        """Test execution pattern matching"""
        test_cases = [
            ('<script>alert(1)</script>', True),
            ('<img onclick="alert(1)">', True),
            ('javascript:alert(1)', True),
            ('expression(alert(1))', True),
            ('confirm(1)', True),
            ('normal text', False),
            ('<div>safe content</div>', False)
        ]
        
        for text, should_match in test_cases:
            # Use the patterns directly
            found = False
            for pattern in scanner.execution_patterns:
                import re
                if re.search(pattern, text, re.IGNORECASE):
                    found = True
                    break
            
            assert found == should_match, f"Pattern matching failed for: {text}"
    
    def test_blocked_pattern_matching(self, scanner):
        """Test blocked pattern matching"""
        test_cases = [
            ('Access Denied', True),
            ('Request blocked by WAF', True),
            ('Forbidden', True),
            ('CloudFlare security check', True),
            ('mod_security violation', True),
            ('Normal response', False),
            ('Welcome to our site', False)
        ]
        
        for text, should_match in test_cases:
            found = False
            for pattern in scanner.blocked_patterns:
                import re
                if re.search(pattern, text, re.IGNORECASE):
                    found = True
                    break
            
            assert found == should_match, f"Blocked pattern matching failed for: {text}"
    
    @patch('time.sleep')
    def test_delay_between_requests(self, mock_sleep, scanner):
        """Test that delay is respected between requests"""
        scanner.delay = 1.0  # Set 1 second delay
        
        with patch('requests.Session.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = '<html><body>Test</body></html>'
            mock_get.return_value = mock_response
            
            url = "https://example.com/search?q=test"
            payloads = ['<script>alert(1)</script>', '<img src=x onerror=alert(1)>']
            
            scanner.scan_url(url, payloads=payloads)
            
            # Should sleep between requests (but not after the last one)
            assert mock_sleep.call_count >= 1
            mock_sleep.assert_called_with(1.0)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])