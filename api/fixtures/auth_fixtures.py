import pytest
from api.clients.auth_client import AuthClient
from api.clients.base_client import BaseClient
from config.settings import Settings


@pytest.fixture(scope="session")
def auth_client():
    """认证客户端fixture"""
    return AuthClient()


@pytest.fixture(scope="session")
def get_login_token(auth_client):
    """登录获取token"""
    response = auth_client.login(auth_client.settings.TEST_USERNAME, auth_client.settings.TEST_PASSWORD)
    print(f"登录响应: {response}")
    token = response.get("data", {}).get("token")
    print(f"获取到的token: {token}")
    return token


@pytest.fixture(scope="session")
def authenticated_client(auth_client, get_login_token):
    """已认证的认证客户端"""
    auth_client.set_token(get_login_token)
    return auth_client


@pytest.fixture(scope="session")
def user_info(authenticated_client):
    """用户信息"""
    response = authenticated_client.get_user_info()
    return response

   
