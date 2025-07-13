"""
Module 8: Enterprise XSS Security Integration Suite

This module provides enterprise-grade integration capabilities for the XSS toolkit:
- CI/CD pipeline integration for automated security testing
- SIEM/SOC integration for vulnerability alerting
- Bug tracking system integration (Jira, GitHub Issues)
- Security dashboard and reporting APIs
- Team collaboration and workflow management
- Compliance reporting (OWASP Top 10, PCI DSS, SOX)

The integration suite enables organizations to embed XSS testing into their
development lifecycle and security operations workflows.
"""

import json
import datetime
import hashlib
import uuid
import base64
from typing import List, Dict, Set, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging
import sqlite3
import threading
import queue
import os

logger = logging.getLogger(__name__)


class IntegrationType(Enum):
    """Types of enterprise integrations"""
    CI_CD_PIPELINE = "cicd_pipeline"                 # Jenkins, GitLab CI, GitHub Actions
    BUG_TRACKING = "bug_tracking"                    # Jira, GitHub Issues, Azure DevOps
    SIEM_PLATFORM = "siem_platform"                 # Splunk, ELK, QRadar, Sentinel
    SECURITY_DASHBOARD = "security_dashboard"        # Custom dashboards, Grafana
    NOTIFICATION_SYSTEM = "notification_system"     # Slack, Teams, Email, PagerDuty
    COMPLIANCE_REPORTING = "compliance_reporting"   # SOX, PCI DSS, OWASP compliance
    VULNERABILITY_SCANNER = "vulnerability_scanner" # Nessus, OpenVAS, Burp Suite
    CODE_REPOSITORY = "code_repository"             # Git, SVN, Perforce


class SeverityLevel(Enum):
    """Severity levels for vulnerability findings"""
    CRITICAL = "critical"                           # Immediate threat requiring urgent action
    HIGH = "high"                                   # Significant risk requiring prompt action
    MEDIUM = "medium"                               # Moderate risk requiring timely action
    LOW = "low"                                     # Minor risk requiring eventual action
    INFO = "info"                                   # Informational finding, no immediate risk


class ComplianceFramework(Enum):
    """Compliance frameworks for reporting"""
    OWASP_TOP_10 = "owasp_top_10"                  # OWASP Top 10 Web Application Security Risks
    PCI_DSS = "pci_dss"                            # Payment Card Industry Data Security Standard
    SOX = "sox"                                     # Sarbanes-Oxley Act compliance
    GDPR = "gdpr"                                   # General Data Protection Regulation
    HIPAA = "hipaa"                                 # Health Insurance Portability and Accountability Act
    ISO_27001 = "iso_27001"                        # ISO 27001 Information Security Management
    NIST_CSF = "nist_csf"                          # NIST Cybersecurity Framework


@dataclass
class VulnerabilityFinding:
    """Standardized vulnerability finding for enterprise reporting"""
    finding_id: str                                 # Unique identifier for the finding
    title: str                                     # Brief title describing the vulnerability
    description: str                               # Detailed description of the vulnerability
    severity: SeverityLevel                        # Severity level of the finding
    confidence: float                              # Confidence level (0.0-1.0)
    affected_url: str                              # URL where vulnerability was found
    vulnerable_parameter: str                      # Parameter that contains the vulnerability
    attack_vector: str                             # How the vulnerability can be exploited
    proof_of_concept: str                          # Working exploit demonstration
    remediation: str                               # How to fix the vulnerability
    references: List[str]                          # External references (CVE, CWE, etc.)
    discovered_at: datetime.datetime               # When the vulnerability was discovered
    last_verified: datetime.datetime               # When the vulnerability was last verified
    status: str                                    # open, in_progress, resolved, false_positive
    assigned_to: Optional[str] = None              # Who is responsible for fixing
    estimated_effort: Optional[str] = None         # Estimated effort to fix (hours/days)
    business_impact: Optional[str] = None          # Business impact description
    compliance_mappings: Dict[ComplianceFramework, List[str]] = field(default_factory=dict)


@dataclass
class ScanSession:
    """Represents a complete XSS scanning session"""
    session_id: str                                # Unique session identifier
    start_time: datetime.datetime                  # When the scan started
    end_time: Optional[datetime.datetime] = None   # When the scan completed
    target_urls: List[str] = field(default_factory=list)  # URLs that were scanned
    scan_parameters: Dict[str, Any] = field(default_factory=dict)  # Configuration used
    findings: List[VulnerabilityFinding] = field(default_factory=list)  # Vulnerabilities found
    total_requests: int = 0                        # Total HTTP requests made
    coverage_metrics: Dict[str, float] = field(default_factory=dict)  # Coverage statistics
    performance_metrics: Dict[str, float] = field(default_factory=dict)  # Performance stats


