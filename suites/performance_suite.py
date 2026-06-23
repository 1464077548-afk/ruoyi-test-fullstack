import pytest
"""性能测试套件"""
pytestmark = [
    pytest.mark.performance,
]

# 包含：所有性能测试
class PerformanceSuite:
    """性能测试套件"""
    
    @pytest.mark.performance
    def test_api_performance(self):
        """测试API性能"""
        from tests.performance.test_api_performance import TestApiPerformance
        test = TestApiPerformance()
        # 这里需要根据实际测试方法调整
        pass
    
    @pytest.mark.performance
    def test_ui_performance(self):
        """测试UI性能"""
        from tests.performance.test_ui_performance import TestUIPerformance
        test = TestUIPerformance()
        # 这里需要根据实际测试方法调整
        pass
    
    @pytest.mark.performance
    def test_system_stability(self):
        """测试系统稳定性"""
        from tests.performance.test_system_stability import TestSystemStability
        test = TestSystemStability()
        # 这里需要根据实际测试方法调整
        pass
    
    def run_login_stress_test(self):
        """运行登录压力测试"""
        from performance.scenarios.login_stress import LoginStressTest
        from config.settings import get_settings
        
        settings = get_settings()
        test = LoginStressTest(settings.base_url)
        test.run()
    
    def run_user_crud_load_test(self):
        """运行用户CRUD负载测试"""
        from performance.scenarios.user_crud_load import UserCrudLoadTest
        from config.settings import get_settings
        
        settings = get_settings()
        test = UserCrudLoadTest(settings.base_url)
        test.run()
    
    def run_concurrent_api_test(self):
        """运行并发API测试"""
        from performance.scenarios.concurrent_api import ConcurrentApiTest
        from config.settings import get_settings
        
        settings = get_settings()
        test = ConcurrentApiTest(settings.base_url)
        test.run()
    
    def run_endurance_test(self):
        """运行稳定性测试"""
        from performance.scenarios.endurance_test import EnduranceTest
        from config.settings import get_settings
        
        settings = get_settings()
        test = EnduranceTest(settings.base_url)
        test.run()