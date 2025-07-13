"""
XSS Payload Analyzer - Advanced payload analysis and categorization.

This module provides comprehensive analysis of XSS payloads, including:
- Context detection (HTML, JavaScript, CSS, etc.)
- XSS type classification (reflected, stored, DOM-based)
- Bypass technique identification
- Risk level assessment
- Proof-of-concept generation

The analyzer helps security researchers and developers understand payload
capabilities and potential impact.
"""

import re
import html
import urllib.parse
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class XSSType(Enum):
    """Different types of XSS vulnerabilities"""
    REFLECTED = "reflected"
    STORED = "stored"
    DOM_BASED = "dom_based"
    UNIVERSAL = "universal"


class Context(Enum):
    """Where the payload gets injected in HTML"""
    HTML_CONTENT = "html_content"          # <div>PAYLOAD</div>
    ATTRIBUTE_VALUE = "attribute_value"    # <div id="PAYLOAD">
    JAVASCRIPT_STRING = "js_string"        # var x = "PAYLOAD";
    JAVASCRIPT_VARIABLE = "js_variable"    # var PAYLOAD = 1;
    CSS_VALUE = "css_value"               # style="color:PAYLOAD"
    URL_PARAMETER = "url_parameter"       # ?param=PAYLOAD
    HTML_COMMENT = "html_comment"         # <!-- PAYLOAD -->
    UNKNOWN = "unknown"


@dataclass
class PayloadAnalysis:
    """Analysis results for an XSS payload"""
    payload: str
    contexts: List[Context]
    xss_types: List[XSSType]
    bypass_techniques: List[str]
    risk_level: str  # "low", "medium", "high", "critical"
    explanation: str
    proof_of_concept: str
    confidence_score: float  # 0.0 to 1.0
    metadata: Dict[str, any]


