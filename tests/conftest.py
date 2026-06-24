"""
全局 pytest 配置和共享 fixtures
"""
import pytest
import os
import sys
import time
import random
import string
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

from config.settings import Settings
from config.cleanup_config import AUTO_CLEANUP_ON_SESSION_END, PRE_CLEANUP_TABLES
from common.logger import Logger
from common.utils.db_helper import DBHelper
from common.utils.data_factory import DataFactory
from common.utils.auth_helper import AuthHelper


# Import API clients and fixtures
from api.clients.base_client import BaseClient  
from api.clients.auth_client import AuthClient
from api.clients.role_client import RoleClient
from api.clients.menu_client import MenuClient
from api.clients.dict_client import DictClient
from api.clients.dept_client import DeptClient
from api.clients.user_client import UserClient
from api.clients.config_client import ConfigClient
from api.clients.notice_client import NoticeClient
from api.clients.monitor_client import MonitorClient
from api.clients.job_client import JobClient


#Import UI business logic
from ui.biz.common_biz import CommonBiz
from ui.biz.normal.login_biz import LoginBiz
from ui.biz.normal.user_biz import UserBiz
from ui.biz.normal.role_biz import RoleBiz
from ui.biz.normal.dept_biz import DeptBiz
from ui.biz.normal.dict_biz import DictBiz
from ui.biz.normal.post_biz import PostBiz
# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)
# =============================================================================
# 全局配置 Fixtures
# =============================================================================
@pytest.fixture(scope="session")
def settings():
    """配置实例"""
    yield Settings()

@pytest.fixture(scope="session")
def ensure_test_user_unlocked():
    """
    Session 级别 fixture - 确保测试用户未被锁定
    
    在并行执行测试时，多个测试文件同时运行登录失败测试可能导致账户锁定
    此 fixture 在测试开始前解锁用户，并在测试结束后再次解锁
    """
    # 在所有测试开始前解锁用户
    print("\n🔐 确保测试用户未被锁定...")
    AuthHelper.ensure_user_unlocked()
    
    yield
    
    # 在所有测试结束后再次解锁用户（以防测试过程中被锁定）
    print("\n🔐 测试完成，解锁测试用户...")
    AuthHelper.unlock_user()


@pytest.fixture(scope="session")
def project_dir() -> Path:
    """项目根目录"""
    return project_root


@pytest.fixture(scope="session")
def report_dir(project_dir) -> Path:
    """测试报告目录"""
    report_path = project_dir / "reports"
    report_path.mkdir(exist_ok=True)
    return report_path


@pytest.fixture(scope="session")
def log_dir(project_dir) -> Path:
    """日志目录"""
    log_path = project_dir / "logs"
    log_path.mkdir(exist_ok=True)
    return log_path


@pytest.fixture(scope="session")
def test_run_id() -> str:
    """测试运行唯一标识"""
    return datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + ''.join(
        random.choices(string.digits, k=4)
    )


@pytest.fixture(scope="session")
def test_environment() -> str:
    """测试环境"""
    return os.getenv("TEST_ENV", "dev")


# =============================================================================
# 数据库 Fixtures
# =============================================================================

@pytest.fixture(scope="session")
def db_helper(test_environment) -> DBHelper:
    """数据库帮助类 (Session 级别复用连接池)"""
    db = DBHelper(environment=test_environment)
    yield db
    db.close()


