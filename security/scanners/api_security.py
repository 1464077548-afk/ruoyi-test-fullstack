"""API安全检测"""
import requests
from typing import Dict, List, Any
from common.logger import Logger


class ApiSecurityScanner:
    """API安全检测扫描器"""
    
    def __init__(self, base_url: str):
        """初始化"""
        self.base_url = base_url
        self.logger = Logger(__name__)
        self.session = requests.Session()
    
    def test_unauthorized_access(self, endpoints: List[str]) -> List[Dict[str, Any]]:
        """测试未授权访问"""
        vulnerabilities = []
        
        for endpoint in endpoints:
            try:
                # 移除所有认证信息
                self.session.headers.pop("Authorization", None)
                
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                
                # 检查是否返回了敏感数据
                if response.status_code == 200:
                    # 检查响应中是否包含敏感信息
                    sensitive_patterns = ["password", "token", "secret", "private"]
                    for pattern in sensitive_patterns:
                        if pattern in response.text.lower():
                            vulnerabilities.append({
                                "type": "Unauthorized Access",
                                "endpoint": endpoint,
                                "status_code": response.status_code,
                                "message": "未授权访问敏感数据"
                            })
                            break
                        
            except Exception as e:
                self.logger.error(f"未授权访问测试失败: {e}")
        
        return vulnerabilities
    
    def test_rate_limiting(self, endpoint: str, requests_count: int = 10) -> List[Dict[str, Any]]:
        """测试速率限制"""
        vulnerabilities = []
        
        try:
            # 登录获取token
            login_response = self.session.post(f"{self.base_url}/login", json={
                "username": "admin",
                "password": "admin123"
            }, timeout=10)
            
            if login_response.status_code == 200:
                token = login_response.json().get("data", {}).get("token")
                if token:
                    self.session.headers.update({"Authorization": f"Bearer {token}"})
                    
                    # 连续发送多个请求
                    status_codes = []
                    for _ in range(requests_count):
                        response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                        status_codes.append(response.status_code)
                    
                    # 检查是否有429状态码（Too Many Requests）
                    if 429 not in status_codes:
                        vulnerabilities.append({
                            "type": "Rate Limiting",
                            "endpoint": endpoint,
                            "status_codes": status_codes,
                            "message": "缺少速率限制"
                        })
        except Exception as e:
            self.logger.error(f"速率限制测试失败: {e}")
        
        return vulnerabilities
    
    def test_sensitive_data_exposure(self, endpoints: List[str]) -> List[Dict[str, Any]]:
        """测试敏感数据暴露"""
        vulnerabilities = []
        
        try:
            # 登录获取token
            login_response = self.session.post(f"{self.base_url}/login", json={
                "username": "admin",
                "password": "admin123"
            }, timeout=10)
            
            if login_response.status_code == 200:
                token = login_response.json().get("data", {}).get("token")
                if token:
                    self.session.headers.update({"Authorization": f"Bearer {token}"})
                    
                    for endpoint in endpoints:
                        response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                        
                        if response.status_code == 200:
                            # 检查响应中是否包含敏感信息
                            sensitive_patterns = [
                                "password", "token", "secret", "private", "credit_card",
                                "ssn", "social_security", "bank_account", "password_hash"
                            ]
                            for pattern in sensitive_patterns:
                                if pattern in response.text.lower():
                                    vulnerabilities.append({
                                        "type": "Sensitive Data Exposure",
                                        "endpoint": endpoint,
                                        "status_code": response.status_code,
                                        "message": f"暴露敏感信息: {pattern}"
                                    })
                                    break
        except Exception as e:
            self.logger.error(f"敏感数据暴露测试失败: {e}")
        
        return vulnerabilities
    
    def test_insecure_direct_object_references(self, endpoint_pattern: str, id_range: range) -> List[Dict[str, Any]]:
        """测试不安全的直接对象引用"""
        vulnerabilities = []
        
        try:
            # 登录获取token
            login_response = self.session.post(f"{self.base_url}/login", json={
                "username": "admin",
                "password": "admin123"
            }, timeout=10)
            
            if login_response.status_code == 200:
                token = login_response.json().get("data", {}).get("token")
                if token:
                    self.session.headers.update({"Authorization": f"Bearer {token}"})
                    
                    for id in id_range:
                        endpoint = endpoint_pattern.format(id=id)
                        response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                        
                        # 检查是否能够访问其他用户的数据
                        if response.status_code == 200:
                            vulnerabilities.append({
                                "type": "Insecure Direct Object References",
                                "endpoint": endpoint,
                                "status_code": response.status_code,
                                "message": "可能存在不安全的直接对象引用"
                            })
        except Exception as e:
            self.logger.error(f"不安全的直接对象引用测试失败: {e}")
        
        return vulnerabilities
    
    def full_scan(self, protected_endpoints: List[str], rate_limit_endpoint: str, sensitive_endpoints: List[str], endpoint_pattern: str, id_range: range) -> Dict[str, List[Dict[str, Any]]]:
        """完整扫描"""
        results = {
            "unauthorized_access": self.test_unauthorized_access(protected_endpoints),
            "rate_limiting": self.test_rate_limiting(rate_limit_endpoint),
            "sensitive_data_exposure": self.test_sensitive_data_exposure(sensitive_endpoints),
            "insecure_direct_object_references": self.test_insecure_direct_object_references(endpoint_pattern, id_range)
        }
        
        return results
