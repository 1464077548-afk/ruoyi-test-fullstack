"""UI性能测试"""
import pytest
import time
from ui.pages.modules.login_page import LoginPage
from ui.pages.modules.home_page import HomePage
from ui.pages.modules.user_page import UserPage
from config.settings import Settings


class TestUiPerformance:
    """UI性能测试类"""
    
    def test_login_page_load_time(self, page):
        """测试登录页面加载时间"""
        login_page = LoginPage(page)
        start_time = time.time()
        login_page.goto()
        # 等待页面完全加载
        login_page.wait_for_load_state()
        end_time = time.time()
        load_time = end_time - start_time
        
        # 考虑并行执行时的资源竞争，适当放宽时间限制
        assert load_time < 5.0, f"登录页面加载时间过长：{load_time}秒"
    
    def test_login_performance(self, page, settings):
        """测试登录性能"""
        login_page = LoginPage(page)
        login_page.goto()
        
        start_time = time.time()
        login_page.login(settings.USERNAME, settings.PASSWORD)
        end_time = time.time()
        login_time = end_time - start_time
        
        assert login_page.is_login_success()
        assert login_time < 10.0, f"登录操作时间过长: {login_time}秒"
    
    def test_home_page_load_time(self, page, settings):
        """测试首页加载时间"""
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(settings.USERNAME, settings.PASSWORD)
        
        home_page = HomePage(page)
        start_time = time.time()
        # 首页应该已经在登录后加载完成，这里测试刷新时间
        page.reload()
        end_time = time.time()
        load_time = end_time - start_time
        
        assert load_time < 2.0, f"首页加载时间过长: {load_time}秒"
    
    def test_user_page_load_time(self, page, settings):
        """测试用户管理页面加载时间"""
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(settings.USERNAME, settings.PASSWORD)
        
        home_page = HomePage(page)
        start_time = time.time()
        home_page.go_to_user_manage()
        end_time = time.time()
        load_time = end_time - start_time
        
        assert load_time < 3.0, f"用户管理页面加载时间过长: {load_time}秒"
    
    def test_user_search_performance(self, page, settings):
        """测试用户搜索性能"""
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(settings.USERNAME, settings.PASSWORD)
        
        home_page = HomePage(page)
        user_page = home_page.go_to_user_manage()
        
        start_time = time.time()
        user_page.search_user("admin")
        end_time = time.time()
        search_time = end_time - start_time
        
        assert search_time < 6.0, f"用户搜索时间过长: {search_time}秒"
