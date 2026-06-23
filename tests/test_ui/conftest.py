"""UI测试配置和共享fixtures"""
import pytest
from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
from config.settings import Settings
from ui.pages.base_page import BasePage
from ui.pages.modules.login_page import LoginPage
from ui.pages.modules.home_page import HomePage
from ui.pages.modules.user_page import UserPage
from ui.pages.modules.role_page import RolePage
from ui.pages.modules.menu_page import MenuPage
from ui.pages.modules.dict_page import DictPage
from ui.pages.modules.dept_page import DeptPage
from common.utils.data_factory import DataFactory
import logging

# Import API clients and fixtures
from api.clients.base_client import BaseClient  
from api.clients.auth_client import AuthClient
from api.clients.role_client import RoleClient
from ui.biz.common_biz import CommonBiz
from ui.biz.normal.login_biz import LoginBiz
from ui.biz.normal.user_biz import UserBiz
from ui.biz.normal.role_biz import RoleBiz
from ui.biz.normal.dept_biz import DeptBiz
from ui.biz.normal.dict_biz import DictBiz



from ui.biz.special.abnormal_biz import AbnormalBiz
from ui.biz.special.security_biz import SecurityBiz
from ui.biz.special.concurrency_biz import ConcurrencyBiz



logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def login_page(page):
    """登录页面实例"""
    return LoginPage(page)

@pytest.fixture(scope="function")
def home_page(login_home):
    """首页实例"""
    login_home.goto("/index")
    return HomePage(login_home.page)

@pytest.fixture(scope="function")
def user_page(login_home):
    """用户管理页面实例"""
    login_home.goto("/system/user")
    return UserPage(login_home.page)
@pytest.fixture(scope="function")
def role_page(login_home):
    """角色管理页面实例"""
    login_home.goto("/system/role")
    return RolePage(login_home.page)
@pytest.fixture(scope="function")
def menu_page(login_home):
    """菜单管理页面实例"""
    login_home.goto("/system/menu")
    return MenuPage(login_home.page)
@pytest.fixture(scope="function")
def dict_page(login_home):
    """字典管理页面实例"""
    login_home.goto("/system/dict")
    return DictPage(login_home.page)
@pytest.fixture(scope="function")
def dept_page(login_home):
    """部门管理页面实例"""
    login_home.goto("/system/dept")
    return DeptPage(login_home.page)
@pytest.fixture(scope="function")
def profile_page(login_home):
    """个人中心页面实例"""
    login_home.goto("/system/profile")
    from ui.pages.modules.profile_page import ProfilePage
    return ProfilePage(login_home.page)

# ===================== 4. 公共业务夹具（直接注入用例，无需重复导入） =====================
@pytest.fixture(scope="function")
def abnormal_biz(page):
    """异常场景业务对象"""
    return AbnormalBiz(page)

@pytest.fixture(scope="function")
def security_biz(page):
    """安全场景业务对象"""
    return SecurityBiz(page)

@pytest.fixture(scope="function")
def concurrency_biz(browser):
    """并发场景业务对象"""
    return ConcurrencyBiz(browser)


