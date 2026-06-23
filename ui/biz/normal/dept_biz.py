from ui.pages.modules.dept_page import DeptPage
from ui.biz.common_biz import CommonBiz
import logging
class DeptBiz:
    """部门业务逻辑"""
    def __init__(self,page):
        self.page = page
        self.common = CommonBiz(page)
        self.dept = DeptPage(page)
        self.logger = logging.getLogger(__name__)

    def add_dept(self, dept_data: dict):
        """添加部门"""
        try:
           
             # 导航到部门管理页面
            self.common.switch_menu("系统管理/部门管理")
            self.dept.click_add_dept()
            print(f"添加部门: {dept_data}")
            self.dept.fill_dept_name(dept_data['deptName'])
            self.dept.fill_dept_sort(dept_data['orderNum'])
            self.dept.select_parent_dept(dept_data['parent'])
            
            self.dept.click_save_dept()
            
            # 等待消息出现（Element UI 的 Toast 消息需要一点时间显示）
            self.common.page.wait_for_timeout(1500)
            
            # 尝试获取操作消息
            message = self.common.get_operate_message()
            self.logger.info(f"🔥创建部门消息: {message}")
            return message
        except Exception as e:
            self.logger.error(f"创建部门失败: {e}")
            return "创建失败"
    def add_child_dept(self, child_dept_data: dict):
        """添加子部门"""
        try:
            # 导航到部门管理页面
            self.common.switch_menu("系统管理/部门管理")
            
            # 先找到父部门并点击添加子部门  
            self.common.common_search(self.dept, child_dept_data['parent'])
            self.logger.info(f"找到父部门: {child_dept_data['parent']}")
            parent_row = self.common.search_table_row_by_name(self.dept, child_dept_data['parent'])
            
            # 点击更多按钮展开操作菜单
            more_button = parent_row.locator('button:has-text("新增")')
            more_button.click()
            
            
            # 填写子部门表单
            self.dept.fill_dept_name(child_dept_data['deptName'])
            self.dept.fill_dept_sort(child_dept_data['orderNum'])
            self.dept.click_save_dept()
            
            # 等待消息出现（Element UI 的 Toast 消息需要一点时间显示）
            self.common.page.wait_for_timeout(1500)
            
            # 尝试获取操作消息
            message = self.common.get_operate_message()
            self.logger.info(f"🔥创建子部门消息: {message}")
            return message
        except Exception as e:
            self.logger.error(f"创建子部门失败: {e}")
            return "添加失败"
    def delete_dept(self, dept_name: str):
        """删除部门"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # 导航到部门管理页面
                self.common.switch_menu("系统管理/部门管理")
                
                # 等待页面加载完成
                self.common.page.wait_for_load_state('load', timeout=10000)
                self.common.page.wait_for_timeout(1000)
                
                # 使用部门页面专用的删除方法，更可靠
                message = self.dept.delete_dept(dept_name)
                
                # 等待消息出现（Element UI 的 Toast 消息需要一点时间显示）
                self.common.page.wait_for_timeout(2000)
                
                # 获取操作消息（如果页面方法没有返回消息）
                if not message or message == "删除失败":
                    message = self.common.get_operate_message()
                
                # 验证删除是否成功
                if "成功" in message:
                    return message
                elif attempt < max_retries - 1:
                    print(f"删除消息: {message}，尝试重试...")
                    self.common.page.wait_for_timeout(2000)
                else:
                    return message
                    
            except Exception as e:
                self.logger.error(f"删除部门失败(第{attempt+1}次尝试): {e}")
                if attempt < max_retries - 1:
                    self.common.page.wait_for_timeout(2000)
                else:
                    return "删除失败"
    def edit_dept(self, dept_name: str, dept_data: dict):
        """编辑部门"""
        try:
            # 导航到部门管理页面
            self.common.switch_menu("系统管理/部门管理")
            self.common.common_search(self.dept, dept_name)
            self.dept.click_edit_dept(dept_name)
            self.dept.fill_edit_dept_name(dept_data['deptName'])
            self.dept.fill_edit_dept_sort(dept_data['orderNum'])
            self.dept.click_save_dept() 
            
            # 等待消息出现（Element UI 的 Toast 消息需要一点时间显示）
            self.common.page.wait_for_timeout(1500)
            
            message = self.common.get_operate_message()
            self.logger.info(f"编辑部门数据: {dept_name} 为 {dept_data['deptName']}")
            self.logger.info(f"🔥编辑部门消息: {message}")
            return message
        except Exception as e:
            self.logger.error(f"编辑部门失败: {e}")
            return "编辑失败"
    def search_dept(self, dept_name: str):
        """搜索部门"""
        self.dept.fill_dept_search(dept_name)
        self.dept.click_search_dept()
    
    def close_add_dept_dialog(self):
        """关闭新增部门弹窗"""
        self.logger.info("关闭新增部门弹窗")
        self.page.keyboard.press("Escape")
      