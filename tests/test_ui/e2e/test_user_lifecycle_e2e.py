"""
L3: 用户生命周期端到端测试
验证从创建到删除的完整用户管理流程
"""
from email import message
from logging import info
from struct import pack
import pytest
import time
from config.settings import Settings

@pytest.mark.ui
@pytest.mark.e2e
class TestUserLifecycleFlow:
    """用户生命周期流程测试"""

    @pytest.mark.l3
    @pytest.mark.p0
    def test_complete_user_lifecycle(self, common_biz,user_biz,role_biz,test_user_data,test_role_data):
        """P0-完整用户生命周期流程"""
        #========== 步骤 1: 创建角色 ==========
        common_biz.switch_menu("系统管理/角色管理")
        print(f"💻开始创建角色: {test_role_data}")
        message = role_biz.add_role(test_role_data)
        assert "成功" in message
        
        # ========== 步骤 2: 创建用户 ==========
        common_biz.switch_menu("系统管理/用户管理")
        print(f"💻开始创建用户: {test_user_data}")
        message = user_biz.add_user(test_user_data)
        assert "成功" in message
        
        # ========== 步骤 3: 验证用户信息 ==========
        print(f"🔍开始验证用户信息: {test_user_data['userName']}")
        user_info = user_biz.get_user_info(test_user_data['userName'])
        assert user_info is not None
        assert test_user_data['userName'] == user_info['userName']
        assert test_user_data['nickName'] == user_info['nickName']
        assert test_user_data['phonenumber'] == user_info['phonenumber']
   
  
        # ========== 步骤 4: 编辑用户 ==========
        print(f"📝开始编辑用户: {test_user_data['userName']}")
        new_nickname = f'已编辑_{test_user_data["nickName"]}'
        message = user_biz.edit_user_nickname(test_user_data['userName'], new_nickname)
        assert "成功" in message
        
        # 验证编辑结果
        print(f"🔍开始验证编辑后的用户信息: {test_user_data['userName']}")
        user_info = user_biz.get_user_info(test_user_data['userName'])
        assert user_info is not None
        assert new_nickname == user_info['nickName']
      
        
        # ========== 步骤 5: 分配角色 ==========
        print(f"🔑开始给用户: {test_user_data['userName']} 分配角色: {test_role_data['roleName']}")
        message = user_biz.assign_roles_for_user(test_user_data['userName'], [test_role_data['roleName']])
        assert "成功" in message
        
        # ========== 步骤 5: 禁用用户 ==========
        print(f"🔒开始禁用用户: {test_user_data['userName']}")
        message = user_biz.switch_user_status(test_user_data['userName'], status="0")
        assert "成功" in message
        user_info = user_biz.get_user_info(test_user_data['userName'])
        assert user_info is not None
        assert user_info['status'] == "0"
        
        # ========== 步骤 6: 启用用户 ==========
        print(f"🔓开始启用用户: {test_user_data['userName']}")
        message = user_biz.switch_user_status(test_user_data['userName'], status="1")
        assert "成功" in message
        user_info = user_biz.get_user_info(test_user_data['userName'])
        assert user_info is not None
        assert user_info['status'] == "1"
        
        # ========== 步骤 7: 重置密码 ==========
        print(f"🔑开始重置密码: {test_user_data['userName']}")
        new_password = 'New@123456'
        message = user_biz.reset_password(test_user_data['userName'], new_password)
        assert "成功" in message
        
        # ========== 步骤 8: 搜索用户 ==========
        print(f"🔍开始搜索用户: {test_user_data['userName']}")
        new_user_info = user_biz.get_user_info(test_user_data['userName'])
        assert new_user_info is not None
        assert new_user_info['nickName'] == new_nickname
        
        # ========== 步骤 9: 重置搜索 ==========
        print(f"🔍开始重置搜索: {test_user_data['userName']}")
        common_biz.reset_search(user_biz.user_page)
        #TODO: 验证搜索结果包含所有用户
        
        # ========== 步骤 10: 删除用户 ==========
        print(f"🗑开始删除用户: {test_user_data['userName']}")
        message = user_biz.delete_user(test_user_data['userName'])
        assert "成功" in message
        user_info = user_biz.get_user_info(test_user_data['userName'])
        assert user_info is None
        
        # ========== 步骤 11: 删除角色 ==========
        common_biz.switch_menu("系统管理/角色管理")
        print(f"🗑开始删除角色: {test_role_data['roleName']}")
        message = role_biz.delete_role(test_role_data['roleName'])
        assert "成功" in message
        
    @pytest.mark.l3
    @pytest.mark.p0
    def test_user_registration_to_login_flow(self, page,user_biz,login_biz,test_user_data):
        """P0-创建用户->登录用户流程"""
        
        # 步骤 1: 创建用户        
        print(f"💻开始创建用户: {test_user_data}")
        message = user_biz.add_user(test_user_data)
        assert "成功" in message
        
        # 步骤 2: 退出管理员登录
        login_biz.logout()

        # 步骤 3: 使用创建的用户登录
        print(f"开始使用新用户登录: {test_user_data['userName']}")
        login_result = login_biz.login(test_user_data['userName'], test_user_data['password'])
        print(f"新用户登录结果: {login_result}")
        
        # 步骤 4: 退出登录
        login_biz.logout()
        print("✅ 新用户登出成功")