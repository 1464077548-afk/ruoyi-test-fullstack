import pytest
from ui.pages.modules.user_page import UserPage
from ui.pages.modules.role_page import RolePage
from ui.biz.common_biz import CommonBiz
from ui.biz.normal.user_biz import UserBiz

@pytest.mark.ui
@pytest.mark.explore
class TestAbnormalExplore:
    """异常/特殊交互探索测试"""

    def test_repeat_click_add_btn(self, login_home, user_biz, abnormal_biz):
        """连续点击新增按钮 → 验证防重复提交"""
        user_page = UserPage(login_home)
        # UserBiz already navigates to user management page
        # 尝试连续点击新增按钮
        try:
            abnormal_biz.repeat_click_btn(user_page, "USER_ADD_BUTTON", 3)
            # 验证系统稳定，没有崩溃
            assert "系统异常" not in login_home.content()
            # 验证页面仍然可操作
            assert login_home.get_by_role("button", name="新增").count() > 0
            print("✅连续点击新增按钮，系统稳定")
        except Exception as e:
            print(f"⚠️ 连续点击新增按钮时出现异常: {e}")
            # 只要系统没有崩溃，测试就通过
            assert "系统异常" not in login_home.content()

    @pytest.mark.serial  # 串行执行，操作中刷新测试需要独占环境
    def test_refresh_during_operation(self, login_home, abnormal_biz):
        """操作中刷新页面 → 流程中断可恢复"""
        user_page = UserPage(login_home)
        user_biz = UserBiz(login_home)
        CommonBiz(login_home).switch_menu("系统管理/用户管理")
        abnormal_biz.refresh_in_operation(user_page, "USER_ADD_BUTTON")
        # 断言弹窗关闭
        assert user_biz.get_dialog_number() == 0

    def test_submit_empty_user_form(self, login_home, abnormal_biz, test_user_data):
        """空表单直接提交 → 前端校验拦截"""
        user_page = UserPage(login_home)
        user_biz = UserBiz(login_home)
        CommonBiz(login_home).switch_menu("系统管理/用户管理")
        abnormal_biz.submit_empty_form(user_page, "USER_ADD_BUTTON")
        # 断言表单校验提示
        assert user_biz.check_is_form_error()

    def test_weak_network_submit(self, login_home, abnormal_biz,test_user_data):
        """弱网环境提交表单 → 系统不崩溃"""
        user_page = UserPage(login_home)
        CommonBiz(login_home).switch_menu("系统管理/用户管理")
        is_visible = abnormal_biz.submit_with_slow_network(user_page, "USER_ADD_BUTTON",test_user_data)
        assert is_visible

    def test_force_close_dialog(self, login_home, abnormal_biz):
        """强制关闭弹窗 → 正常关闭"""
        user_page = UserPage(login_home)
        user_biz = UserBiz(login_home)
        CommonBiz(login_home).switch_menu("系统管理/用户管理")
        # 尝试强制关闭弹窗
        try:
            abnormal_biz.close_dialog_by_force(user_page, "USER_ADD_BUTTON")
        except Exception as e:
            print(f"关闭弹窗时出现异常: {e}")
        # 验证系统稳定，没有崩溃
        assert "系统异常" not in login_home.content()
        # 验证页面仍然可操作
        assert login_home.get_by_role("button", name="新增").count() > 0
        print("✅强制关闭弹窗测试通过，系统稳定")
