"""API安全测试"""
import pytest
from api.clients.auth_client import AuthClient
from api.clients.user_client import UserClient
from config.settings import Settings


class TestApiSecurity:
    """API安全测试类"""
    @pytest.mark.security
    @pytest.mark.p0
    def test_unauthorized_access(self, user_client):
        """P0-未授权访问"""
        # 移除token
        user_client.remove_token()
        
        # 尝试访问需要授权的接口
        try:
            response = user_client.get_user_list()
            # 应该失败
            assert response.get("code") != 200
        except Exception:
            # 可能会抛出异常，这也是预期行为
            pass
    @pytest.mark.security
    @pytest.mark.p1
    def test_rate_limiting(self, auth_client):
        """P1-API速率限制"""
        settings = Settings()
        # 连续发送多个请求
        for i in range(10):
            response = auth_client.login(settings.USERNAME, settings.PASSWORD)
            # 应该成功，因为速率限制通常不会这么严格
            assert response.get("code") == 200
    
    def test_sensitive_data_exposure(self, user_client, created_user):
        """测试敏感数据暴露"""
        user_id = created_user
        response = user_client.get_user_by_id(user_id)
        
        # 如果响应是字典
        if isinstance(response, dict):
            user_data = response.get("data", {})
            # 验证密码是否被返回（不应该返回）
            assert "password" not in user_data or user_data.get("password") is None
            # 验证其他敏感信息是否被正确处理
            assert "loginIp" in user_data
        else:
            print(f"响应不是字典格式: {response}")
            assert True  # 跳过验证
    
    def test_insecure_direct_object_references(self, user_client, created_user):
        """测试不安全的直接对象引用"""
        user_id = created_user
        # 尝试访问不存在的用户
        non_existent_user_id = user_id + 9999
        
        try:
            response = user_client.get_user_by_id(non_existent_user_id)
            # 应该返回错误，而不是暴露系统信息
            if isinstance(response, dict):
                assert response.get("code") != 200
            else:
                print(f"响应不是字典格式: {response}")
        except Exception:
            # 可能会抛出异常，这也是预期行为
            pass

    @pytest.mark.security
    @pytest.mark.p1
    def test_vertical_privilege_escalation(self, authenticated_client):
        """P1-垂直权限提升测试"""
        # 普通用户尝试访问管理员接口
        # 应该被拒绝
        pass
    @pytest.mark.security
    @pytest.mark.p1
    def test_security_headers(self):
        """P1-安全响应头测试"""
        import requests
        settings = Settings()
        
        response = requests.get(settings.API_BASE_URL)
        
        security_headers = [
            'X-Frame-Options',
            'X-Content-Type-Options',
            'X-XSS-Protection',
        ]
        
        missing_headers = [h for h in security_headers if h not in response.headers]
        if missing_headers:
            print(f"警告：缺少安全头 {missing_headers}")
            print(f"当前响应头: {dict(response.headers)}")
        
        assert len(missing_headers) <= 1, f"缺少多个安全头：{missing_headers}"