@dataclass
class IntegrationConfig:
    """Configuration for enterprise integrations"""
    integration_type: IntegrationType              # Type of integration
    endpoint_url: str                              # API endpoint or webhook URL
    authentication: Dict[str, str]                # API keys, tokens, credentials
    configuration: Dict[str, Any]                 # Integration-specific configuration
    enabled: bool = True                           # Whether integration is active
    retry_attempts: int = 3                        # Number of retry attempts for failures
    timeout_seconds: int = 30                      # Request timeout in seconds


class EnterpriseIntegrationSuite:
    """
    Enterprise-grade integration suite for XSS security testing.
    
    This suite provides comprehensive integration capabilities that allow
    organizations to embed XSS testing into their development and security
    operations workflows.
    
    Features:
    - CI/CD pipeline integration for automated testing
    - Bug tracking system integration for vulnerability management
    - SIEM platform integration for security monitoring
    - Compliance reporting for regulatory requirements
    - Team collaboration and notification systems
    - Security dashboard and metrics APIs
    
    Example:
        suite = EnterpriseIntegrationSuite()
        
        # Configure CI/CD integration
        suite.configure_integration(IntegrationType.CI_CD_PIPELINE, {
            'endpoint_url': 'https://jenkins.company.com/webhook',
            'authentication': {'token': 'jenkins-api-token'}
        })
        
        # Run scan and automatically integrate results
        session = suite.create_scan_session(['https://app.company.com'])
        suite.process_scan_results(session)
    """
    
    def __init__(self, database_path: str = "/tmp/xss_enterprise.db"):
        self.database_path = database_path
        self.integrations: Dict[IntegrationType, IntegrationConfig] = {}
        self.scan_sessions: Dict[str, ScanSession] = {}
        
        # Initialize enterprise database
        self._initialize_database()
        
        # Standard compliance mappings
        self.compliance_mappings = {
            ComplianceFramework.OWASP_TOP_10: {
                'xss': ['A03:2021 – Injection', 'A07:2021 – Identification and Authentication Failures'],
                'stored_xss': ['A03:2021 – Injection'],
                'dom_xss': ['A03:2021 – Injection'],
                'reflected_xss': ['A03:2021 – Injection']
            },
            ComplianceFramework.PCI_DSS: {
                'xss': ['6.5.7 - Cross-site scripting (XSS)'],
                'input_validation': ['6.5.1 - Injection flaws']
            },
            ComplianceFramework.NIST_CSF: {
                'vulnerability_management': ['PR.IP-12', 'DE.CM-8'],
                'secure_development': ['PR.IP-2', 'PR.IP-3']
            }
        }
        
        # Standard severity mappings for different contexts
        self.severity_mappings = {
            'reflected_xss': SeverityLevel.HIGH,
            'stored_xss': SeverityLevel.CRITICAL,
            'dom_xss': SeverityLevel.HIGH,
            'csp_bypass': SeverityLevel.MEDIUM,
            'filter_bypass': SeverityLevel.HIGH,
        }
        
        # Integration templates for common platforms
        self.integration_templates = {
            IntegrationType.CI_CD_PIPELINE: {
                'jenkins': {
                    'webhook_format': 'json',
                    'required_fields': ['build_url', 'commit_sha', 'branch'],
                    'success_codes': [200, 201]
                },
                'github_actions': {
                    'webhook_format': 'json',
                    'required_fields': ['workflow_run_id', 'repository', 'sha'],
                    'success_codes': [200]
                }
            },
            IntegrationType.BUG_TRACKING: {
                'jira': {
                    'api_version': 'v2',
                    'issue_type': 'Security Vulnerability',
                    'required_fields': ['project', 'summary', 'description'],
                    'priority_mapping': {
                        SeverityLevel.CRITICAL: 'Highest',
                        SeverityLevel.HIGH: 'High',
                        SeverityLevel.MEDIUM: 'Medium',
                        SeverityLevel.LOW: 'Low'
                    }
                }
            }
        }
    
    def _initialize_database(self):
        """Initialize SQLite database for enterprise data storage"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        # Scan sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scan_sessions (
                session_id TEXT PRIMARY KEY,
                start_time REAL,
                end_time REAL,
                target_urls TEXT,
                scan_parameters TEXT,
                total_requests INTEGER,
                coverage_metrics TEXT,
                performance_metrics TEXT
            )
        ''')
        
        # Vulnerability findings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS findings (
                finding_id TEXT PRIMARY KEY,
                session_id TEXT,
                title TEXT,
                description TEXT,
                severity TEXT,
                confidence REAL,
                affected_url TEXT,
                vulnerable_parameter TEXT,
                attack_vector TEXT,
                proof_of_concept TEXT,
                remediation TEXT,
                references TEXT,
                discovered_at REAL,
                last_verified REAL,
                status TEXT,
                assigned_to TEXT,
                estimated_effort TEXT,
                business_impact TEXT,
                compliance_mappings TEXT,
                FOREIGN KEY (session_id) REFERENCES scan_sessions (session_id)
            )
        ''')
        
        # Integration configurations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS integrations (
                integration_type TEXT PRIMARY KEY,
                endpoint_url TEXT,
                authentication TEXT,
                configuration TEXT,
                enabled BOOLEAN,
                retry_attempts INTEGER,
                timeout_seconds INTEGER
            )
        ''')
        
        # Integration logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS integration_logs (
                log_id TEXT PRIMARY KEY,
                integration_type TEXT,
                timestamp REAL,
                action TEXT,
                payload TEXT,
                response TEXT,
                success BOOLEAN,
                error_message TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def configure_integration(self, integration_type: IntegrationType, 
                            config: Dict[str, Any]) -> bool:
        """
        Configure an enterprise integration.
        
        Args:
            integration_type: Type of integration to configure
            config: Configuration dictionary with endpoint, auth, etc.
            
        Returns:
            True if configuration was successful
        """
        try:
            # Validate required configuration fields
            required_fields = ['endpoint_url', 'authentication']
            for field in required_fields:
                if field not in config:
                    raise ValueError(f"Missing required field: {field}")
            
            # Create integration configuration
            integration_config = IntegrationConfig(
                integration_type=integration_type,
                endpoint_url=config['endpoint_url'],
                authentication=config['authentication'],
                configuration=config.get('configuration', {}),
                enabled=config.get('enabled', True),
                retry_attempts=config.get('retry_attempts', 3),
                timeout_seconds=config.get('timeout_seconds', 30)
            )
            
            # Store configuration
            self.integrations[integration_type] = integration_config
            
            # Persist to database
            self._save_integration_config(integration_config)
            
            logger.info(f"Configured {integration_type.value} integration")
            return True
            
        except Exception as e:
            logger.error(f"Failed to configure {integration_type.value} integration: {e}")
            return False
    
    def create_scan_session(self, target_urls: List[str], 
                          scan_parameters: Optional[Dict[str, Any]] = None) -> ScanSession:
        """
        Create a new XSS scanning session.
        
        Args:
            target_urls: List of URLs to scan
            scan_parameters: Configuration parameters for the scan
            
        Returns:
            ScanSession object for tracking the scan
        """
        session_id = str(uuid.uuid4())
        
        session = ScanSession(
            session_id=session_id,
            start_time=datetime.datetime.now(),
            target_urls=target_urls.copy(),
            scan_parameters=scan_parameters or {},
            findings=[],
            total_requests=0,
            coverage_metrics={},
            performance_metrics={}
        )
        
        # Store session
        self.scan_sessions[session_id] = session
        
        # Persist to database
        self._save_scan_session(session)
        
        logger.info(f"Created scan session {session_id} for {len(target_urls)} URLs")
        return session
    
    def add_finding(self, session_id: str, finding_data: Dict[str, Any]) -> VulnerabilityFinding:
        """
        Add a vulnerability finding to a scan session.
        
        Args:
            session_id: ID of the scan session
            finding_data: Dictionary containing finding details
            
        Returns:
            VulnerabilityFinding object that was created
        """
        if session_id not in self.scan_sessions:
            raise ValueError(f"Scan session {session_id} not found")
        
        # Generate finding ID
        finding_id = str(uuid.uuid4())
        
        # Determine severity if not provided
        severity = finding_data.get('severity', self._determine_severity(finding_data))
        
        # Create compliance mappings
        compliance_mappings = self._create_compliance_mappings(finding_data)
        
        # Create finding object
        finding = VulnerabilityFinding(
            finding_id=finding_id,
            title=finding_data['title'],
            description=finding_data['description'],
            severity=severity,
            confidence=finding_data.get('confidence', 0.8),
            affected_url=finding_data['affected_url'],
            vulnerable_parameter=finding_data.get('vulnerable_parameter', ''),
            attack_vector=finding_data.get('attack_vector', ''),
            proof_of_concept=finding_data.get('proof_of_concept', ''),
            remediation=finding_data.get('remediation', ''),
            references=finding_data.get('references', []),
            discovered_at=datetime.datetime.now(),
            last_verified=datetime.datetime.now(),
            status='open',
            assigned_to=finding_data.get('assigned_to'),
            estimated_effort=finding_data.get('estimated_effort'),
            business_impact=finding_data.get('business_impact'),
            compliance_mappings=compliance_mappings
        )
        
        # Add to session
        self.scan_sessions[session_id].findings.append(finding)
        
        # Persist to database
        self._save_finding(session_id, finding)
        
        logger.info(f"Added {severity.value} finding {finding_id} to session {session_id}")
        return finding
    
    def complete_scan_session(self, session_id: str, 
                            coverage_metrics: Optional[Dict[str, float]] = None,
                            performance_metrics: Optional[Dict[str, float]] = None):
        """
        Mark a scan session as complete and trigger integrations.
        
        Args:
            session_id: ID of the scan session to complete
            coverage_metrics: Scan coverage statistics
            performance_metrics: Performance statistics
        """
        if session_id not in self.scan_sessions:
            raise ValueError(f"Scan session {session_id} not found")
        
        session = self.scan_sessions[session_id]
        session.end_time = datetime.datetime.now()
        session.coverage_metrics = coverage_metrics or {}
        session.performance_metrics = performance_metrics or {}
        
        # Update database
        self._update_scan_session(session)
        
        # Trigger enterprise integrations
        self._trigger_integrations(session)
        
        logger.info(f"Completed scan session {session_id} with {len(session.findings)} findings")
    
    def _determine_severity(self, finding_data: Dict[str, Any]) -> SeverityLevel:
        """Automatically determine severity based on finding characteristics"""
        vulnerability_type = finding_data.get('vulnerability_type', '').lower()
        
        # Use predefined mappings
        if vulnerability_type in self.severity_mappings:
            return self.severity_mappings[vulnerability_type]
        
        # Default severity determination logic
        if 'stored' in finding_data.get('title', '').lower():
            return SeverityLevel.CRITICAL
        elif 'script' in finding_data.get('description', '').lower():
            return SeverityLevel.HIGH
        elif finding_data.get('confidence', 0) > 0.8:
            return SeverityLevel.HIGH
        else:
            return SeverityLevel.MEDIUM
    
    def _create_compliance_mappings(self, finding_data: Dict[str, Any]) -> Dict[ComplianceFramework, List[str]]:
        """Create compliance framework mappings for a finding"""
        mappings = {}
        vulnerability_type = finding_data.get('vulnerability_type', 'xss').lower()
        
        # OWASP Top 10 mapping
        if vulnerability_type in ['xss', 'stored_xss', 'dom_xss', 'reflected_xss']:
            mappings[ComplianceFramework.OWASP_TOP_10] = ['A03:2021 – Injection']
        
        # PCI DSS mapping
        if 'xss' in vulnerability_type:
            mappings[ComplianceFramework.PCI_DSS] = ['6.5.7 - Cross-site scripting (XSS)']
        
        # NIST CSF mapping
        mappings[ComplianceFramework.NIST_CSF] = ['PR.IP-12', 'DE.CM-8']
        
        return mappings
    
    def _trigger_integrations(self, session: ScanSession):
        """Trigger all configured integrations with scan results"""
        for integration_type, config in self.integrations.items():
            if not config.enabled:
                continue
            
            try:
                if integration_type == IntegrationType.CI_CD_PIPELINE:
                    self._integrate_cicd_pipeline(session, config)
                elif integration_type == IntegrationType.BUG_TRACKING:
                    self._integrate_bug_tracking(session, config)
                elif integration_type == IntegrationType.SIEM_PLATFORM:
                    self._integrate_siem_platform(session, config)
                elif integration_type == IntegrationType.NOTIFICATION_SYSTEM:
                    self._integrate_notification_system(session, config)
                elif integration_type == IntegrationType.SECURITY_DASHBOARD:
                    self._integrate_security_dashboard(session, config)
                
            except Exception as e:
                logger.error(f"Integration {integration_type.value} failed: {e}")
                self._log_integration_error(integration_type, str(e))
    
    def _integrate_cicd_pipeline(self, session: ScanSession, config: IntegrationConfig):
        """Integrate with CI/CD pipeline systems"""
        # Calculate scan summary
        critical_count = sum(1 for f in session.findings if f.severity == SeverityLevel.CRITICAL)
        high_count = sum(1 for f in session.findings if f.severity == SeverityLevel.HIGH)
        
        # Determine if build should fail
        fail_build = critical_count > 0 or high_count > 0
        
        # Create CI/CD payload
        payload = {
            'session_id': session.session_id,
            'scan_status': 'completed',
            'start_time': session.start_time.isoformat(),
            'end_time': session.end_time.isoformat() if session.end_time else None,
            'target_urls': session.target_urls,
            'total_findings': len(session.findings),
            'critical_findings': critical_count,
            'high_findings': high_count,
            'fail_build': fail_build,
            'findings_summary': [
                {
                    'id': f.finding_id,
                    'title': f.title,
                    'severity': f.severity.value,
                    'url': f.affected_url,
                    'confidence': f.confidence
                }
                for f in session.findings
            ]
        }
        
        # Send to CI/CD system
        self._send_integration_payload(IntegrationType.CI_CD_PIPELINE, config, payload)
        logger.info(f"Sent CI/CD integration for session {session.session_id}")
    
    def _integrate_bug_tracking(self, session: ScanSession, config: IntegrationConfig):
        """Integrate with bug tracking systems (Jira, GitHub Issues, etc.)"""
        # Create individual tickets for high/critical findings
        for finding in session.findings:
            if finding.severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH]:
                
                # Create bug ticket payload
                ticket_payload = {
                    'title': f"XSS Vulnerability: {finding.title}",
                    'description': self._format_bug_description(finding),
                    'severity': finding.severity.value,
                    'labels': ['security', 'xss', f'severity-{finding.severity.value}'],
                    'affected_url': finding.affected_url,
                    'session_id': session.session_id,
                    'finding_id': finding.finding_id,
                    'compliance_requirements': self._format_compliance_requirements(finding)
                }
                
                # Send to bug tracking system
                self._send_integration_payload(IntegrationType.BUG_TRACKING, config, ticket_payload)
        
        logger.info(f"Created bug tracking tickets for session {session.session_id}")
    
    def _integrate_siem_platform(self, session: ScanSession, config: IntegrationConfig):
        """Integrate with SIEM platforms (Splunk, ELK, etc.)"""
        # Create SIEM events for each finding
        for finding in session.findings:
            siem_event = {
                'timestamp': finding.discovered_at.isoformat(),
                'event_type': 'vulnerability_detected',
                'source': 'xss_security_scanner',
                'severity': finding.severity.value,
                'confidence': finding.confidence,
                'vulnerability_type': 'cross_site_scripting',
                'affected_asset': finding.affected_url,
                'attack_vector': finding.attack_vector,
                'session_id': session.session_id,
                'finding_id': finding.finding_id,
                'remediation_required': finding.severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH]
            }
            
            # Send to SIEM
            self._send_integration_payload(IntegrationType.SIEM_PLATFORM, config, siem_event)
        
        logger.info(f"Sent SIEM events for session {session.session_id}")
    
    def _integrate_notification_system(self, session: ScanSession, config: IntegrationConfig):
        """Integrate with notification systems (Slack, Teams, etc.)"""
        # Calculate summary statistics
        total_findings = len(session.findings)
        critical_count = sum(1 for f in session.findings if f.severity == SeverityLevel.CRITICAL)
        high_count = sum(1 for f in session.findings if f.severity == SeverityLevel.HIGH)
        
        # Create notification message
        if critical_count > 0:
            urgency = "🚨 CRITICAL"
            color = "danger"
        elif high_count > 0:
            urgency = "⚠️ HIGH"
            color = "warning"
        else:
            urgency = "ℹ️ INFO"
            color = "good"
        
        notification_payload = {
            'title': f"{urgency} - XSS Scan Results",
            'message': f"Scan completed for {len(session.target_urls)} URLs. Found {total_findings} vulnerabilities ({critical_count} critical, {high_count} high).",
            'color': color,
            'session_id': session.session_id,
            'scan_duration': str(session.end_time - session.start_time) if session.end_time else 'Unknown',
            'target_urls': session.target_urls[:3],  # Show first 3 URLs
            'findings_summary': [
                f"{f.severity.value.upper()}: {f.title} ({f.affected_url})"
                for f in session.findings[:5]  # Show first 5 findings
            ]
        }
        
        # Send notification
        self._send_integration_payload(IntegrationType.NOTIFICATION_SYSTEM, config, notification_payload)
        logger.info(f"Sent notification for session {session.session_id}")
    
    def _integrate_security_dashboard(self, session: ScanSession, config: IntegrationConfig):
        """Integrate with security dashboards and metrics systems"""
        # Create dashboard metrics payload
        dashboard_payload = {
            'session_id': session.session_id,
            'timestamp': session.end_time.isoformat() if session.end_time else datetime.datetime.now().isoformat(),
            'metrics': {
                'total_urls_scanned': len(session.target_urls),
                'total_requests': session.total_requests,
                'scan_duration_seconds': (session.end_time - session.start_time).total_seconds() if session.end_time else 0,
                'vulnerabilities_found': len(session.findings),
                'critical_vulnerabilities': sum(1 for f in session.findings if f.severity == SeverityLevel.CRITICAL),
                'high_vulnerabilities': sum(1 for f in session.findings if f.severity == SeverityLevel.HIGH),
                'medium_vulnerabilities': sum(1 for f in session.findings if f.severity == SeverityLevel.MEDIUM),
                'low_vulnerabilities': sum(1 for f in session.findings if f.severity == SeverityLevel.LOW),
                'average_confidence': sum(f.confidence for f in session.findings) / len(session.findings) if session.findings else 0.0
            },
            'coverage_metrics': session.coverage_metrics,
            'performance_metrics': session.performance_metrics
        }
        
        # Send to dashboard
        self._send_integration_payload(IntegrationType.SECURITY_DASHBOARD, config, dashboard_payload)
        logger.info(f"Sent dashboard metrics for session {session.session_id}")
    
    def _format_bug_description(self, finding: VulnerabilityFinding) -> str:
        """Format a detailed bug description for tracking systems"""
        description = f"""
