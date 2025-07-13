#!/usr/bin/env python3
"""
Tests for XSS Payload Library

This test suite validates the payload library functionality including
payload categorization, searching, filtering, and library management.

Test Categories:
- Unit tests for individual library methods
- Payload content validation tests
- Search and filter functionality tests
- Library statistics and reporting tests
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from payloads.payload_library import (
    PayloadLibrary, PayloadCategory, XSSPayload
)


class TestPayloadLibrary:
    """Test cases for the PayloadLibrary class"""
    
    @pytest.fixture
    def library(self):
        """Create a PayloadLibrary instance for testing"""
        return PayloadLibrary()
    
    def test_library_initialization(self, library):
        """Test that the library initializes with all categories"""
        assert isinstance(library.payloads, dict)
        
        # Check that all categories are present
        for category in PayloadCategory:
            assert category in library.payloads
            assert isinstance(library.payloads[category], list)
        
        # Check that we have payloads in each category
        for category in PayloadCategory:
            assert len(library.payloads[category]) > 0
    
    def test_payload_data_integrity(self, library):
        """Test that all payloads have required fields and valid data"""
        for category, payloads in library.payloads.items():
            for payload in payloads:
                # Check required fields
                assert isinstance(payload.payload, str)
                assert len(payload.payload) > 0
                assert isinstance(payload.category, PayloadCategory)
                assert payload.category == category
                assert isinstance(payload.description, str)
                assert len(payload.description) > 0
                assert isinstance(payload.contexts, list)
                assert len(payload.contexts) > 0
                assert isinstance(payload.bypass_techniques, list)
                assert isinstance(payload.success_rate, float)
                assert 0.0 <= payload.success_rate <= 1.0
                assert isinstance(payload.source, str)
                assert len(payload.source) > 0
                assert payload.severity in ["low", "medium", "high", "critical"]
                assert isinstance(payload.requires_interaction, bool)
    
    def test_get_payloads_by_category(self, library):
        """Test retrieving payloads by category"""
        # Test each category
        for category in PayloadCategory:
            payloads = library.get_payloads_by_category(category)
            assert isinstance(payloads, list)
            assert len(payloads) > 0
            
            # All payloads should belong to the requested category
            for payload in payloads:
                assert payload.category == category
        
        # Test invalid category
        empty_payloads = library.get_payloads_by_category("invalid")
        assert empty_payloads == []
    
    def test_get_payloads_by_context(self, library):
        """Test retrieving payloads by injection context"""
        test_contexts = [
            "html_content",
            "attribute_value",
            "javascript_string",
            "url_parameter"
        ]
        
        for context in test_contexts:
            payloads = library.get_payloads_by_context(context)
            assert isinstance(payloads, list)
            
            # All payloads should support the requested context
            for payload in payloads:
                assert context in payload.contexts
            
            # Should be sorted by success rate (descending)
            if len(payloads) > 1:
                success_rates = [p.success_rate for p in payloads]
                assert success_rates == sorted(success_rates, reverse=True)
    
    def test_get_payloads_by_bypass_technique(self, library):
        """Test retrieving payloads by bypass technique"""
        # First, find what techniques are available
        all_techniques = set()
        for category_payloads in library.payloads.values():
            for payload in category_payloads:
                all_techniques.update(payload.bypass_techniques)
        
        # Test a few techniques
        test_techniques = list(all_techniques)[:5]
        
        for technique in test_techniques:
            payloads = library.get_payloads_by_bypass_technique(technique)
            assert isinstance(payloads, list)
            
            # All payloads should use the requested technique
            for payload in payloads:
                assert technique in payload.bypass_techniques
    
    def test_get_payloads_by_severity(self, library):
        """Test retrieving payloads by severity level"""
        severity_levels = ["low", "medium", "high", "critical"]
        
        for severity in severity_levels:
            payloads = library.get_payloads_by_severity(severity)
            assert isinstance(payloads, list)
            
            # All payloads should have the requested severity
            for payload in payloads:
                assert payload.severity == severity
    
    def test_get_best_payloads(self, library):
        """Test retrieving highest success rate payloads"""
        # Test default limit
        best_payloads = library.get_best_payloads()
        assert len(best_payloads) <= 10
        assert isinstance(best_payloads, list)
        
        # Should be sorted by success rate (descending)
        if len(best_payloads) > 1:
            success_rates = [p.success_rate for p in best_payloads]
            assert success_rates == sorted(success_rates, reverse=True)
        
        # Test custom limit
        best_5 = library.get_best_payloads(limit=5)
        assert len(best_5) <= 5
        
        # Test limit larger than total payloads
        all_payloads_count = sum(len(payloads) for payloads in library.payloads.values())
        best_large = library.get_best_payloads(limit=all_payloads_count + 100)
        assert len(best_large) == all_payloads_count
    
    def test_get_random_payloads(self, library):
        """Test retrieving random payloads"""
        # Test default count
        random_payloads = library.get_random_payloads()
        assert len(random_payloads) <= 5
        assert isinstance(random_payloads, list)
        
        # Test custom count
        random_10 = library.get_random_payloads(count=10)
        assert len(random_10) <= 10
        
        # Test with specific category
        basic_random = library.get_random_payloads(count=3, category=PayloadCategory.BASIC)
        assert len(basic_random) <= 3
        for payload in basic_random:
            assert payload.category == PayloadCategory.BASIC
        
        # Test randomness (run multiple times, should get different results)
        results = [library.get_random_payloads(count=3) for _ in range(5)]
        # At least some results should be different (very high probability)
        unique_results = set(tuple(p.payload for p in result) for result in results)
        assert len(unique_results) > 1 or len(results[0]) <= 1
    
    def test_search_payloads(self, library):
        """Test payload search functionality"""
        # Test search by common terms
        search_terms = ["alert", "script", "img", "svg", "javascript"]
        
        for term in search_terms:
            results = library.search_payloads(term)
            assert isinstance(results, list)
            
            # All results should contain the search term
            for payload in results:
                term_lower = term.lower()
                assert (term_lower in payload.payload.lower() or
                       term_lower in payload.description.lower() or
                       term_lower in payload.source.lower() or
                       (payload.notes and term_lower in payload.notes.lower()))
        
        # Test case insensitive search
        upper_results = library.search_payloads("ALERT")
        lower_results = library.search_payloads("alert")
        assert len(upper_results) == len(lower_results)
        
        # Test search for non-existent term
        no_results = library.search_payloads("nonexistentterm12345")
        assert no_results == []
    
    def test_get_payload_stats(self, library):
        """Test payload statistics generation"""
        stats = library.get_payload_stats()
        
        # Check required fields
        assert "total_payloads" in stats
        assert "categories" in stats
        assert "avg_success_rate" in stats
        
        # Check category counts
        for category in PayloadCategory:
            category_key = f"{category.value}_count"
            assert category_key in stats
            assert stats[category_key] >= 0
        
        # Check severity distribution
        for severity in ["low", "medium", "high", "critical"]:
            assert severity in stats
            assert stats[severity] >= 0
        
        # Validate totals
        total_from_categories = sum(stats[f"{cat.value}_count"] for cat in PayloadCategory)
        assert stats["total_payloads"] == total_from_categories
        
        total_from_severity = sum(stats[sev] for sev in ["low", "medium", "high", "critical"])
        assert stats["total_payloads"] == total_from_severity
        
        # Validate average success rate
        assert 0.0 <= stats["avg_success_rate"] <= 1.0
    
    def test_generate_payload_report(self, library):
        """Test payload report generation"""
        report = library.generate_payload_report()
        
        assert isinstance(report, str)
        assert "XSS PAYLOAD LIBRARY REPORT" in report
        assert "Total Payloads:" in report
        assert "CATEGORY BREAKDOWN:" in report
        assert "SEVERITY DISTRIBUTION:" in report
        assert "TOP PAYLOADS BY CATEGORY:" in report
        
        # Should contain information about each category
        for category in PayloadCategory:
            assert category.value.title() in report
    
    def test_export_payloads_list_format(self, library):
        """Test exporting payloads in list format"""
        # Export all payloads
        exported = library.export_payloads(format_type="list")
        assert isinstance(exported, list)
        assert len(exported) > 0
        assert all(isinstance(payload, str) for payload in exported)
        
        # Export specific category
        basic_exported = library.export_payloads(category=PayloadCategory.BASIC, format_type="list")
        assert isinstance(basic_exported, list)
        assert len(basic_exported) > 0
        
        # Should match the number of basic payloads
        basic_payloads = library.get_payloads_by_category(PayloadCategory.BASIC)
        assert len(basic_exported) == len(basic_payloads)
    
    def test_export_payloads_csv_format(self, library):
        """Test exporting payloads in CSV format"""
        exported = library.export_payloads(format_type="csv")
        assert isinstance(exported, list)
        assert len(exported) > 1  # Should have header + data rows
        
        # Check header
        header = exported[0]
        assert "payload" in header
        assert "category" in header
        assert "description" in header
        assert "success_rate" in header
        assert "severity" in header
        
        # Check data rows
        for row in exported[1:]:
            assert row.count(',') >= 4  # Should have at least 5 fields
    
    def test_export_payloads_json_format(self, library):
        """Test exporting payloads in JSON format"""
        import json
        
        exported = library.export_payloads(format_type="json", category=PayloadCategory.BASIC)
        assert isinstance(exported, list)
        assert len(exported) > 0
        
        # Each item should be valid JSON
        for json_str in exported:
            payload_data = json.loads(json_str)
            assert "payload" in payload_data
            assert "category" in payload_data
            assert "description" in payload_data
            assert "success_rate" in payload_data
            assert "severity" in payload_data
    
    def test_validate_payload_library(self, library):
        """Test payload library validation"""
        issues = library.validate_payload_library()
        
        assert isinstance(issues, dict)
        assert "duplicates" in issues
        assert "missing_data" in issues
        assert "invalid_rates" in issues
        assert "empty_contexts" in issues
        
        # All issue lists should be lists
        for issue_list in issues.values():
            assert isinstance(issue_list, list)
        
        # Ideally, there should be no issues (but we don't enforce this in tests)
        # The validation method is working if it returns the correct structure
    
    def test_basic_payload_quality(self, library):
        """Test that basic payloads meet quality standards"""
        basic_payloads = library.get_payloads_by_category(PayloadCategory.BASIC)
        
        # Should have reasonable number of basic payloads
        assert len(basic_payloads) >= 5
        
        # Basic payloads should have good success rates
        avg_success_rate = sum(p.success_rate for p in basic_payloads) / len(basic_payloads)
        assert avg_success_rate >= 0.6
        
        # Should include common XSS vectors
        payload_strings = [p.payload.lower() for p in basic_payloads]
        assert any('<script>' in payload for payload in payload_strings)
        assert any('<img' in payload and 'onerror' in payload for payload in payload_strings)
        assert any('javascript:' in payload for payload in payload_strings)
    
    def test_bypass_payload_quality(self, library):
        """Test that bypass payloads have appropriate bypass techniques"""
        bypass_payloads = library.get_payloads_by_category(PayloadCategory.BYPASS)
        
        # Should have bypass payloads
        assert len(bypass_payloads) >= 5
        
        # All bypass payloads should have bypass techniques
        for payload in bypass_payloads:
            assert len(payload.bypass_techniques) > 0
    
    def test_polyglot_payload_quality(self, library):
        """Test that polyglot payloads work in multiple contexts"""
        polyglot_payloads = library.get_payloads_by_category(PayloadCategory.POLYGLOT)
        
        # Should have polyglot payloads
        assert len(polyglot_payloads) >= 3
        
        # Polyglot payloads should work in multiple contexts
        for payload in polyglot_payloads:
            assert len(payload.contexts) >= 2
    
    def test_advanced_payload_quality(self, library):
        """Test that advanced payloads use modern techniques"""
        advanced_payloads = library.get_payloads_by_category(PayloadCategory.ADVANCED)
        
        # Should have advanced payloads
        assert len(advanced_payloads) >= 5
        
        # Should include HTML5 techniques
        payload_strings = [p.payload.lower() for p in advanced_payloads]
        html5_elements = ['<video>', '<audio>', '<details>', '<template>', '<math>']
        assert any(any(elem in payload for elem in html5_elements) for payload in payload_strings)
    
    def test_stored_payload_characteristics(self, library):
        """Test that stored payloads have appropriate characteristics"""
        stored_payloads = library.get_payloads_by_category(PayloadCategory.STORED)
        
        # Should have stored payloads
        assert len(stored_payloads) >= 3
        
        # Stored payloads should often be high/critical severity
        high_severity_count = sum(1 for p in stored_payloads if p.severity in ["high", "critical"])
        assert high_severity_count >= len(stored_payloads) // 2
    
    def test_blind_payload_characteristics(self, library):
        """Test that blind payloads have callback mechanisms"""
        blind_payloads = library.get_payloads_by_category(PayloadCategory.BLIND)
        
        # Should have blind payloads
        assert len(blind_payloads) >= 3
        
        # Blind payloads should contain external references or callbacks
        for payload in blind_payloads:
            payload_lower = payload.payload.lower()
            has_callback = any(indicator in payload_lower for indicator in [
                'fetch(', 'new image()', 'websocket', 'beacon', '://', 'sendbea', 'location='
            ])
            assert has_callback, f"Blind payload should have callback mechanism: {payload.payload}"
    
    def test_payload_uniqueness(self, library):
        """Test that payloads are unique across the library"""
        all_payloads = []
        for category_payloads in library.payloads.values():
            all_payloads.extend(category_payloads)
        
        payload_strings = [p.payload for p in all_payloads]
        unique_payloads = set(payload_strings)
        
        # Should have minimal duplicates (some duplicates might be intentional)
        duplicate_count = len(payload_strings) - len(unique_payloads)
        duplicate_percentage = duplicate_count / len(payload_strings)
        assert duplicate_percentage < 0.1, f"Too many duplicate payloads: {duplicate_percentage:.1%}"
    
    def test_context_coverage(self, library):
        """Test that the library covers all important contexts"""
        important_contexts = [
            "html_content",
            "attribute_value", 
            "javascript_string",
            "url_parameter",
            "script_content",
            "event_handler"
        ]
        
        for context in important_contexts:
            context_payloads = library.get_payloads_by_context(context)
            assert len(context_payloads) >= 3, f"Insufficient coverage for context: {context}"
    
    def test_bypass_technique_coverage(self, library):
        """Test that the library covers important bypass techniques"""
        important_techniques = [
            "case_variation",
            "encoded_chars",
            "unicode_encoding",
            "protocol_confusion",
            "attribute_breaking",
            "whitespace_abuse"
        ]
        
        for technique in important_techniques:
            technique_payloads = library.get_payloads_by_bypass_technique(technique)
            assert len(technique_payloads) >= 1, f"No payloads for technique: {technique}"
    
    def test_library_size_and_completeness(self, library):
        """Test that the library has a reasonable size and completeness"""
        stats = library.get_payload_stats()
        
        # Should have a reasonable total number of payloads
        assert stats["total_payloads"] >= 50, "Library should have at least 50 payloads"
        assert stats["total_payloads"] <= 200, "Library shouldn't be too large for initial version"
        
        # Should have payloads in all categories
        for category in PayloadCategory:
            category_count = stats[f"{category.value}_count"]
            assert category_count >= 3, f"Category {category.value} should have at least 3 payloads"
        
        # Should have good distribution across severity levels
        for severity in ["low", "medium", "high", "critical"]:
            assert stats[severity] > 0, f"Should have some {severity} severity payloads"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])