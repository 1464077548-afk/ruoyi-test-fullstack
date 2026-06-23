"""认证安全测试场景"""
from security.scanners.auth_scanner import AuthScanner
from config.settings import Settings
from common.logger import Logger


class AuthSecurityScenario:
    """认证安全测试场景"""
    
    def __init__(self):
        """初始化"""
        self.settings = Settings()
        self.scanner = AuthScanner(self.settings.BASE_URL)
        self.logger = Logger(__name__)
    
    def test_brute_force_attack(self):
        """测试暴力破解攻击"""
        self.logger.info("开始测试暴力破解攻击")
        
        # 弱密码列表
        weak_passwords = [
            "admin", "123456", "password", "12345678", "qwerty",
            "123456789", "1234", "12345", "111111", "1234567"
        ]
        
        results = self.scanner.test_brute_force(self.settings.TEST_USERNAME, weak_passwords)
        
        if results:
            self.logger.warning(f"发现暴力破解漏洞: {results}")
        else:
            self.logger.info("未发现暴力破解漏洞")
        
        return results
    
    def test_session_management(self):
        """测试会话管理"""
        self.logger.info("开始测试会话管理")
        
        results = self.scanner.test_session_management()
        
        if results:
            self.logger.warning(f"发现会话管理漏洞: {results}")
        else:
            self.logger.info("会话管理正常")
        
        return results
    
    def test_csrf_protection(self):
        """测试CSRF防护"""
        self.logger.info("开始测试CSRF防护")
        
        results = self.scanner.test_csrf_protection()
        
        if results:
            self.logger.warning(f"发现CSRF防护漏洞: {results}")
        else:
            self.logger.info("CSRF防护正常")
        
        return results
    
    def test_password_policy(self):
        """测试密码策略"""
        self.logger.info("开始测试密码策略")
        
        # 弱密码列表
        weak_passwords = ["123456", "password", "admin123", "123456789"]
        
        results = self.scanner.test_password_policy(weak_passwords)
        
        if results:
            self.logger.warning(f"发现密码策略漏洞: {results}")
        else:
            self.logger.info("密码策略正常")
        
        return results
    
    def run_all_tests(self):
        """运行所有测试"""
        self.logger.info("开始运行认证安全测试场景")
        
        results = {
            "brute_force": self.test_brute_force_attack(),
            "session_management": self.test_session_management(),
            "csrf_protection": self.test_csrf_protection(),
            "password_policy": self.test_password_policy()
        }
        
        self.logger.info("认证安全测试场景运行完成")
        return results
