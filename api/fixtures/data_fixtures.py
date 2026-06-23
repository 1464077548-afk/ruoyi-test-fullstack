import pytest
from common.utils.data_factory import DataFactory
from api.clients.user_client import UserClient
from api.clients.role_client import RoleClient
from api.clients.menu_client import MenuClient
from api.clients.monitor_client import MonitorClient
from api.clients.dict_client import DictClient
from api.clients.dept_client import DeptClient
from api.clients.config_client import ConfigClient
from api.clients.notice_client import NoticeClient


@pytest.fixture(scope="function")
def test_user_data():
    """测试用户数据"""
    return DataFactory.generate_user_data()


@pytest.fixture(scope="function")
def test_role_data():
    """测试角色数据"""
    return DataFactory.generate_role_data()


@pytest.fixture(scope="function")
def user_client(get_login_token):
    """用户客户端"""
    client = UserClient()
    client.set_token(get_login_token)
    print(f"user_client token: {get_login_token[:20]}...")
    return client


@pytest.fixture(scope="function")
def role_client(get_login_token):
    """角色客户端"""
    client = RoleClient()
    client.set_token(get_login_token)
    print(f"role_client token: {get_login_token[:20]}...")
    return client

@pytest.fixture(scope="function")
def menu_client(get_login_token):
    """菜单客户端"""
    client = MenuClient()
    client.set_token(get_login_token)
    print(f"menu_client token: {get_login_token[:20]}...")
    return client

@pytest.fixture(scope="function")
def monitor_client(get_login_token):
    """监控客户端"""
    client = MonitorClient()
    client.set_token(get_login_token)
    print(f"monitor_client token: {get_login_token[:20]}...")
    return client


@pytest.fixture(scope="function")
def dict_client(get_login_token):
    """字典客户端"""
    client = DictClient()
    client.set_token(get_login_token)
    print(f"dict_client token: {get_login_token[:20]}...")
    return client


@pytest.fixture(scope="function")
def dept_client(get_login_token):
    """部门客户端"""
    client = DeptClient()
    client.set_token(get_login_token)
    print(f"dept_client token: {get_login_token[:20]}...")
    return client


@pytest.fixture(scope="function")
def config_client(get_login_token):
    """配置客户端"""
    client = ConfigClient()
    client.set_token(get_login_token)
    print(f"config_client token: {get_login_token[:20]}...")
    return client


@pytest.fixture(scope="function")
def notice_client(get_login_token):
    """通知客户端"""
    client = NoticeClient()
    client.set_token(get_login_token)
    print(f"notice_client token: {get_login_token[:20]}...")
    return client



@pytest.fixture(scope="function")
def created_user(user_client, test_user_data):
    """创建测试用户"""
    # 创建用户
    response = user_client.create_user(test_user_data)
    # 通过用户名查询获取用户ID
    user_list_response = user_client.get_user_list(userName=test_user_data.get("userName"))
    user_id = user_list_response.get("rows")[0].get("userId")
    
    # 获取创建的用户
    user_info = user_client.get_user_by_id(user_id)
    
    yield user_info.get("data", {})
    
    # 清理：删除创建的用户
    try:
        user_client.delete_user(user_id)
    except Exception as e:
        print(f"清理用户失败: {e}")


@pytest.fixture(scope="function")
def created_user_id(created_user):
    """创建测试用户并返回用户ID"""
    return created_user.get("userId")


@pytest.fixture(scope="function")
def created_role(role_client, test_role_data):
    """创建测试角色"""
    # 创建角色
    response = role_client.create_role(test_role_data)
    assert response.get("code") == 200
    
    # 通过角色名查询获取角色ID
    role_list_response = role_client.get_role_list(roleName=test_role_data.get("roleName"))
    assert role_list_response.get("code") == 200
    assert len(role_list_response.get("rows", [])) > 0
    role_id = role_list_response.get("rows")[0].get("roleId")
    assert role_id, "创建角色失败"
    
    # 获取创建的角色
    role_info = role_client.get_role_by_id(role_id)
    assert role_info.get("code") == 200
    
    yield role_info.get("data", {})
    
    # 清理：删除创建的角色
    try:
        role_client.delete_role(role_id)
    except Exception as e:
        print(f"清理角色失败: {e}")
