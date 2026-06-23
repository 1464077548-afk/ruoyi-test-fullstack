import pytest
from ui.pages.modules.login_page import LoginPage
from config.settings import Settings


@pytest.mark.module
@pytest.mark.ui
class TestLoginModule:
    """登录模块测试类"""

    def test_login_success(self, login_page):
        """P0-成功登录"""
        settings = Settings()  
        # 打开登录页面
        login_page.goto("/login")
        
        # 登录
        login_page.login(settings.USERNAME, settings.PASSWORD)
        
        # 验证登录成功
        assert login_page.is_login_success(), "登录失败"
    
    @pytest.mark.ui
    @pytest.mark.l1
    @pytest.mark.p1
    @pytest.mark.parametrize("username,password,expected_error", [
        ("admin", "wrong_password","用户不存在/密码错误"),
        ("nonexistent_user", "admin123","用户不存在/密码错误"),
        ("","admin23","用户名不能为空"), #前端校验
        ("admin","","密码不能为空"),
        ])
    def test_login_invalid_username(self, login_page, username, password, expected_error):
        """P1-登录失败"""
        
        # 打开登录页面
        login_page.goto("/login")
        
        # 登录
        error_msg = login_page.login(username, password)
        
        # 验证错误信息
        assert error_msg, f"应该显示错误信息"