"""
Reflection-based XSS Scanner

This scanner tests for reflected XSS vulnerabilities by injecting payloads
into parameters and analyzing responses for reflection. It includes:
- Parameter discovery and testing
- Context-aware payload selection
- Response analysis and evidence collection
- Rate limiting and ethical testing practices
- Professional vulnerability reporting

The scanner follows responsible disclosure practices and includes
safeguards to prevent abuse.
"""

import requests
import time
import re
import html
import urllib.parse
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Local imports
from ..core.payload_analyzer import PayloadAnalyzer, PayloadAnalysis
from ..payloads.payload_library import PayloadLibrary, PayloadCategory, XSSPayload

logger = logging.getLogger(__name__)


@dataclass
class XSSTestResult:
    """Result of an XSS test against a specific parameter"""
    url: str
    parameter: str
    payload: str
    method: str  # GET, POST, etc.
    success: bool
    confidence: float  # 0.0 to 1.0
    response_code: int
    response_time: float
    evidence: str
    context: str
    bypass_techniques: List[str]
    payload_analysis: Optional[PayloadAnalysis]
    timestamp: float
    error: Optional[str] = None


@dataclass
class ScanConfiguration:
    """Configuration for XSS scanning"""
    delay_between_requests: float = 1.0
    max_concurrent_requests: int = 5
    request_timeout: int = 10
    max_payload_length: int = 1000
    test_get_parameters: bool = True
    test_post_parameters: bool = True
    test_headers: bool = False
    follow_redirects: bool = True
    verify_ssl: bool = True
    max_redirects: int = 5
    user_agent: str = "XSS-Scanner/1.0 (Educational Security Testing Tool)"


