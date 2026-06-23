"""端到端集成测试"""
from math import fabs
import pytest
from ui.pages.modules.login_page import LoginPage
from ui.pages.modules.home_page import HomePage
from ui.pages.modules.user_page import UserPage
from api.clients.user_client import UserClient
from config.settings import Settings
from common.utils.data_factory import DataFactory


class TestEndToEnd:
    """端到端集成测试类"""
    
    def test_complete_user_management_flow(self, user_biz, user_client):
        """测试完整的用户管理流程"""
        settings = Settings()
        test_user_data = DataFactory.generate_user_data()
        
        try:
            # 1. UI创建用户
            user_biz.add_user(test_user_data)
            
            # 2. API验证用户创建,查询用户列表获取userId
            user_list_response = user_client.get_user_list(userName=test_user_data["userName"])
            assert user_list_response.get("code") == 200, f"API未找到创建的用户{test_user_data['userName']}"
            assert len(user_list_response.get("rows", [])) > 0
            user_id = user_list_response.get("rows")[0].get("userId")
            assert user_id,"用户ID不存在"

            # 5. UI搜索用户
            user_biz.search_user(test_user_data["userName"])
            ui_user_list = user_biz.get_user_list()
            assert test_user_data["userName"] in ui_user_list, "UI未找到创建的用户"
            
            # 6. API删除用户
            delete_response = user_client.delete_user(user_id)
            assert delete_response.get("code") == 200, "API删除用户失败"
            
        except Exception as e:
            # 清理
            if 'user_id' in locals():
                try:
                    user_client.delete_user(user_id)
                except:
                    pass
            raise e
