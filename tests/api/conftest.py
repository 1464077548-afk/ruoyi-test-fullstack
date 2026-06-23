"""
API 测试专用 fixtures
"""
import pytest
import time
from typing import Dict, Any, Optional
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from api.clients.base_client import BaseClient  
from api.clients.auth_client import AuthClient
from common.utils.data_factory import DataFactory
from common.logger import get_logger   
logger = get_logger(__name__)
# =============================================================================
# API 客户端 Fixtures
# =============================================================================
@pytest.fixture(scope="session")
def global_token(settings) -> str:
    """
    ⚠️ 仅用于只读测试的 Session 级别 Token
    
    注意：使用此 fixture 的测试用例中绝对不能调用 logout()
    适合用于大量的只读查询测试，提高执行速度
    """
    auth = AuthClient()
    login_result = auth.login(
        username=settings.USERNAME,
        password=settings.PASSWORD
    )
    
    if login_result.get('code') != 200:
        pytest.fail("全局登录失败")
    
    token = login_result.get('data', {}).get('token') or login_result.get('token')
    
    logger.info(f"全局 Token 已创建: {token[:20]}...")
    yield token


@pytest.fixture(scope="function")
def api_client_with_token(global_token,settings) -> BaseClient:
    """
    使用全局 Token 的客户端 (只读测试专用)
    """
    client = BaseClient(base_url=settings.API_BASE_URL)
    client.set_token(global_token)
    yield client

# =============================================================================
# API 响应验证 Fixtures
# =============================================================================

@pytest.fixture(scope="function")
def assert_api_success():
    """断言 API 响应成功"""
    def _assert(response: dict, message: str = ""):
        assert response.get('code') == 200, f"{message}: {response.get('msg')}"
        return response
    return _assert


@pytest.fixture(scope="function")
def assert_api_failure():
    """断言 API 响应失败"""
    def _assert(response: dict, expected_code: int = None, message: str = ""):
        assert response.get('code') != 200, f"{message}: 期望失败但成功"
        if expected_code:
            assert response.get('code') == expected_code, \
                f"{message}: 期望错误码 {expected_code}, 实际 {response.get('code')}"
        return response
    return _assert


