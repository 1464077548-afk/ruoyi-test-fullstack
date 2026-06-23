"""L3: 权限流程接口业务流测试"""
import pytest
from api.clients.role_client import RoleClient
from api.clients.menu_client import MenuClient
from api.clients.user_client import UserClient
from common.utils.data_factory import DataFactory


class TestPermissionFlow:
    """权限流程测试类"""
    
    @pytest.mark.api
    @pytest.mark.l3
    @pytest.mark.e2e
    @pytest.mark.p0
    def test_role_permission_assignment_flow(self, role_client, menu_client, user_client,test_role_data,test_user_data):
        """P0-角色权限分配流程"""
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
            
            # 4. 获取菜单列表
            menu_response = menu_client.get_menu_list()
            assert menu_response.get("code") == 200
            menus = menu_response.get("data", [])
            assert len(menus) > 0, "菜单列表为空"
            
            # 5. 提取菜单ID
            menu_ids = [menu.get("menuId") for menu in menus if menu.get("menuId")]
            assert len(menu_ids) > 0, "没有可用的菜单ID"
            
            # 6. 分配菜单权限给角色
            assign_response = role_client.assign_menus(role_id, menu_ids[:5])  # 分配前5个菜单
            assert assign_response.get("code") == 200, "菜单权限分配失败"
            
            # 7. 验证角色菜单权限
            role_menus_response = role_client.get_role_menus(role_id)
            assert role_menus_response.get("code") == 200, "获取角色菜单权限失败"
            
            # 8. 创建用户并分配角色
            user_data["roleIds"] = [role_id]
            create_response = user_client.create_user(user_data)
            assert create_response.get("code") == 200
            
            # 9. 查询用户列表获取userId
            user_list_response = user_client.get_user_list(userName=user_data.get("userName"))
            assert user_list_response.get("code") == 200
            assert len(user_list_response.get("rows", [])) > 0
            user_id = user_list_response.get("rows")[0].get("userId")
            assert user_id
            
            # 10. 验证用户角色分配
            user_detail = user_client.get_user_by_id(user_id)
            assert user_detail.get("code") == 200, "获取用户详情失败"
            
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
    def test_user_role_assignment_flow(self, user_client, role_client,test_role_data,test_user_data):
        """P1-用户角色分配流程"""
        # 1. 准备测试数据
        role_data1 = test_role_data.copy()
        role_data2 = DataFactory.generate_role_data()
        
        role_id1 = None
        role_id2 = None
        user_id = None
        
        try:
            # 2. 创建第一个角色
            role_response1 = role_client.create_role(role_data1)
            assert role_response1.get("code") == 200
            
            # 3. 查询角色列表获取roleId1
            role_list_response1 = role_client.get_role_list(roleName=role_data1.get("roleName"))
            assert role_list_response1.get("code") == 200
            assert len(role_list_response1.get("rows", [])) > 0
            role_id1 = role_list_response1.get("rows")[0].get("roleId")
            assert role_id1
            
            # 4. 创建第二个角色
            role_response2 = role_client.create_role(role_data2)
            assert role_response2.get("code") == 200
            
            # 5. 查询角色列表获取roleId2
            role_list_response2 = role_client.get_role_list(roleName=role_data2.get("roleName"))
            assert role_list_response2.get("code") == 200
            assert len(role_list_response2.get("rows", [])) > 0
            role_id2 = role_list_response2.get("rows")[0].get("roleId")
            assert role_id2
            
            # 6. 创建用户并分配第一个角色
            test_user_data["roleIds"] = [role_id1]
            create_response = user_client.create_user(test_user_data)
            assert create_response.get("code") == 200
            
            # 7. 查询用户列表获取userId
            user_list_response = user_client.get_user_list(userName=test_user_data.get("userName"))
            assert user_list_response.get("code") == 200
            assert len(user_list_response.get("rows", [])) > 0
            user_id = user_list_response.get("rows")[0].get("userId")
            assert user_id
            
            # 8. 为用户分配第二个角色
            assign_response = user_client.add_auth_role(user_id, [role_id2])
            assert assign_response.code == 200
            
        finally:
            # 清理资源
            if user_id:
                try:
                    user_client.delete_user(user_id)
                except:
                    pass
            if role_id1:
                try:
                    role_client.delete_role(role_id1)
                except:
                    pass
            if role_id2:
                try:
                    role_client.delete_role(role_id2)
                except:
                    pass
