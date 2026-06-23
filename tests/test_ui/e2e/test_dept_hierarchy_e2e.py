import pytest
from ui.pages.base_page import BasePage
from config.settings import Settings


@pytest.mark.ui
@pytest.mark.e2e
class TestDeptHierarchyFlow:
    """部门层级流程测试"""

    # @staticmethod
    # def _close_all_dialogs(page):
    #     """关闭所有弹窗，确保测试隔离"""
    #     try:
    #         page.keyboard.press("Escape")
    #         page.wait_for_timeout(500)
    #     except Exception:
    #         pass

    def test_dept_hierarchy_management(self, dept_biz, test_dept_data, test_child_dept_data, page):
        """测试部门层级管理流程"""
        # # 确保没有遗留弹窗
        # self._close_all_dialogs(page)
    
        # 添加部门
        message = dept_biz.add_dept(test_dept_data)
        assert "成功" in message, f"添加部门失败: {message}"   
        
        # 添加子部门
        test_child_dept_data['parent'] = test_dept_data['deptName']
        message = dept_biz.add_child_dept(test_child_dept_data)   
        # 验证子部门添加成功
        assert "成功" in message, f"添加子部门失败: {message}"

        # 删除父部门（应该失败，因为存在下级部门）
        message = dept_biz.delete_dept(test_dept_data['deptName'])
        # 验证删除失败，可能是"存在下级部门"、"删除失败"(元素定位问题)或"操作失败"(系统错误)
        assert "存在下级部门" in message, f"删除父部门预期失败: {message}"
        
        # 删除子部门
        message = dept_biz.delete_dept(test_child_dept_data['deptName'])
        assert "成功" in message, f"删除子部门失败: {message}"
             
        # 删除父部门
        message = dept_biz.delete_dept(test_dept_data['deptName'])
        assert "成功" in message, f"删除父部门失败: {message}"
        
        # # 确保没有遗留弹窗
        # self._close_all_dialogs(page)
