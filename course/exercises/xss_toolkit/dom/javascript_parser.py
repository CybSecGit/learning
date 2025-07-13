"""
Module 2: DOM XSS JavaScript Parser and Source/Sink Analysis

This module analyzes JavaScript code for DOM-based XSS vulnerabilities by:
- Identifying dangerous sources (user-controlled input)
- Identifying dangerous sinks (code execution points)
- Tracing data flow from sources to sinks
- Generating appropriate DOM XSS payloads

The parser uses pattern matching and data flow analysis to identify
vulnerabilities that exist entirely in client-side JavaScript.
"""

import re
import json
from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


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
    CREATE_ELEMENT = "createElement"            # document.createElement() with dangerous attributes


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
    
    Example:
        parser = JavaScriptParser()
        sources, sinks, flows = parser.analyze_javascript(js_code)
        for flow in flows:
            print(f"DOM XSS: {flow.source.source_type} -> {flow.sink.sink_type}")
    """
    
    def __init__(self):
        # Enhanced patterns for identifying sources
        self.source_patterns = {
            SourceType.URL_LOCATION: [
                r'(?:window\.|document\.)?location(?:\.href)?(?!\s*=)',
                r'(?:window\.|document\.)?location\.(?:pathname|search|hash|host|hostname|port|protocol)',
                r'document\.URL',
                r'document\.documentURI',
                r'window\.location\.toString\(\)'
            ],
            SourceType.URL_SEARCH: [
                r'location\.search',
                r'window\.location\.search',
                r'document\.location\.search',
                r'URLSearchParams\s*\(\s*(?:window\.)?location\.search\s*\)'
            ],
            SourceType.URL_HASH: [
                r'location\.hash',
                r'window\.location\.hash',
                r'document\.location\.hash',
                r'location\.hash\.(?:substr|substring|slice)'
            ],
            SourceType.REFERRER: [
                r'document\.referrer',
                r'document\.referrer\.(?:split|match|indexOf)'
            ],
            SourceType.POSTMESSAGE: [
                r'addEventListener\s*\(\s*["\']message["\']\s*,',
                r'window\.addEventListener\s*\(\s*["\']message["\']\s*,',
                r'onmessage\s*=',
                r'event\.data',
                r'e\.data'
            ],
            SourceType.LOCAL_STORAGE: [
                r'localStorage\.getItem\s*\(',
                r'localStorage\[["\'][^"\']+["\']\]',
                r'localStorage\.[a-zA-Z_]\w*'
            ],
            SourceType.SESSION_STORAGE: [
                r'sessionStorage\.getItem\s*\(',
                r'sessionStorage\[["\'][^"\']+["\']\]',
                r'sessionStorage\.[a-zA-Z_]\w*'
            ],
            SourceType.COOKIE: [
                r'document\.cookie',
                r'document\.cookie\.(?:split|match|indexOf)'
            ],
            SourceType.USER_INPUT: [
                r'\.value(?!\s*=)',
                r'prompt\s*\(',
                r'confirm\s*\(',
                r'\.getAttribute\s*\(["\']value["\']\)',
                r'getElementById\([^)]+\)\.value',
                r'querySelector\([^)]+\)\.value',
                r'\$\([^)]+\)\.val\(\)'
            ],
            SourceType.WINDOW_NAME: [
                r'window\.name',
                r'window\.name\.(?:split|match|indexOf)'
            ]
        }
        
        # Enhanced patterns for identifying sinks
        self.sink_patterns = {
            SinkType.INNER_HTML: [
                r'\.innerHTML\s*=',
                r'\.innerHTML\s*\+=',
                r'innerHTML\s*=',
                r'\.innerHTML\s*\([^)]*\)'
            ],
            SinkType.OUTER_HTML: [
                r'\.outerHTML\s*=',
                r'\.outerHTML\s*\+=',
                r'outerHTML\s*='
            ],
            SinkType.DOCUMENT_WRITE: [
                r'document\.write\s*\(',
                r'document\.writeln\s*\(',
                r'document\.open\s*\(\s*\)\.write\s*\('
            ],
            SinkType.EVAL: [
                r'\beval\s*\(',
                r'Function\s*\(',
                r'new\s+Function\s*\(',
                r'setTimeout\s*\(\s*["\'][^"\']+["\']\s*\+',
                r'setInterval\s*\(\s*["\'][^"\']+["\']\s*\+'
            ],
            SinkType.SET_TIMEOUT: [
                r'setTimeout\s*\(',
                r'setInterval\s*\(',
                r'setImmediate\s*\('
            ],
            SinkType.SCRIPT_SRC: [
                r'\.src\s*=.*script',
                r'script.*\.src\s*=',
                r'\.setAttribute\s*\(\s*["\']src["\']\s*,.*script'
            ],
            SinkType.IFRAME_SRC: [
                r'iframe.*\.src\s*=',
                r'\.src\s*=.*iframe',
                r'\.setAttribute\s*\(\s*["\']src["\']\s*,.*iframe'
            ],
            SinkType.LOCATION_HREF: [
                r'location\.href\s*=',
                r'window\.location\.href\s*=',
                r'location\.assign\s*\(',
                r'location\.replace\s*\(',
                r'window\.location\s*='
            ],
            SinkType.JQUERY_HTML: [
                r'\$\([^)]+\)\.html\s*\(',
                r'jQuery\([^)]+\)\.html\s*\(',
                r'\.html\s*\([^)]+\)'
            ],
            SinkType.JQUERY_APPEND: [
                r'\$\([^)]+\)\.append\s*\(',
                r'jQuery\([^)]+\)\.append\s*\(',
                r'\.append\s*\([^)]+\)',
                r'\.prepend\s*\([^)]+\)',
                r'\.after\s*\([^)]+\)',
                r'\.before\s*\([^)]+\)'
            ],
            SinkType.INSERT_ADJACENT_HTML: [
                r'\.insertAdjacentHTML\s*\(',
                r'insertAdjacentHTML\s*\('
            ],
            SinkType.CREATE_ELEMENT: [
                r'document\.createElement\s*\(',
                r'createElement\s*\('
            ]
        }
        
        # Variable tracking for data flow analysis
        self.variable_assignments = {}
        self.data_flows = []
        self.tainted_variables = set()
        
        # Common transformation functions
        self.transformation_functions = {
            'decodeURIComponent', 'encodeURIComponent', 'escape', 'unescape',
            'atob', 'btoa', 'toLowerCase', 'toUpperCase', 'trim', 'replace',
            'substring', 'substr', 'slice', 'split', 'join', 'concat',
            'parseInt', 'parseFloat', 'toString', 'valueOf'
        }
    
    def analyze_javascript(self, javascript_code: str) -> Tuple[List[JavaScriptSource], List[JavaScriptSink], List[DataFlowPath]]:
        """
        Analyze JavaScript code for DOM XSS vulnerabilities.
        
        Args:
            javascript_code: JavaScript code to analyze
            
        Returns:
            Tuple of (sources, sinks, data_flow_paths)
        """
        logger.info("Starting JavaScript analysis for DOM XSS...")
        
        # Reset state
        self.variable_assignments = {}
        self.data_flows = []
        self.tainted_variables = set()
        
        # Split into lines for analysis
        lines = javascript_code.split('\n')
        
        # Find sources and sinks
        sources = self._find_sources(lines)
        sinks = self._find_sinks(lines)
        
        logger.info(f"Found {len(sources)} sources and {len(sinks)} sinks")
        
        # Trace data flows
        data_flows = self._trace_data_flows(lines, sources, sinks)
        
        logger.info(f"Identified {len(data_flows)} potential DOM XSS vulnerabilities")
        
        return sources, sinks, data_flows
    
    def _find_sources(self, lines: List[str]) -> List[JavaScriptSource]:
        """Find dangerous data sources in JavaScript code"""
        sources = []
        
        for line_num, line in enumerate(lines, 1):
            line_clean = line.strip()
            
            for source_type, patterns in self.source_patterns.items():
                for pattern in patterns:
                    try:
                        if re.search(pattern, line_clean, re.IGNORECASE):
                            # Extract variable name if assignment
                            var_name = self._extract_variable_assignment(line_clean)
                            
                            # Calculate risk level
                            risk_level = self._calculate_source_risk(source_type, line_clean)
                            
                            # Check if this is a real source (not just setting it)
                            if not self._is_setting_source(line_clean, pattern):
                                source = JavaScriptSource(
                                    source_type=source_type,
                                    variable_name=var_name or f"source_{line_num}",
                                    line_number=line_num,
                                    code_snippet=line_clean,
                                    risk_level=risk_level
                                )
                                sources.append(source)
                                
                                # Track tainted variable
                                if var_name:
                                    self.tainted_variables.add(var_name)
                                    self.variable_assignments[var_name] = {
                                        'source_type': source_type,
                                        'line': line_num,
                                        'tainted': True,
                                        'source': source
                                    }
                                
                                break
                    except re.error:
                        continue
        
        return sources
    
    def _find_sinks(self, lines: List[str]) -> List[JavaScriptSink]:
        """Find dangerous data sinks in JavaScript code"""
        sinks = []
        
        for line_num, line in enumerate(lines, 1):
            line_clean = line.strip()
            
            for sink_type, patterns in self.sink_patterns.items():
                for pattern in patterns:
                    try:
                        if re.search(pattern, line_clean, re.IGNORECASE):
                            # Extract variable being used
                            var_name = self._extract_sink_variable(line_clean, pattern)
                            
                            # Calculate risk level
                            risk_level = self._calculate_sink_risk(sink_type, line_clean)
                            
                            # Determine if user interaction is required
                            requires_interaction = self._requires_user_interaction(sink_type, line_clean)
                            
                            sink = JavaScriptSink(
                                sink_type=sink_type,
                                variable_name=var_name or f"sink_{line_num}",
                                line_number=line_num,
                                code_snippet=line_clean,
                                risk_level=risk_level,
                                requires_user_interaction=requires_interaction
                            )
                            sinks.append(sink)
                            
                            break
                    except re.error:
                        continue
        
        return sinks
    
    def _trace_data_flows(self, lines: List[str], sources: List[JavaScriptSource], 
                         sinks: List[JavaScriptSink]) -> List[DataFlowPath]:
        """Trace data flow from sources to sinks"""
        data_flows = []
        
        # First, build complete variable flow map
        self._track_variable_flow(lines)
        
        # For each sink, check if it uses tainted data
        for sink in sinks:
            for source in sources:
                flow_path = self._find_flow_path(source, sink, lines)
                if flow_path:
                    data_flows.append(flow_path)
        
        return data_flows
    
    def _track_variable_flow(self, lines: List[str]):
        """Track how variables flow through the code"""
        for line_num, line in enumerate(lines, 1):
            line_clean = line.strip()
            
            # Look for variable assignments
            # Pattern: var/let/const name = value OR name = value
            assignment_patterns = [
                r'(?:var|let|const)\s+([a-zA-Z_$][\w$]*)\s*=\s*(.+)',
                r'([a-zA-Z_$][\w$]*)\s*=\s*([^=].+)'
            ]
            
            for pattern in assignment_patterns:
                match = re.match(pattern, line_clean)
                if match:
                    var_name = match.group(1)
                    assignment_value = match.group(2)
                    
                    # Check if assignment uses tainted variables
                    is_tainted = self._is_value_tainted(assignment_value)
                    
                    # Track transformations
                    transformations = self._detect_transformations_in_value(assignment_value)
                    
                    self.variable_assignments[var_name] = {
                        'line': line_num,
                        'value': assignment_value,
                        'tainted': is_tainted,
                        'transformations': transformations
                    }
                    
                    if is_tainted:
                        self.tainted_variables.add(var_name)
                    
                    break
    
    def _is_value_tainted(self, value: str) -> bool:
        """Check if a value contains tainted variables or sources"""
        # Check for tainted variables
        for tainted_var in self.tainted_variables:
            if re.search(r'\b' + re.escape(tainted_var) + r'\b', value):
                return True
        
        # Check for direct source usage
        for source_type, patterns in self.source_patterns.items():
            for pattern in patterns:
                try:
                    if re.search(pattern, value, re.IGNORECASE):
                        return True
                except re.error:
                    continue
        
        return False
    
    def _find_flow_path(self, source: JavaScriptSource, sink: JavaScriptSink, 
                       lines: List[str]) -> Optional[DataFlowPath]:
        """Find if there's a data flow path from source to sink"""
        
        # Direct usage check
        if source.variable_name in sink.code_snippet:
            confidence = 0.9
            payload = self._generate_dom_xss_payload(source, sink)
            steps = self._generate_exploitation_steps(source, sink)
            
            return DataFlowPath(
                source=source,
                sink=sink,
                intermediate_variables=[],
                transformations=[],
                vulnerability_confidence=confidence,
                exploit_payload=payload,
                exploitation_steps=steps
            )
        
        # Check indirect flow through tainted variables
        if sink.variable_name in self.variable_assignments:
            var_info = self.variable_assignments[sink.variable_name]
            
            if var_info.get('tainted', False):
                # Find intermediate variables
                intermediate_vars = self._find_intermediate_variables(source, sink)
                transformations = var_info.get('transformations', [])
                
                confidence = self._calculate_flow_confidence(source, sink, intermediate_vars, transformations)
                payload = self._generate_dom_xss_payload(source, sink)
                steps = self._generate_exploitation_steps(source, sink)
                
                return DataFlowPath(
                    source=source,
                    sink=sink,
                    intermediate_variables=intermediate_vars,
                    transformations=transformations,
                    vulnerability_confidence=confidence,
                    exploit_payload=payload,
                    exploitation_steps=steps
                )
        
        # Check if sink uses any tainted variable
        for tainted_var in self.tainted_variables:
            if tainted_var in sink.code_snippet:
                confidence = 0.7
                payload = self._generate_dom_xss_payload(source, sink)
                steps = self._generate_exploitation_steps(source, sink)
                
                return DataFlowPath(
                    source=source,
                    sink=sink,
                    intermediate_variables=[tainted_var],
                    transformations=[],
                    vulnerability_confidence=confidence,
                    exploit_payload=payload,
                    exploitation_steps=steps
                )
        
        return None
    
    def _calculate_flow_confidence(self, source: JavaScriptSource, sink: JavaScriptSink,
                                 intermediate_vars: List[str], transformations: List[str]) -> float:
        """Calculate confidence that this is a real vulnerability"""
        confidence = 0.5  # Base confidence
        
        # High-risk sources increase confidence
        if source.source_type in [SourceType.URL_LOCATION, SourceType.URL_HASH, 
                                  SourceType.URL_SEARCH, SourceType.POSTMESSAGE]:
            confidence += 0.3
        
        # High-risk sinks increase confidence
        if sink.sink_type in [SinkType.INNER_HTML, SinkType.EVAL, 
                             SinkType.DOCUMENT_WRITE, SinkType.EXECUTE_SCRIPT]:
            confidence += 0.3
        
        # Direct flow increases confidence
        if not intermediate_vars:
            confidence += 0.2
        else:
            # More intermediate variables decrease confidence
            confidence -= len(intermediate_vars) * 0.05
        
        # Certain transformations might sanitize
        safe_transforms = {'encodeURIComponent', 'escape'}
        if any(t in safe_transforms for t in transformations):
            confidence -= 0.3
        
        # User interaction requirement decreases confidence
        if sink.requires_user_interaction:
            confidence -= 0.1
        
        return min(1.0, max(0.1, confidence))
    
    def _generate_dom_xss_payload(self, source: JavaScriptSource, sink: JavaScriptSink) -> str:
        """Generate appropriate DOM XSS payload for source/sink combination"""
        
        # URL-based sources
        if source.source_type in [SourceType.URL_HASH, SourceType.URL_SEARCH]:
            if sink.sink_type == SinkType.INNER_HTML:
                return "#<img src=x onerror=alert('DOM-XSS')>"
            elif sink.sink_type == SinkType.EVAL:
                return "#';alert('DOM-XSS');//"
            elif sink.sink_type == SinkType.DOCUMENT_WRITE:
                return "#<script>alert('DOM-XSS')</script>"
            elif sink.sink_type == SinkType.JQUERY_HTML:
                return "#<img/src/onerror=alert('DOM-XSS')>"
        
        # Location.href sink
        elif source.source_type == SourceType.URL_LOCATION:
            if sink.sink_type == SinkType.LOCATION_HREF:
                return "javascript:alert('DOM-XSS')"
        
        # PostMessage source
        elif source.source_type == SourceType.POSTMESSAGE:
            if sink.sink_type == SinkType.INNER_HTML:
                return '{"message":"<img src=x onerror=alert(\'DOM-XSS\')>"}'
            elif sink.sink_type == SinkType.EVAL:
                return '{"code":"alert(\'DOM-XSS\')"}'
        
        # Storage-based sources
        elif source.source_type in [SourceType.LOCAL_STORAGE, SourceType.SESSION_STORAGE]:
            if sink.sink_type == SinkType.INNER_HTML:
                return "<svg onload=alert('DOM-XSS')>"
        
        # Cookie source
        elif source.source_type == SourceType.COOKIE:
            if sink.sink_type == SinkType.INNER_HTML:
                return "user=<script>alert('DOM-XSS')</script>"
        
        # Default payload
        return "<img src=x onerror=alert('DOM-XSS')>"
    
    def _generate_exploitation_steps(self, source: JavaScriptSource, sink: JavaScriptSink) -> List[str]:
        """Generate step-by-step exploitation instructions"""
        steps = []
        
        if source.source_type == SourceType.URL_HASH:
            steps.append("1. Navigate to the vulnerable page")
            steps.append(f"2. Append the payload to the URL hash: {self._generate_dom_xss_payload(source, sink)}")
            steps.append("3. The payload will be processed by the JavaScript code")
            steps.append(f"4. The sink ({sink.sink_type.value}) will execute the malicious code")
        
        elif source.source_type == SourceType.POSTMESSAGE:
            steps.append("1. Create a malicious page that will send the postMessage")
            steps.append(f"2. Use window.postMessage with payload: {self._generate_dom_xss_payload(source, sink)}")
            steps.append("3. The vulnerable page will receive and process the message")
            steps.append(f"4. The sink ({sink.sink_type.value}) will execute the payload")
        
        elif source.source_type in [SourceType.LOCAL_STORAGE, SourceType.SESSION_STORAGE]:
            steps.append(f"1. Set malicious data in {source.source_type.value}")
            steps.append(f"2. Use console or another XSS to set: {self._generate_dom_xss_payload(source, sink)}")
            steps.append("3. Navigate to the vulnerable page")
            steps.append(f"4. The sink ({sink.sink_type.value}) will read and execute the payload")
        
        else:
            steps.append("1. Identify the injection point")
            steps.append(f"2. Inject the payload: {self._generate_dom_xss_payload(source, sink)}")
            steps.append("3. Trigger the vulnerable code path")
            steps.append(f"4. The sink ({sink.sink_type.value}) executes the payload")
        
        return steps
    
    def _extract_variable_assignment(self, line: str) -> Optional[str]:
        """Extract variable name from assignment"""
        patterns = [
            r'(?:var|let|const)\s+([a-zA-Z_$][\w$]*)\s*=',
            r'([a-zA-Z_$][\w$]*)\s*='
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_sink_variable(self, line: str, pattern: str) -> Optional[str]:
        """Extract variable being used in a sink"""
        # Try different extraction patterns based on sink type
        if 'innerHTML' in pattern or 'outerHTML' in pattern:
            match = re.search(r'([a-zA-Z_$][\w$]*)\s*\.(?:inner|outer)HTML', line)
            if match:
                return match.group(1)
        
        elif 'eval' in pattern or 'Function' in pattern:
            match = re.search(r'(?:eval|Function)\s*\(\s*([a-zA-Z_$][\w$]*)', line)
            if match:
                return match.group(1)
        
        # Generic pattern
        match = re.search(r'=\s*([a-zA-Z_$][\w$]*)', line)
        if match:
            return match.group(1)
        
        return None
    
    def _calculate_source_risk(self, source_type: SourceType, code: str) -> str:
        """Calculate risk level for a source"""
        high_risk = [
            SourceType.URL_LOCATION, SourceType.URL_HASH, 
            SourceType.POSTMESSAGE, SourceType.URL_SEARCH
        ]
        medium_risk = [
            SourceType.REFERRER, SourceType.LOCAL_STORAGE,
            SourceType.SESSION_STORAGE, SourceType.WINDOW_NAME
        ]
        
        if source_type in high_risk:
            return "high"
        elif source_type in medium_risk:
            return "medium"
        else:
            return "low"
    
    def _calculate_sink_risk(self, sink_type: SinkType, code: str) -> str:
        """Calculate risk level for a sink"""
        critical_risk = [SinkType.EVAL, SinkType.DOCUMENT_WRITE, SinkType.EXECUTE_SCRIPT]
        high_risk = [
            SinkType.INNER_HTML, SinkType.OUTER_HTML, 
            SinkType.SET_TIMEOUT, SinkType.INSERT_ADJACENT_HTML
        ]
        medium_risk = [
            SinkType.SCRIPT_SRC, SinkType.IFRAME_SRC, 
            SinkType.LOCATION_HREF, SinkType.CREATE_ELEMENT
        ]
        
        if sink_type in critical_risk:
            return "critical"
        elif sink_type in high_risk:
            return "high"
        elif sink_type in medium_risk:
            return "medium"
        else:
            return "low"
    
    def _is_setting_source(self, line: str, pattern: str) -> bool:
        """Check if the line is setting a source rather than reading it"""
        # Check for assignment to location properties
        if 'location' in pattern.lower():
            if re.search(r'location(?:\.href)?\s*=', line, re.IGNORECASE):
                return True
        
        return False
    
    def _requires_user_interaction(self, sink_type: SinkType, code: str) -> bool:
        """Determine if the sink requires user interaction to trigger"""
        # Check for event handlers
        event_patterns = [
            r'onclick', r'onmouseover', r'onfocus', r'onload',
            r'addEventListener\s*\(\s*["\']click["\']',
            r'\.click\s*\(\s*function'
        ]
        
        for pattern in event_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                return True
        
        return False
    
    def _find_intermediate_variables(self, source: JavaScriptSource, sink: JavaScriptSink) -> List[str]:
        """Find intermediate variables in the data flow"""
        intermediate = []
        
        # This is a simplified implementation
        # In a real implementation, we would trace the complete data flow graph
        for var_name, var_info in self.variable_assignments.items():
            if var_info.get('tainted') and var_name != source.variable_name:
                if var_name in sink.code_snippet or var_name == sink.variable_name:
                    intermediate.append(var_name)
        
        return intermediate
    
    def _detect_transformations(self, source: JavaScriptSource, sink: JavaScriptSink) -> List[str]:
        """Detect data transformations that might affect exploitation"""
        transformations = []
        
        # Look for transformation functions in sink code
        for transform in self.transformation_functions:
            if transform in sink.code_snippet:
                transformations.append(transform)
        
        return transformations
    
    def _detect_transformations_in_value(self, value: str) -> List[str]:
        """Detect transformations applied in a value assignment"""
        transformations = []
        
        for transform in self.transformation_functions:
            if transform in value:
                transformations.append(transform)
        
        return transformations
    
    def generate_dom_xss_report(self, sources: List[JavaScriptSource], 
                               sinks: List[JavaScriptSink], 
                               flows: List[DataFlowPath]) -> str:
        """Generate a detailed DOM XSS analysis report"""
        report = "DOM XSS Analysis Report\n"
        report += "=" * 50 + "\n\n"
        
        report += f"Sources Found: {len(sources)}\n"
        report += f"Sinks Found: {len(sinks)}\n"
        report += f"Vulnerable Flows: {len(flows)}\n\n"
        
        if flows:
            report += "VULNERABILITIES FOUND:\n"
            report += "-" * 30 + "\n\n"
            
            for i, flow in enumerate(flows, 1):
                report += f"[{i}] DOM XSS Vulnerability\n"
                report += f"Source: {flow.source.source_type.value} (line {flow.source.line_number})\n"
                report += f"  Code: {flow.source.code_snippet}\n"
                report += f"Sink: {flow.sink.sink_type.value} (line {flow.sink.line_number})\n"
                report += f"  Code: {flow.sink.code_snippet}\n"
                report += f"Confidence: {flow.vulnerability_confidence:.2f}\n"
                report += f"Risk: {flow.sink.risk_level.upper()}\n"
                
                if flow.intermediate_variables:
                    report += f"Data Flow: {' -> '.join(flow.intermediate_variables)}\n"
                
                if flow.transformations:
                    report += f"Transformations: {', '.join(flow.transformations)}\n"
                
                report += f"\nExploit Payload:\n{flow.exploit_payload}\n"
                report += "\nExploitation Steps:\n"
                for step in flow.exploitation_steps:
                    report += f"  {step}\n"
                
                report += "\n" + "-" * 30 + "\n\n"
        
        return report