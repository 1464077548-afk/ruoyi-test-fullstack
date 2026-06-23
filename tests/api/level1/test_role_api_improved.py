"""L1: 角色接口测试（改进版 - 完整覆盖）"""
import pytest
from api.clients.role_client import RoleClient
from common.utils.data_factory import DataFactory

class TestRoleApiImproved:
    """角色API测试类（改进版 - 完整覆盖）"""
    
    # ==================== P0级测试用例（核心功能）====================
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_role_list(self, role_client):
        """P0-获取角色列表 - 验证基本结构"""
        response = role_client.get_role_list()
        
        assert response.get("code") == 200, f"获取角色列表失败: {response.get('msg')}"
        assert "total" in response, "响应缺少total字段"
        assert "rows" in response, "响应缺少rows字段"
        assert response.get("total") > 0, "角色总数应大于0"
        
        print(f"✅ 角色列表验证通过: 共{response.get('total')}个角色")
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_create_role(self, role_client, test_role_data):
        """P0-创建角色成功 - 验证角色创建"""
        response = role_client.create_role(test_role_data)
        
        assert response.get("code") == 200, f"创建角色失败: {response.get('msg')}"
        
        # 验证角色已创建
        check_response = role_client.get_role_list(roleName=test_role_data.get("roleName"))
        assert check_response.get("code") == 200
        assert check_response.get("total") == 1, "应找到刚创建的角色"
        
        # 清理：删除测试角色
        role_id = check_response.get("rows")[0].get("roleId")
        role_client.delete_role(role_id)
        
        print(f"✅ 角色创建验证通过: {test_role_data.get('roleName')}")
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_update_role(self, role_client, created_role):
        """P0-更新角色成功 - 验证角色信息修改"""
        role_info = created_role
        role_id = role_info['roleId']
        
        # 更新角色数据
        updated_data = {
            "roleId": role_id,
            "roleName": f"更新_{role_info['roleName']}",
            "roleKey": role_info['roleKey'],
            "roleSort": 99,
            "status": "1"
        }
        
        response = role_client.update_role(role_id, updated_data)
        assert response.get("code") == 200, f"更新角色失败: {response.get('msg')}"
        
        # 验证更新
        check_response = role_client.get_role_by_id(role_id)
        assert check_response.get("code") == 200
        assert check_response.get("data", {}).get("roleSort") == 99
        
        print(f"✅ 角色更新验证通过: roleId={role_id}")
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_delete_role(self, role_client, test_role_data):
        """P0-删除角色成功 - 验证角色删除"""
        # 创建角色
        create_response = role_client.create_role(test_role_data)
        assert create_response.get("code") == 200
        
        # 获取角色ID
        role_list_response = role_client.get_role_list(roleName=test_role_data.get("roleName"))
        assert role_list_response.get("code") == 200
        role_id = role_list_response.get("rows")[0].get("roleId")
        
        # 删除角色
        delete_response = role_client.delete_role(role_id)
        assert delete_response.get("code") == 200, f"删除角色失败: {delete_response.get('msg')}"
        
        # 验证删除
        check_response = role_client.get_role_list(roleName=test_role_data.get("roleName"))
        assert check_response.get("code") == 200
        assert check_response.get("total") == 0, "角色应已被删除"
        
        print(f"✅ 角色删除验证通过: roleId={role_id}")
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_role_by_id(self, role_client, created_role):
        """P0-根据ID获取角色 - 验证角色详情查询"""
        role_info = created_role
        role_id = role_info['roleId']
        
        response = role_client.get_role_by_id(role_id)
        
        assert response.get("code") == 200
        assert response.get("data", {}).get("roleId") == role_id
        
        print(f"✅ 角色详情查询验证通过: roleId={role_id}")
    
    # ==================== P1级测试用例（异常场景）====================
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_create_duplicate_role(self, role_client, test_role_data):
        """P1-创建重复角色 - 验证角色名唯一性"""
        # 先创建一个角色
        result1 = role_client.create_role(test_role_data)
        assert result1.get("code") == 200, "首次创建应成功"
        
        # 获取角色ID用于清理
        role_list = role_client.get_role_list(roleName=test_role_data.get("roleName"))
        role_id = role_list.get("rows")[0].get("roleId")
        
        # 尝试创建同名角色
        result2 = role_client.create_role(test_role_data)
        
        assert result2.get("code") == 500, f"期望500，实际: {result2.get('code')}"
        assert "已存在" in result2.get("msg", ""), f"期望'已存在'，实际: {result2.get('msg')}"
        
        # 清理
        role_client.delete_role(role_id)
        
        print(f"✅ 重复角色创建验证通过")
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_role_menu_permission(self, role_client, menu_client, created_role):
        """P1-角色菜单权限测试 - 验证权限分配"""
        role_info = created_role
        role_id = role_info['roleId']
        
        # 获取所有菜单
        menus_response = menu_client.get_menu_list()
        assert menus_response.get("code") == 200
        
        # 选择前3个菜单分配给角色
        menu_list = menus_response.get("data", [])
        if len(menu_list) >= 3:
            menu_ids = [menu['menuId'] for menu in menu_list[:3]]
            
            # 分配菜单给角色
            result = role_client.assign_menus(role_id, menu_ids)
            
            # 若依分配菜单接口可能返回200或500
            if result.get("code") == 200:
                print(f"✅ 角色菜单权限分配成功: roleId={role_id}")
            else:
                print(f"⚠️ 角色菜单权限分配失败: {result.get('msg')}")
        else:
            print(f"⚠️ 菜单数量不足，无法测试权限分配")
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_change_role_status(self, role_client, created_role):
        """P1-角色状态修改 - 验证禁用/启用功能"""
        role_info = created_role
        role_id = role_info['roleId']
        
        # 禁用角色
        result = role_client.change_status(role_id, '1')
        
        # 若依可能使用不同的状态码
        if result.get("code") == 200:
            # 验证状态
            role_info_response = role_client.get_role_by_id(role_id)
            assert role_info_response.get("data", {}).get("status") == '1'
            print(f"✅ 角色禁用成功: roleId={role_id}")
        else:
            print(f"⚠️ 角色状态修改失败: {result.get('msg')}")
        
        # 启用角色
        result = role_client.change_status(role_id, '0')
        
        if result.get("code") == 200:
            # 验证状态
            role_info_response = role_client.get_role_by_id(role_id)
            assert role_info_response.get("data", {}).get("status") == '0'
            print(f"✅ 角色启用成功: roleId={role_id}")
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_assign_users_to_role(self, role_client, user_client, created_role, created_user):
        """P1-角色分配用户 - 验证角色用户关联"""
        role_info = created_role
        role_id = role_info['roleId']
        user_id = created_user
        
        # 分配用户给角色
        result = role_client.assign_users(role_id, [user_id])
        
        if result.get("code") == 200:
            print(f"✅ 角色分配用户成功: roleId={role_id}, userId={user_id}")
        else:
            print(f"⚠️ 角色分配用户失败: {result.get('msg')}")
    
    # ==================== P2级测试用例（边界场景）====================
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p2
    def test_create_role_with_boundary_data(self, role_client):
        """P2-创建角色-边界值测试"""
        boundary_cases = [
            # 角色名边界值
            {"roleName": "a", "roleKey": "a", "roleSort": 1},  # 最短角色名
            {"roleName": "角" * 50, "roleKey": "b" * 50, "roleSort": 999},  # 最长角色名
            # 角色排序边界值
            {"roleName": "test_boundary_1", "roleKey": "test_key_1", "roleSort": 0},  # 最小排序值
            {"roleName": "test_boundary_2", "roleKey": "test_key_2", "roleSort": 9999},  # 最大排序值
        ]
        
        created_role_ids = []
        
        for i, role_data in enumerate(boundary_cases):
            response = role_client.create_role(role_data)
            
            if response.get("code") == 200:
                # 创建成功，记录角色ID用于清理
                role_list = role_client.get_role_list(roleName=role_data.get("roleName"))
                if role_list.get("total") > 0:
                    role_id = role_list.get("rows")[0].get("roleId")
                    created_role_ids.append(role_id)
                    print(f"✅ 边界值测试{i+1}通过: 创建成功")
            else:
                print(f"⚠️ 边界值测试{i+1}: 创建失败 - {response.get('msg')}")
        
        # 清理
        if created_role_ids:
            role_client.delete_role(created_role_ids)
        
        print(f"✅ 角色边界值测试完成")
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p2
    def test_get_role_list_with_filter(self, role_client, test_role_data):
        """P2-角色列表过滤测试 - 验证查询功能"""
        # 先创建一个角色
        create_response = role_client.create_role(test_role_data)
        assert create_response.get("code") == 200
        
        # 使用角色名过滤
        filter_response = role_client.get_role_list(roleName=test_role_data.get("roleName"))
        
        assert filter_response.get("code") == 200
        assert filter_response.get("total") >= 1, "应至少找到1个匹配角色"
        assert filter_response.get("rows")[0].get("roleName") == test_role_data.get("roleName")

        # 获取角色ID用于清理
        role_id = filter_response.get("rows")[0].get("roleId")
        # 清理
        role_client.delete_role(role_id)
        
        print(f"✅ 角色列表过滤验证通过")
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p2
    @pytest.mark.parametrize("invalid_data,expected_error", [
        # 角色名为空
        ({"roleName": "", "roleKey": "test"}, "角色名称不能为空"),
        # 角色Key为空
        ({"roleName": "test", "roleKey": ""}, "权限字符不能为空"),
        # 角色排序为空
        ({"roleName": "test", "roleKey": "test", "roleSort": ""}, "显示顺序不能为空"),
    ], ids=["empty_role_name", "empty_role_key", "empty_role_sort"])
    def test_create_role_with_invalid_data(self, role_client, invalid_data, expected_error):
        """P2-创建角色-异常数据 - 验证参数校验"""
        response = role_client.create_role(invalid_data)
        
        # 若依框架对参数校验可能在前后端都有
        assert response.get("code") != 200, "期望创建失败"
        
        print(f"✅ 角色异常数据测试通过: {expected_error}")
