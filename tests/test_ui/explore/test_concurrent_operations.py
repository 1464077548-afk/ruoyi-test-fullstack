import pytest
import time
from config.settings import Settings
from ui.biz.normal.login_biz import LoginBiz
from ui.biz.normal.user_biz import UserBiz


@pytest.mark.ui
@pytest.mark.exploratory
class TestConcurrentOperations:
    """并发操作测试"""


    def test_multi_tab_operate_same_user(self, login_home, concurrency_biz):
        """多标签页操作同一条数据 → 数据一致"""
        concurrency_biz.multi_tab_operate_same_data(login_home, "/system/user", "admin")

    def test_same_user_multi_login(self, concurrency_biz):
        """同账号多端登录 → 支持多点登录"""
        ctx_pages = concurrency_biz.same_user_multi_login("admin", "admin123", 2)
        for ctx, page in ctx_pages:
            assert "若依管理系统"  in page.title()
            ctx.close()
            
    @pytest.mark.parametrize("test_user_data_batch", [3], indirect=True)
    def test_multi_user_concurrent_login(self, login_home, concurrency_biz, test_user_data_batch,user_client):
        """多用户并发登录 → 会话隔离"""
        user_biz = UserBiz(login_home)
        # 1.先创建多个用户
        user_list = test_user_data_batch
        # 准备并发登录的用户列表 (username, password) 元组
        login_list = []
        for user in user_list:
            message = user_biz.add_user(user)
            assert "成功" in message, f"创建用户{user}失败"
            # 添加到登录列表
            login_list.append((user['userName'], user['password']))
        # 2.创建LoginBiz对象并退出登录
        login_biz = LoginBiz(login_home.page)
        login_biz.logout()
        # 3.并发登录
        ctx_pages = concurrency_biz.multi_user_concurrent_login(login_list)
        for ctx, page in ctx_pages:
            assert "若依管理系统" in page.title()
            ctx.close()
        #清理数据
        for user in user_list:
            user_list_response = user_client.get_user_list(userName=user.get("userName"))
            assert user_list_response.get("code") == 200
            user_id = user_list_response.get("rows")[0].get("userId")
            result = user_client.delete_user(user_id)
            assert result.get("code") == 200

    def test_rapid_logins(self, page):
        """测试快速连续登录操作"""
        settings = Settings()
        login_biz = LoginBiz(page)
         
        # 快速连续登录尝试
        for i in range(3):
            try:
                login_biz.login(settings.USERNAME, settings.PASSWORD)
                print(f"✅第{i+1}次登录尝试成功")
            except Exception as e:
                print(f"⚠️第{i+1}次登录尝试失败: {e}")
            time.sleep(1)  # 稍微错开时间
        
        # 验证系统能够处理快速连续操作
        result = login_biz.is_logged_in()
        assert "成功" in result, "登录失败"
        print("✅系统能够处理快速连续登录操作")
