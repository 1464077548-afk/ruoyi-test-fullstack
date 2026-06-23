"""跨模块集成测试"""
import pytest
from api.clients.user_client import UserClient
from api.clients.role_client import RoleClient
from api.clients.menu_client import MenuClient
from common.utils.data_factory import DataFactory


class TestCrossModule:
    """跨模块集成测试类"""
    
    def test_user_role_menu_integration(self, user_client, role_client, menu_client, test_role_data, test_user_data):
        """测试用户、角色、菜单模块的集成"""
        # 1. 准备测试数据
        role_id = None
        user_id = None
        
        try:
            # 2. 创建角色
            role_response = role_client.create_role(test_role_data)
            assert role_response.get("code") == 200, "角色创建失败"
            print(f"1️⃣创建角色成功: {test_role_data}")
            
            # 查询角色列表获取roleId
            role_list = role_client.get_role_list(roleName=test_role_data.get("roleName"))
            assert role_list.get("code") == 200
            assert len(role_list.get("rows", [])) > 0
            role_id = role_list.get("rows")[0].get("roleId")
            assert role_id, "角色ID获取失败"
            print(f"2️⃣获取角色ID成功: {role_id}")
            
            
            # 3. 获取菜单列表
            menu_response = menu_client.get_menu_list()
            menus = menu_response.get("data", [])
            assert len(menus) > 0, "菜单列表为空"
 
            # 4. 提取菜单ID
            menu_ids = [menu.get("menuId") for menu in menus if menu.get("menuId")]
            assert len(menu_ids) > 0, "没有可用的菜单ID"
            print(f"4️⃣提取菜单ID成功: {menu_ids[:3]}")
            
            # 5. 分配菜单权限给角色
            assign_response = role_client.assign_menus(role_id, menu_ids[:3])
            assert assign_response.get("code") == 200, "菜单权限分配失败"
            print(f"5️⃣分配菜单权限成功: {role_id} -> {menu_ids[:3]}")
          
            
            # 6. 创建用户并分配角色
            test_user_data["roleIds"] = [role_id]
            create_response = user_client.create_user(test_user_data)
            assert create_response.get("code") == 200, "用户创建失败"
            print(f"6️⃣创建用户成功: {test_user_data}")
            
            # 查询用户列表获取userId
            user_list = user_client.get_user_list(userName=test_user_data.get("userName"))
            assert user_list.get("code") == 200
            assert len(user_list.get("rows", [])) > 0
            user_id = user_list.get("rows")[0].get("userId")
            assert user_id, "用户ID获取失败"
            print(f"7️⃣获取用户ID成功: {user_id}")
            
            # 7. 验证用户、角色、菜单的关联
            user_detail = user_client.get_user_by_id(user_id)
            assert user_detail.get("code") == 200, "获取用户详情失败"
            
            user_roles = user_detail.get("data", {}).get("roles", [])
            assert len(user_roles) > 0, "用户未分配角色"
            assert role_id in [role.get("roleId") for role in user_roles], "用户未分配指定角色"
            print(f"8️⃣验证用户角色关联成功: {user_roles}")
            
            role_detail = role_client.get_role_by_id(role_id)
            print(f"9️⃣获取角色详情成功: {role_detail}")
            assert role_detail.get("code") == 200, "获取角色详情失败"
            assert role_detail.get("data", {}).get("roleId") == role_id, "角色ID不匹配"
            assert role_detail.get("data", {}).get("roleName") == test_role_data.get("roleName"), "角色名称不匹配"
             # 验证菜单权限分配（通过角色菜单树接口验证）
            menu_tree_response = menu_client.get_role_menu_tree(role_id)
            assert menu_tree_response.get("code") == 200, "获取角色菜单树失败"
            assigned_menu_ids = menu_tree_response.get("checkedKeys", [])
            print(f"10️⃣验证菜单权限: 已分配菜单ID -> {assigned_menu_ids}")
            for menu_id in menu_ids[:3]:
                assert menu_id in assigned_menu_ids, f"菜单ID {menu_id} 未正确分配给角色"
            print("✅ 用户、角色、菜单集成测试验证完成")
            
        finally:
            # 清理资源
            if user_id:
                try:
                    user_client.delete_user(user_id)
                    print(f"10️⃣删除用户成功: {user_id}")
                except:
                    pass
            if role_id:
                try:
                    role_client.delete_role(role_id)
                    print(f"11️⃣删除角色成功: {role_id}")
                except:
                    pass
