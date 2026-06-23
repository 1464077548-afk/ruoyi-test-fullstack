"""
L2: 角色管理模块测试
验证角色管理功能的完整测试
"""
import pytest
from config.settings import Settings


class TestRoleManageModule:
    """角色管理模块测试类"""
    
    # ========== 新增功能 ==========
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_role_add_success(self, common_biz, role_biz, test_role_data):
        """P0-新增角色成功"""
        common_biz.switch_menu("系统管理/角色管理")
        # 创建角色
        message = role_biz.add_role(test_role_data)
        
        # 验证操作成功提示
        assert "成功" in message
        
        # 通过UI验证：刷新页面后检查表格中是否存在新角色
        role_info = role_biz.search_role_by_name(test_role_data['roleName'])
        assert role_info is not None, f"角色 {test_role_data['roleName']} 未在UI表格中找到"
        assert role_info["roleName"] == test_role_data['roleName']
        print(f"✅ 角色 {test_role_data['roleName']} 创建成功并在UI中验证通过")
        #删除角色
        message = role_biz.delete_role(test_role_data['roleName'])
        # 验证操作成功提示
        assert "成功" in message
        print(f"✅ 角色 {test_role_data['roleName']} 删除成功")
        # 通过UI验证：刷新页面后检查表格中是否存在新角色
        role_info = role_biz.search_role_by_name(test_role_data['roleName'])
        assert role_info["roleName"] == "", f"角色 {test_role_data['roleName']} 在UI表格中找到"
        print(f"✅ 角色 {test_role_data['roleName']} 删除成功并在UI中验证通过")
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_role_add_with_permissions(self, common_biz, role_biz, test_role_data):
        """P1-为角色分配数据权限"""
        common_biz.switch_menu("系统管理/角色管理")
        # 创建角色
        print(f"测试数据: {test_role_data}")
        message = role_biz.add_role(test_role_data)
        # 验证操作成功提示
        assert "成功" in message
        message=role_biz.assign_data_permissions(test_role_data['roleName'],option_text="全部数据权限")
        # 验证操作成功提示
        assert "成功" in message
        #删除角色
        message = role_biz.delete_role(test_role_data['roleName'])
        # 验证操作成功提示
        assert "成功" in message
        print(f"✅ 角色 {test_role_data['roleName']} 删除成功")
        # 通过UI验证：刷新页面后检查表格中是否存在新角色
        role_info = role_biz.search_role_by_name(test_role_data['roleName'])
        assert role_info["roleName"] == "", f"角色 {test_role_data['roleName']} 在UI表格中找到"
        print(f"✅ 角色 {test_role_data['roleName']} 删除成功并在UI中验证通过")
    
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
  
    def test_role_add_duplicate(self, common_biz, role_biz, test_role_data):
        """P1-新增重复角色"""
        common_biz.switch_menu("系统管理/角色管理")
        # 先创建一个角色
        message = role_biz.add_role(test_role_data)
        # 验证操作成功提示
        assert "成功" in message
        
        # 再创建同名角色
        message = role_biz.add_role(test_role_data)
        # 验证重复提示
        assert "已存在" in message or "失败" in message
        #关闭新增角色弹窗
        role_biz.role.press_key("Escape")
        #删除角色
        message = role_biz.delete_role(test_role_data['roleName'])
        # 验证操作成功提示
        assert "成功" in message
     
    # ========== 编辑功能 ==========
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_role_edit_success(self, common_biz, role_biz, test_role_data):
        """P0-编辑角色成功"""
        common_biz.switch_menu("系统管理/角色管理")
        # 先创建一个角色
        message = role_biz.add_role(test_role_data)
        # 验证操作成功提示
        assert "成功" in message

        new_role_name =f"new_{test_role_data['roleName']}"
        message = role_biz.edit_role(test_role_data['roleName'],new_role_name)
        # 验证操作成功提示
        assert "成功" in message
        
        # 验证修改成功
        role_info = role_biz.search_role_by_name(new_role_name)
        # 验证角色列表包含新创建的角色
        assert new_role_name == role_info['roleName']

        #删除角色
        message = role_biz.delete_role(new_role_name)
        # 验证操作成功提示
        assert "成功" in message
        print(f"✅ 角色 {new_role_name} 删除成功")
  

    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_role_edit_status(self, common_biz, role_biz, test_role_data):
        """P1-编辑角色状态"""
        common_biz.switch_menu("系统管理/角色管理")
        # 先创建一个角色
        role_biz.add_role(test_role_data)
        # 切换角色状态
        message = role_biz.toggle_role_status(test_role_data['roleName'])
        assert "成功" in message
        
        # 验证状态变化
        role_info = role_biz.search_role_by_name(test_role_data['roleName'])
        assert not role_info['status'] , f"角色状态未禁用"

        # 再次切换状态，验证恢复
        message = role_biz.toggle_role_status(test_role_data['roleName'])
        assert "成功" in message
        
        role_info = role_biz.search_role_by_name(test_role_data['roleName'])
        assert role_info['status'] , f"角色状态未改变"
        #删除角色
        message = role_biz.delete_role(test_role_data['roleName'])
        # 验证操作成功提示
        assert "成功" in message
        print(f"✅ 角色 {test_role_data['roleName']} 删除成功")
       
    
    # ========== 删除功能 ==========
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_role_delete_success(self, common_biz, role_biz, test_role_data):
        """P0-删除角色成功"""
        common_biz.switch_menu("系统管理/角色管理")
        # 先创建一个角色
        role_biz.add_role(test_role_data)
        
        # 删除
        message = role_biz.delete_role(test_role_data['roleName'])
        assert "成功" in message
        
        # 验证角色列表不包含已删除角色
        role_info = role_biz.search_role_by_name(test_role_data['roleName'])
        print(f"删除后角色信息: {role_info}")
        assert test_role_data['roleName'] != role_info['roleName'], f"角色 {test_role_data['roleName']} 在UI表格中找到,删除失败"
    

    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_role_delete_with_users(self, common_biz, user_biz, role_biz, test_user_data, test_role_data, user_client):
        """P1-删除有关联用户的角色"""
        try:
            # 先创建一个用户
            common_biz.switch_menu("系统管理/用户管理")
            message = user_biz.add_user(test_user_data)
            assert "成功" in message, f"创建用户失败: {message}"
  
            common_biz.switch_menu("系统管理/角色管理")
            # 创建角色
            message = role_biz.add_role(test_role_data)
            assert "成功" in message, f"创建角色失败: {message}"
            
            # 给角色分配用户
            message = role_biz.assign_user(test_role_data['roleName'], user_name=test_user_data['userName'])
            assert "成功" in message, f"分配用户失败: {message}"
            
            # 关闭分配用户Tab页
            role_biz.close_tab()
            
            # 切换到角色管理tab页
            role_biz.switch_tab("角色管理")
            
            # 删除角色（应该失败，因为有关联用户）
            message = role_biz.delete_role(test_role_data['roleName'])
            assert "失败" in message or "已分配" in message or "无法删除" in message, f"预期删除失败但成功了: {message}"    

            # 切换到用户管理tab页
            role_biz.switch_tab("用户管理")
            message = user_biz.delete_user(test_user_data['userName'])
            assert "成功" in message, f"删除用户失败: {message}"
            # role_biz.close_tab()

            # 切换到角色管理tab页
            role_biz.switch_tab("角色管理")
            message = role_biz.delete_role(test_role_data['roleName'])
            assert "成功" in message, f"删除角色失败: {message}"
            
        finally:
            # 清理残留数据
            try:
                api_result = user_client.get_user_list(userName=test_user_data['userName'])
                if api_result.get('total', 0) > 0:
                    user_id = api_result['rows'][0]['userId']
                    user_client.delete_user(user_id)
            except Exception:
                pass
            
            try:
                role_biz.switch_tab("角色管理")
                role_biz.delete_role(test_role_data['roleName'])
            except Exception:
                pass
    # ========== 搜索功能 ==========
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_role_search_by_name(self, common_biz, role_biz, test_role_data):
        """P0-按角色名搜索"""
        common_biz.switch_menu("系统管理/角色管理")
        message = role_biz.add_role(test_role_data)
        assert "成功" in message
        
        role_info = role_biz.search_role_by_name(test_role_data['roleName'])
        
        # 验证搜索结果
        assert role_info["roleName"] == test_role_data['roleName']

        #删除角色
        message = role_biz.delete_role(test_role_data['roleName'])
        # 验证操作成功提示
        assert "成功" in message
        print(f"✅ 角色 {test_role_data['roleName']} 删除成功")
        # 通过UI验证：刷新页面后检查表格中是否存在新角色
        role_info = role_biz.search_role_by_name(test_role_data['roleName'])
        assert role_info["roleName"] == "", f"角色 {test_role_data['roleName']} 在UI表格中找到"
        print(f"✅ 角色 {test_role_data['roleName']} 删除成功并在UI中验证通过")
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_role_search_by_key(self, common_biz, role_biz, test_role_data, role_client):
        """P1-按角色键搜索"""
        common_biz.switch_menu("系统管理/角色管理")
        message = role_biz.add_role(test_role_data)
        assert "成功" in message
        
        role_info = role_biz.search_role_by_key(test_role_data['roleKey'])
        
        # 验证搜索结果
        assert role_info["roleKey"] == test_role_data['roleKey']

        #删除角色
        message = role_biz.delete_role(test_role_data['roleName'])
        # 验证操作成功提示
        assert "成功" in message
        print(f"✅ 角色 {test_role_data['roleName']} 删除成功")
        