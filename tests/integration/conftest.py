"""
集成测试专用 fixtures (UI + API 联合测试)
"""
import pytest
from typing import Dict, Any
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.settings import Config, Settings
from ui.pages.modules.login_page import LoginPage
from common.logger import get_logger

logger = get_logger(__name__)

# =============================================================================
# 联合认证 Fixtures
# =============================================================================

@pytest.fixture(scope="function")
def ui_api_authenticated(page, authenticated_client):
    """
    UI 和 API 都认证的状态

    用于测试 UI 操作与 API 数据的一致性
    """



    # UI 登录
    login_page = LoginPage(page)
    home_page = login_page.login(
        Config.DEFAULT_USERNAME,
        Config.DEFAULT_PASSWORD
    )

    yield {
        'page': page,
        'home': home_page,
        'api_client': authenticated_client
    }


# =============================================================================
# 数据一致性 Fixtures
# =============================================================================

@pytest.fixture(scope="function")
def data_sync_validator(ui_api_authenticated):
    """数据同步验证器"""

    def validate_user_list():
        """验证用户列表数据一致性"""
        # API 获取
        api_result = ui_api_authenticated['api_client'].get('/system/user/list')
        api_users = {u['userId']: u for u in api_result['rows']}

        # UI 获取
        ui_page = ui_api_authenticated['home'].go_to_user_manage()
        ui_users = ui_page.get_all_users()

        # 比较
        return {
            'api_count': len(api_users),
            'ui_count': len(ui_users),
            'consistent': len(api_users) == len(ui_users)
        }

    return validate_user_list


@pytest.fixture(scope="function")
def cross_module_test_data(unique_id) -> Dict[str, Any]:
    """跨模块测试数据"""
    return {
        'user': {
            'username': f'user_{unique_id}',
            'nickName': f'测试用户_{unique_id}',
        },
        'role': {
            'roleName': f'测试角色_{unique_id}',
            'roleKey': f'test_role_{unique_id}',
        },
        'dept': {
            'deptName': f'测试部门_{unique_id}',
        },
    }


# =============================================================================
# 端到端流程 Fixtures
# =============================================================================

@pytest.fixture(scope="function")
def e2e_flow_context() -> Dict[str, Any]:
    """端到端流程上下文"""
    return {
        'steps': [],
        'results': [],
        'cleanup_actions': [],
    }


@pytest.fixture(scope="function")
def e2e_flow_executor(e2e_flow_context):
    """端到端流程执行器"""

    def execute(steps: list, context: Dict[str, Any]):
        results = []
        for step in steps:
            try:
                result = step(context)
                results.append({'step': step.__name__, 'status': 'success', 'result': result})
                e2e_flow_context['steps'].append(step.__name__)
            except Exception as e:
                results.append({'step': step.__name__, 'status': 'failed', 'error': str(e)})
                break
        return results

    return execute


@pytest.fixture(scope="function")
def e2e_cleanup(e2e_flow_context, authenticated_client):
    """端到端测试清理"""
    yield

    # 执行清理动作
    for cleanup in e2e_flow_context.get('cleanup_actions', []):
        try:
            cleanup(authenticated_client)
            logger.info(f"清理完成：{cleanup.__name__}")
        except Exception as e:
            logger.warning(f"清理失败 {cleanup.__name__}: {e}")
