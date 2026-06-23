"""
L2: 菜单管理模块测试
验证菜单管理功能的完整测试
"""
import pytest


class TestMenuManageModule:
    """菜单管理模块测试类"""
    
    # ========== 新增功能 ==========
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_menu_add_directory(self, menu_page, test_menu_data):
        """P0-新增目录菜单"""
        test_menu_data['type'] = '目录'    
        message = menu_page.create_menu(test_menu_data)
        assert "成功" in message

    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_menu_add_menu(self, menu_page, test_menu_data):
        """P0-新增菜单"""
        test_menu_data['type'] = '菜单'    
        message = menu_page.create_menu(test_menu_data)
        assert "成功" in message
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_menu_add_button(self, menu_page, test_menu_data):
        """P1-新增按钮"""
        test_menu_data['type'] = '按钮'    
        message = menu_page.create_menu(test_menu_data)
        assert "成功" in message
        
    
    # ========== 编辑功能 ==========
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_menu_edit_success(self, menu_page, test_menu_data):
        """P0-编辑菜单成功"""
        message = menu_page.create_menu(test_menu_data)
        assert "成功" in message

        new_menu_name =f'edit_{test_menu_data["menuName"]}'
        message = menu_page.edit_menu(test_menu_data['menuName'],new_menu_name)
        assert "成功" in message
    
    # ========== 删除功能 ==========
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_menu_delete_success(self, menu_page, test_menu_data):
        """P0-删除菜单成功"""
        message = menu_page.create_menu(test_menu_data)
        assert "成功" in message
        
        message = menu_page.delete_menu(test_menu_data['menuName'])
        assert "成功" in message
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_menu_delete_with_children(self, menu_page):
        """P1-删除有子菜单的父菜单"""
        
        # 注意：menu_page的方法需要实现
        # 暂时跳过验证，等待方法实现
        pass
    
    # ========== 其他功能 ==========
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_menu_expand_collapse(self, menu_page):
        """P1-菜单展开/折叠"""
        
        # 注意：menu_page的方法需要实现
        # 暂时跳过验证，等待方法实现
        pass
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p2
    def test_menu_tree_display(self, menu_page):
        """P2-菜单树形显示"""
        
        # 注意：menu_page的方法需要实现
        # 暂时跳过验证，等待方法实现
        pass