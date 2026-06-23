"""L2: 角色模块接口测试"""
import pytest
from api.clients.role_client import RoleClient
from api.clients.menu_client import MenuClient
from common.utils.data_factory import DataFactory


class TestRoleModule:
    """角色模块测试类"""
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p0
    def test_role_crud_flow(self, role_client,test_role_data):
        """P0-角色完整CRUD流程"""
        # 1. 创建角色
        create_response = role_client.create_role(test_role_data)
        assert create_response.get("code") == 200
        
        # 2. 查询角色列表获取roleId
        role_list_response = role_client.get_role_list(roleName=test_role_data.get("roleName"))
        assert role_list_response.get("code") == 200
        assert len(role_list_response.get("rows", [])) > 0
        role_id = role_list_response.get("rows")[0].get("roleId")
        assert role_id
        
        try:
            # 3. 查询角色列表
            list_response = role_client.get_role_list(roleName=test_role_data.get("roleName"))
            assert list_response.get("code") == 200
            assert len(list_response.get("rows", [])) > 0
            
            # 4. 更新角色
            update_data = {
                "roleName": f"{test_role_data['roleName']}_updated",
                "roleKey": test_role_data.get("roleKey"),
                "roleSort": test_role_data.get("roleSort"),
                "status": test_role_data.get("status"),
                "remark": f"Updated remark for {test_role_data['roleName']}"
            }
            update_response = role_client.update_role(role_id, update_data)
            assert update_response.get("code") == 200
            
            # 5. 获取角色详情
            detail_response = role_client.get_role_by_id(role_id)
            assert detail_response.get("code") == 200
            assert detail_response.get("data", {}).get("roleName") == update_data["roleName"]
            
            # 6. 删除角色
            delete_response = role_client.delete_role(role_id)
            assert delete_response.get("code") == 200
            
            # 7. 验证角色已被删除
            role_list_response = role_client.get_role_list(roleName=update_data["roleName"])
            assert role_list_response.get("code") == 200
            assert role_list_response.get("total") == 0
            
        finally:
            # 清理
            if role_id:
                try:
                    role_client.delete_role(role_id)
                except:
                    pass
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p0
    def test_role_menu_assignment(self, role_client, menu_client,test_role_data):
        """P0-角色菜单分配"""
        # 1. 创建角色
        create_response = role_client.create_role(test_role_data)
        assert create_response.get("code") == 200
        
        # 2. 查询角色列表获取roleId
        role_list_response = role_client.get_role_list(roleName=test_role_data.get("roleName"))
        assert role_list_response.get("code") == 200
        assert len(role_list_response.get("rows", [])) > 0
        role_id = role_list_response.get("rows")[0].get("roleId")
        assert role_id
        
        try:
            # 3. 获取菜单列表
            menu_response = menu_client.get_menu_list()
            assert menu_response.get("code") == 200
            menus = menu_response.get("data", [])
            assert len(menus) > 0
            
            # 4. 提取菜单ID
            menu_ids = [menu.get("menuId") for menu in menus if menu.get("menuId")]
            assert len(menu_ids) > 0
            
            # 5. 分配菜单权限
            assign_response = role_client.assign_menus(role_id, menu_ids[:3])  # 只分配前3个菜单
            assert assign_response.get("code") == 200
            
            # 6. 验证菜单权限
            menu_perm_response = role_client.get_role_menus(role_id)
            assert menu_perm_response.get("code") == 200
            
        finally:
            # 清理
            if role_id:
                role_client.delete_role(role_id)
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p1
    def test_role_batch_operations(self, role_client,test_role_data):
        """P1-角色批量操作"""
        # 批量创建
        role_ids = []
        for i in range(3):
            role_data = test_role_data.copy()
            role_data['roleName'] = f"{test_role_data['roleName']}_{i}"
            role_data['roleKey'] = f"{test_role_data['roleKey']}_{i}"
            create_response = role_client.create_role(role_data)
            assert create_response.get("code") == 200
            
            # 查询角色列表获取roleId
            role_list_response = role_client.get_role_list(roleName=role_data.get("roleName"))
            assert role_list_response.get("code") == 200
            assert len(role_list_response.get("rows", [])) > 0
            role_id = role_list_response.get("rows")[0].get("roleId")
            role_ids.append(role_id)
        
        # 批量删除
        delete_response = role_client.batch_delete_roles(role_ids)
        assert delete_response.get("code") == 200
