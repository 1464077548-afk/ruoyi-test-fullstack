"""OWASP扫描器"""
import requests
from typing import Dict, List, Any
from common.logger import Logger


class OwaspScanner:
    """OWASP Top 10 安全扫描"""
    VULNERABILITIES = {
        'A01': 'Broken Access Control',
        'A02': 'Cryptographic Failures',
        'A03': 'Injection',
        'A04': 'Insecure Design',
        'A05': 'Security Misconfiguration',
        'A06': 'Vulnerable Components',
        'A07': 'Authentication Failures',
        'A08': 'Software Integrity Failures',
        'A09': 'Logging Failures',
        'A10': 'SSRF',
    }
    
    def __init__(self, base_url: str):
        """初始化"""
        self.base_url = base_url
        self.logger = Logger(__name__)
        self.session = requests.Session()
        self.findings = []
    
    def scan_sql_injection(self, endpoints: List[str]) -> List[Dict[str, Any]]:
        """扫描SQL注入漏洞"""
        vulnerabilities = []
        payloads = [
            "' OR 1=1 --",
            "' OR '1'='1",
            """' UNION SELECT username, password FROM users --""",
            "' AND 1=0 UNION SELECT 1,2,3 --",
            "'; DROP TABLE users; --",
            "1; SELECT * FROM users",
        ]
        
        for endpoint in endpoints:
            for payload in payloads:
                url = f"{self.base_url}{endpoint}?id={payload}"
                try:
                    response = self.session.get(url, timeout=10)
                    if 'sql' in response.text.lower() or "error" in response.text.lower() or "syntax" in response.text.lower():
                        vulnerabilities.append({
                            "type": self.VULNERABILITIES['A03'],
                            "endpoint": endpoint,
                            "severity": "CRITICAL",
                            "payload": payload,
                            "status_code": response.status_code,
                            "description": "可能存在SQL注入漏洞"
                        })
                        self.findings.append({
                            "type": self.VULNERABILITIES['A03'],
                            "endpoint": endpoint,
                            "severity": "CRITICAL",
                            "payload": payload,
                            "description": "可能存在SQL注入漏洞"
                        })
                except Exception as e:
                    self.logger.error(f"SQL注入扫描失败: {e}")
        
        return vulnerabilities
    
    def scan_xss(self, endpoints: List[str]) -> List[Dict[str, Any]]:
        """扫描XSS漏洞"""
        vulnerabilities = []
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src='x' onerror='alert(1)'>",
            "<iframe src='javascript:alert(1)'></iframe>",
            "'onmouseover=\"alert(1)\"'"
        ]
        
        for endpoint in endpoints:
            for payload in payloads:
                url = f"{self.base_url}{endpoint}?q={payload}"
                try:
                    response = self.session.get(url, timeout=10)
                    if payload in response.text:
                        vulnerabilities.append({
                            "type": self.VULNERABILITIES['A03'],
                            "severity": "CRITICAL",
                            "endpoint": endpoint,
                            "payload": payload,
                            "status_code": response.status_code,
                            "description": "可能存在XSS漏洞"
                        })
                        self.findings.append({
                            "type": self.VULNERABILITIES['A03'],
                            "endpoint": endpoint,
                            "severity": "CRITICAL",
                            "payload": payload,
                            "description": "可能存在XSS漏洞"
                        })
                except Exception as e:
                    self.logger.error(f"XSS扫描失败: {e}")
        
        return vulnerabilities
    
    def scan_csrf(self, endpoints: List[str]) -> List[Dict[str, Any]]:
        """扫描CSRF漏洞"""
        vulnerabilities = []
        
        for endpoint in endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                if "csrf" not in response.text.lower() and "token" not in response.text.lower():
                    vulnerabilities.append({
                        "type": self.VULNERABILITIES['A03'],
                        "severity": "CRITICAL",
                        "endpoint": endpoint,
                        "status_code": response.status_code,
                        "description": "缺少CSRF令牌"
                    })
            except Exception as e:
                self.logger.error(f"CSRF扫描失败: {e}")
        
        return vulnerabilities
    
    def scan_security_headers(self) -> List[Dict[str, Any]]:
        """扫描安全头"""
        vulnerabilities = []
        required_headers = [
            "Content-Security-Policy",
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Strict-Transport-Security"
        ]
        
        try:
            response = self.session.get(self.base_url, timeout=10)
            headers = response.headers
            
            for header in required_headers:
                if header not in headers:
                    vulnerabilities.append({
                        "type": self.VULNERABILITIES['A05'],
                        "severity": "MEDIUM",
                        "header": header,
                        "status_code": response.status_code,
                        "description": f"缺少安全头: {header}"
                    })
                    self.findings.append({
                        "type": self.VULNERABILITIES['A05'],
                        "endpoint": self.base_url,
                        "severity": "MEDIUM",
                        "header": header,
                        "status_code": response.status_code,
                        "description": f"缺少安全头: {header}"
                    })
        except Exception as e:
            self.logger.error(f"安全头扫描失败: {e}")
        
        return vulnerabilities
    
    def full_scan(self, endpoints: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """完整扫描"""
        results = {
            "sql_injection": self.scan_sql_injection(endpoints),
            "xss": self.scan_xss(endpoints),
            "csrf": self.scan_csrf(endpoints),
            "security_headers": self.scan_security_headers()
        }
        
        return results
