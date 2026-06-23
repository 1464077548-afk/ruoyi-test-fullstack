from math import e
from ui.pages.modules.base_module_page import BaseModulePage
from ui.components.select_component import SelectComponent
from typing import List
from playwright.sync_api import expect


class DeptPage(BaseModulePage):
    """部门管理页面"""
    # ========== 公共元素 ==========
    TABLE_LIST = 'common.table_list'
    OPERATE_MESSAGE = 'common.operate_message'
    SYS_PROMOPT_CONFIRM = 'common.sys_prompt_confirm'
    
    # ========== 新增功能 ==========
    ADD_BUTTON = 'dept.add_button'
    ADD_CHILD_BUTTON = 'dept.add_child_button'
    DEPT_NAME_INPUT = 'dept.dept_name'
    DEPT_SORT_INPUT = 'dept.dept_sort'
    SAVE_BUTTON = 'dept.save_button'
    CANCEL_BUTTON = 'dept.cancel_button'
    TRESELECT_DEPT = 'dept.treeselect'
    
    # ========== 搜索功能 ==========
    SEARCH_INPUT = 'dept.search_input'
    SEARCH_BUTTON = 'dept.search_button'
    
    # ========== 表格功能 ==========
    TABLE_LIST = 'common.table_list'
    
    # ========== 编辑功能 ==========
    EDIT_BUTTON = 'dept.edit_button'
    EDIT_DEPT_NAME_INPUT = 'dept.edit_dept_name'
    EDIT_DEPT_SORT_INPUT = 'dept.edit_dept_sort'
    
    # ========== 删除功能 ==========
    DELETE_BUTTON = 'dept.delete_button'
    CONFIRM_DELETE = 'dept.confirm_delete'

    def click_add_dept(self):
        """点击新增部门"""
        self.click(self.ADD_BUTTON)

    def click_add_child_dept(self):
        """点击新增子部门"""
        self.click(self.ADD_CHILD_BUTTON)
    def fill_dept_name(self, dept_name: str):
        """填写部门名称"""
        self.fill(self.DEPT_NAME_INPUT, dept_name)
    def fill_dept_sort(self, dept_sort: int):
        """填写部门排序"""
        self.fill(self.DEPT_SORT_INPUT, str(dept_sort))
    def fill_edit_dept_name(self, dept_name: str):
        """填写编辑部门名称"""
        self.fill(self.EDIT_DEPT_NAME_INPUT, dept_name)
    def fill_edit_dept_sort(self, dept_sort: int):
        """填写编辑部门排序"""
        self.fill(self.EDIT_DEPT_SORT_INPUT, str(dept_sort))
    def select_parent_dept(self, parent_dept: str):
        """选择上级部门"""
        select_component = SelectComponent(self.page)
        select_component.select_treeselect(self.TRESELECT_DEPT, parent_dept)
    
    def fill_dept_form(self, dept_data: dict):
        """填写部门表单"""
        # 填写上级部门
        # 打开下拉
        select_component = SelectComponent(self.page)
        select_component.select_treeselect(self.TRESELECT_DEPT, dept_data['parent'])
        
        self.fill(self.DEPT_NAME_INPUT, dept_data['deptName'])
        # 将dept_sort转换为字符串
        self.fill(self.DEPT_SORT_INPUT, str(dept_data['orderNum']))

    def click_save_dept(self):
        """点击保存部门"""
        self.click(self.SAVE_BUTTON)
        self.wait_for_load_state()

    def click_cancel_dept(self):
        """点击取消"""
        self.click(self.CANCEL_BUTTON)
        self.wait_for_load_state()

    def create_dept(self, dept_data: dict):
        """创建部门"""
        try:
            self.click_add_dept()
            self.fill_dept_form(dept_data)
            self.click_save_dept()
            
            # 尝试获取操作消息
            self.wait_for_locator(self.OPERATE_MESSAGE, state='visible', timeout=5000)
            message = self.get_text(self.OPERATE_MESSAGE)
            self.logger.info(f"🔥创建部门消息: {message}")
            # 等待消息从dom中移除
            self.wait_for_locator(self.OPERATE_MESSAGE, state='detached', timeout=5000)
            return message
        except Exception as e:
            self.logger.error(f"创建部门失败: {e}")
            return "创建失败"

    def create_child_dept(self, child_dept_data: dict):
        """创建子部门"""
        try:
            # 先找到父部门并点击添加子部门
            
            self.search_dept(child_dept_data['parent'])
            print(f"找到父部门: {child_dept_data['parent']}")
            parent_row = self.get_locator(self.TABLE_LIST).filter(has_text=f"{child_dept_data['parent']}")
            
            # 点击更多按钮展开操作菜单
            more_button = parent_row.locator('button:has-text("新增")')
            more_button.click()
            
            
            # 填写子部门表单
            self.fill(self.DEPT_NAME_INPUT, child_dept_data['deptName'])
            self.fill(self.DEPT_SORT_INPUT, str(child_dept_data['orderNum']))
            self.click_save_dept()
            
            # 尝试获取操作消息
            self.wait_for_locator(self.OPERATE_MESSAGE, state='visible', timeout=5000)
            message = self.get_text(self.OPERATE_MESSAGE)
            self.logger.info(f"🔥创建子部门消息: {message}")
            # 等待消息从dom中移除
            self.wait_for_locator(self.OPERATE_MESSAGE, state='detached', timeout=5000)
            return message
        except Exception as e:
            self.logger.error(f"创建子部门失败: {e}")
            return "添加失败"

    def search_dept(self, dept_name: str):
        """搜索部门"""
        self.search(dept_name, self.SEARCH_INPUT, self.SEARCH_BUTTON)
    def fill_dept_search(self, dept_name: str):
        """填写搜索部门名称"""
        self.fill(self.SEARCH_INPUT, dept_name)
    def click_search_dept(self):
        """点击搜索部门"""
        self.click(self.SEARCH_BUTTON)
        self.wait_for_load_state()

    def click_edit_dept(self, dept_name: str):
        """点击编辑部门"""
        # 先刷新页面，确保显示最新数据
        self.page.reload()
        self.wait_for_load_state()
        self.page.wait_for_timeout(1000)
        
        # 使用更精确的匹配，查找包含完整部门名称的行
        table = self.get_locator(self.TABLE_LIST)
        row = table.locator('tr').filter(has_text=f"{dept_name}")
        print(f"找到部门行: {len(row.all())}")
        
        # 查找该行的编辑按钮
        edit_btn = row.locator('button:has-text("修改")')
        if edit_btn.is_visible():
            edit_btn.click()
            self.wait_for_load_state()
            self.page.wait_for_timeout(500)
        else:
            raise Exception(f"部门 '{dept_name}' 的编辑按钮不可见")

    def edit_dept(self, dept_name: str, dept_data: dict):
        """编辑部门"""
        self.click_edit_dept(dept_name)
        self.fill_dept_form(dept_data)
        self.click_save_dept()
        
        message = self.get_text(self.OPERATE_MESSAGE)
        self.wait_for_locator(self.OPERATE_MESSAGE, state='detached')
        self.logger.info(f"编辑部门数据: {dept_name} 为 {dept_data['deptName']}")
        self.logger.info(f"🔥编辑部门消息: {message}")
        return message

    def click_delete_dept(self, dept_name: str):
        """点击删除部门"""
        self.search_dept(dept_name)
        self.get_locator(self.TABLE_LIST).filter(has_text=dept_name).locator("button").filter(has_text="删除").first.click()

    def delete_dept(self, dept_name: str):
        """删除部门"""
        try:
            # 搜索部门
            self.search_dept(dept_name)
            # 等待表格加载
            self.wait_for_load_state()
            # 使用更通用的选择器定位删除按钮
            rows = self.get_locator(self.TABLE_LIST).all()
            for row in rows:
                row_text = row.text_content()
                if dept_name in row_text:
                    # 查找该行的删除按钮
                    delete_btn = row.locator("button").filter(has_text="删除")
                    if delete_btn.count() > 0:
                        delete_btn.click()
                        # 确认删除
                        self.click(self.SYS_PROMOPT_CONFIRM)
                        # 获取操作消息
                        self.page.wait_for_timeout(2000)
                        return self.get_operate_message()
            return "删除失败"
        except Exception as e:
            self.logger.error(f"删除部门失败: {e}")
            return "删除失败"

    def get_dept_list(self) -> List[str]:
        """获取部门列表"""
        locator = self.get_locator('dept.dept_list')
        elements = locator.all()
        return [element.text_content().strip() for element in elements]