@pytest.fixture(scope="session", autouse=AUTO_CLEANUP_ON_SESSION_END)
def session_cleanup(db_helper):
    """
    会话级别的数据清理（自动执行）
    
    在测试会话开始前清理残留数据，在会话结束后再次清理
    并行执行时，只清理当前工作器创建的数据，避免影响其他工作器
    """
    import os
    # 获取worker_id，在非并行模式下默认为None
    worker_id = os.environ.get('PYTEST_XDIST_WORKER')
    logger.info(f"当前工作器ID: {worker_id if worker_id else 'master (非并行模式)'}")
    
    # 测试开始前清理（清理所有残留数据）
    logger.info("开始清理测试会话前的残留数据...")
    try:
        pre_cleanup = db_helper.cleanup_test_data(tables=PRE_CLEANUP_TABLES, dry_run=False, worker_id=None)
        if pre_cleanup['total_records'] > 0:
            logger.info(f"测试前清理完成: 删除了 {pre_cleanup['total_records']} 条记录")
    except Exception as e:
        logger.warning(f"测试前清理失败: {e}")
    
    yield
    
    # 测试结束后清理（只清理当前工作器的数据）
    logger.info("开始清理测试会话后的测试数据...")
    try:
        post_cleanup = db_helper.cleanup_test_data(dry_run=False, worker_id=worker_id)
        if post_cleanup['total_records'] > 0:
            logger.info(f"测试后清理完成: 删除了 {post_cleanup['total_records']} 条记录")
        else:
            logger.info("没有需要清理的测试数据")
    except Exception as e:
        logger.warning(f"测试后清理失败: {e}")


@pytest.fixture(scope="function")
def db_session(db_helper):
    """数据库会话 (每个用例独立事务)"""
    # 开始事务
    db_helper.start_transaction()
    yield db_helper
    # 回滚事务，确保数据隔离
    db_helper.rollback_transaction()


@pytest.fixture(scope="function")
def clean_database(db_helper):
    """清理测试数据 (用于需要真实提交数据的场景)"""
    yield
    # 测试结束后清理脏数据
    db_helper.cleanup_test_data()


@pytest.fixture(scope="function")
def dry_run_cleanup(db_helper):
    """试运行清理，查看有哪些测试数据"""
    def _dry_run(tables=None):
        return db_helper.cleanup_test_data(tables=tables, dry_run=True)
    return _dry_run


@pytest.fixture(scope="function")
def cleanup_tables(db_helper):
    """清理指定表的测试数据"""
    def _cleanup(tables):
        return db_helper.cleanup_test_data(tables=tables, dry_run=False)
    return _cleanup


# =============================================================================
# 时间相关 Fixtures
# =============================================================================

@pytest.fixture(scope="function")
def timestamp() -> str:
    """当前时间戳字符串"""
    return str(int(time.time() * 1000))


@pytest.fixture(scope="function")
def unique_id() -> str:
    """唯一标识符"""
    return datetime.now().strftime("%Y%m%d%H%M%S") + '_' + ''.join(
        random.choices(string.ascii_lowercase + string.digits, k=6)
    )


# =============================================================================
# 重试机制 Fixtures
# =============================================================================

@pytest.fixture(scope="function")
def retry_on_failure(request):
    """失败重试装饰器"""
    max_retries = getattr(request.module, "MAX_RETRIES", 2)
    retry_delay = getattr(request.module, "RETRY_DELAY", 1)
    
    for attempt in range(max_retries + 1):
        try:
            yield attempt
            break
        except Exception as e:
            if attempt == max_retries:
                raise
            logger.warning(f"重试 {attempt + 1}/{max_retries}: {str(e)}")
            time.sleep(retry_delay)


# =============================================================================
# 测试标记 Fixtures
# =============================================================================

@pytest.fixture(scope="function")
def test_marker(request):
    """获取当前测试用例的标记"""
    markers = {mark.name: mark.args for mark in request.node.iter_markers()}
    return markers


# =============================================================================
# 日志收集 Fixtures
# =============================================================================

@pytest.fixture(scope="function")
def test_logger(request, log_dir) -> logging.Logger:
    """每个测试用例独立日志"""
    test_name = request.node.name
    logger = Logger(f"test_{test_name}")
    
    # 添加文件处理器
    log_file = log_dir / f"{test_name}.log"
    handler = logging.FileHandler(log_file, encoding='utf-8')
    handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s'
    ))
    logger.addHandler(handler)
    
    yield logger
    
    # 清理 handler
    handler.close()
    logger.removeHandler(handler)


# =============================================================================
# 截图/录屏 Fixtures (UI 测试用)
# =============================================================================

@pytest.fixture(scope="function")
def screenshot_on_failure(request):
    """失败时自动截图"""
    yield
    if request.node.rep_call.failed:
        # 由 UI fixture 处理截图
        pass


