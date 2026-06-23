import pytest
"""安全测试套件"""
pytestmark = [
    pytest.mark.security,
]
class SecuritySuite:
    """安全测试套件"""
    
    @pytest.mark.security
    def test_auth_security(self):
        """测试认证安全"""
        from tests.security.test_auth_security import TestAuthSecurity
        test = TestAuthSecurity()
        # 这里需要根据实际测试方法调整
        pass
    
    @pytest.mark.security
    def test_input_security(self):
        """测试输入安全"""
        from tests.security.test_input_security import TestInputSecurity
        test = TestInputSecurity()
        # 这里需要根据实际测试方法调整
        pass
    
    @pytest.mark.security
    def test_api_security(self):
        """测试API安全"""
        from tests.security.test_api_security import TestApiSecurity
        test = TestApiSecurity()
        # 这里需要根据实际测试方法调整
        pass
    
    @pytest.mark.security
    def test_data_security(self):
        """测试数据安全"""
        from tests.security.test_data_security import TestDataSecurity
        test = TestDataSecurity()
        # 这里需要根据实际测试方法调整
        pass
    
    def run_owasp_scan(self):
        """运行OWASP扫描"""
        from security.scanners.owasp_scanner import OwaspScanner
        from config.settings import get_settings
        
        settings = get_settings()
        scanner = OwaspScanner(settings.base_url)
        scanner.scan_all()
    
    def run_auth_security_test(self):
        """运行认证安全测试"""
        from security.scanners.auth_scanner import AuthScanner
        from config.settings import get_settings
        
        settings = get_settings()
        scanner = AuthScanner(settings.base_url)
        scanner.scan_all()
    
    def run_sql_injection_test(self):
        """运行SQL注入测试"""
        from security.scanners.sql_injection import SqlInjectionScanner
        from config.settings import get_settings
        
        settings = get_settings()
        scanner = SqlInjectionScanner(settings.base_url)
        scanner.scan_all()
    
    def run_xss_test(self):
        """运行XSS测试"""
        from security.scanners.xss_scanner import XssScanner
        from config.settings import get_settings
        
        settings = get_settings()
        scanner = XssScanner(settings.base_url)
        scanner.scan_all()