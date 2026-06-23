"""L3: 数据流程接口业务流测试"""
import pytest
from api.clients.user_client import UserClient
from api.clients.role_client import RoleClient
from common.utils.data_factory import DataFactory


class TestDataFlow:
    """数据流程测试类"""
    
    @pytest.mark.api
    @pytest.mark.l3
    @pytest.mark.e2e
    @pytest.mark.p0
    def test_data_consistency_flow(self, user_client, role_client,test_role_data,test_user_data):
        """P0-数据一致性流程"""
        # 1. 准备测试数据
        role_data = test_role_data.copy()
        user_data = test_user_data.copy()
        
        role_id = None
        user_id = None
        
        try:
            # 2. 创建角色
            role_response = role_client.create_role(role_data)
            assert role_response.get("code") == 200
            
            # 3. 查询角色列表获取roleId
            role_list_response = role_client.get_role_list(roleName=role_data.get("roleName"))
            assert role_list_response.get("code") == 200
            assert len(role_list_response.get("rows", [])) > 0
            role_id = role_list_response.get("rows")[0].get("roleId")
            assert role_id
            
            # 4. 验证角色数据一致性
            role_detail = role_client.get_role_by_id(role_id)
            assert role_detail.get("code") == 200, "获取角色详情失败"
            assert role_detail.get("data", {}).get("roleName") == role_data["roleName"]
            assert role_detail.get("data", {}).get("roleKey") == role_data["roleKey"]
            
            # 5. 创建用户
            user_data["roleIds"] = [role_id]
            create_response = user_client.create_user(user_data)
            assert create_response.get("code") == 200
            
            # 6. 查询用户列表获取userId
            user_list_response = user_client.get_user_list(userName=user_data.get("userName"))
            assert user_list_response.get("code") == 200
            assert len(user_list_response.get("rows", [])) > 0
            user_id = user_list_response.get("rows")[0].get("userId")
            assert user_id
            
            # 7. 验证用户数据一致性
            user_detail = user_client.get_user_by_id(user_id)
            assert user_detail.get("code") == 200, "获取用户详情失败"
            assert user_detail.get("data", {}).get("userName") == user_data["userName"]
            assert user_detail.get("data", {}).get("nickName") == user_data["nickName"]
            
            # 8. 测试用户列表数据一致性
            user_list = user_client.get_user_list(userName=user_data["userName"])
            assert user_list.get("code") == 200, "获取用户列表失败"
            assert len(user_list.get("rows", [])) > 0, "用户列表中未找到创建的用户"
            
            # 9. 测试角色列表数据一致性
            role_list = role_client.get_role_list(roleName=role_data["roleName"])
            assert role_list.get("code") == 200, "获取角色列表失败"
            assert len(role_list.get("rows", [])) > 0, "角色列表中未找到创建的角色"
            
        finally:
            # 清理资源
            if user_id:
                try:
                    user_client.delete_user(user_id)
                except:
                    pass
            if role_id:
                try:
                    role_client.delete_role(role_id)
                except:
                    pass
    
    @pytest.mark.api
    @pytest.mark.l3
    @pytest.mark.e2e
    @pytest.mark.p1
    def test_data_update_flow(self, user_client, role_client,test_role_data,test_user_data):
        """P1-数据更新流程"""
        # 1. 准备测试数据
        role_data = test_role_data.copy()
        user_data = test_user_data.copy()
        
        role_id = None
        user_id = None
        
        try:
            # 2. 创建角色
            role_response = role_client.create_role(role_data)
            assert role_response.get("code") == 200
            
            # 3. 查询角色列表获取roleId
            role_list_response = role_client.get_role_list(roleName=role_data.get("roleName"))
            assert role_list_response.get("code") == 200
            assert len(role_list_response.get("rows", [])) > 0
            role_id = role_list_response.get("rows")[0].get("roleId")
            assert role_id
            
            # 4. 创建用户
            user_data["roleIds"] = [role_id]
            create_response = user_client.create_user(user_data)
            assert create_response.get("code") == 200
            
            # 5. 查询用户列表获取userId
            user_list_response = user_client.get_user_list(userName=user_data.get("userName"))
            assert user_list_response.get("code") == 200
            assert len(user_list_response.get("rows", [])) > 0
            user_id = user_list_response.get("rows")[0].get("userId")
            assert user_id
            
            # 6. 更新角色信息
            updated_role_data = {
                "roleName": f"{role_data['roleName']}_updated",
                "roleKey": f"{role_data['roleKey']}_updated",
                "roleSort": role_data.get("roleSort"),
                "status": role_data.get("status"),
                "remark": f"Updated remark for {role_data['roleName']}"
            }
            update_role_response = role_client.update_role(role_id, updated_role_data)
            assert update_role_response.get("code") == 200
            
            # 7. 验证角色更新
            updated_role_detail = role_client.get_role_by_id(role_id)
            assert updated_role_detail.get("code") == 200
            assert updated_role_detail.get("data", {}).get("roleName") == updated_role_data["roleName"]
            
            # 8. 更新用户信息
            updated_user_data = {
                "userName": user_data.get("userName"),
                "nickName": f"{user_data['nickName']}_updated",
                "email": f"updated_{user_data['email']}"
            }
            update_user_response = user_client.update_user(user_id, updated_user_data)
            assert update_user_response.code == 200
            
            # 9. 验证用户更新
            updated_user_detail = user_client.get_user_by_id(user_id)
            assert updated_user_detail.get("code") == 200
            assert updated_user_detail.get("data", {}).get("nickName") == updated_user_data["nickName"]
            
        finally:
            # 清理资源
            if user_id:
                try:
                    user_client.delete_user(user_id)
                except:
                    pass
            if role_id:
                try:
                    role_client.delete_role(role_id)
                except:
                    pass
