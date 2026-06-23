import pytest
from ui.pages.modules.user_page import UserPage
from ui.biz.common_biz import CommonBiz
from ui.biz.normal.user_biz import UserBiz

@pytest.mark.ui
@pytest.mark.explore
class TestBoundaryExplore:
    """边界值/特殊字符探索测试"""

    def test_user_name_special_char(self, login_home, user_biz, test_user_data):
        """用户名输入特殊字符 → 系统正常处理"""
        import random
        import string
        user_biz = UserBiz(login_home)
        CommonBiz(login_home).switch_menu("系统管理/用户管理")
        # 生成随机后缀，确保用户名唯一
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        test_user_data['userName'] = f")_+-=[]|，。、；：？！{random_suffix}"
        test_user_data['nickName'] = f"test@#$%^&*()_+-=[]|，。、；：？！{random_suffix}"
        message = user_biz.add_user(test_user_data)
        assert "成功" in message, f"添加用户失败: {message}"

        #删除用户
        message = user_biz.delete_user(test_user_data['userName'])
        assert "成功" in message, f"删除用户失败: {message}"

    def test_long_text_nickname(self, login_home, user_biz,test_user_data):
        """超长文本昵称 → 前端截断/正常提交"""
        user_biz = UserBiz(login_home)
        CommonBiz(login_home).switch_menu("系统管理/用户管理")
        test_user_data['nickName'] = "a" * 200  # 超长文本
        umessage = user_biz.add_user(test_user_data)
        assert "成功" in umessage, f"添加用户失败: {umessage}"

        #delete user
        message = user_biz.delete_user(test_user_data['userName'])
        assert "成功" in message, f"删除用户失败: {message}"
        