class ReflectionScanner:
    """
    Advanced reflection-based XSS scanner with intelligent payload selection.
    
    This scanner automatically discovers parameters, selects appropriate payloads
    based on context analysis, and provides detailed vulnerability reports.
    
    Features:
    - Automatic parameter discovery
    - Context-aware payload selection
    - Intelligent response analysis
    - Rate limiting and ethical testing
    - Comprehensive reporting
    
    Example:
        scanner = ReflectionScanner("https://example.com", delay=1.0)
        results = scanner.scan_url("https://example.com/search", ["q", "category"])
        report = scanner.generate_report()
    """
    
    def __init__(self, base_url: str, config: Optional[ScanConfiguration] = None):
        self.base_url = base_url
        self.config = config or ScanConfiguration()
        
        # Initialize components
        self.session = self._create_session()
        self.payload_analyzer = PayloadAnalyzer()
        self.payload_library = PayloadLibrary()
        
        # Results storage
        self.results: List[XSSTestResult] = []
        self.scan_stats = {
            'total_requests': 0,
            'successful_injections': 0,
            'parameters_tested': 0,
            'start_time': None,
            'end_time': None
        }
        
        logger.info(f"ReflectionScanner initialized for {base_url}")
    
    def _create_session(self) -> requests.Session:
        """Create configured HTTP session"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': self.config.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache'
        })
        
        # Configure session settings
        session.verify = self.config.verify_ssl
        session.allow_redirects = self.config.follow_redirects
        session.max_redirects = self.config.max_redirects
        
        return session
    
    def scan_url(self, url: str, parameters: Optional[List[str]] = None) -> List[XSSTestResult]:
        """
        Scan a specific URL for XSS vulnerabilities.
        
        Args:
            url: Target URL to scan
            parameters: List of parameters to test (auto-discovered if None)
            
        Returns:
            List of XSSTestResult objects
        """
        logger.info(f"🎯 Starting XSS scan of {url}")
        self.scan_stats['start_time'] = time.time()
        
        try:
            # Discover parameters if not provided
            if parameters is None:
                parameters = self._discover_parameters(url)
                
            if not parameters:
                logger.warning(f"No parameters found to test for {url}")
                return []
            
            logger.info(f"Testing {len(parameters)} parameters: {parameters}")
            
            # Test each parameter
            scan_results = []
            for param in parameters:
                logger.info(f"  🔍 Testing parameter: {param}")
                param_results = self._test_parameter(url, param)
                scan_results.extend(param_results)
                self.scan_stats['parameters_tested'] += 1
                
                # Rate limiting
                time.sleep(self.config.delay_between_requests)
            
            self.results.extend(scan_results)
            return scan_results
            
        except Exception as e:
            logger.error(f"Error during scan: {e}")
            return []
        finally:
            self.scan_stats['end_time'] = time.time()
    
    def _discover_parameters(self, url: str) -> List[str]:
        """Discover parameters by analyzing the page and common patterns"""
        discovered_params = set()
        
        try:
            # Get the page content
            response = self.session.get(url, timeout=self.config.request_timeout)
            content = response.text
            
            # Extract parameters from forms
            form_params = self._extract_form_parameters(content)
            discovered_params.update(form_params)
            
            # Extract parameters from existing URL
            url_params = self._extract_url_parameters(url)
            discovered_params.update(url_params)
            
            # Add common parameter names
            common_params = {
                'q', 'search', 'query', 'keyword', 'term',
                'name', 'username', 'email', 'message', 'comment',
                'id', 'page', 'category', 'tag', 'filter',
                'input', 'data', 'value', 'text', 'content',
                'title', 'description', 'url', 'link'
            }
            
            # Only add common params that seem relevant
            for param in common_params:
                if param in content.lower():
                    discovered_params.add(param)
            
            logger.info(f"Discovered {len(discovered_params)} parameters")
            return list(discovered_params)
            
        except Exception as e:
            logger.error(f"Error discovering parameters: {e}")
            return ['q', 'search', 'test']  # Fallback parameters
    
    def _extract_form_parameters(self, html_content: str) -> Set[str]:
        """Extract parameter names from HTML forms"""
        params = set()
        
        # Find input fields
        input_pattern = r'<input[^>]+name=["\']([^"\']+)["\'][^>]*>'
        matches = re.findall(input_pattern, html_content, re.IGNORECASE)
        params.update(matches)
        
        # Find textarea fields
        textarea_pattern = r'<textarea[^>]+name=["\']([^"\']+)["\'][^>]*>'
        matches = re.findall(textarea_pattern, html_content, re.IGNORECASE)
        params.update(matches)
        
        # Find select fields
        select_pattern = r'<select[^>]+name=["\']([^"\']+)["\'][^>]*>'
        matches = re.findall(select_pattern, html_content, re.IGNORECASE)
        params.update(matches)
        
        return params
    
    def _extract_url_parameters(self, url: str) -> Set[str]:
        """Extract parameter names from URL query string"""
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        return set(query_params.keys())
    
    def _test_parameter(self, url: str, parameter: str) -> List[XSSTestResult]:
        """Test a specific parameter with multiple payloads"""
        results = []
        
        # Start with basic payloads
        basic_payloads = self.payload_library.get_payloads_by_category(PayloadCategory.BASIC)
        
        for payload_obj in basic_payloads[:5]:  # Test first 5 basic payloads
            result = self._test_single_payload(url, parameter, payload_obj)
            results.append(result)
            
            if result.success:
                logger.info(f"    ✅ XSS found with basic payload: {payload_obj.payload[:50]}...")
                # If basic payload works, try bypass techniques
                bypass_results = self._test_bypass_payloads(url, parameter)
                results.extend(bypass_results)
                break
            
            # Rate limiting between payloads
            time.sleep(self.config.delay_between_requests)
        
        return results
    
    def _test_single_payload(self, url: str, parameter: str, payload_obj: XSSPayload) -> XSSTestResult:
        """Test a single payload against a parameter"""
        start_time = time.time()
        self.scan_stats['total_requests'] += 1
        
        try:
            # Prepare test request
            if self.config.test_get_parameters:
                test_url = f"{url}?{parameter}={urllib.parse.quote(payload_obj.payload)}"
                response = self.session.get(test_url, timeout=self.config.request_timeout)
                method = "GET"
            else:
                # POST method testing would go here
                method = "GET"  # For now, default to GET
                response = self.session.get(url, timeout=self.config.request_timeout)
            
            response_time = time.time() - start_time
            
            # Analyze response for XSS
            success, confidence, evidence, context = self._analyze_response(
                payload_obj.payload, response.text, response.headers
            )
            
            if success:
                self.scan_stats['successful_injections'] += 1
            
            # Analyze the payload
            payload_analysis = self.payload_analyzer.analyze_payload(payload_obj.payload)
            
            return XSSTestResult(
                url=test_url if method == "GET" else url,
                parameter=parameter,
                payload=payload_obj.payload,
                method=method,
                success=success,
                confidence=confidence,
                response_code=response.status_code,
                response_time=response_time,
                evidence=evidence,
                context=context,
                bypass_techniques=payload_obj.bypass_techniques,
                payload_analysis=payload_analysis,
                timestamp=time.time()
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            logger.error(f"Error testing payload {payload_obj.payload[:30]}...: {e}")
            
            return XSSTestResult(
                url=url,
                parameter=parameter,
                payload=payload_obj.payload,
                method="GET",
                success=False,
                confidence=0.0,
                response_code=0,
                response_time=response_time,
                evidence="",
                context="error",
                bypass_techniques=payload_obj.bypass_techniques,
                payload_analysis=None,
                timestamp=time.time(),
                error=str(e)
            )
    
    def _analyze_response(self, payload: str, response_text: str, headers: Dict) -> Tuple[bool, float, str, str]:
        """
        Analyze HTTP response for XSS vulnerability indicators.
        
        Returns:
            (success, confidence, evidence, context)
        """
        # Check for direct reflection
        if payload in response_text:
            confidence = 0.9
            evidence = self._extract_evidence(payload, response_text)
            context = self._determine_reflection_context(payload, response_text)
            return True, confidence, evidence, context
        
        # Check for HTML-encoded reflection
        html_encoded = html.escape(payload)
        if html_encoded in response_text:
            confidence = 0.7
            evidence = self._extract_evidence(html_encoded, response_text)
            context = "html_encoded"
            return True, confidence, evidence, context
        
        # Check for URL-encoded reflection
        url_encoded = urllib.parse.quote(payload)
        if url_encoded in response_text:
            confidence = 0.6
            evidence = self._extract_evidence(url_encoded, response_text)
            context = "url_encoded"
            return True, confidence, evidence, context
        
        # Check for partial reflection (might indicate filtering)
        payload_words = payload.split()
        partial_matches = sum(1 for word in payload_words if word in response_text)
        if partial_matches > 0 and len(payload_words) > 1:
            confidence = 0.3 + (partial_matches / len(payload_words)) * 0.4
            evidence = f"Partial reflection: {partial_matches}/{len(payload_words)} words found"
            context = "partial_reflection"
            return True, confidence, evidence, context
        
        return False, 0.0, "", "no_reflection"
    
    def _extract_evidence(self, payload: str, response_text: str) -> str:
        """Extract evidence of payload reflection from response"""
        lines = response_text.split('\n')
        evidence_lines = []
        
        for i, line in enumerate(lines):
            if payload in line:
                # Include surrounding context
                start = max(0, i - 2)
                end = min(len(lines), i + 3)
                context_lines = lines[start:end]
                
                # Highlight the payload in the evidence
                for j, context_line in enumerate(context_lines):
                    if payload in context_line:
                        highlighted = context_line.replace(payload, f"**{payload}**")
                        context_lines[j] = highlighted
                
                evidence_lines.extend(context_lines)
                break
        
        if evidence_lines:
            return '\n'.join(evidence_lines)
        else:
            return f"Payload '{payload}' found in response"
    
    def _determine_reflection_context(self, payload: str, response_text: str) -> str:
        """Determine the HTML context where payload is reflected"""
        # Find the line containing the payload
        for line in response_text.split('\n'):
            if payload in line:
                line_lower = line.lower()
                
                # Check various contexts
                if '<script' in line_lower and '</script>' in line_lower:
                    return "script_tag"
                elif any(f'on{event}=' in line_lower for event in ['load', 'error', 'click', 'mouseover']):
                    return "event_handler"
                elif 'href=' in line_lower or 'src=' in line_lower:
                    return "attribute_value"
                elif '<!--' in line and '-->' in line:
                    return "html_comment"
                elif '<style' in line_lower:
                    return "css_context"
                else:
                    return "html_content"
        
        return "unknown_context"
    
    def _test_bypass_payloads(self, url: str, parameter: str) -> List[XSSTestResult]:
        """Test bypass payloads if basic payload worked"""
        logger.info(f"    🔧 Testing bypass techniques for {parameter}...")
        
        bypass_payloads = self.payload_library.get_payloads_by_category(PayloadCategory.BYPASS)
        results = []
        
        for payload_obj in bypass_payloads[:3]:  # Test first 3 bypass payloads
            result = self._test_single_payload(url, parameter, payload_obj)
            results.append(result)
            
            if result.success:
                logger.info(f"    🚀 Bypass successful: {payload_obj.description}")
            
            time.sleep(self.config.delay_between_requests)
        
        return results
    
    def scan_multiple_urls(self, urls: List[str]) -> Dict[str, List[XSSTestResult]]:
        """Scan multiple URLs concurrently"""
        logger.info(f"Scanning {len(urls)} URLs...")
        all_results = {}
        
        with ThreadPoolExecutor(max_workers=self.config.max_concurrent_requests) as executor:
            future_to_url = {executor.submit(self.scan_url, url): url for url in urls}
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    results = future.result()
                    if results:
                        all_results[url] = results
                except Exception as e:
                    logger.error(f"Error scanning {url}: {e}")
        
        return all_results
    
    def generate_report(self, format: str = "text") -> str:
        """Generate comprehensive scan report"""
        if not self.results:
            return "No XSS scan results available."
        
        successful_results = [r for r in self.results if r.success]
        total_scan_time = (self.scan_stats.get('end_time', time.time()) - 
                          self.scan_stats.get('start_time', time.time()))
        
        if format == "text":
            return self._generate_text_report(successful_results, total_scan_time)
        elif format == "json":
            return self._generate_json_report(successful_results, total_scan_time)
        else:
            raise ValueError(f"Unsupported report format: {format}")
    
    def _generate_text_report(self, successful_results: List[XSSTestResult], scan_time: float) -> str:
        """Generate text-based vulnerability report"""
        report = f"""
