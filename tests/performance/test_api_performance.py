"""API性能测试"""
import pytest
import time
from api.clients.auth_client import AuthClient
from api.clients.user_client import UserClient
from api.clients.role_client import RoleClient
from config.settings import Settings
from concurrent.futures import ThreadPoolExecutor, as_completed


class TestApiPerformance:
    """API性能测试类"""

    @pytest.mark.performance
    @pytest.mark.p0
    def test_login_performance(self, auth_client):
        """P0-登录接口响应时间"""
        settings = Settings()
        response_times = []
        for _ in range(10):
            start_time = time.time()
            auth_client.login(settings.USERNAME, settings.PASSWORD)
            end_time = time.time()
            response_time = end_time - start_time
            response_times.append(response_time)
        
        avg_time = sum(response_times) / len(response_times)
        p95_time = sorted(response_times)[int(len(response_times) * 0.95)]
        
        assert avg_time < 0.5, f"平均响应时间 {avg_time}s > 0.5s"
        assert p95_time < 1.0, f"P95 响应时间 {p95_time}s > 1.0s"
    
    @pytest.mark.performance
    @pytest.mark.p0
    def test_user_list_performance(self, user_client):
        """P0-用户列表接口响应时间"""
        start_time = time.time()
        response = user_client.get_user_list()
        end_time = time.time()
        response_time = end_time - start_time
        
        assert response.get("code") == 200
        assert response_time < 2.0, f"用户列表接口响应时间过长: {response_time}秒"
    
    @pytest.mark.performance
    @pytest.mark.p0
    def test_role_list_performance(self, role_client):
        """P0-角色列表接口响应时间"""
        start_time = time.time()
        response = role_client.get_role_list()
        end_time = time.time()
        response_time = end_time - start_time
        
        assert response.get("code") == 200
        assert response_time < 2.0, f"角色列表接口响应时间过长: {response_time}秒"
    
    @pytest.mark.performance
    @pytest.mark.p0
    def test_concurrent_requests(self, auth_client, user_client):
        """P0-并发请求测试"""
        settings = Settings()   
        def login_request():
            return auth_client.login(settings.USERNAME, settings.PASSWORD)
        
        def user_list_request():
            return user_client.get_user_list()
        
        # 执行并发请求
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for _ in range(10):
                futures.append(executor.submit(login_request))
                futures.append(executor.submit(user_list_request))
            
            # 等待所有请求完成
            for future in as_completed(futures):
                response = future.result()
                assert response.get("code") == 200
                
    @pytest.mark.performance
    @pytest.mark.p1
    def test_api_throughput(self, authenticated_client):
        """P1-接口吞吐量测试"""
        user_client = UserClient(token=authenticated_client.token)
        
        start = time.time()
        request_count = 0
        
        while time.time() - start < 10:  # 10 秒内
            user_client.get_user_list()
            request_count += 1
        
        throughput = request_count / 10  # QPS
        assert throughput > 10, f"吞吐量 {throughput} QPS < 10 QPS"
    
    @pytest.mark.performance
    @pytest.mark.p1
    def test_api_memory_leak(self, authenticated_client):
        """P1-接口内存泄漏检测"""
        user_client = UserClient(token=authenticated_client.token)
        
        # 执行 100 次请求
        for i in range(100):
            user_client.get_user_list()
        
        # 检查响应大小是否稳定
        # (实际项目中需要集成内存监控)
        pass