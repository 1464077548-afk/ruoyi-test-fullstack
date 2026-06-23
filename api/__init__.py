"""接口测试层"""
from .clients.dept_client import DeptClient
from .clients.auth_client import AuthClient
from .clients.user_client import UserClient
from .clients.role_client import RoleClient
from .clients.menu_client import MenuClient
from .clients.dict_client import DictClient
from .clients.config_client import ConfigClient
from .clients.monitor_client import MonitorClient
from .clients.notice_client import NoticeClient

__all__ = [
    'DeptClient',
    'AuthClient',
    'UserClient',
    'RoleClient',
    'MenuClient',
    'DictClient',
    'ConfigClient',
    'MonitorClient',
    'NoticeClient'
]
