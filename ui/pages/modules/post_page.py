from ui.pages.base_page import BasePage
from typing import List


class PostPage(BasePage):
    """岗位管理页面"""
    # ========== 公共元素 ==========
    TABLE_LIST = 'common.table_list'
    OPERATE_MESSAGE = 'common.operate_message'
    SYS_PROMOPT_CONFIRM = 'common.sys_prompt_confirm'
    BATCH_DELETE_BUTTON = 'common.batch_delete_button'
    SYS_PROMPT_CONFIRM_DELETE = 'common.sys_prompt_confirm'
    
    # ========== 新增功能 ==========
    ADD_BUTTON = 'common.add_button'
    POST_NAME_INPUT = 'post.post_name'
    POST_CODE_INPUT = 'post.post_code'
    POST_SORT_INPUT = 'post.post_sort'
    SAVE_BUTTON = 'post.save_button'
    CANCEL_BUTTON = 'post.cancel_button'
    
    # ========== 搜索功能 ==========
    SEARCH_INPUT = 'post.search_input'
    SEARCH_BUTTON = 'post.search_button'
    
    # ========== 编辑功能 ==========
    EDIT_BUTTON = 'post.edit_button'
    
    # ========== 删除功能 ==========
    DELETE_BUTTON = 'post.delete_button'
    CONFIRM_DELETE = 'post.confirm_delete'

    def click_add_post(self):
        """点击新增岗位"""
        self.click(self.ADD_BUTTON)
        self.wait_for_load_state()
    def fill_post_name(self, post_name: str):
        """填写岗位名称"""
        self.fill(self.POST_NAME_INPUT, post_name)
    def fill_post_code(self, post_code: str):
        """填写岗位编码"""
        self.fill(self.POST_CODE_INPUT, post_code)
    def fill_post_sort(self, post_sort: str):
        """填写岗位排序"""
        self.fill(self.POST_SORT_INPUT, post_sort)
    

    def fill_search_input(self, post_name: str):
        """填写搜索输入框"""
        self.fill(self.SEARCH_INPUT, post_name)
    def click_search_button(self):
        """点击搜索按钮"""
        self.click(self.SEARCH_BUTTON)
    def click_batch_delete_button(self):
        """点击批量删除按钮"""
        self.click(self.BATCH_DELETE_BUTTON)
        self.wait_for_load_state()
    def click_confirm_delete(self):
        """点击确认删除"""
        self.click(self.SYS_PROMPT_CONFIRM_DELETE)
  
    def checked_row(self):
        """勾选岗位行 - 使用全选框"""
        # 点击表头的全选复选框
        try:
            # 定位表头的复选框
            table_header = self.page.locator(".el-table__header-wrapper")
            select_all_checkbox = table_header.locator(".el-checkbox").first
            #检查复选框是否选中
            if not select_all_checkbox.is_checked():
                select_all_checkbox.click()
                print("已点击全选框")
                self.logger.info("已点击全选框")
                # self.page.wait_for_timeout(500)
            else:
                print("全选复选框已是选中状态")   
        except Exception as e:
            # 方式2 直接勾选每行的复选框
            try:
                rows = self.click(self.TABLE_LIST).locator("tr").all()
                for row in rows:
                    row.locator(".el-checkbox").first.click()
            except Exception as e:
                print(f"勾选每行复选框失败: {e}")
        
    def fill_post_form(self, post_name: str, post_code: str, post_sort: str):
        """填写岗位表单"""
        # 等待弹窗出现
        dialog = self.page.get_by_role("dialog").last
        dialog.wait_for(state="visible", timeout=5000)
        
        # 填写表单字段
        post_name_input = dialog.get_by_placeholder("请输入岗位名称")
        post_name_input.wait_for(state="visible", timeout=5000)
        post_name_input.fill(post_name)
        
        post_code_input = dialog.get_by_placeholder("请输入编码名称")
        post_code_input.wait_for(state="visible", timeout=5000)
        post_code_input.fill(post_code)
        
        post_sort_input = dialog.get_by_role("spinbutton")
        post_sort_input.wait_for(state="visible", timeout=5000)
        post_sort_input.fill(post_sort)

    def click_save_post(self):
        """点击保存岗位"""
        # 找到可见弹窗中的保存按钮
        visible_dialogs = self.page.locator(".el-dialog__wrapper").filter(has=self.page.locator(".el-dialog:visible"))
        
        self.logger.info(f"可见弹窗数量: {visible_dialogs.count()}")
        
        if visible_dialogs.count() == 0:
            self.logger.warning("未找到可见弹窗")
            return
        
        # 获取最后一个可见弹窗（通常是新增或编辑弹窗）
        dialog = visible_dialogs.last
        
        # 在弹窗内查找保存按钮
        save_button = dialog.locator("button").filter(has_text="确定").first
        
        if save_button.count() == 0:
            # 尝试其他方式定位按钮
            save_button = dialog.locator(".el-dialog__footer button.el-button--primary").first
        
        save_button.wait_for(state="visible", timeout=5000)
        self.logger.info(f"保存按钮状态 - 可见: {save_button.is_visible()}, 可用: {save_button.is_enabled()}")
        
        # 检查页面上是否有任何错误提示
        error_messages = dialog.locator(".el-form-item__error")
        if error_messages.count() > 0:
            self.logger.warning(f"发现 {error_messages.count()} 个错误提示")
            for i in range(error_messages.count()):
                self.logger.warning(f"错误 {i+1}: {error_messages.nth(i).text_content()}")
        
        # 点击保存按钮
        save_button.click(timeout=self.timeout)
        
        # 等待一小段时间让表单提交
        self.page.wait_for_timeout(1500)
        
        # 再次检查错误提示
        error_messages = dialog.locator(".el-form-item__error")
        if error_messages.count() > 0:
            self.logger.warning(f"点击保存后发现 {error_messages.count()} 个错误提示")
            for i in range(error_messages.count()):
                self.logger.warning(f"错误 {i+1}: {error_messages.nth(i).text_content()}")
        
        # 等待弹窗关闭
        try:
            dialog.wait_for(state="detached", timeout=5000)
            self.logger.info("弹窗已关闭")
        except Exception as e:
            self.logger.warning(f"等待弹窗关闭失败: {e}")

    def click_cancel_post(self):
        """点击取消"""
        # 找到可见弹窗中的取消按钮
        visible_dialogs = self.page.locator(".el-dialog__wrapper").filter(has=self.page.locator(".el-dialog:visible"))
        
        if visible_dialogs.count() == 0:
            self.logger.warning("未找到可见弹窗")
            return
        
        # 获取最后一个可见弹窗
        dialog = visible_dialogs.last
        
        # 找到弹窗中的取消按钮
        cancel_button = dialog.locator("button").filter(has_text="取消").first
        cancel_button.wait_for(state="visible", timeout=5000)
        cancel_button.click()
        self.wait_for_load_state()

    def create_post(self, post_data: dict):
        """创建岗位"""
        self.click_add_post()
        self.fill_post_form(post_data['postName'], post_data['postCode'], post_data['postSort'])
        
        # 等待一下确保表单填写完成
        self.page.wait_for_timeout(500)
        
        # 点击保存按钮
        self.click_save_post()
        
        # 等待弹窗关闭
        self.page.wait_for_timeout(1000)
        
        # 检查弹窗是否关闭
        dialog_count = self.page.get_by_role("dialog").count()
        print(f"弹窗数量: {dialog_count}")
        
        # 如果弹窗还在，尝试按ESC关闭
        if dialog_count > 0:
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(500)
        
        # 使用多种方式获取操作消息
        message = self._get_operate_message()
        self.logger.info(f"创建岗位数据: {post_data}")
        self.logger.info(f"🔥创建岗位消息: {message}")
        return message

    def _get_operate_message(self) -> str:
        """获取操作消息（支持多种定位方式）"""
        self.page.wait_for_timeout(800)
        
        # 方法1: 尝试通过 role="alert" 定位
        try:
            toast = self.page.get_by_role("alert").first
            toast.wait_for(state="visible", timeout=3000)
            message = toast.text_content().strip()
            toast.wait_for(state='detached', timeout=5000)
            return message
        except Exception:
            pass
        
        # 方法2: 尝试通过常见的Toast类定位
        try:
            toast = self.page.locator(".el-message, .el-toast, .Toast, .toast")
            if toast.count() > 0:
                toast.first.wait_for(state="visible", timeout=3000)
                message = toast.first.text_content().strip()
                toast.first.wait_for(state='detached', timeout=5000)
                return message
        except Exception:
            pass
        
        # 方法3: 尝试通过包含"成功"或"失败"的元素定位
        try:
            success_msg = self.page.locator("text*=成功")
            error_msg = self.page.locator("text*=失败")
            
            if success_msg.count() > 0:
                success_msg.first.wait_for(state="visible", timeout=1000)
                return success_msg.first.text_content().strip()
            elif error_msg.count() > 0:
                error_msg.first.wait_for(state="visible", timeout=1000)
                return error_msg.first.text_content().strip()
        except Exception:
            pass
        
        # 方法4: 尝试获取页面上任何可见的消息元素
        try:
            msg_elements = self.page.locator("[role='alert'], .el-message, .el-notification, .el-toast")
            if msg_elements.count() > 0:
                return msg_elements.first.text_content().strip()
        except Exception:
            pass
        
        # 所有方法都失败，返回默认值
        return "操作失败"

    def search_post(self, post_name: str):
        """搜索岗位"""
        self.fill_search_input(post_name)
        self.click_search_button()
        
        self.wait_for_load_state()

    def click_edit_post(self, post_name: str):
        """点击编辑岗位"""
        self.search_post(post_name)
        self.get_locator(self.TABLE_LIST).locator(f"tr:has-text('{post_name}')").locator("button").filter(has_text="修改").click()

    def edit_post(self, post_name: str, new_post_name: str, new_post_code: str, new_post_sort: str):
        """编辑岗位"""
        self.click_edit_post(post_name)
        self.fill_post_form(new_post_name, new_post_code, new_post_sort)
        self.click_save_post()
        
        message = self._get_operate_message()
        self.logger.info(f"编辑岗位数据: {post_name} 为 {new_post_name}")
        self.logger.info(f"🔥编辑岗位消息: {message}")
        return message

    def click_delete_post(self, post_name: str):
        """点击删除岗位"""
        self.search_post(post_name)
        self.get_locator(self.TABLE_LIST).locator(f"tr:has-text('{post_name}')").locator("button").filter(has_text="删除").click()

    def delete_post(self, post_name: str):
        """删除岗位"""
        self.click_delete_post(post_name)
        # 确认删除
        self.click(self.SYS_PROMOPT_CONFIRM)
        
        message = self.get_text(self.OPERATE_MESSAGE)
        self.wait_for_locator(self.OPERATE_MESSAGE, state='detached')
        self.logger.info(f"🔥删除岗位: {post_name},🔥操作消息: {message}")
        return message

    def get_post_list(self) -> List[str]:
        """获取岗位列表"""
        locator = self.get_locator('post.post_list')
        elements = locator.all()
        return [element.text_content().strip() for element in elements]

    def close_add_post_dialog(self):
        """关闭新增岗位弹窗"""
        try:
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(300)
        except Exception:
            pass

    def close_all_dialogs(self):
        """关闭所有弹窗"""
        try:
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(300)
            for _ in range(3):
                if self.page.locator('[role="dialog"]').is_visible():
                    self.page.keyboard.press("Escape")
                    self.page.wait_for_timeout(200)
        except Exception:
            pass