XSS Vulnerability Scan Report
=============================

Target: {self.base_url}
Scan Duration: {scan_time:.2f} seconds
Total Requests: {self.scan_stats['total_requests']}
Parameters Tested: {self.scan_stats['parameters_tested']}
Vulnerabilities Found: {len(successful_results)}

"""
        
        if successful_results:
            report += "VULNERABILITIES FOUND:\n"
            report += "=" * 50 + "\n\n"
            
            for i, result in enumerate(successful_results, 1):
                severity = "HIGH" if result.confidence > 0.8 else "MEDIUM" if result.confidence > 0.5 else "LOW"
                
                report += f"[{i}] {severity} - XSS in '{result.parameter}' parameter\n"
                report += f"URL: {result.url}\n"
                report += f"Payload: {result.payload}\n"
                report += f"Context: {result.context}\n"
                report += f"Confidence: {result.confidence:.2f}\n"
                report += f"Response Code: {result.response_code}\n"
                
                if result.bypass_techniques:
                    report += f"Bypass Techniques: {', '.join(result.bypass_techniques)}\n"
                
                report += f"Evidence:\n{result.evidence}\n"
                report += "-" * 50 + "\n\n"
        else:
            report += "No XSS vulnerabilities detected.\n"
        
        # Add recommendations
        report += self._generate_recommendations(successful_results)
        
        return report
    
    def _generate_json_report(self, successful_results: List[XSSTestResult], scan_time: float) -> str:
        """Generate JSON-formatted vulnerability report"""
        import json
        
        report_data = {
            "scan_info": {
                "target": self.base_url,
                "scan_duration": scan_time,
                "total_requests": self.scan_stats['total_requests'],
                "parameters_tested": self.scan_stats['parameters_tested'],
                "vulnerabilities_found": len(successful_results)
            },
            "vulnerabilities": []
        }
        
        for result in successful_results:
            vuln_data = {
                "url": result.url,
                "parameter": result.parameter,
                "payload": result.payload,
                "method": result.method,
                "confidence": result.confidence,
                "context": result.context,
                "response_code": result.response_code,
                "response_time": result.response_time,
                "evidence": result.evidence,
                "bypass_techniques": result.bypass_techniques,
                "timestamp": result.timestamp
            }
            
            if result.payload_analysis:
                vuln_data["payload_analysis"] = {
                    "risk_level": result.payload_analysis.risk_level,
                    "contexts": [ctx.value for ctx in result.payload_analysis.contexts],
                    "xss_types": [xss_type.value for xss_type in result.payload_analysis.xss_types]
                }
            
            report_data["vulnerabilities"].append(vuln_data)
        
        return json.dumps(report_data, indent=2)
    
    def _generate_recommendations(self, successful_results: List[XSSTestResult]) -> str:
        """Generate remediation recommendations"""
        if not successful_results:
            return ""
        
        recommendations = """
