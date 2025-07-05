#!/usr/bin/env python3
"""
GitHub GraphQL Security Exercise 02: Advanced Security Analysis

Exercise Objective:
Build an advanced GitHub security analyzer that can:
1. Perform organization-wide security assessment  
2. Analyze repository configurations and access controls
3. Implement custom security rules and policies
4. Generate executive security reports with risk prioritization

Learning Goals:
- Advanced GraphQL queries with pagination
- Security policy implementation and evaluation
- Risk assessment and prioritization algorithms
- Executive-level reporting and dashboards

Prerequisites:
- Completion of Exercise 01
- GitHub organization access or multiple repositories
- Understanding of security frameworks (ISO 27001, etc.)

Time Investment: 60 minutes

Instructions:
1. Implement the missing security analysis functions
2. Define custom security rules for your organization
3. Run analysis against multiple repositories
4. Generate executive-level security dashboard

Security Focus:
This exercise emphasizes enterprise security management, policy
enforcement, and risk-based security decision making.
"""

import os
import json
import time
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import requests


class SecuritySeverity(Enum):
    """Security finding severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class RiskLevel(Enum):
    """Risk level classification"""
    CRITICAL = "critical"
    HIGH = "high" 
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class SecurityFinding:
    """Security finding or policy violation"""
    id: str
    title: str
    description: str
    severity: SecuritySeverity
    category: str
    repository: str
    recommendation: str
    evidence: Dict[str, Any]
    policy_id: Optional[str] = None


@dataclass
class RepositorySecurityProfile:
    """Complete security profile for a repository"""
    name: str
    is_private: bool
    primary_language: str
    vulnerability_count: int
    critical_vulns: int
    high_vulns: int
    has_vulnerability_alerts: bool
    has_branch_protection: bool
    admin_count: int
    collaborator_count: int
    last_push: str
    findings: List[SecurityFinding]
    risk_score: float
    risk_level: RiskLevel


@dataclass
class SecurityPolicy:
    """Custom security policy definition"""
    id: str
    name: str
    description: str
    category: str
    severity: SecuritySeverity
    check_function: Callable[[Dict[str, Any]], bool]
    recommendation: str


class AdvancedSecurityAnalyzer:
    """Advanced GitHub security analyzer for enterprise assessment"""
    
    def __init__(self, token: str):
        """Initialize the advanced security analyzer"""
        self.token = token
        self.base_url = "https://api.github.com/graphql"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "Advanced-Security-Analyzer/2.0"
        })
        
        # Security policies registry
        self.policies: List[SecurityPolicy] = []
        self._register_default_policies()
        
        # Rate limiting
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = None
    
    def _execute_query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute GraphQL query with rate limiting"""
        # Check rate limit
        if self.rate_limit_remaining < 100:
            if self.rate_limit_reset:
                wait_time = max(0, self.rate_limit_reset - time.time())
                if wait_time > 0:
                    print(f"⏳ Rate limit low ({self.rate_limit_remaining} remaining). Waiting {wait_time:.0f}s...")
                    time.sleep(wait_time + 1)
        
        payload = {
            "query": query,
            "variables": variables or {}
        }
        
        response = self.session.post(self.base_url, json=payload, timeout=30)
        response.raise_for_status()
        
        # Update rate limit info
        self.rate_limit_remaining = int(response.headers.get("X-RateLimit-Remaining", 5000))
        reset_timestamp = response.headers.get("X-RateLimit-Reset")
        if reset_timestamp:
            self.rate_limit_reset = int(reset_timestamp)
        
        result = response.json()
        
        if "errors" in result:
            error_messages = [error.get("message", "Unknown error") for error in result["errors"]]
            raise Exception(f"GraphQL errors: {'; '.join(error_messages)}")
        
        return result.get("data", {})
    
    def _register_default_policies(self):
        """Register default security policies"""
        
        # TODO: Implement security policy registration
        # Add the following security policies:
        
        # 1. Critical Vulnerabilities Policy
        self.register_policy(SecurityPolicy(
            id="critical_vulns",
            name="Critical Vulnerabilities",
            description="Repositories with critical security vulnerabilities",
            category="vulnerability",
            severity=SecuritySeverity.CRITICAL,
            check_function=lambda repo: repo.get("critical_vulnerabilities", 0) > 0,
            recommendation="Immediately address critical vulnerabilities through dependency updates or patches"
        ))
        
        # 2. Missing Vulnerability Alerts Policy
        self.register_policy(SecurityPolicy(
            id="missing_vuln_alerts",
            name="Missing Vulnerability Alerts",
            description="Repositories without vulnerability alerts enabled",
            category="configuration",
            severity=SecuritySeverity.MEDIUM,
            check_function=lambda repo: not repo.get("hasVulnerabilityAlertsEnabled", False),
            recommendation="Enable vulnerability alerts in repository settings"
        ))
        
        # 3. Public Repository with High Vulnerabilities
        self.register_policy(SecurityPolicy(
            id="public_high_vulns",
            name="Public Repository with High Vulnerabilities",
            description="Public repositories containing high-severity vulnerabilities",
            category="exposure",
            severity=SecuritySeverity.HIGH,
            check_function=lambda repo: (
                not repo.get("isPrivate", True) and 
                repo.get("high_vulnerabilities", 0) > 0
            ),
            recommendation="Address vulnerabilities in public repositories or consider making repository private"
        ))
        
        # 4. Missing Branch Protection
        self.register_policy(SecurityPolicy(
            id="missing_branch_protection",
            name="Missing Branch Protection",
            description="Repositories without branch protection on main branch",
            category="access_control",
            severity=SecuritySeverity.MEDIUM,
            check_function=lambda repo: not repo.get("has_branch_protection", False),
            recommendation="Enable branch protection rules requiring reviews and status checks"
        ))
        
        # 5. Excessive Admin Access
        self.register_policy(SecurityPolicy(
            id="excessive_admin_access",
            name="Excessive Admin Access",
            description="Repositories with too many administrators",
            category="access_control", 
            severity=SecuritySeverity.MEDIUM,
            check_function=lambda repo: repo.get("admin_count", 0) > 5,
            recommendation="Review admin access and apply principle of least privilege"
        ))
    
    def register_policy(self, policy: SecurityPolicy):
        """Register a custom security policy"""
        self.policies.append(policy)
    
    def get_organization_repositories(self, org_name: str, max_repos: int = 50) -> List[Dict[str, Any]]:
        """
        TODO: Implement organization repository discovery
        
        Get repositories from a GitHub organization with security-relevant information.
        
        Args:
            org_name: Organization name
            max_repos: Maximum number of repositories to fetch
            
        Returns:
            List of repository data dictionaries
            
        GraphQL Query should include:
        - Basic repository info (name, visibility, language)
        - Vulnerability alerts summary
        - Branch protection information
        - Collaborator/admin information
        - Security settings
        """
        query = """
        query OrganizationRepositories($org: String!, $cursor: String, $first: Int!) {
          organization(login: $org) {
            repositories(first: $first, after: $cursor, orderBy: {field: UPDATED_AT, direction: DESC}) {
              pageInfo {
                hasNextPage
                endCursor
              }
              nodes {
                name
                isPrivate
                primaryLanguage {
                  name
                }
                pushedAt
                hasVulnerabilityAlertsEnabled
                
                vulnerabilityAlerts(first: 1) {
                  totalCount
                  nodes {
                    securityVulnerability {
                      severity
                    }
                  }
                }
                
                # Get detailed vulnerability breakdown
                criticalAlerts: vulnerabilityAlerts(first: 100, states: [OPEN]) {
                  nodes {
                    securityVulnerability {
                      severity
                    }
                  }
                }
                
                branchProtectionRules(first: 5) {
                  totalCount
                  nodes {
                    pattern
                    requiresApprovingReviews
                    requiredApprovingReviewCount
                  }
                }
                
                collaborators(first: 100) {
                  totalCount
                  nodes {
                    permission
                  }
                }
              }
            }
          }
        }
        """
        
        repositories = []
        cursor = None
        fetched = 0
        
        while fetched < max_repos:
            batch_size = min(20, max_repos - fetched)
            variables = {
                "org": org_name,
                "cursor": cursor,
                "first": batch_size
            }
            
            try:
                result = self._execute_query(query, variables)
                org_data = result.get("organization", {})
                
                if not org_data:
                    print(f"Organization '{org_name}' not found or not accessible")
                    break
                
                repos_data = org_data.get("repositories", {})
                repos = repos_data.get("nodes", [])
                
                # Process each repository
                for repo in repos:
                    # Count vulnerabilities by severity
                    critical_count = 0
                    high_count = 0
                    total_vulns = repo.get("vulnerabilityAlerts", {}).get("totalCount", 0)
                    
                    for alert in repo.get("criticalAlerts", {}).get("nodes", []):
                        severity = alert.get("securityVulnerability", {}).get("severity", "").upper()
                        if severity == "CRITICAL":
                            critical_count += 1
                        elif severity == "HIGH":
                            high_count += 1
                    
                    # Count admin users
                    admin_count = len([
                        collab for collab in repo.get("collaborators", {}).get("nodes", [])
                        if collab.get("permission") == "ADMIN"
                    ])
                    
                    # Check branch protection
                    has_protection = repo.get("branchProtectionRules", {}).get("totalCount", 0) > 0
                    
                    # Enrich repository data
                    repo["vulnerability_count"] = total_vulns
                    repo["critical_vulnerabilities"] = critical_count
                    repo["high_vulnerabilities"] = high_count
                    repo["admin_count"] = admin_count
                    repo["collaborator_count"] = repo.get("collaborators", {}).get("totalCount", 0)
                    repo["has_branch_protection"] = has_protection
                    
                    repositories.append(repo)
                    fetched += 1
                
                # Check pagination
                page_info = repos_data.get("pageInfo", {})
                if not page_info.get("hasNextPage") or fetched >= max_repos:
                    break
                
                cursor = page_info.get("endCursor")
                
            except Exception as e:
                print(f"Error fetching repositories: {e}")
                break
        
        print(f"📚 Discovered {len(repositories)} repositories in organization '{org_name}'")
        return repositories
    
    def analyze_repository_security(self, repo_data: Dict[str, Any]) -> RepositorySecurityProfile:
        """
        TODO: Implement comprehensive repository security analysis
        
        Analyze a repository against all registered security policies.
        
        Args:
            repo_data: Repository data from GraphQL query
            
        Returns:
            RepositorySecurityProfile with findings and risk assessment
            
        Steps:
        1. Evaluate all registered policies against the repository
        2. Calculate risk score based on findings
        3. Determine risk level
        4. Create comprehensive security profile
        """
        findings = []
        
        # Evaluate all policies
        for policy in self.policies:
            try:
                if policy.check_function(repo_data):
                    finding = SecurityFinding(
                        id=f"{policy.id}_{repo_data.get('name', 'unknown')}",
                        title=policy.name,
                        description=policy.description,
                        severity=policy.severity,
                        category=policy.category,
                        repository=repo_data.get("name", "unknown"),
                        recommendation=policy.recommendation,
                        evidence={
                            "policy_id": policy.id,
                            "repository_data": {
                                "vulnerability_count": repo_data.get("vulnerability_count", 0),
                                "critical_vulnerabilities": repo_data.get("critical_vulnerabilities", 0),
                                "high_vulnerabilities": repo_data.get("high_vulnerabilities", 0),
                                "hasVulnerabilityAlertsEnabled": repo_data.get("hasVulnerabilityAlertsEnabled", False),
                                "isPrivate": repo_data.get("isPrivate", True),
                                "has_branch_protection": repo_data.get("has_branch_protection", False),
                                "admin_count": repo_data.get("admin_count", 0)
                            }
                        },
                        policy_id=policy.id
                    )
                    findings.append(finding)
            except Exception as e:
                print(f"Error evaluating policy {policy.id}: {e}")
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(repo_data, findings)
        
        # Determine risk level
        if risk_score >= 80:
            risk_level = RiskLevel.CRITICAL
        elif risk_score >= 60:
            risk_level = RiskLevel.HIGH
        elif risk_score >= 30:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        # Create security profile
        profile = RepositorySecurityProfile(
            name=repo_data.get("name", "unknown"),
            is_private=repo_data.get("isPrivate", True),
            primary_language=repo_data.get("primaryLanguage", {}).get("name", "Unknown"),
            vulnerability_count=repo_data.get("vulnerability_count", 0),
            critical_vulns=repo_data.get("critical_vulnerabilities", 0),
            high_vulns=repo_data.get("high_vulnerabilities", 0),
            has_vulnerability_alerts=repo_data.get("hasVulnerabilityAlertsEnabled", False),
            has_branch_protection=repo_data.get("has_branch_protection", False),
            admin_count=repo_data.get("admin_count", 0),
            collaborator_count=repo_data.get("collaborator_count", 0),
            last_push=repo_data.get("pushedAt", ""),
            findings=findings,
            risk_score=risk_score,
            risk_level=risk_level
        )
        
        return profile
    
    def _calculate_risk_score(self, repo_data: Dict[str, Any], findings: List[SecurityFinding]) -> float:
        """
        TODO: Implement risk score calculation
        
        Calculate a numerical risk score (0-100) based on repository data and findings.
        
        Args:
            repo_data: Repository data
            findings: List of security findings
            
        Returns:
            Risk score between 0-100
            
        Consider factors like:
        - Number and severity of vulnerabilities
        - Security configuration gaps
        - Access control issues
        - Repository visibility and sensitivity
        """
        score = 0.0
        
        # Vulnerability scoring
        critical_vulns = repo_data.get("critical_vulnerabilities", 0)
        high_vulns = repo_data.get("high_vulnerabilities", 0)
        total_vulns = repo_data.get("vulnerability_count", 0)
        
        # High impact for critical and high vulnerabilities
        score += critical_vulns * 25  # 25 points per critical
        score += high_vulns * 15     # 15 points per high
        score += max(0, total_vulns - critical_vulns - high_vulns) * 2  # 2 points per other
        
        # Configuration scoring
        if not repo_data.get("hasVulnerabilityAlertsEnabled", False):
            score += 10
        
        if not repo_data.get("has_branch_protection", False):
            score += 15
        
        # Access control scoring
        admin_count = repo_data.get("admin_count", 0)
        if admin_count > 5:
            score += (admin_count - 5) * 3  # 3 points per excess admin
        
        # Exposure risk
        if not repo_data.get("isPrivate", True):
            if total_vulns > 0:
                score += 20  # Public repo with vulnerabilities
        
        # Policy violation scoring
        for finding in findings:
            if finding.severity == SecuritySeverity.CRITICAL:
                score += 15
            elif finding.severity == SecuritySeverity.HIGH:
                score += 10
            elif finding.severity == SecuritySeverity.MEDIUM:
                score += 5
        
        # Cap at 100
        return min(100.0, score)
    
    def generate_executive_report(self, profiles: List[RepositorySecurityProfile]) -> Dict[str, Any]:
        """
        TODO: Implement executive security report generation
        
        Generate an executive-level security report for leadership.
        
        Args:
            profiles: List of repository security profiles
            
        Returns:
            Executive report dictionary
            
        Report should include:
        - High-level security metrics and KPIs
        - Risk distribution and trends
        - Top security issues requiring attention
        - Strategic recommendations
        - Compliance status overview
        """
        if not profiles:
            return {"error": "No repository profiles provided"}
        
        # Calculate high-level metrics
        total_repos = len(profiles)
        total_vulns = sum(p.vulnerability_count for p in profiles)
        critical_repos = len([p for p in profiles if p.risk_level == RiskLevel.CRITICAL])
        high_risk_repos = len([p for p in profiles if p.risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]])
        
        # Risk distribution
        risk_distribution = {
            "critical": len([p for p in profiles if p.risk_level == RiskLevel.CRITICAL]),
            "high": len([p for p in profiles if p.risk_level == RiskLevel.HIGH]),
            "medium": len([p for p in profiles if p.risk_level == RiskLevel.MEDIUM]),
            "low": len([p for p in profiles if p.risk_level == RiskLevel.LOW])
        }
        
        # Top vulnerable repositories
        top_vulnerable = sorted(profiles, key=lambda p: p.risk_score, reverse=True)[:10]
        
        # Security configuration gaps
        missing_alerts = len([p for p in profiles if not p.has_vulnerability_alerts])
        missing_protection = len([p for p in profiles if not p.has_branch_protection])
        
        # Generate strategic recommendations
        recommendations = []
        if critical_repos > 0:
            recommendations.append(f"🚨 URGENT: {critical_repos} repositories require immediate security attention")
        if missing_alerts > total_repos * 0.3:
            recommendations.append(f"📢 Enable vulnerability alerts on {missing_alerts} repositories")
        if missing_protection > total_repos * 0.5:
            recommendations.append(f"🔒 Implement branch protection on {missing_protection} repositories")
        if total_vulns > total_repos * 5:
            recommendations.append("🔄 Consider automated dependency management tools")
        
        recommendations.extend([
            "📊 Establish regular security monitoring and reporting",
            "🎓 Provide security training for development teams",
            "🔐 Implement security scanning in CI/CD pipelines"
        ])
        
        return {
            "executive_summary": {
                "total_repositories": total_repos,
                "total_vulnerabilities": total_vulns,
                "high_risk_repositories": high_risk_repos,
                "critical_repositories": critical_repos,
                "average_risk_score": sum(p.risk_score for p in profiles) / total_repos,
                "security_posture": "CRITICAL" if critical_repos > 0 else "NEEDS_ATTENTION" if high_risk_repos > total_repos * 0.2 else "GOOD"
            },
            "risk_distribution": risk_distribution,
            "configuration_gaps": {
                "missing_vulnerability_alerts": missing_alerts,
                "missing_branch_protection": missing_protection,
                "repositories_without_security_scanning": missing_alerts
            },
            "top_vulnerable_repositories": [
                {
                    "name": p.name,
                    "risk_score": p.risk_score,
                    "risk_level": p.risk_level.value,
                    "critical_vulnerabilities": p.critical_vulns,
                    "high_vulnerabilities": p.high_vulns,
                    "total_vulnerabilities": p.vulnerability_count
                }
                for p in top_vulnerable
            ],
            "strategic_recommendations": recommendations,
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "repositories_analyzed": total_repos,
                "analyzer_version": "2.0"
            }
        }
    
    def print_executive_report(self, report: Dict[str, Any]):
        """Print formatted executive report"""
        summary = report["executive_summary"]
        
        print(f"\n{'='*70}")
        print(f"🏢 EXECUTIVE SECURITY REPORT")
        print(f"{'='*70}")
        
        print(f"\n📊 ORGANIZATION SECURITY POSTURE: {summary['security_posture']}")
        print(f"   Total Repositories: {summary['total_repositories']}")
        print(f"   Total Vulnerabilities: {summary['total_vulnerabilities']}")
        print(f"   High-Risk Repositories: {summary['high_risk_repositories']}")
        print(f"   Average Risk Score: {summary['average_risk_score']:.1f}/100")
        
        print(f"\n📈 RISK DISTRIBUTION:")
        for level, count in report["risk_distribution"].items():
            percentage = (count / summary['total_repositories']) * 100
            emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}[level]
            print(f"   {emoji} {level.upper()}: {count} ({percentage:.1f}%)")
        
        print(f"\n⚠️  TOP VULNERABLE REPOSITORIES:")
        for repo in report["top_vulnerable_repositories"][:5]:
            print(f"   • {repo['name']}: {repo['risk_score']:.1f} (Critical: {repo['critical_vulnerabilities']}, High: {repo['high_vulnerabilities']})")
        
        print(f"\n💡 STRATEGIC RECOMMENDATIONS:")
        for rec in report["strategic_recommendations"]:
            print(f"   {rec}")
        
        print(f"\n📅 Report Generated: {report['report_metadata']['generated_at']}")
        print(f"{'='*70}\n")


