"""系统稳定性测试"""
import pytest
import time
from api.clients.auth_client import AuthClient
from api.clients.user_client import UserClient
from api.clients.role_client import RoleClient
from config.settings import Settings


class TestSystemStability:
    """系统稳定性测试类"""
    
    def test_long_running_stability(self, auth_client, user_client, role_client):
        """测试系统长时间运行稳定性"""
        settings = Settings()
        test_duration = 60  # 测试持续时间（秒）
        start_time = time.time()
        request_count = 0
        
        while time.time() - start_time < test_duration:
            # 执行登录请求
            login_response = auth_client.login(settings.USERNAME, settings.PASSWORD)
            assert login_response.get("code") == 200
            
            # 执行用户列表请求
            user_list_response = user_client.get_user_list()
            assert user_list_response.get("code") == 200
            
            # 执行角色列表请求
            role_list_response = role_client.get_role_list()
            assert role_list_response.get("code") == 200
            
            request_count += 3
            # 短暂休息，避免请求过于频繁
            time.sleep(0.5)
        
        print(f"在{test_duration}秒内执行了{request_count}个请求，系统运行稳定")
    
    def test_repeated_login_logout(self, auth_client):
        """测试重复登录登出操作的稳定性"""
        settings = Settings()
        repeat_count = 50  # 重复次数
        
        for i in range(repeat_count):
            # 登录
            login_response = auth_client.login(settings.USERNAME, settings.PASSWORD)
            assert login_response.get("code") == 200
            
            # 登出
            logout_response = auth_client.logout()
            assert logout_response.get("code") == 200
            
            # 短暂休息
            time.sleep(0.2)
        
        print(f"成功执行了{repeat_count}次登录登出操作，系统运行稳定")
    
    def test_concurrent_stability(self, auth_client, user_client):
        """测试并发操作的稳定性"""
        import concurrent.futures
        settings = Settings()
        concurrent_count = 20  # 并发数
        
        def perform_operations():
            # 登录
            login_response = auth_client.login(settings.USERNAME, settings.PASSWORD)
            assert login_response.get("code") == 200
            
            # 获取用户列表
            user_list_response = user_client.get_user_list()
            assert user_list_response.get("code") == 200
            
            # 登出
            logout_response = auth_client.logout()
            assert logout_response.get("code") == 200
        
        # 执行并发操作
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for _ in range(concurrent_count):
                futures.append(executor.submit(perform_operations))
            
            # 等待所有操作完成
            for future in concurrent.futures.as_completed(futures):
                future.result()
        
        print(f"成功执行了{concurrent_count}个并发操作，系统运行稳定")
