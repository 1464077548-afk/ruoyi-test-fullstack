"""L1: 认证接口单接口测试"""
import pytest
from config.settings import Settings
from api.clients.auth_client import AuthClient


class TestAuthApi:
    """认证API测试类"""
    settings = Settings()

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_login_success(self, auth_client):
        """P0-登录成功"""
        response = auth_client.login(self.settings.USERNAME, self.settings.PASSWORD)
        print(f"登录接口响应: {response}")
        assert response.get("code") == 200
        assert "token" in response.get("data", {})
        assert response.get("token") is not None

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    @pytest.mark.parametrize("username,password,expected_error", [
        ("test_user_not_exists", "wrong_password","用户不存在/密码错误"),
        ("nonexistent_user", "admin123","用户不存在/密码错误"),
        ("","admin23","用户名不能为空"),
        ("test_user_not_exists","","密码不能为空"),
        ])
    def test_login_failure(self, auth_client, username, password, expected_error):
        """P1-登录失败"""
        response = auth_client.login(username, password)
        print(f"登录失败响应：{response}")
        assert response.get("code") == 500



    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_user_info(self, authenticated_client):
        """P0-获取用户信息"""
        auth_client = AuthClient()
        auth_client.session.headers.update(authenticated_client.session.headers)
        response = auth_client.get_user_info()
        print(f"获取用户信息响应: {response}")
        assert response.code == 200
        assert hasattr(response, "roles") and response.roles is not None
        assert hasattr(response, "permissions") and response.permissions is not None
        assert hasattr(response, "user") and response.user is not None
        assert response.user.userName == "admin"
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_logout(self, auth_client):
        """P0-登出成功"""
        response = auth_client.login(self.settings.USERNAME, self.settings.PASSWORD)
        print(f"登录接口响应: {response}")
        assert response.get("code") == 200

        response = auth_client.logout()
        assert response.get("code") == 200

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_get_user_info_without_auth(self,auth_client):
        """P1-未认证获取用户信息"""
        result = auth_client.get_user_info()
        
        assert result.code == 401
        assert "认证失败" in result.msg 