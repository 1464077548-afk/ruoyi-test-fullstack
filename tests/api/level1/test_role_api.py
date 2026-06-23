"""角色API测试"""
import pytest
from api.clients.role_client import RoleClient


class TestRoleApi:
    """角色API测试类"""
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_role_list(self, role_client):
        """p0-获取角色列表"""
        response = role_client.get_role_list()
        assert response.get("code") == 200
        assert len(response.get("rows", [])) > 0
        assert response.get("total") > 0

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_create_role(self, role_client, test_role_data):
        """p0-创建角色"""
        response = role_client.create_role(test_role_data)
        assert response.get("code") == 200
        
        # 通过角色名查询获取角色ID
        role_list_response = role_client.get_role_list(roleName=test_role_data.get("roleName"))
        assert role_list_response.get("code") == 200
        assert len(role_list_response.get("rows", [])) == 1
        role_id = role_list_response.get("rows")[0].get("roleId")
        assert role_id
        
        # 清理
        role_client.delete_role(role_id)

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_update_role(self, role_client, created_role):
        """p0-更新角色"""
        import time
        role_id = created_role.get("roleId")
        # 使用唯一的角色名称，避免冲突
        unique_id = str(int(time.time() * 1000))
        updated_data = {
            "roleName": f"测试角色_更新_{unique_id}",
            "roleKey": created_role.get('roleKey'),
            "roleSort": created_role.get('roleSort'),
            "status": created_role.get('status'),
            "remark": "更新后的角色备注"
        }
        response = role_client.update_role(role_id, updated_data)
        assert response.get("code") == 200
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_delete_role(self, role_client, test_role_data):
        """p0-删除角色"""
        # 创建角色
        create_response = role_client.create_role(test_role_data)
        assert create_response.get("code") == 200
        
        # 通过角色名查询获取角色ID
        role_list_response = role_client.get_role_list(roleName=test_role_data.get("roleName"))
        assert role_list_response.get("code") == 200
        assert len(role_list_response.get("rows", [])) == 1
        role_id = role_list_response.get("rows")[0].get("roleId")
        assert role_id
        
        # 删除角色
        delete_response = role_client.delete_role(role_id)
        assert delete_response.get("code") == 200
        
        # 验证角色已被删除
        role_list_response = role_client.get_role_list(roleName=test_role_data.get("roleName"))
        assert role_list_response.get("code") == 200
        assert len(role_list_response.get("rows", [])) == 0
        assert role_list_response.get("total") == 0
        
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_role_by_id(self, role_client, created_role):
        """p0-根据ID获取角色"""
        role_id = created_role.get("roleId")
        response = role_client.get_role_by_id(role_id)
        assert response.get("code") == 200
        assert response.get("data", {}).get("roleId") == role_id
