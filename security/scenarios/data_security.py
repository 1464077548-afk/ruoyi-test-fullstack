"""数据安全测试场景"""
from security.scanners.api_security import ApiSecurityScanner
from config.settings import Settings
from common.logger import Logger


class DataSecurityScenario:
    """数据安全测试场景"""
    
    def __init__(self):
        """初始化"""
        self.settings = Settings()
        self.scanner = ApiSecurityScanner(self.settings.BASE_URL)
        self.logger = Logger(__name__)
    
    def test_sensitive_data_exposure(self):
        """测试敏感数据暴露"""
        self.logger.info("开始测试敏感数据暴露")
        
        # 可能包含敏感数据的接口
        sensitive_endpoints = [
            "/system/user/list",
            "/system/user/1",
            "/getInfo",
            "/monitor/server"
        ]
        
        results = self.scanner.test_sensitive_data_exposure(sensitive_endpoints)
        
        if results:
            self.logger.warning(f"发现敏感数据暴露漏洞: {results}")
        else:
            self.logger.info("未发现敏感数据暴露漏洞")
        
        return results
    
    def test_insecure_direct_object_references(self):
        """测试不安全的直接对象引用"""
        self.logger.info("开始测试不安全的直接对象引用")
        
        # 用户ID范围
        id_range = range(1, 10)
        
        results = self.scanner.test_insecure_direct_object_references("/system/user/{id}", id_range)
        
        if results:
            self.logger.warning(f"发现不安全的直接对象引用漏洞: {results}")
        else:
            self.logger.info("未发现不安全的直接对象引用漏洞")
        
        return results
    
    def test_unauthorized_access(self):
        """测试未授权访问"""
        self.logger.info("开始测试未授权访问")
        
        # 需要授权的接口
        protected_endpoints = [
            "/system/user/list",
            "/system/role/list",
            "/system/menu/list",
            "/getInfo"
        ]
        
        results = self.scanner.test_unauthorized_access(protected_endpoints)
        
        if results:
            self.logger.warning(f"发现未授权访问漏洞: {results}")
        else:
            self.logger.info("未发现未授权访问漏洞")
        
        return results
    
    def run_all_tests(self):
        """运行所有测试"""
        self.logger.info("开始运行数据安全测试场景")
        
        results = {
            "sensitive_data_exposure": self.test_sensitive_data_exposure(),
            "insecure_direct_object_references": self.test_insecure_direct_object_references(),
            "unauthorized_access": self.test_unauthorized_access()
        }
        
        self.logger.info("数据安全测试场景运行完成")
        return results
