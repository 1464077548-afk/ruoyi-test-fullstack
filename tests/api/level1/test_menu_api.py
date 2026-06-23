"""L1: 菜单接口单接口测试"""
import pytest
from api.clients.menu_client import MenuClient
from common.utils.data_factory import DataFactory


class TestMenuApi:
    """菜单API测试类"""
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_menu_list(self, menu_client):
        """P0-获取菜单列表"""
        response = menu_client.get_menu_list()
        assert response.get("code") == 200
        assert isinstance(response.get("data"), list)
        
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_menu_tree(self, menu_client):
        """P0-获取菜单树"""
        response = menu_client.get_menu_tree()
        assert response.get("code") == 200
        assert isinstance(response.get("data"), list)
        
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_user_menu_list(self, menu_client):
        """P0-获取用户菜单列表"""
        response = menu_client.get_user_menu_list()
        assert response.get("code") == 200
        assert isinstance(response.get("data"), list)
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_menu_by_id(self, menu_client):
        """P0-根据ID获取菜单"""
        # 先获取菜单列表，选择第一个菜单的ID
        menu_list = menu_client.get_menu_list()
        assert menu_list.get("code") == 200
        menus = menu_list.get("data", [])
        assert len(menus) > 0
        
        menu_id = menus[0].get("menuId")
        assert menu_id
        
        # 根据ID获取菜单
        response = menu_client.get_menu_by_id(menu_id)
        assert response.get("code") == 200
        assert response.get("data", {}).get("menuId") == menu_id
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_get_role_menu_tree(self, menu_client, created_role):
        """P1-获取角色菜单树"""
        role_id = created_role.get("roleId")
        response = menu_client.get_role_menu_tree(role_id)
        assert response.get("code") == 200
        assert "checkedKeys" in response
        assert isinstance(response.get("checkedKeys"), list)