def main():
    """Main function for advanced security analysis exercise"""
    print("🚀 Advanced GitHub Security Analysis Exercise")
    print("=" * 55)
    
    # Get configuration from environment
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ Error: GITHUB_TOKEN environment variable not set")
        return
    
    org_name = os.getenv("GITHUB_ORG", "microsoft")  # Default to Microsoft for examples
    max_repos = int(os.getenv("MAX_REPOS", "20"))
    
    print(f"🏢 Analyzing organization: {org_name}")
    print(f"📊 Maximum repositories: {max_repos}")
    
    try:
        # Initialize analyzer
        analyzer = AdvancedSecurityAnalyzer(token)
        print("✅ Advanced security analyzer initialized")
        
        # Get organization repositories
        print("🔍 Discovering repositories...")
        repositories = analyzer.get_organization_repositories(org_name, max_repos)
        
        if not repositories:
            print("❌ No repositories found. Check organization name and permissions.")
            return
        
        # Analyze each repository
        print("📋 Analyzing repository security...")
        profiles = []
        for repo in repositories:
            profile = analyzer.analyze_repository_security(repo)
            profiles.append(profile)
            
            # Show progress
            status = "🔴" if profile.risk_level == RiskLevel.CRITICAL else "🟠" if profile.risk_level == RiskLevel.HIGH else "🟡" if profile.risk_level == RiskLevel.MEDIUM else "🟢"
            print(f"   {status} {profile.name}: {profile.risk_score:.1f} ({len(profile.findings)} findings)")
        
        # Generate executive report
        print("\n📊 Generating executive report...")
        exec_report = analyzer.generate_executive_report(profiles)
        analyzer.print_executive_report(exec_report)
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save executive report
        exec_filename = f"executive_security_report_{org_name}_{timestamp}.json"
        with open(exec_filename, 'w') as f:
            json.dump(exec_report, f, indent=2, default=str)
        
        # Save detailed profiles
        detailed_filename = f"detailed_security_analysis_{org_name}_{timestamp}.json"
        profiles_data = [asdict(profile) for profile in profiles]
        with open(detailed_filename, 'w') as f:
            json.dump(profiles_data, f, indent=2, default=str, ensure_ascii=False)
        
        print(f"📄 Executive report saved: {exec_filename}")
        print(f"📄 Detailed analysis saved: {detailed_filename}")
        
        print(f"\n🎯 Exercise Complete! Analyzed {len(profiles)} repositories.")
        print("Next steps: Review findings and implement security improvements.")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()