REMEDIATION RECOMMENDATIONS:
===========================

1. INPUT VALIDATION
   - Implement strict input validation for all user parameters
   - Use whitelist validation where possible
   - Reject or sanitize dangerous characters: < > " ' & 

2. OUTPUT ENCODING
   - HTML encode all user data before output
   - Use context-appropriate encoding (HTML, JavaScript, URL)
   - Consider using template engines with auto-escaping

3. CONTENT SECURITY POLICY (CSP)
   - Implement a strict Content Security Policy
   - Use 'nonce' or 'strict-dynamic' for inline scripts
   - Disable 'unsafe-inline' and 'unsafe-eval'

4. SECURE DEVELOPMENT
   - Use security-focused frameworks and libraries
   - Implement automated security testing in CI/CD
   - Regular security code reviews

5. TESTING
   - Implement regular XSS testing
   - Use both automated tools and manual testing
   - Test all user input points and parameters

"""
        
        # Add specific recommendations based on found vulnerabilities
        contexts_found = set(result.context for result in successful_results)
        
        if "script_tag" in contexts_found:
            recommendations += "⚠️  CRITICAL: Script tag injection found - implement immediate output encoding\n"
        
        if "event_handler" in contexts_found:
            recommendations += "⚠️  HIGH: Event handler injection found - validate attribute values\n"
        
        if any("bypass" in ' '.join(result.bypass_techniques) for result in successful_results):
            recommendations += "⚠️  WARNING: Bypass techniques successful - review and strengthen filters\n"
        
        return recommendations
    
    def export_results(self, filename: str, format: str = "json"):
        """Export scan results to file"""
        if format == "json":
            report = self._generate_json_report([r for r in self.results if r.success], 0)
        else:
            report = self.generate_report(format)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Scan results exported to {filename}")
    
    def get_statistics(self) -> Dict[str, any]:
        """Get comprehensive scan statistics"""
        successful_results = [r for r in self.results if r.success]
        
        stats = {
            'total_tests': len(self.results),
            'successful_injections': len(successful_results),
            'success_rate': len(successful_results) / len(self.results) if self.results else 0,
            'average_confidence': sum(r.confidence for r in successful_results) / len(successful_results) if successful_results else 0,
            'contexts_found': list(set(r.context for r in successful_results)),
            'parameters_vulnerable': list(set(r.parameter for r in successful_results)),
            'bypass_techniques_successful': list(set(
                tech for r in successful_results for tech in r.bypass_techniques
            )),
            'scan_duration': (self.scan_stats.get('end_time', time.time()) - 
                            self.scan_stats.get('start_time', time.time())),
            'requests_per_second': (self.scan_stats['total_requests'] / 
                                  max(1, (self.scan_stats.get('end_time', time.time()) - 
                                        self.scan_stats.get('start_time', time.time()))))
        }
        
        return stats