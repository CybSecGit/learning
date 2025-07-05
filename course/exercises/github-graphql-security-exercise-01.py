#!/usr/bin/env python3
"""
GitHub GraphQL Security Exercise 01: Basic Vulnerability Scanner

Exercise Objective:
Build a basic GitHub GraphQL vulnerability scanner that can:
1. Authenticate with GitHub's GraphQL API
2. Query repository vulnerability alerts
3. Parse and categorize vulnerabilities by severity
4. Generate a basic security report

Learning Goals:
- Set up secure GitHub GraphQL authentication
- Write basic GraphQL queries for security data
- Handle API responses and error cases
- Generate actionable security insights

Prerequisites:
- GitHub account with access to repositories
- GitHub personal access token with appropriate scopes
- Python 3.8+ with requests library

Time Investment: 45 minutes

Instructions:
1. Set up your environment variables (see step 1)
2. Implement the missing functions marked with TODO
3. Run the scanner against a test repository
4. Review the generated security report

Security Focus:
This exercise emphasizes secure API practices, proper token management,
and defensive security scanning techniques.
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class VulnerabilityInfo:
    """Structure for vulnerability information"""
    id: str
    severity: str
    package_name: str
    ecosystem: str
    summary: str
    created_at: str
    state: str
    ghsa_id: Optional[str] = None
    cvss_score: Optional[float] = None


class GitHubGraphQLSecurityScanner:
    """Basic GitHub GraphQL security scanner for learning"""
    
    def __init__(self, token: str):
        """
        Initialize the scanner with a GitHub token
        
        Args:
            token: GitHub personal access token with security_events scope
        """
        self.token = token
        self.base_url = "https://api.github.com/graphql"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "GitHub-Security-Scanner-Exercise/1.0"
        })
        
        # Validate token on initialization
        if not self._validate_token():
            raise ValueError("Invalid or insufficient token permissions")
    
    def _validate_token(self) -> bool:
        """
        TODO: Implement token validation
        
        Validate that the token has necessary permissions for security scanning.
        Use a simple GraphQL query to test basic access.
        
        Returns:
            bool: True if token is valid and has necessary permissions
            
        Hint: Try querying the viewer's login to test basic access
        """
        query = """
        query TokenValidation {
          viewer {
            login
          }
          rateLimit {
            remaining
          }
        }
        """
        
        try:
            result = self._execute_query(query)
            # Check if we got a valid response with viewer data
            return bool(result.get("viewer", {}).get("login"))
        except Exception:
            return False
    
    def _execute_query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a GraphQL query
        
        Args:
            query: GraphQL query string
            variables: Optional query variables
            
        Returns:
            Dict containing the query response data
            
        Raises:
            Exception: If the query fails or returns errors
        """
        payload = {
            "query": query,
            "variables": variables or {}
        }
        
        response = self.session.post(self.base_url, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        if "errors" in result:
            error_messages = [error.get("message", "Unknown error") for error in result["errors"]]
            raise Exception(f"GraphQL errors: {'; '.join(error_messages)}")
        
        return result.get("data", {})
    
    def scan_repository_vulnerabilities(self, owner: str, name: str) -> List[VulnerabilityInfo]:
        """
        TODO: Implement repository vulnerability scanning
        
        Scan a repository for vulnerability alerts using GitHub's GraphQL API.
        
        Args:
            owner: Repository owner (user or organization)
            name: Repository name
            
        Returns:
            List of VulnerabilityInfo objects
            
        Steps:
        1. Create a GraphQL query to fetch vulnerability alerts
        2. Include severity, package info, and advisory details
        3. Parse the response and create VulnerabilityInfo objects
        4. Handle pagination if there are many vulnerabilities
        
        GraphQL Query Structure:
        - Use the repository(owner: $owner, name: $name) field
        - Query vulnerabilityAlerts with relevant fields
        - Include securityVulnerability and advisory information
        """
        query = """
        query RepositoryVulnerabilities($owner: String!, $name: String!, $cursor: String) {
          repository(owner: $owner, name: $name) {
            vulnerabilityAlerts(first: 100, after: $cursor) {
              pageInfo {
                hasNextPage
                endCursor
              }
              nodes {
                id
                createdAt
                state
                securityVulnerability {
                  severity
                  package {
                    name
                    ecosystem
                  }
                  advisory {
                    ghsaId
                    summary
                    cvss {
                      score
                    }
                  }
                }
              }
            }
          }
        }
        """
        
        variables = {"owner": owner, "name": name}
        vulnerabilities = []
        cursor = None
        
        while True:
            if cursor:
                variables["cursor"] = cursor
            
            try:
                result = self._execute_query(query, variables)
                repo_data = result.get("repository", {})
                
                if not repo_data:
                    print(f"Repository {owner}/{name} not found or not accessible")
                    break
                
                alerts_data = repo_data.get("vulnerabilityAlerts", {})
                alerts = alerts_data.get("nodes", [])
                
                # Parse each vulnerability alert
                for alert in alerts:
                    vuln = alert.get("securityVulnerability", {})
                    package = vuln.get("package", {})
                    advisory = vuln.get("advisory", {})
                    cvss = advisory.get("cvss", {})
                    
                    vulnerability = VulnerabilityInfo(
                        id=alert.get("id", ""),
                        severity=vuln.get("severity", "UNKNOWN"),
                        package_name=package.get("name", ""),
                        ecosystem=package.get("ecosystem", ""),
                        summary=advisory.get("summary", ""),
                        created_at=alert.get("createdAt", ""),
                        state=alert.get("state", ""),
                        ghsa_id=advisory.get("ghsaId"),
                        cvss_score=cvss.get("score") if cvss else None
                    )
                    vulnerabilities.append(vulnerability)
                
                # Check for pagination
                page_info = alerts_data.get("pageInfo", {})
                if not page_info.get("hasNextPage"):
                    break
                
                cursor = page_info.get("endCursor")
                
            except Exception as e:
                print(f"Error scanning {owner}/{name}: {e}")
                break
        
        return vulnerabilities
    
    def categorize_vulnerabilities(self, vulnerabilities: List[VulnerabilityInfo]) -> Dict[str, List[VulnerabilityInfo]]:
        """
        TODO: Implement vulnerability categorization
        
        Categorize vulnerabilities by severity level.
        
        Args:
            vulnerabilities: List of VulnerabilityInfo objects
            
        Returns:
            Dict with severity levels as keys and lists of vulnerabilities as values
            
        Categories should include: CRITICAL, HIGH, MODERATE, LOW, UNKNOWN
        """
        categories = {
            "CRITICAL": [],
            "HIGH": [],
            "MODERATE": [],
            "LOW": [],
            "UNKNOWN": []
        }
        
        for vuln in vulnerabilities:
            severity = vuln.severity.upper()
            if severity in categories:
                categories[severity].append(vuln)
            else:
                categories["UNKNOWN"].append(vuln)
        
        return categories
    
    def generate_security_report(self, owner: str, name: str, vulnerabilities: List[VulnerabilityInfo]) -> Dict[str, Any]:
        """
        TODO: Implement security report generation
        
        Generate a comprehensive security report for the scanned repository.
        
        Args:
            owner: Repository owner
            name: Repository name  
            vulnerabilities: List of found vulnerabilities
            
        Returns:
            Dict containing the security report
            
        Report should include:
        - Repository information
        - Vulnerability summary by severity
        - Top vulnerable packages
        - Risk assessment
        - Recommendations
        """
        categorized = self.categorize_vulnerabilities(vulnerabilities)
        
        # Count vulnerabilities by severity
        severity_counts = {
            severity: len(vulns) for severity, vulns in categorized.items()
        }
        
        # Find most vulnerable packages
        package_counts = {}
        for vuln in vulnerabilities:
            if vuln.package_name:
                package_counts[vuln.package_name] = package_counts.get(vuln.package_name, 0) + 1
        
        top_packages = sorted(package_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Calculate risk score (simple algorithm)
        risk_score = (
            severity_counts.get("CRITICAL", 0) * 10 +
            severity_counts.get("HIGH", 0) * 7 +
            severity_counts.get("MODERATE", 0) * 4 +
            severity_counts.get("LOW", 0) * 1
        )
        
        # Determine risk level
        if risk_score > 50:
            risk_level = "CRITICAL"
        elif risk_score > 20:
            risk_level = "HIGH"
        elif risk_score > 10:
            risk_level = "MODERATE"
        else:
            risk_level = "LOW"
        
        # Generate recommendations
        recommendations = []
        if severity_counts.get("CRITICAL", 0) > 0:
            recommendations.append("🚨 URGENT: Address critical vulnerabilities immediately")
        if severity_counts.get("HIGH", 0) > 0:
            recommendations.append("⚠️ HIGH PRIORITY: Review and patch high-severity vulnerabilities")
        if len(vulnerabilities) > 20:
            recommendations.append("📋 Consider implementing automated dependency updates")
        if not vulnerabilities:
            recommendations.append("✅ No vulnerabilities detected - maintain current security practices")
        
        recommendations.extend([
            "🔄 Enable Dependabot alerts for automatic vulnerability notifications",
            "📊 Regularly audit and update dependencies",
            "🔒 Implement security scanning in CI/CD pipeline"
        ])
        
        return {
            "repository": {
                "owner": owner,
                "name": name,
                "full_name": f"{owner}/{name}"
            },
            "scan_summary": {
                "total_vulnerabilities": len(vulnerabilities),
                "severity_breakdown": severity_counts,
                "risk_score": risk_score,
                "risk_level": risk_level
            },
            "top_vulnerable_packages": [
                {"package": pkg, "vulnerability_count": count} 
                for pkg, count in top_packages
            ],
            "recommendations": recommendations,
            "scan_metadata": {
                "scan_date": datetime.now().isoformat(),
                "scanner_version": "1.0"
            }
        }
    
    def print_report(self, report: Dict[str, Any]) -> None:
        """
        Print a formatted security report to console
        
        Args:
            report: Security report dictionary
        """
        repo = report["repository"]
        summary = report["scan_summary"]
        
        print(f"\n{'='*60}")
        print(f"🔐 SECURITY REPORT: {repo['full_name']}")
        print(f"{'='*60}")
        
        print(f"\n📊 VULNERABILITY SUMMARY:")
        print(f"   Total Vulnerabilities: {summary['total_vulnerabilities']}")
        print(f"   Risk Level: {summary['risk_level']}")
        print(f"   Risk Score: {summary['risk_score']}")
        
        print(f"\n📈 SEVERITY BREAKDOWN:")
        for severity, count in summary["severity_breakdown"].items():
            if count > 0:
                emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MODERATE": "🟡", "LOW": "🟢"}.get(severity, "⚪")
                print(f"   {emoji} {severity}: {count}")
        
        if report["top_vulnerable_packages"]:
            print(f"\n📦 TOP VULNERABLE PACKAGES:")
            for pkg_info in report["top_vulnerable_packages"]:
                print(f"   • {pkg_info['package']}: {pkg_info['vulnerability_count']} vulnerabilities")
        
        print(f"\n💡 RECOMMENDATIONS:")
        for recommendation in report["recommendations"]:
            print(f"   {recommendation}")
        
        print(f"\n📅 Scan Date: {report['scan_metadata']['scan_date']}")
        print(f"{'='*60}\n")


def main():
    """
    Main function to run the security scanner exercise
    """
    print("🚀 GitHub GraphQL Security Scanner Exercise")
    print("=" * 50)
    
    # TODO: Set up environment variables
    # Create a .env file or set these environment variables:
    # GITHUB_TOKEN=your_personal_access_token_here
    # GITHUB_REPO_OWNER=repository_owner
    # GITHUB_REPO_NAME=repository_name
    
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ Error: GITHUB_TOKEN environment variable not set")
        print("Please set your GitHub personal access token:")
        print("export GITHUB_TOKEN=your_token_here")
        return
    
    # Get repository to scan from environment or use defaults
    repo_owner = os.getenv("GITHUB_REPO_OWNER", "facebook")
    repo_name = os.getenv("GITHUB_REPO_NAME", "react")
    
    print(f"🔍 Scanning repository: {repo_owner}/{repo_name}")
    
    try:
        # Initialize scanner
        scanner = GitHubGraphQLSecurityScanner(token)
        print("✅ GitHub GraphQL client initialized successfully")
        
        # Scan for vulnerabilities
        print("🔎 Scanning for vulnerabilities...")
        vulnerabilities = scanner.scan_repository_vulnerabilities(repo_owner, repo_name)
        
        # Generate and display report
        report = scanner.generate_security_report(repo_owner, repo_name, vulnerabilities)
        scanner.print_report(report)
        
        # Save report to file
        report_filename = f"security_report_{repo_owner}_{repo_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"📄 Detailed report saved to: {report_filename}")
        
        # Exercise completion message
        if vulnerabilities:
            print(f"\n🎯 Exercise Complete! Found {len(vulnerabilities)} vulnerabilities.")
            print("Next steps: Try scanning your own repositories and implement the TODO functions.")
        else:
            print(f"\n🎯 Exercise Complete! No vulnerabilities found in {repo_owner}/{repo_name}.")
            print("Try scanning a repository with known vulnerabilities to see more results.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check that your GitHub token has 'security_events' scope")
        print("2. Ensure the repository exists and you have access")
        print("3. Verify your internet connection")


if __name__ == "__main__":
    main()


"""
EXERCISE CHECKLIST:
- [ ] Set up GITHUB_TOKEN environment variable
- [ ] Implement _validate_token() method
- [ ] Implement scan_repository_vulnerabilities() method  
- [ ] Implement categorize_vulnerabilities() method
- [ ] Implement generate_security_report() method
- [ ] Run scanner against a test repository
- [ ] Review and understand the generated report
- [ ] Try scanning your own repositories

BONUS CHALLENGES:
- [ ] Add support for dependency graph queries
- [ ] Implement rate limiting and retry logic
- [ ] Add filtering by ecosystem (npm, pip, etc.)
- [ ] Create a simple CLI interface with argparse
- [ ] Add support for scanning multiple repositories

SECURITY NOTES:
- Never commit your GitHub token to version control
- Use environment variables or secure secret management
- Consider token scoping and principle of least privilege
- Implement proper error handling for production use
"""