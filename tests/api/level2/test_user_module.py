"""L2: 用户模块接口测试"""
import pytest
from api.clients.user_client import UserClient
from api.clients.role_client import RoleClient
from common.utils.data_factory import DataFactory


class TestUserModule:
    """L2: 用户模块接口测试类"""
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p0
    def test_user_crud_flow(self, user_client, role_client,test_role_data,test_user_data):
        """P0-用户完整CRUD流程"""
        # 1. 创建测试角色
        role_response = role_client.create_role(test_role_data)
        assert role_response.get("code") == 200
        
        # 2. 查询角色列表获取roleId
        role_list_response = role_client.get_role_list(roleName=test_role_data.get("roleName"))
        assert role_list_response.get("code") == 200
        assert len(role_list_response.get("rows", [])) > 0
        role_id = role_list_response.get("rows")[0].get("roleId")
        assert role_id
        
        try:
            # 2. 创建用户
            test_user_data["roleIds"] = [role_id]
            create_response = user_client.create_user(test_user_data)
            assert create_response.get("code") == 200
            
            # 3. 查询用户列表获取userId
            user_list_response = user_client.get_user_list(userName=test_user_data.get("userName"))
            assert user_list_response.get("code") == 200
            assert len(user_list_response.get("rows", [])) > 0
            user_id = user_list_response.get("rows")[0].get("userId")
            assert user_id
            
            # 3. 查询用户列表
            list_response = user_client.get_user_list(userName=test_user_data.get("userName"))
            assert list_response.get("code") == 200
            assert len(list_response.get("rows", [])) > 0
            
            # 4. 更新用户
            update_data = {
                "userId": user_id,
                "userName": test_user_data["userName"],
                "nickName": f"{test_user_data['nickName']}_updated",
                "email": f"updated_{test_user_data['email']}"
            }
            update_response = user_client.update_user(user_id, update_data)
            assert update_response.code == 200
            
            # 5. 获取用户详情
            detail_response = user_client.get_user_by_id(user_id)
            assert detail_response.get("code") == 200
            assert detail_response.get("data", {}).get("nickName") == update_data["nickName"]
            
            # 6. 删除用户
            delete_response = user_client.delete_user(user_id)
            assert delete_response.get("code") == 200
            assert user_id not in list_response.get("data", {}).get("list", [])
            
        finally:
            # 清理角色
            if role_id:
                role_client.delete_role(role_id)
        
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p0
    def test_user_role_assignment(self, user_client, role_client,test_role_data,test_user_data):
        """P0-用户角色分配"""
        user_id = None
        role_id = None
        
        try:
            # 1. 创建测试角色
            role_response = role_client.create_role(test_role_data)
            assert role_response.get("code") == 200
            
            # 2. 查询角色列表获取roleId
            role_list_response = role_client.get_role_list(roleName=test_role_data.get("roleName"))
            assert role_list_response.get("code") == 200
            assert len(role_list_response.get("rows", [])) > 0
            role_id = role_list_response.get("rows")[0].get("roleId")
            assert role_id
            
            # 3. 创建用户
            create_response = user_client.create_user(test_user_data)
            assert create_response.get("code") == 200
            
            # 4. 查询用户列表获取userId
            user_list_response = user_client.get_user_list(userName=test_user_data.get("userName"))
            assert user_list_response.get("code") == 200
            assert len(user_list_response.get("rows", [])) > 0
            user_id = user_list_response.get("rows")[0].get("userId")
            assert user_id
            
            # 5. 分配角色
            assign_response = user_client.add_auth_role(user_id, [role_id])
            assert assign_response.code == 200
            
        finally:
            # 清理
            if user_id:
                user_client.delete_user(user_id)
            if role_id:
                role_client.delete_role(role_id)

    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p1
    def test_user_search_combinations(self, user_client):
        """P1-用户搜索组合条件"""
  
        # 测试各种搜索组合
        search_cases = [
            {'userName': 'admin'},
            {'phonenumber': '138'},
            {'userName': 'admin', 'phonenumber': '138'},
            {'status': '0'},
            {'deptId': 1},
        ]
        
        for params in search_cases:
            result = user_client.get_user_list(**params)
            assert result['code'] == 200
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p1
    def test_user_batch_operations(self, user_client, test_user_data):
        """P1-用户批量操作"""

        # 批量创建
        user_ids = []
        for i in range(3):
            data = test_user_data.copy()
            data['nickName'] = f"{data['nickName']}_{i}"
            data['userName'] = f"{data['userName']}_{i}"  # Unique username
            data['phonenumber'] = f"{data['phonenumber'][:-1]}{i}"  # Unique phone number
            data['email'] = f"{data['email'].split('@')[0]}_{i}@{data['email'].split('@')[1]}"  # Unique email
            result = user_client.create_user(data)
            assert result.get('code') == 200
            
            # 查询用户列表获取userId
            user_list_response = user_client.get_user_list(userName=data.get('userName'))
            assert user_list_response.get('code') == 200
            assert len(user_list_response.get('rows', [])) > 0
            user_id = user_list_response.get('rows')[0].get('userId')
            user_ids.append(user_id)
        
        # 批量删除
        result = user_client.batch_delete_users(user_ids)
        assert result.get('code') == 200
