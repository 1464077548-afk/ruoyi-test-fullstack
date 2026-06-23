from ui.pages.base_page import BasePage
from typing import Dict, List, Optional


class BaseModulePage(BasePage):
    """模块页面基类，包含所有模块共有的方法"""
    
    # 通用元素
    TABLE_LIST = 'common.table_list'
    OPERATE_MESSAGE = 'common.operate_message'
    SYS_PROMOPT_CONFIRM = 'user.sys_prompt_confirm'
    SYS_PROMOPT_CANCEL = 'user.sys_prompt_cancel'
    
    def __init__(self, page):
        super().__init__(page)
    
    def search(self, keyword: str, search_input_locator: str, search_button_locator: str):
        """通用搜索方法"""
        self.fill(search_input_locator, keyword)
        self.click(search_button_locator)
        self.wait_for_load_state()
    
    def create(self, data: dict, add_button_locator: str, form_locator: str, save_button_locator: str, **kwargs):
        """通用创建方法"""
        try:
            # 点击新增按钮
            self.click(add_button_locator)
            # 等待表单出现
            if form_locator:
                self.wait_for_locator(form_locator, state="visible")
            # 填写表单
            self.fill_form(data, **kwargs)
            # 点击保存按钮
            self.click(save_button_locator)
            # 获取操作消息
            message = self.get_operate_message()
            return message
        except Exception as e:
            self.logger.error(f"创建操作失败: {e}")
            return "创建失败"
    
    def fill_form(self, data: dict, **kwargs):
        """通用表单填写方法，子类可以重写"""
        pass
    
    def edit(self, keyword: str, data: dict, edit_button_locator: str, form_locator: str, save_button_locator: str, **kwargs):
        """通用编辑方法"""
        try:
            # 搜索
            self.search(keyword, getattr(self, 'SEARCH_INPUT', ''), getattr(self, 'SEARCH_BUTTON', ''))
            # 点击编辑按钮
            self.click_edit_button(keyword, edit_button_locator)
            # 等待表单出现
            if form_locator:
                self.wait_for_locator(form_locator, state="visible")
            # 填写表单
            self.fill_form(data, **kwargs)
            # 点击保存按钮
            self.click(save_button_locator)
            # 获取操作消息
            message = self.get_operate_message()
            return message
        except Exception as e:
            self.logger.error(f"编辑操作失败: {e}")
            return "编辑失败"
    
    def delete(self, keyword: str, delete_button_locator: str):
        """通用删除方法"""
        try:
            # 搜索
            self.search(keyword, getattr(self, 'SEARCH_INPUT', ''), getattr(self, 'SEARCH_BUTTON', ''))
            # 点击删除按钮
            self.click_delete_button(keyword, delete_button_locator)
            # 确认删除
            self.click(self.SYS_PROMOPT_CONFIRM)
            # 获取操作消息
            message = self.get_operate_message()
            return message
        except Exception as e:
            self.logger.error(f"删除操作失败: {e}")
            return "删除失败"
    
    def click_edit_button(self, keyword: str, edit_button_locator: str):
        """点击编辑按钮"""
        row = self.get_locator(self.TABLE_LIST).filter(has_text=keyword)
        edit_button = row.locator(edit_button_locator) if edit_button_locator else row.locator("button").filter(has_text="修改")
        edit_button.click()
    
    def click_delete_button(self, keyword: str, delete_button_locator: str):
        """点击删除按钮"""
        row = self.get_locator(self.TABLE_LIST).filter(has_text=keyword)
        delete_button = row.locator(delete_button_locator) if delete_button_locator else row.locator("button").filter(has_text="删除")
        delete_button.click()
    
    def toggle_status(self, keyword: str, status_locator: str = '.el-switch'):
        """通用状态切换方法"""
        try:
            # 搜索
            self.search(keyword, getattr(self, 'SEARCH_INPUT', ''), getattr(self, 'SEARCH_BUTTON', ''))
            # 点击状态切换按钮
            row = self.get_locator(self.TABLE_LIST).filter(has_text=keyword)
            status_button = row.locator(status_locator)
            status_button.click()
            # 确认操作
            self.wait_for_locator(self.SYS_PROMOPT_CONFIRM, state="visible")
            self.click(self.SYS_PROMOPT_CONFIRM)
            # 获取操作消息
            message = self.get_operate_message()
            return message
        except Exception as e:
            self.logger.error(f"状态切换失败: {e}")
            return "状态切换失败"
    
    def get_operate_message(self) -> str:
        """获取操作消息"""
        try:
            self.wait_for_locator(self.OPERATE_MESSAGE, state='visible', timeout=5000)
            message = self.get_text(self.OPERATE_MESSAGE)
            self.logger.info(f"操作消息: {message}")
            # 等待消息从dom中移除
            self.wait_for_locator(self.OPERATE_MESSAGE, state='detached', timeout=5000)
            return message
        except Exception as e:
            self.logger.error(f"获取操作消息失败: {e}")
            return "操作失败"
    
    def get_row_by_keyword(self, keyword: str):
        """根据关键字获取行"""
        self.search(keyword, getattr(self, 'SEARCH_INPUT', ''), getattr(self, 'SEARCH_BUTTON', ''))
        row = self.get_locator(self.TABLE_LIST).filter(has_text=keyword)
        return row
    
    def click_more_button(self, keyword: str, more_button_text: str = "更多"):
        """点击更多按钮"""
        row = self.get_row_by_keyword(keyword)
        more_button = row.locator("button").filter(has_text=more_button_text)
        more_button.click()
