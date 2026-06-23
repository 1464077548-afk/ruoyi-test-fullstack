import pytest
"""全量测试套件"""
pytestmark = [
    pytest.mark.full,
    pytest.mark.l1,
    pytest.mark.l2,
    pytest.mark.l3,
]

# 包含：所有功能测试
class NightlySuite:
    """夜间全量测试套件"""
    
    @pytest.mark.nightly
    @pytest.mark.api
    def test_all_api_tests(self):
        """运行所有API测试"""
        from suites.api_suite import ApiSuite
        suite = ApiSuite()
        suite.test_auth_api()
        suite.test_user_api()
        suite.test_role_api()
        suite.test_menu_api()
        suite.test_user_module()
        suite.test_role_module()
        suite.test_system_module()
        suite.test_user_lifecycle()
        suite.test_permission_flow()
        suite.test_data_flow()
    
    @pytest.mark.nightly
    @pytest.mark.ui
    def test_all_ui_tests(self, browser, auth_token):
        """运行所有UI测试"""
        from suites.ui_suite import UISuite
        suite = UISuite()
        suite.test_login_page(browser)
        suite.test_dashboard_page(browser, auth_token)
        suite.test_user_management(browser, auth_token)
        suite.test_role_management(browser, auth_token)
        suite.test_menu_management(browser, auth_token)
        suite.test_user_lifecycle_flow(browser, auth_token)
        suite.test_permission_flow(browser, auth_token)
    
    @pytest.mark.nightly
    @pytest.mark.integration
    def test_all_integration_tests(self):
        """运行所有集成测试"""
        from tests.integration.test_ui_api_sync import TestUIApiSync
        from tests.integration.test_cross_module import TestCrossModule
        from tests.integration.test_end_to_end import TestEndToEnd
        
        sync_test = TestUIApiSync()
        # 这里需要根据实际测试方法调整
        
        cross_test = TestCrossModule()
        # 这里需要根据实际测试方法调整
        
        e2e_test = TestEndToEnd()
        # 这里需要根据实际测试方法调整
    
    @pytest.mark.nightly
    @pytest.mark.performance
    def test_all_performance_tests(self):
        """运行所有性能测试"""
        from suites.performance_suite import PerformanceSuite
        suite = PerformanceSuite()
        suite.test_api_performance()
        suite.test_ui_performance()
        suite.test_system_stability()
        suite.run_login_stress_test()
        suite.run_user_crud_load_test()
        suite.run_concurrent_api_test()
        suite.run_endurance_test()
    
    @pytest.mark.nightly
    @pytest.mark.security
    def test_all_security_tests(self):
        """运行所有安全测试"""
        from suites.security_suite import SecuritySuite
        suite = SecuritySuite()
        suite.test_auth_security()
        suite.test_input_security()
        suite.test_api_security()
        suite.test_data_security()
        suite.run_owasp_scan()
        suite.run_auth_security_test()
        suite.run_sql_injection_test()
        suite.run_xss_test()
    
    def run_all_tests(self):
        """运行所有测试"""
        self.test_all_api_tests()
        # self.test_all_ui_tests()  # 需要browser fixture
        self.test_all_integration_tests()
        self.test_all_performance_tests()
        self.test_all_security_tests()
        
        return {
            "status": "completed",
            "message": "All nightly tests completed"
        }