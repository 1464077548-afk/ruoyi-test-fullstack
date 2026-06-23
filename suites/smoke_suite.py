import pytest
"""冒烟测试套件"""
pytestmark = [
    pytest.mark.smoke,
    pytest.mark.p0,
]

# 包含：API L1 核心 + UI L2 核心
class SmokeSuite:
    """冒烟测试套件"""
    
    @pytest.mark.smoke
    @pytest.mark.api
    def test_login_api(self):
        """测试登录接口"""
        from api.clients.auth_client import AuthClient
        from config.settings import get_settings
        
        settings = get_settings()
        auth_client = AuthClient(settings.base_url)
        
        response = auth_client.login({
            "username": "admin",
            "password": "123456"
        })
        assert response.get("code") == 200
        assert "token" in response
    
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_login_ui(self, browser):
        """测试登录UI"""
        from ui.pages.base_page import BasePage
        from config.settings import get_settings
        
        settings = get_settings()
        page = BasePage(browser, settings.base_url)
        
        # 这里需要根据实际页面元素调整
        # 例如：page.login("admin", "123456")
        # assert page.is_logged_in()
        pass
    
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_user_list(self, auth_token):
        """测试获取用户列表"""
        from api.clients.user_client import UserClient
        from config.settings import get_settings
        
        settings = get_settings()
        user_client = UserClient(settings.base_url, auth_token)
        
        response = user_client.get_user_list()
        assert response.get("code") == 200
        assert "data" in response
    
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_menu_list(self, auth_token):
        """测试获取菜单列表"""
        from api.clients.menu_client import MenuClient
        from config.settings import get_settings
        
        settings = get_settings()
        menu_client = MenuClient(settings.base_url, auth_token)
        
        response = menu_client.get_menu_list()
        assert response.get("code") == 200
        assert "data" in response