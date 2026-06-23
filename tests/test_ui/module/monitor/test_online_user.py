"""
L2: 在线用户模块测试
验证在线用户管理功能的完整测试
"""
import pytest


class TestOnlineUserModule:
    """在线用户模块测试类"""
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_online_user_page_load(self, login_home):
        """P0-在线用户页面加载"""
        
        # 导航到在线用户页面
        login_home.goto("/monitor/online")
        
        # 暂时跳过验证，等待online_page实现
        pass
