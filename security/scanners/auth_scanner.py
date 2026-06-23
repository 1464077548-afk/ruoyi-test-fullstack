"""认证安全检测"""
import requests
from typing import Dict, List, Any
from common.logger import Logger


class AuthScanner:
    """认证安全检测扫描器"""
    
    def __init__(self, base_url: str):
        """初始化"""
        self.base_url = base_url
        self.logger = Logger(__name__)
        self.session = requests.Session()
    
    def test_brute_force(self, username: str, passwords: List[str]) -> List[Dict[str, Any]]:
        """测试暴力破解"""
        vulnerabilities = []
        
        for password in passwords:
            try:
                response = self.session.post(f"{self.base_url}/login", json={
                    "username": username,
                    "password": password
                }, timeout=10)
                
                if response.status_code == 200:
                    vulnerabilities.append({
                        "type": "Brute Force",
                        "endpoint": "/login",
                        "username": username,
                        "password": password,
                        "status_code": response.status_code,
                        "message": "弱密码或无暴力破解防护"
                    })
                    break
                    
            except Exception as e:
                self.logger.error(f"暴力破解测试失败: {e}")
        
        return vulnerabilities
    
    def test_session_management(self) -> List[Dict[str, Any]]:
        """测试会话管理"""
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
                    # 测试token有效期
                    self.session.headers.update({"Authorization": f"Bearer {token}"})
                    
                    # 测试获取用户信息
                    user_info_response = self.session.get(f"{self.base_url}/getInfo", timeout=10)
                    if user_info_response.status_code == 200:
                        # 测试登出
                        logout_response = self.session.post(f"{self.base_url}/logout", timeout=10)
                        if logout_response.status_code == 200:
                            # 测试登出后token是否失效
                            try:
                                after_logout_response = self.session.get(f"{self.base_url}/getInfo", timeout=10)
                                if after_logout_response.status_code == 200:
                                    vulnerabilities.append({
                                        "type": "Session Management",
                                        "endpoint": "/logout",
                                        "status_code": after_logout_response.status_code,
                                        "message": "登出后token未失效"
                                    })
                            except Exception:
                                pass
        except Exception as e:
            self.logger.error(f"会话管理测试失败: {e}")
        
        return vulnerabilities
    
    def test_csrf_protection(self) -> List[Dict[str, Any]]:
        """测试CSRF防护"""
        vulnerabilities = []
        
        try:
            # 登录
            login_response = self.session.post(f"{self.base_url}/login", json={
                "username": "admin",
                "password": "admin123"
            }, timeout=10)
            
            if login_response.status_code == 200:
                token = login_response.json().get("data", {}).get("token")
                if token:
                    self.session.headers.update({"Authorization": f"Bearer {token}"})
                    
                    # 测试是否需要CSRF token
                    # 这里简化处理，实际应该检查表单是否包含CSRF token
                    user_response = self.session.get(f"{self.base_url}/system/user/list", timeout=10)
                    if user_response.status_code == 200:
                        if "csrf" not in user_response.text.lower() and "token" not in user_response.text.lower():
                            vulnerabilities.append({
                                "type": "CSRF Protection",
                                "endpoint": "/system/user/list",
                                "status_code": user_response.status_code,
                                "message": "缺少CSRF防护"
                            })
        except Exception as e:
            self.logger.error(f"CSRF防护测试失败: {e}")
        
        return vulnerabilities
    
    def test_password_policy(self, weak_passwords: List[str]) -> List[Dict[str, Any]]:
        """测试密码策略"""
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
                    
                    # 测试创建用户时的密码策略
                    for weak_password in weak_passwords:
                        create_response = self.session.post(f"{self.base_url}/system/user", json={
                            "username": f"test_{weak_password}",
                            "password": weak_password,
                            "nickname": "Test User",
                            "email": f"test_{weak_password}@example.com",
                            "status": "1"
                        }, timeout=10)
                        
                        if create_response.status_code == 200:
                            vulnerabilities.append({
                                "type": "Password Policy",
                                "endpoint": "/system/user",
                                "password": weak_password,
                                "status_code": create_response.status_code,
                                "message": "弱密码策略"
                            })
                            
                            # 清理
                            user_id = create_response.json().get("data", {}).get("userId")
                            if user_id:
                                self.session.delete(f"{self.base_url}/system/user/{user_id}")
        except Exception as e:
            self.logger.error(f"密码策略测试失败: {e}")
        
        return vulnerabilities
    
    def full_scan(self, username: str, passwords: List[str], weak_passwords: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """完整扫描"""
        results = {
            "brute_force": self.test_brute_force(username, passwords),
            "session_management": self.test_session_management(),
            "csrf_protection": self.test_csrf_protection(),
            "password_policy": self.test_password_policy(weak_passwords)
        }
        
        return results