# Hook: 记录测试结果
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """记录每个测试阶段的结果"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

# =============================================================================
# Playwright Fixtures (覆盖 pytest-playwright 插件，避免 asyncio 冲突)
# =============================================================================

@pytest.fixture(scope="session")
def playwright():
    """Playwright实例（同步版本，避免 asyncio 冲突）"""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        yield p
# ===================== 1. 全局浏览器会话（session级，每个worker独立） =====================
@pytest.fixture(scope="session")
def browser(playwright, settings):
    """浏览器实例
    在 pytest-xdist 并行模式下，每个 worker 会创建独立的浏览器实例
    避免多个 worker 共享同一浏览器实例导致连接关闭问题
    """
    import os
    import sys
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
    browser_type = settings.BROWSER
    
    # 尝试查找系统安装的 Chrome
    chrome_executable = None
    if sys.platform == 'win32':
        # Windows 上常见的 Chrome 安装路径
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                chrome_executable = path
                break
    
    if browser_type == 'chrome' or browser_type == 'chromium':
        launch_args = {
            'headless': settings.HEADLESS,
            'slow_mo': settings.SLOW_MO,
            'args': [
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-setuid-sandbox",
                "--remote-debugging-port=0",
            ]
        }
        # 如果找到系统 Chrome，使用它
        if chrome_executable:
            launch_args['executable_path'] = chrome_executable
            print(f"DEBUG: Using system Chrome at {chrome_executable}")
        
        try:
            browser = playwright.chromium.launch(**launch_args)
        except Exception as e:
            print(f"WARNING: Failed to launch Chromium: {e}")
            print("Falling back to API-only tests...")
            pytest.skip("Browser not available, skipping UI tests")
            
    elif browser_type == 'firefox':
        browser = playwright.firefox.launch(
            headless=settings.HEADLESS,
            slow_mo=settings.SLOW_MO,
        )
    elif browser_type == 'webkit':
        browser = playwright.webkit.launch(
            headless=settings.HEADLESS,
            slow_mo=settings.SLOW_MO,
        )
    else:
        raise ValueError(f"不支持的浏览器类型: {browser_type}")
    
    yield browser
    browser.close()
# ===================== 2. 浏览器上下文+页面（用例级，每个用例独立环境） =====================
@pytest.fixture(scope="function")
def context(browser) -> object:
    """上下文实例
    每个测试用例创建一个全新的上下文，隔离 Cookies/LocalStorage/Cache
    """
    import os
    import uuid
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "no-worker")
    recordings_dir = f"recordings/{worker_id}_{uuid.uuid4().hex[:8]}"
    
    context = browser.new_context(
        bypass_csp=True, 
        record_video_dir=recordings_dir,
        ignore_https_errors=True,
        viewport=None
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context, request) -> object:
    """页面实例"""
    page = context.new_page()
    # 开启控制台日志捕获，方便调试
    page.on("console", lambda msg: logger.debug(f"[Console] {msg.type}: {msg.text}"))
    page.on("pageerror", lambda err: logger.warning(f"[PageError] 页面异常: {err}"))
    yield page
    # if request.node.rep_call.failed:
    #     # 测试失败时，自动截图
    #     page.screenshot(path=f"failed_screenshots/{request.node.name}.png")
    page.close()


# =============================================================================
# 认证相关 Fixtures
# =============================================================================
@pytest.fixture(scope="function")
def get_login_token(settings) -> str:
    """获取登录Token""" 
    auth = AuthClient()
    
    login_result = auth.login(
        username=settings.USERNAME,
        password=settings.PASSWORD
    )
    
    if login_result.get('code') != 200:
        pytest.fail(f"登录失败: {login_result.get('msg', 'Unknown error')}")
    
    token = login_result.get('data', {}).get('token') or login_result.get('token')
    return token


@pytest.fixture(scope="function")
def authenticated_client(settings) -> BaseClient:
    """
    ✅ 已认证的 API 客户端 (Function Scope - 关键修复)
    
    每个测试用例独立登录，获取独立 Token。
    即使其他用例调用了 logout，也不会影响当前用例。
    
    这是解决"单用例通过，全量失败"问题的核心 fixture。
    """
    # 1. 创建认证客户端并登录
    auth = AuthClient()
    
    login_result = auth.login(
        username=settings.USERNAME,
        password=settings.PASSWORD
    )
    
    # 如果登录失败，检查是否是账户被锁定
    if login_result.get('code') != 200:
        msg = login_result.get('msg', '')
        if "锁定" in msg or "账号已被锁定" in msg or "账户已锁定" in msg:
            print(f"⚠️ 检测到账户锁定，尝试自动解锁...")
            AuthHelper.unlock_user()
            
            # 解锁后重试登录
            login_result = auth.login(
                username=settings.USERNAME,
                password=settings.PASSWORD
            )
    
    if login_result.get('code') != 200:
        pytest.fail(f"登录失败: {login_result.get('msg', 'Unknown error')}")
    
    token = login_result.get('data', {}).get('token') or login_result.get('token')
    logger.info(f"登录成功，Token: {token[:20]}...")
    
    # 2. 使用已认证的 AuthClient（包含 get_user_info 和 logout 方法）
    auth.set_token(token)
    
    yield auth
    
    # 3. ⚠️ 重要：不要在这里调用 logout!
    # 让 Token 自然过期，避免影响其他用例


# =============================================================================
# API 业务客户端 Fixtures
# =============================================================================
@pytest.fixture(scope="function")
def api_client() -> BaseClient:
    """
    基础 API 客户端 (无认证)
    每个用例获取全新实例，确保线程安全
    """
    client = BaseClient()
    yield client
# AuthClient fixture for tests that need login/logout methods
@pytest.fixture(scope="function")
def auth_client() -> AuthClient:
    """认证客户端 (提供 login/logout 方法)"""
    client = AuthClient()
    yield client

@pytest.fixture(scope="function")
def user_client(authenticated_client) -> object:
    """用户接口客户端"""
    client = UserClient()
    # 从authenticated_client复制会话头信息
    client.session.headers.update(authenticated_client.session.headers)
    yield client

@pytest.fixture(scope="function")
def role_client(authenticated_client) -> RoleClient:
    """角色接口客户端"""
    client = RoleClient()
    # 从authenticated_client复制会话头信息
    client.session.headers.update(authenticated_client.session.headers)
    yield client

@pytest.fixture(scope="function")
def menu_client(authenticated_client) -> MenuClient:
    """菜单接口客户端"""
    client = MenuClient()
    # 从authenticated_client复制会话头信息
    client.session.headers.update(authenticated_client.session.headers)
    yield client

@pytest.fixture(scope="function")
def dept_client(authenticated_client) -> DeptClient:
    """部门接口客户端"""
    client = DeptClient()
    # 从authenticated_client复制会话头信息
    client.session.headers.update(authenticated_client.session.headers)
    yield client

@pytest.fixture(scope="function")
def dict_client(authenticated_client) -> DictClient:
    """字典接口客户端"""
    from api.clients.dict_client import DictClient
    client = DictClient()
    # 从authenticated_client复制会话头信息
    client.session.headers.update(authenticated_client.session.headers)
    yield client

@pytest.fixture(scope="function")
def notice_client(authenticated_client) -> NoticeClient:
    """通知接口客户端"""
    client = NoticeClient()
    # 从authenticated_client复制会话头信息
    client.session.headers.update(authenticated_client.session.headers)
    yield client


@pytest.fixture(scope="function")
def monitor_client(authenticated_client) -> MonitorClient:
    """监控接口客户端"""
    client = MonitorClient()
    # 从authenticated_client复制会话头信息
    client.session.headers.update(authenticated_client.session.headers)
    yield client

@pytest.fixture(scope="function")
def config_client(authenticated_client) -> object:
    """配置接口客户端"""
    client = ConfigClient()
    client.session.headers.update(authenticated_client.session.headers)
    yield client

@pytest.fixture(scope="function")
def job_client(authenticated_client) -> JobClient:
    """定时任务接口客户端"""
    client = JobClient()
    client.session.headers.update(authenticated_client.session.headers)
    yield client

@pytest.fixture(scope="function")
def post_client(authenticated_client):
    """岗位接口客户端"""
    from api.clients.post_client import PostClient
    client = PostClient()
    client.session.headers.update(authenticated_client.session.headers)
    yield client


# =============================================================================
# UI 业务客户端 Fixtures
# =============================================================================
# ===================== 3. 自动登录夹具（所有探索用例默认已登录） =====================
@pytest.fixture(scope="function")
def login_home(page, settings):
    """自动管理员登录，返回已登录状态（HomePage对象，支持页面导航）"""
    from ui.pages.modules.home_page import HomePage
    login_biz = LoginBiz(page)
    result = login_biz.login(settings.USERNAME, settings.PASSWORD)
    if "成功" not in result:
        pytest.fail(f"登录失败: {result}")
    yield HomePage(page)

# ===================== 4. 公共业务夹具（直接注入用例，无需重复导入） =====================
@pytest.fixture(scope="function")
def common_biz(login_home, page):
    return CommonBiz(page)
@pytest.fixture(scope="function")
def login_biz(page):
    return LoginBiz(page)
@pytest.fixture(scope="function")
def user_biz(login_home, page):
    return UserBiz(page)
@pytest.fixture(scope="function")
def role_biz(login_home, page):
    return RoleBiz(page)
@pytest.fixture(scope="function")
def dept_biz(login_home, page):
    return DeptBiz(page)
@pytest.fixture(scope="function")
def dict_biz(login_home, page):
    return DictBiz(page)
@pytest.fixture(scope="function")
def post_biz(login_home, page):
    return PostBiz(page)
# =============================================================================
# 测试数据 Fixtures
# =============================================================================

# ===================== 自动生成唯一测试数据（避免数据冲突） =====================
@pytest.fixture(scope="function")
def test_user_data()-> Dict[str, Any]:
    """用户测试数据"""
    return DataFactory.generate_user_data()

@pytest.fixture(scope="function")
def test_user_data_batch(request):
    """批量用户测试数据"""
    # num = request.param if hasattr(request, 'param') else 2
    # 核心：获取传入的参数，无参数则使用默认值 2
    num = getattr(request, "param", 2)
    return DataFactory.generate_user_data_batch(num)
  
@pytest.fixture(scope="function")
def test_role_data():
    """角色测试数据"""
    return DataFactory.generate_role_data()
@pytest.fixture(scope="function")
def test_role_menu_data():
    """角色菜单测试数据"""
    return DataFactory.generate_role_menu_data()
@pytest.fixture(scope="function")
def test_menu_data():
    """菜单测试数据"""
    return DataFactory.generate_menu_data()   
@pytest.fixture(scope="function")
def test_menu_api_data():
    """菜单测试数据"""
    return DataFactory.generate_menu_api_data()

@pytest.fixture(scope="function")
def test_dept_data() -> Dict[str, Any]:
    """部门测试数据"""
    return DataFactory.generate_dept_data()
@pytest.fixture(scope="function")
def test_child_dept_data():
    """子部门测试数据"""
    return DataFactory.generate_child_dept_data()
@pytest.fixture(scope="function")
def test_post_data():
    """岗位测试数据"""
    return DataFactory.generate_post_data()
@pytest.fixture(scope="function")
def test_post_data_batch(request):
    """批量岗位测试数据"""
    # num = request.param if hasattr(request, 'param') else 2
    # 核心：获取传入的参数，无参数则使用默认值 2
    num = getattr(request, "param", 2)
    return DataFactory.generate_post_data_batch(num)

@pytest.fixture(scope="function")
def test_dict_type_data():
    """字典类型测试数据"""
    return DataFactory.generate_dict_type_data()

@pytest.fixture(scope="function")
def test_dict_data():
    """字典数据测试数据"""
    return DataFactory.generate_dict_data()

@pytest.fixture(scope="function")
def test_job_data(unique_id) -> Dict[str, Any]:
    """定时任务测试数据"""
    return DataFactory.generate_job_data()

@pytest.fixture(scope="function")
def test_config_data(unique_id) -> Dict[str, Any]:
    """配置测试数据"""
    return DataFactory.generate_config_data()

# =============================================================================
# 已创建数据 Fixtures (带自动清理)
# =============================================================================

@pytest.fixture(scope="function")
def created_user(user_client, test_user_data) -> int:
    """
    已创建的用户 ID (自动清理)
    
    使用此 fixture 的测试用例会：
    1. 自动创建用户
    2. 返回用户 ID 供测试使用
    3. 测试结束后自动删除用户
    """
    # 创建用户
    result = user_client.create_user(test_user_data)
    
    if result.get('code') != 200:
        pytest.fail(f"创建用户失败: {result.get('msg')}")
    
    # 通过用户名查询获取用户ID
    user_list_response = user_client.get_user_list(userName=test_user_data.get("userName"))
    if user_list_response.get('code') != 200:
        pytest.fail(f"查询用户列表失败: {user_list_response.get('msg')}")
    
    rows = user_list_response.get('rows', [])
    if not rows:
        pytest.fail("未找到创建的用户")
    
    user_id = rows[0].get('userId')
    if not user_id:
        pytest.fail("未找到用户ID")
    
    logger.info(f"创建测试用户: {user_id}")
    
    yield user_id
    
    # 清理：删除用户
    try:
        user_client.delete_user(user_id)
        logger.info(f"清理测试用户: {user_id}")
    except Exception as e:
        logger.warning(f"清理用户失败 {user_id}: {e}")


@pytest.fixture(scope="function")
def created_role(role_client, test_role_data) -> dict:
    """已创建的角色信息 (自动清理)"""
    result = role_client.create_role(test_role_data)
    
    if result.get('code') != 200:
        pytest.fail(f"创建角色失败: {result.get('msg')}")
    
    # 通过角色名查询获取角色信息
    role_list_response = role_client.get_role_list(roleName=test_role_data.get("roleName"))
    if role_list_response.get('code') != 200:
        pytest.fail(f"查询角色列表失败: {role_list_response.get('msg')}")
    
    rows = role_list_response.get('rows', [])
    if not rows:
        pytest.fail("未找到创建的角色")
    
    role_info = rows[0]
    role_id = role_info.get('roleId')
    if not role_id:
        pytest.fail("未找到角色ID")
    
    logger.info(f"创建测试角色: {role_id}")
    
    yield role_info
    
    # 清理
    try:
        role_client.delete_role(role_id)
        logger.info(f"清理测试角色: {role_id}")
    except Exception as e:
        logger.warning(f"清理角色失败 {role_id}: {e}")


@pytest.fixture(scope="function")
def created_user_with_role(
    user_client, 
    role_client, 
    test_user_data, 
    test_role_data
) -> Dict[str, int]:
    """
    已创建的用户和角色 (带关联，自动清理)
    """
    # 1. 创建角色
    role_result = role_client.create_role(test_role_data)
    role_id = role_result.get('roleId')
    
    # 2. 创建用户并分配角色
    test_user_data['roleIds'] = [role_id]
    user_result = user_client.create_user(test_user_data)
    user_id = user_result.get('userId')
    
    logger.info(f"创建测试用户 {user_id} 和角色 {role_id}")
    
    yield {
        'user_id': user_id,
        'role_id': role_id,
        'username': test_user_data['username']
    }
    
    # 清理 (先删用户，再删角色)
    try:
        user_client.delete_user([user_id])
        role_client.delete_role([role_id])
        logger.info(f"清理测试数据完成")
    except Exception as e:
        logger.warning(f"清理失败: {e}")


@pytest.fixture(scope="function")
def created_dept(dept_client, test_dept_data) -> int:
    """已创建的部门 ID (自动清理)"""
    result = dept_client.create_dept(test_dept_data)
    
    if result.get('code') != 200:
        pytest.fail(f"创建部门失败: {result.get('msg')}")
    
    dept_id = result.get('deptId') or result.get('dept_id')
    logger.info(f"创建测试部门: {dept_id}")
    
    yield dept_id
    
    try:
        dept_client.delete_dept(dept_id)
        logger.info(f"清理测试部门: {dept_id}")
    except Exception as e:
        logger.warning(f"清理部门失败 {dept_id}: {e}")


@pytest.fixture(scope="function")
def created_job(job_client, test_job_data) -> int:
    """已创建的任务 ID (自动清理)"""
    result = job_client.create_job(test_job_data)
    
    if result.get('code') != 200:
        pytest.fail(f"创建任务失败: {result.get('msg')}")
    
    job_id = result.get('jobId') or result.get('job_id')
    logger.info(f"创建测试任务: {job_id}")
    
    yield job_id
    
    try:
        job_client.delete_job([job_id])
        logger.info(f"清理测试任务: {job_id}")
    except Exception as e:
        logger.warning(f"清理任务失败 {job_id}: {e}")


# =============================================================================
# pytest-xdist 并行执行支持
# =============================================================================

def pytest_collection_modifyitems(config, items):
    """
    收集serial标记的测试nodeid，并调整测试执行顺序
    """
    worker_id = os.environ.get('PYTEST_XDIST_WORKER')
    
    if worker_id:
        # 并行模式下不调整顺序，由调度器处理
        pass
    else:
        # 非并行模式下，确保serial标记的测试先执行
        serial_tests = [item for item in items if 'serial' in item.keywords]
        other_tests = [item for item in items if 'serial' not in item.keywords]
        
        if serial_tests:
            items[:] = serial_tests + other_tests


def pytest_xdist_make_scheduler(config, log):
    """自定义测试调度器，确保serial标记的测试用例串行执行（仅在xdist插件可用时生效）"""
    # 检查xdist插件是否可用
    if not config.pluginmanager.hasplugin('xdist'):
        return None  # 返回None表示使用默认调度器
    
    from xdist.scheduler import LoadScopeScheduling
    
    class SerialFirstScheduling(LoadScopeScheduling):
        def _split_scope(self, nodeid):
            if nodeid.endswith('::test_') or '::test_' in nodeid:
                parts = nodeid.split('::')
                if len(parts) >= 3:
                    test_name = parts[-1]
                    test_file = parts[-2] if parts[-2].endswith('.py') else parts[-3]
                    
                    import importlib.util
                    import os
                    test_path = os.path.join(config.rootdir, test_file)
                    if os.path.exists(test_path):
                        spec = importlib.util.spec_from_file_location("test_module", test_path)
                        if spec and spec.loader:
                            try:
                                test_module = importlib.util.module_from_spec(spec)
                                spec.loader.exec_module(test_module)
                                if hasattr(test_module, test_name):
                                    test_func = getattr(test_module, test_name)
                                    if hasattr(test_func, 'pytestmark'):
                                        for mark in test_func.pytestmark:
                                            if mark.name == 'serial':
                                                return f"serial_{nodeid}"
                            except Exception:
                                pass
                return super()._split_scope(nodeid)
            return super()._split_scope(nodeid)
    
    return SerialFirstScheduling(config, log)


def pytest_xdist_auto_num_workers(config):
    """自动设置worker数量（仅在xdist插件可用时生效）"""
    import multiprocessing
    import sys
    
    # 检查xdist插件是否可用
    if not config.pluginmanager.hasplugin('xdist'):
        return None  # 返回None表示使用默认worker数量
    
    # Windows下限制worker数量，避免进程池问题
    if sys.platform.startswith('win'):
        # Windows下使用spawn模式，开销较大，限制最大4个worker
        return max(1, min(multiprocessing.cpu_count(), 4))
    else:
        return max(1, min(multiprocessing.cpu_count(), 8))


def pytest_configure(config):
    """pytest配置钩子 - 设置Windows特定的多进程上下文"""
    import sys
    
    if sys.platform.startswith('win'):
        # Windows下强制使用spawn模式，避免fork导致的问题
        import multiprocessing
        try:
            multiprocessing.set_start_method('spawn', force=True)
        except RuntimeError:
            # 如果已经设置过，忽略错误
            pass