"""
ADVANCED EXERCISE CHECKLIST:
- [ ] Set up environment variables (GITHUB_TOKEN, GITHUB_ORG)
- [ ] Implement get_organization_repositories() method
- [ ] Implement analyze_repository_security() method
- [ ] Implement _calculate_risk_score() method
- [ ] Implement generate_executive_report() method
- [ ] Run analysis against an organization
- [ ] Review executive security report
- [ ] Customize security policies for your needs

BONUS CHALLENGES:
- [ ] Add compliance framework mapping (ISO 27001, SOC 2)
- [ ] Implement trend analysis with historical data
- [ ] Create HTML executive dashboard
- [ ] Add integration with security tools (Jira, Slack)
- [ ] Implement automated remediation suggestions
- [ ] Add support for GitHub Enterprise Server

ENTERPRISE CONSIDERATIONS:
- [ ] Scale to handle 1000+ repositories
- [ ] Implement caching for large organizations
- [ ] Add role-based report filtering
- [ ] Create scheduled scanning capabilities
- [ ] Implement alerting for critical findings
- [ ] Add audit logging and compliance reporting

SECURITY BEST PRACTICES:
- Use least-privilege token scoping
- Implement secure secret management
- Add rate limiting and error handling
- Follow security policy frameworks
- Regular security assessment cycles
- Executive reporting and accountability
"""