import pytest
from ui.pages.modules.home_page import HomePage
from config.settings import Settings


@pytest.mark.ui
@pytest.mark.component
class TestMenuComponent:
    """菜单组件测试"""

    def test_menu_visibility(self, login_home):
        """测试菜单可见性"""
        home_page = HomePage(login_home)
        
        # 验证菜单可见
        assert home_page.is_menu_visible()
        
    def test_menu_navigation(self, common_biz):
        """测试菜单导航功能"""
        common_biz.switch_menu("系统管理/用户管理") 
        assert "user" in common_biz.user.page.url.lower()
       
