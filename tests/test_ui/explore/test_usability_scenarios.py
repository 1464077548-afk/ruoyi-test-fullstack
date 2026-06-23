"""
L4: 可用性探索式测试
验证系统的用户体验（键盘导航、响应式设计、无障碍测试）
"""
import pytest
from config.settings import Settings
from ui.biz.special.test_usability_biz import UsabilityBiz
from ui.biz.normal.user_biz import UserBiz
from ui.biz.common_biz import CommonBiz


class TestUsabilityScenarios:
    """可用性场景测试"""
    
    @pytest.mark.ui
    @pytest.mark.l4
    @pytest.mark.exploratory
    @pytest.mark.usability
    def test_keyboard_navigation(self, page):
        """可用性测试 - 键盘导航"""
        settings = Settings()
        page.goto(settings.BASE_URL + "/login")
        usability_biz = UsabilityBiz(page)
        result = usability_biz.test_keyboard_navigation()
        assert "成功" in result      
        # 验证可以通过键盘完成操作
        print("✅键盘导航测试通过")
    
    @pytest.mark.ui
    @pytest.mark.l4
    @pytest.mark.exploratory
    @pytest.mark.usability
    def test_responsive_design(self, page, login_home):
        """可用性测试 - 响应式设计"""
        usability_biz = UsabilityBiz(page)
        result = usability_biz.test_responsive_design()
        assert result == True      
        print("✅响应式设计测试通过")
    @pytest.mark.ui
    @pytest.mark.l4
    @pytest.mark.exploratory
    @pytest.mark.usability
    def test_loading_states(self, page, login_home):
        """可用性测试 - 加载状态"""
        user_biz = UserBiz(login_home)
        # 导航到用户管理页面
        CommonBiz(login_home).switch_menu("系统管理/用户管理")
        # 触发加载     
        result = user_biz.search_user("admin")
        
        assert result >= 0, "搜索用户失败"
        
        # 验证页面未崩溃
        assert page.is_visible("body"), "页面在加载过程中崩溃"
        print("✅加载状态测试通过")

    
    @pytest.mark.ui
    @pytest.mark.l4
    @pytest.mark.exploratory
    @pytest.mark.accessibility
    def test_accessibility(self, page, login_home):
        """可用性测试 - 无障碍访问"""
        usability_biz = UsabilityBiz(login_home)
        result = usability_biz.test_accessibility()
        assert result == True, "无障碍访问测试失败"
        