"""L2: 菜单模块接口测试"""
import pytest
from api.clients.menu_client import MenuClient
from api.clients.role_client import RoleClient
from common.utils.data_factory import DataFactory


class TestMenuModule:
    """菜单模块测试类"""
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p0
    def test_menu_crud_flow(self, menu_client):
        """P0-菜单完整CRUD流程"""
        # 1. 获取菜单列表
        menu_list_response = menu_client.get_menu_list()
        assert menu_list_response.get("code") == 200
        menus = menu_list_response.get("data", [])
        assert len(menus) > 0
        
        # 2. 获取菜单树
        menu_tree_response = menu_client.get_menu_tree()
        assert menu_tree_response.get("code") == 200
        assert isinstance(menu_tree_response.get("data"), list)
        
        # 3. 获取用户菜单列表
        user_menu_response = menu_client.get_user_menu_list()
        assert user_menu_response.get("code") == 200
        assert isinstance(user_menu_response.get("data"), list)
        
        # 4. 根据ID获取菜单
        menu_id = menus[0].get("menuId")
        assert menu_id
        menu_detail_response = menu_client.get_menu_by_id(menu_id)
        assert menu_detail_response.get("code") == 200
        assert menu_detail_response.get("data", {}).get("menuId") == menu_id
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p0
    def test_role_menu_tree(self, menu_client, role_client,test_role_data):
        """P0-角色菜单树测试"""
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
            # 3. 获取角色菜单树
            role_menu_tree_response = menu_client.get_role_menu_tree(role_id)
            assert role_menu_tree_response.get("code") == 200
            assert "checkedKeys" in role_menu_tree_response
            assert isinstance(role_menu_tree_response.get("checkedKeys"), list)
            
        finally:
            # 清理
            if role_id:
                role_client.delete_role(role_id)
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p1
    def test_menu_hierarchy(self, menu_client):
        """P1-菜单层次结构测试"""
        # 1. 获取菜单树
        menu_tree_response = menu_client.get_menu_tree()
        assert menu_tree_response.get("code") == 200
        menu_tree = menu_tree_response.get("data", [])
        assert len(menu_tree) > 0
        
        # 2. 验证菜单层次结构
        def check_menu_hierarchy(menus):
            for menu in menus:
                assert "id" in menu
                assert "label" in menu
                if "children" in menu and menu["children"]:
                    check_menu_hierarchy(menu["children"])
        
        check_menu_hierarchy(menu_tree)
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p1
    def test_menu_access_control(self, menu_client):
        """P1-菜单访问控制测试"""
        # 1. 获取用户菜单列表
        user_menu_response = menu_client.get_user_menu_list()
        assert user_menu_response.get("code") == 200
        user_menus = user_menu_response.get("data", [])
        assert isinstance(user_menus, list)
        
        # 2. 验证用户菜单列表结构
        for menu in user_menus:
            assert "path" in menu
            assert "component" in menu
            if "meta" in menu:
                assert "title" in menu["meta"]