import pytest
import random
from ui.pages.modules.login_page import LoginPage
from ui.pages.modules.user_page import UserPage
from config.settings import Settings
from common.utils.data_factory import DataFactory


@pytest.mark.module
@pytest.mark.ui
class TestUserModule:
    """用户管理模块测试类"""

    def test_add_user_success(self, page):
        """测试成功添加用户"""
        settings = Settings()
        login_page = LoginPage(page)
        user_page = UserPage(page)
        
        # 登录
        login_page.goto()
        login_page.login(settings.USERNAME, settings.PASSWORD)
        
        # 导航到用户管理页面
        login_page.goto("/system/user")
        # 等待页面加载
        page.wait_for_load_state('load', timeout=30000)
        
        # 填写用户表单
        username = DataFactory.generate_unique_username()
        # 生成唯一的手机号码
        phone = f"138{random.randint(10000000, 99999999)}"
        user_data = {
            'userName': username,
            'nickName': f"测试用户{username}",
            'password': "123456",
            'email': f"{username}@example.com",
            'phonenumber': phone
        }
        
        # 使用create_user方法创建用户（该方法会自动点击新增按钮）
        message = user_page.create_user(user_data)
        assert "成功" in message, f"创建用户失败: {message}"
        
        # 搜索用户
        user_page.search_user(username)
        
        # 验证用户存在
        user_list = user_page.get_user_list()
        assert any(username in user for user in user_list), f"用户 {username} 未找到"

        #删除用户
        user_page.delete_user(username)
    
    def test_search_user(self, page):
        """测试搜索用户"""
        settings = Settings()
        login_page = LoginPage(page)
        user_page = UserPage(page)
        
        # 登录
        login_page.goto()
        login_page.login(settings.USERNAME, settings.PASSWORD)
        
        # 导航到用户管理页面
        login_page.goto("/system/user")
        page.wait_for_load_state('load', timeout=30000)
        
        # 搜索管理员用户
        user_page.search_user("admin")
        
        # 验证搜索结果
        user_list = user_page.get_user_list()
        assert any("admin" in user for user in user_list), "未找到管理员用户"