class PayloadAnalyzer:
    """
    Analyzes XSS payloads and determines their capabilities.
    
    The analyzer uses pattern matching and heuristics to identify:
    - Injection contexts where the payload might work
    - Types of XSS vulnerabilities it could exploit
    - Bypass techniques employed
    - Overall risk level and confidence
    
    Example:
        analyzer = PayloadAnalyzer()
        analysis = analyzer.analyze_payload('<script>alert("XSS")</script>')
        print(f"Risk: {analysis.risk_level}, Contexts: {analysis.contexts}")
    """
    
    def __init__(self):
        # Common HTML tags that can execute JavaScript
        self.script_tags = {
            'script', 'img', 'svg', 'iframe', 'object', 'embed', 
            'video', 'audio', 'source', 'track', 'input', 'body',
            'html', 'meta', 'link', 'style', 'form', 'details',
            'math', 'template', 'canvas', 'marquee'
        }
        
        # JavaScript event handlers
        self.event_handlers = {
            'onload', 'onerror', 'onclick', 'onmouseover', 'onfocus',
            'onblur', 'onsubmit', 'onchange', 'onkeyup', 'onkeydown',
            'onmousedown', 'onmouseup', 'ondblclick', 'oncontextmenu',
            'onwheel', 'ondrag', 'ondrop', 'onanimationend', 'ontransitionend',
            'ontoggle', 'onplay', 'onpause', 'onended', 'oncanplay',
            'onloadstart', 'onprogress', 'onseeking', 'onseeked'
        }
        
        # WAF bypass techniques patterns
        self.bypass_patterns = {
            'case_variation': r'[sS][cC][rR][iI][pP][tT]|[oO][nN][lL][oO][aA][dD]',
            'encoded_chars': r'&#\d+;|&#x[0-9a-fA-F]+;|%[0-9a-fA-F]{2}',
            'unicode_encoding': r'\\u[0-9a-fA-F]{4}|\\x[0-9a-fA-F]{2}',
            'mixed_quotes': r'[\'\"]+.*[\'\"]+',
            'comment_breaking': r'/\*.*?\*/|<!--.*?-->',
            'whitespace_abuse': r'[\s\n\r\t\f\v]+',
            'protocol_confusion': r'javascript:|data:|vbscript:|about:',
            'attribute_breaking': r'\w+\s*=\s*[^\s>]+',
            'tag_breaking': r'</\w+>.*<\w+',
            'double_encoding': r'%25[0-9a-fA-F]{2}',
            'null_byte': r'%00|\x00',
            'newline_injection': r'%0[aAdD]|\n|\r',
            'filter_evasion': r'script|alert|prompt|confirm',
            'obfuscation': r'String\.fromCharCode|eval\s*\(|atob\s*\(',
            'template_literals': r'`[^`]*`',
            'bracket_notation': r'\[[\'\"]\w+[\'\"]\]'
        }
        
        # Dangerous JavaScript functions and objects
        self.dangerous_js = {
            'eval', 'Function', 'setTimeout', 'setInterval', 'execScript',
            'document.write', 'document.writeln', 'innerHTML', 'outerHTML',
            'insertAdjacentHTML', 'location.href', 'location.assign',
            'location.replace', 'window.open', 'execCommand'
        }
        
        # HTML5 specific vectors
        self.html5_vectors = {
            'svg': ['onload', 'onerror', 'onclick'],
            'details': ['ontoggle'],
            'video': ['onplay', 'onended', 'onerror'],
            'audio': ['onplay', 'onended', 'onerror'],
            'canvas': ['onclick', 'onmouseover'],
            'template': ['innerHTML content'],
            'math': ['href attributes']
        }
    
    def analyze_payload(self, payload: str) -> PayloadAnalysis:
        """
        Comprehensive analysis of an XSS payload.
        
        Args:
            payload: The XSS payload string to analyze
            
        Returns:
            PayloadAnalysis object with detailed analysis results
        """
        logger.info(f"Analyzing payload: {payload[:50]}...")
        
        try:
            # Normalize payload for analysis
            normalized = self._normalize_payload(payload)
            
            # Detect contexts where this payload might work
            contexts = self._detect_contexts(payload)
            
            # Determine XSS types
            xss_types = self._determine_xss_types(payload)
            
            # Identify bypass techniques
            bypass_techniques = self._identify_bypass_techniques(payload)
            
            # Calculate risk level and confidence
            risk_level, confidence = self._calculate_risk_and_confidence(
                payload, contexts, bypass_techniques
            )
            
            # Generate explanation
            explanation = self._generate_explanation(
                payload, contexts, xss_types, bypass_techniques
            )
            
            # Create proof of concept
            proof_of_concept = self._generate_proof_of_concept(payload, contexts)
            
            # Collect metadata
            metadata = self._collect_metadata(payload, normalized, contexts)
            
            analysis = PayloadAnalysis(
                payload=payload,
                contexts=contexts,
                xss_types=xss_types,
                bypass_techniques=bypass_techniques,
                risk_level=risk_level,
                explanation=explanation,
                proof_of_concept=proof_of_concept,
                confidence_score=confidence,
                metadata=metadata
            )
            
            logger.info(f"Analysis complete: {risk_level} risk, {confidence:.2f} confidence")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing payload: {e}")
            # Return minimal analysis on error
            return PayloadAnalysis(
                payload=payload,
                contexts=[Context.UNKNOWN],
                xss_types=[XSSType.REFLECTED],
                bypass_techniques=[],
                risk_level="low",
                explanation=f"Analysis failed: {str(e)}",
                proof_of_concept="Unable to generate PoC",
                confidence_score=0.0,
                metadata={"error": str(e)}
            )
    
    def _normalize_payload(self, payload: str) -> str:
        """Normalize payload by decoding common encodings"""
        try:
            # HTML decode
            decoded = html.unescape(payload)
            
            # URL decode (multiple passes for double encoding)
            for _ in range(3):  # Handle triple encoding
                old_decoded = decoded
                decoded = urllib.parse.unquote(decoded)
                if decoded == old_decoded:
                    break
            
            # Unicode decode (basic)
            try:
                decoded = decoded.encode().decode('unicode_escape', errors='ignore')
            except (UnicodeDecodeError, UnicodeEncodeError):
                pass  # Keep original if unicode decode fails
            
            return decoded.lower()
        except Exception:
            return payload.lower()
    
    def _detect_contexts(self, payload: str) -> List[Context]:
        """Detect which HTML contexts this payload might exploit"""
        contexts = []
        payload_lower = payload.lower()
        
        # HTML Content Context - tags that would execute in HTML body
        if any(f'<{tag}' in payload_lower for tag in self.script_tags):
            contexts.append(Context.HTML_CONTENT)
        
        # Attribute Value Context - event handlers and dangerous attributes
        if any(handler in payload_lower for handler in self.event_handlers):
            contexts.append(Context.ATTRIBUTE_VALUE)
        
        # JavaScript String Context - characters that break out of JS strings
        if any(char in payload for char in ['"', "'", '\\', '\n', '\r']):
            contexts.append(Context.JAVASCRIPT_STRING)
        
        # JavaScript Variable Context - looks like JS variable assignment
        if re.search(r'\w+\s*=', payload):
            contexts.append(Context.JAVASCRIPT_VARIABLE)
        
        # CSS Value Context - CSS expressions and url() functions
        if any(term in payload_lower for term in ['expression(', 'url(', 'import', '@']):
            contexts.append(Context.CSS_VALUE)
        
        # URL Parameter Context - protocol handlers
        if any(protocol in payload_lower for protocol in ['javascript:', 'data:', 'vbscript:', 'about:']):
            contexts.append(Context.URL_PARAMETER)
        
        # HTML Comment Context - comment breaking
        if any(seq in payload for seq in ['-->', '<!--', '*/']):
            contexts.append(Context.HTML_COMMENT)
        
        return contexts if contexts else [Context.UNKNOWN]
    
    def _determine_xss_types(self, payload: str) -> List[XSSType]:
        """Determine what types of XSS this payload might achieve"""
        types = []
        payload_lower = payload.lower()
        
        # Reflected XSS indicators - immediate execution payloads
        if ('<script>' in payload_lower or 
            any(handler in payload_lower for handler in self.event_handlers) or
            'javascript:' in payload_lower):
            types.append(XSSType.REFLECTED)
        
        # Stored XSS indicators - payloads that might persist
        if (len(payload) < 100 and 
            not any(char in payload for char in ['<', '>', '"', "'"]) and
            any(term in payload_lower for term in ['alert', 'eval', 'script'])):
            types.append(XSSType.STORED)
        
        # DOM-based XSS indicators - client-side manipulation
        if any(term in payload_lower for term in [
            'document.', 'window.', 'location.', 'eval(', 'innerhtml',
            'outerhtml', 'document.write', 'location.href'
        ]):
            types.append(XSSType.DOM_BASED)
        
        # Universal payloads - work in multiple contexts
        if (('<img' in payload_lower and 'onerror=' in payload_lower) or
            ('svg' in payload_lower and 'onload=' in payload_lower) or
            'javascript:' in payload_lower):
            types.append(XSSType.UNIVERSAL)
        
        return types if types else [XSSType.REFLECTED]
    
    def _identify_bypass_techniques(self, payload: str) -> List[str]:
        """Identify WAF bypass techniques used in the payload"""
        techniques = []
        
        for technique, pattern in self.bypass_patterns.items():
            try:
                if re.search(pattern, payload, re.IGNORECASE | re.DOTALL):
                    techniques.append(technique)
            except re.error:
                # Skip malformed regex patterns
                continue
        
        # Additional heuristic checks
        if len(set(c.lower() for c in payload if c.isalpha())) > len(payload) // 3:
            techniques.append('mixed_case_evasion')
        
        if payload.count('"') != payload.count("'"):
            techniques.append('quote_imbalance')
        
        return techniques
    
    def _calculate_risk_and_confidence(self, payload: str, contexts: List[Context], 
                                     bypass_techniques: List[str]) -> Tuple[str, float]:
        """Calculate the risk level and confidence score of the payload"""
        risk_score = 0
        confidence = 0.5  # Base confidence
        
        # Length-based scoring
        if len(payload) > 200:
            risk_score += 2
            confidence += 0.1
        elif len(payload) > 100:
            risk_score += 1
        
        # Context-based scoring
        high_risk_contexts = {
            Context.HTML_CONTENT, Context.JAVASCRIPT_STRING, 
            Context.ATTRIBUTE_VALUE, Context.URL_PARAMETER
        }
        context_score = len([c for c in contexts if c in high_risk_contexts])
        risk_score += context_score * 2
        confidence += context_score * 0.1
        
        # Bypass technique scoring
        risk_score += len(bypass_techniques)
        confidence += len(bypass_techniques) * 0.05
        
        # Dangerous element detection
        payload_lower = payload.lower()
        if '<script>' in payload_lower:
            risk_score += 4
            confidence += 0.3
        
        if any(func in payload_lower for func in self.dangerous_js):
            risk_score += 3
            confidence += 0.2
        
        # HTML5 vector detection
        for tag, events in self.html5_vectors.items():
            if tag in payload_lower and any(event in payload_lower for event in events):
                risk_score += 2
                confidence += 0.15
        
        # Risk level mapping
        if risk_score >= 8:
            risk_level = "critical"
        elif risk_score >= 6:
            risk_level = "high"
        elif risk_score >= 3:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        # Confidence capping
        confidence = min(1.0, max(0.1, confidence))
        
        return risk_level, confidence
    
    def _generate_explanation(self, payload: str, contexts: List[Context], 
                            xss_types: List[XSSType], bypass_techniques: List[str]) -> str:
        """Generate human-readable explanation of the payload"""
        explanation = "This payload attempts XSS exploitation through: "
        
        if contexts and contexts != [Context.UNKNOWN]:
            context_names = [ctx.value.replace('_', ' ') for ctx in contexts]
            explanation += f"injection into {', '.join(context_names)} context(s)"
        else:
            explanation += "unknown injection context"
        
        if bypass_techniques:
            explanation += f", using bypass techniques: {', '.join(bypass_techniques)}"
        
        if xss_types:
            xss_type_names = [xss_type.value.replace('_', ' ') for xss_type in xss_types]
            explanation += f". Likely to succeed as {', '.join(xss_type_names)} XSS."
        
        # Add specific vector information
        payload_lower = payload.lower()
        if '<script>' in payload_lower:
            explanation += " Uses direct script tag injection."
        elif any(handler in payload_lower for handler in ['onerror', 'onload', 'onclick']):
            explanation += " Uses event handler injection."
        elif 'javascript:' in payload_lower:
            explanation += " Uses JavaScript protocol injection."
        
        return explanation
    
    def _generate_proof_of_concept(self, payload: str, contexts: List[Context]) -> str:
        """Generate a proof of concept for testing the payload"""
        poc = "Proof of Concept:\n\n"
        
        for context in contexts:
            if context == Context.HTML_CONTENT:
                poc += f"HTML Context: <div>{payload}</div>\n"
            elif context == Context.ATTRIBUTE_VALUE:
                poc += f"Attribute Context: <input value=\"{payload}\">\n"
            elif context == Context.JAVASCRIPT_STRING:
                poc += f"JavaScript Context: var x = \"{payload}\";\n"
            elif context == Context.URL_PARAMETER:
                poc += f"URL Context: https://example.com/page?param={urllib.parse.quote(payload)}\n"
            elif context == Context.CSS_VALUE:
                poc += f"CSS Context: <div style=\"color:{payload}\">test</div>\n"
            elif context == Context.HTML_COMMENT:
                poc += f"Comment Context: <!-- {payload} -->\n"
        
        poc += f"\nDirect test: {payload}\n"
        poc += "\nTesting Instructions:\n"
        poc += "1. Inject the payload into the identified context(s)\n"
        poc += "2. Observe if JavaScript executes (alert boxes, console messages)\n"
        poc += "3. Check browser developer tools for errors or execution\n"
        
        return poc
    
    def _collect_metadata(self, payload: str, normalized: str, contexts: List[Context]) -> Dict[str, any]:
        """Collect additional metadata about the payload"""
        metadata = {
            'original_length': len(payload),
            'normalized_length': len(normalized),
            'encoding_detected': payload != normalized,
            'character_diversity': len(set(payload.lower())),
            'contains_script_tag': '<script' in payload.lower(),
            'contains_event_handler': any(handler in payload.lower() for handler in self.event_handlers),
            'contains_javascript_protocol': 'javascript:' in payload.lower(),
            'context_count': len(contexts),
            'special_characters': [c for c in payload if c in '<>"\'&%;=()[]{}'],
            'word_count': len(payload.split()),
        }
        
        # Detect specific payload families
        if 'alert(' in payload.lower():
            metadata['payload_family'] = 'alert_based'
        elif 'eval(' in payload.lower():
            metadata['payload_family'] = 'eval_based'
        elif 'document.write' in payload.lower():
            metadata['payload_family'] = 'document_write'
        elif any(tag in payload.lower() for tag in ['<img', '<svg', '<iframe']):
            metadata['payload_family'] = 'tag_based'
        else:
            metadata['payload_family'] = 'unknown'
        
        return metadata
    
    def batch_analyze(self, payloads: List[str]) -> List[PayloadAnalysis]:
        """Analyze multiple payloads in batch"""
        logger.info(f"Batch analyzing {len(payloads)} payloads...")
        results = []
        
        for i, payload in enumerate(payloads):
            logger.debug(f"Analyzing payload {i+1}/{len(payloads)}")
            analysis = self.analyze_payload(payload)
            results.append(analysis)
        
        logger.info(f"Batch analysis complete: {len(results)} analyses generated")
        return results
    
    def get_analysis_summary(self, analyses: List[PayloadAnalysis]) -> Dict[str, any]:
        """Generate summary statistics from multiple analyses"""
        if not analyses:
            return {}
        
        risk_counts = {}
        context_counts = {}
        technique_counts = {}
        
        for analysis in analyses:
            # Count risk levels
            risk_counts[analysis.risk_level] = risk_counts.get(analysis.risk_level, 0) + 1
            
            # Count contexts
            for context in analysis.contexts:
                context_counts[context.value] = context_counts.get(context.value, 0) + 1
            
            # Count techniques
            for technique in analysis.bypass_techniques:
                technique_counts[technique] = technique_counts.get(technique, 0) + 1
        
        return {
            'total_payloads': len(analyses),
            'average_confidence': sum(a.confidence_score for a in analyses) / len(analyses),
            'risk_distribution': risk_counts,
            'most_common_contexts': sorted(context_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            'most_common_techniques': sorted(technique_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            'high_confidence_payloads': len([a for a in analyses if a.confidence_score > 0.8]),
        }