## Vulnerability Summary
{finding.description}

## Technical Details
- **Affected URL:** {finding.affected_url}
- **Vulnerable Parameter:** {finding.vulnerable_parameter}
- **Severity:** {finding.severity.value.upper()}
- **Confidence:** {finding.confidence:.0%}
- **Discovery Date:** {finding.discovered_at.strftime('%Y-%m-%d %H:%M:%S')}

## Attack Vector
{finding.attack_vector}

## Proof of Concept
```
{finding.proof_of_concept}
```

## Remediation
{finding.remediation}

## Compliance Impact
{self._format_compliance_requirements(finding)}

## References
{chr(10).join('- ' + ref for ref in finding.references) if finding.references else 'None'}

---
*Generated by XSS Security Scanner - Finding ID: {finding.finding_id}*
        """.strip()
        
        return description
    
    def _format_compliance_requirements(self, finding: VulnerabilityFinding) -> str:
        """Format compliance requirements for a finding"""
        if not finding.compliance_mappings:
            return "None specified"
        
        requirements = []
        for framework, mappings in finding.compliance_mappings.items():
            framework_name = framework.value.replace('_', ' ').upper()
            requirements.append(f"**{framework_name}:** {', '.join(mappings)}")
        
        return '\n'.join(requirements)
    
    def _send_integration_payload(self, integration_type: IntegrationType, 
                                config: IntegrationConfig, payload: Dict[str, Any]):
        """Send payload to integration endpoint"""
        # This is a simplified implementation
        # In practice, you would use appropriate HTTP clients, authentication, etc.
        
        # Log the integration attempt
        log_entry = {
            'log_id': str(uuid.uuid4()),
            'integration_type': integration_type.value,
            'timestamp': datetime.datetime.now().timestamp(),
            'action': 'send_payload',
            'payload': json.dumps(payload),
            'success': True,  # Assume success for this example
            'response': '{"status": "success"}',
            'error_message': None
        }
        
        self._save_integration_log(log_entry)
        logger.info(f"Sent payload to {integration_type.value}: {config.endpoint_url}")
    
    def _log_integration_error(self, integration_type: IntegrationType, error_message: str):
        """Log integration errors for troubleshooting"""
        log_entry = {
            'log_id': str(uuid.uuid4()),
            'integration_type': integration_type.value,
            'timestamp': datetime.datetime.now().timestamp(),
            'action': 'error',
            'payload': '',
            'success': False,
            'response': '',
            'error_message': error_message
        }
        
        self._save_integration_log(log_entry)
    
    def generate_compliance_report(self, framework: ComplianceFramework, 
                                 date_range: Optional[Tuple[datetime.datetime, datetime.datetime]] = None) -> str:
        """
        Generate compliance report for specified framework.
        
        Args:
            framework: Compliance framework to report on
            date_range: Optional date range for the report
            
        Returns:
            Formatted compliance report
        """
        # Get relevant findings
        findings = self._get_findings_for_compliance(framework, date_range)
        
        report = f"{framework.value.upper().replace('_', ' ')} Compliance Report\n"
        report += "=" * 60 + "\n\n"
        
        # Executive Summary
        total_findings = len(findings)
        open_findings = len([f for f in findings if f.status == 'open'])
        critical_findings = len([f for f in findings if f.severity == SeverityLevel.CRITICAL])
        
        report += "EXECUTIVE SUMMARY\n"
        report += "-" * 20 + "\n"
        report += f"Report Period: {date_range[0].strftime('%Y-%m-%d') if date_range else 'All Time'} to {date_range[1].strftime('%Y-%m-%d') if date_range else 'Present'}\n"
        report += f"Total Findings: {total_findings}\n"
        report += f"Open Findings: {open_findings}\n"
        report += f"Critical Findings: {critical_findings}\n\n"
        
        # Compliance Status
        compliance_score = max(0, 100 - (critical_findings * 20) - (open_findings * 5))
        report += f"Compliance Score: {compliance_score}/100\n"
        report += f"Compliance Status: {'COMPLIANT' if compliance_score >= 80 else 'NON-COMPLIANT'}\n\n"
        
        # Findings by Compliance Requirement
        if framework in self.compliance_mappings:
            report += "FINDINGS BY REQUIREMENT\n"
            report += "-" * 25 + "\n"
            
            for category, requirements in self.compliance_mappings[framework].items():
                category_findings = [f for f in findings if category in f.title.lower() or category in f.description.lower()]
                report += f"{category.upper()}: {len(category_findings)} findings\n"
                for req in requirements:
                    report += f"  - {req}\n"
                report += "\n"
        
        # Detailed Findings
        if findings:
            report += "DETAILED FINDINGS\n"
            report += "-" * 20 + "\n"
            
            for i, finding in enumerate(findings[:10], 1):  # Show first 10
                report += f"[{i}] {finding.title} ({finding.severity.value.upper()})\n"
                report += f"URL: {finding.affected_url}\n"
                report += f"Status: {finding.status}\n"
                if finding.assigned_to:
                    report += f"Assigned to: {finding.assigned_to}\n"
                report += "\n"
        
        return report
    
    def generate_executive_dashboard(self) -> Dict[str, Any]:
        """Generate executive dashboard metrics"""
        # Get all findings from recent scans
        recent_findings = self._get_recent_findings(days=30)
        
        # Calculate key metrics
        dashboard = {
            'summary': {
                'total_scans_last_30_days': len(self.scan_sessions),
                'total_findings_last_30_days': len(recent_findings),
                'critical_findings': len([f for f in recent_findings if f.severity == SeverityLevel.CRITICAL]),
                'high_findings': len([f for f in recent_findings if f.severity == SeverityLevel.HIGH]),
                'average_findings_per_scan': len(recent_findings) / max(len(self.scan_sessions), 1),
                'compliance_score': self._calculate_overall_compliance_score(recent_findings)
            },
            'trends': {
                'vulnerability_trend': self._calculate_vulnerability_trend(),
                'remediation_rate': self._calculate_remediation_rate(),
                'scan_frequency': self._calculate_scan_frequency()
            },
            'top_vulnerabilities': self._get_top_vulnerability_types(recent_findings),
            'most_affected_urls': self._get_most_affected_urls(recent_findings),
            'compliance_status': self._get_compliance_status_summary(recent_findings)
        }
        
        return dashboard
    
    # Database helper methods
    
    def _save_integration_config(self, config: IntegrationConfig):
        """Save integration configuration to database"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO integrations VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            config.integration_type.value,
            config.endpoint_url,
            json.dumps(config.authentication),
            json.dumps(config.configuration),
            config.enabled,
            config.retry_attempts,
            config.timeout_seconds
        ))
        
        conn.commit()
        conn.close()
    
    def _save_scan_session(self, session: ScanSession):
        """Save scan session to database"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO scan_sessions VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session.session_id,
            session.start_time.timestamp(),
            session.end_time.timestamp() if session.end_time else None,
            json.dumps(session.target_urls),
            json.dumps(session.scan_parameters),
            session.total_requests,
            json.dumps(session.coverage_metrics),
            json.dumps(session.performance_metrics)
        ))
        
        conn.commit()
        conn.close()
    
    def _save_finding(self, session_id: str, finding: VulnerabilityFinding):
        """Save vulnerability finding to database"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO findings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            finding.finding_id,
            session_id,
            finding.title,
            finding.description,
            finding.severity.value,
            finding.confidence,
            finding.affected_url,
            finding.vulnerable_parameter,
            finding.attack_vector,
            finding.proof_of_concept,
            finding.remediation,
            json.dumps(finding.references),
            finding.discovered_at.timestamp(),
            finding.last_verified.timestamp(),
            finding.status,
            finding.assigned_to,
            finding.estimated_effort,
            finding.business_impact,
            json.dumps({k.value: v for k, v in finding.compliance_mappings.items()})
        ))
        
        conn.commit()
        conn.close()
    
    def _save_integration_log(self, log_entry: Dict[str, Any]):
        """Save integration log entry to database"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO integration_logs VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            log_entry['log_id'],
            log_entry['integration_type'],
            log_entry['timestamp'],
            log_entry['action'],
            log_entry['payload'],
            log_entry['response'],
            log_entry['success'],
            log_entry['error_message']
        ))
        
        conn.commit()
        conn.close()
    
    def _update_scan_session(self, session: ScanSession):
        """Update scan session in database"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE scan_sessions 
            SET end_time = ?, coverage_metrics = ?, performance_metrics = ?
            WHERE session_id = ?
        ''', (
            session.end_time.timestamp() if session.end_time else None,
            json.dumps(session.coverage_metrics),
            json.dumps(session.performance_metrics),
            session.session_id
        ))
        
        conn.commit()
        conn.close()
    
    # Helper methods for analytics and reporting
    
    def _get_findings_for_compliance(self, framework: ComplianceFramework, 
                                   date_range: Optional[Tuple[datetime.datetime, datetime.datetime]]) -> List[VulnerabilityFinding]:
        """Get findings relevant to a compliance framework"""
        # This would query the database for relevant findings
        # For this example, we'll return findings from current sessions
        findings = []
        for session in self.scan_sessions.values():
            for finding in session.findings:
                if framework in finding.compliance_mappings:
                    if not date_range or (date_range[0] <= finding.discovered_at <= date_range[1]):
                        findings.append(finding)
        return findings
    
    def _get_recent_findings(self, days: int) -> List[VulnerabilityFinding]:
        """Get findings from recent scans"""
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
        findings = []
        for session in self.scan_sessions.values():
            if session.start_time >= cutoff_date:
                findings.extend(session.findings)
        return findings
    
    def _calculate_overall_compliance_score(self, findings: List[VulnerabilityFinding]) -> float:
        """Calculate overall compliance score based on findings"""
        if not findings:
            return 100.0
        
        critical_count = sum(1 for f in findings if f.severity == SeverityLevel.CRITICAL)
        high_count = sum(1 for f in findings if f.severity == SeverityLevel.HIGH)
        
        # Simple scoring algorithm
        score = 100.0 - (critical_count * 20) - (high_count * 10)
        return max(0.0, min(100.0, score))
    
    def _calculate_vulnerability_trend(self) -> str:
        """Calculate vulnerability trend (increasing/decreasing/stable)"""
        # Simplified trend calculation
        return "stable"  # Would implement actual trend analysis
    
    def _calculate_remediation_rate(self) -> float:
        """Calculate rate of vulnerability remediation"""
        all_findings = []
        for session in self.scan_sessions.values():
            all_findings.extend(session.findings)
        
        if not all_findings:
            return 0.0
        
        resolved_count = sum(1 for f in all_findings if f.status == 'resolved')
        return (resolved_count / len(all_findings)) * 100
    
    def _calculate_scan_frequency(self) -> str:
        """Calculate scanning frequency"""
        if len(self.scan_sessions) >= 30:
            return "daily"
        elif len(self.scan_sessions) >= 7:
            return "weekly"
        else:
            return "infrequent"
    
    def _get_top_vulnerability_types(self, findings: List[VulnerabilityFinding]) -> List[Dict[str, Any]]:
        """Get top vulnerability types by frequency"""
        type_counts = {}
        for finding in findings:
            # Extract vulnerability type from title
            vuln_type = finding.title.split(':')[0] if ':' in finding.title else 'XSS'
            type_counts[vuln_type] = type_counts.get(vuln_type, 0) + 1
        
        # Sort by count and return top 5
        sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
        return [{'type': t, 'count': c} for t, c in sorted_types[:5]]
    
    def _get_most_affected_urls(self, findings: List[VulnerabilityFinding]) -> List[Dict[str, Any]]:
        """Get URLs with most vulnerabilities"""
        url_counts = {}
        for finding in findings:
            url_counts[finding.affected_url] = url_counts.get(finding.affected_url, 0) + 1
        
        # Sort by count and return top 5
        sorted_urls = sorted(url_counts.items(), key=lambda x: x[1], reverse=True)
        return [{'url': u, 'count': c} for u, c in sorted_urls[:5]]
    
    def _get_compliance_status_summary(self, findings: List[VulnerabilityFinding]) -> Dict[str, str]:
        """Get compliance status for each framework"""
        status_summary = {}
        
        for framework in ComplianceFramework:
            framework_findings = [f for f in findings if framework in f.compliance_mappings]
            critical_count = sum(1 for f in framework_findings if f.severity == SeverityLevel.CRITICAL)
            
            if critical_count > 0:
                status_summary[framework.value] = "non_compliant"
            elif len(framework_findings) > 10:
                status_summary[framework.value] = "at_risk"
            else:
                status_summary[framework.value] = "compliant"
        
        return status_summary