from ui.pages.base_page import BasePage


class DialogComponent(BasePage):
    """对话框组件"""

    def __init__(self, page):
        """初始化"""
        # 检查 page 是否有 page 属性（如 LoginPage 对象）
        if hasattr(page, 'page'):
            super().__init__(page.page)
        else:
            super().__init__(page)

    def is_visible(self):
        """对话框是否可见"""
        return self.page.locator('.el-dialog').is_visible()

    def get_title(self):
        """获取对话框标题"""
        title = self.page.locator('.el-dialog__title').text_content()
        return title.strip() if title else ""

    def close(self):
        """关闭对话框"""
        close_button = self.page.locator('.el-dialog__headerbtn')
        if close_button.is_visible():
            close_button.click()

    def cancel(self):
        """取消对话框"""
        cancel_button = self.page.locator('.el-dialog__footer .el-button--default')
        if cancel_button.is_visible():
            cancel_button.click()

    def submit(self):
        """提交对话框"""
        submit_button = self.page.locator('.el-dialog__footer .el-button--primary')
        if submit_button.is_visible():
            submit_button.click()

    def click_overlay(self):
        """点击遮罩层"""
        overlay = self.page.locator('.el-dialog__wrapper')
        if overlay.is_visible():
            # 点击遮罩层（非对话框内容区域）
            overlay.click(position={'x': 10, 'y': 10})

    def open_dialog(self, trigger_locator: str):
        """打开对话框"""
        self.click(trigger_locator)

    def close_dialog(self, close_locator: str):
        """关闭对话框"""
        self.click(close_locator)

    def is_dialog_visible(self, dialog_locator: str) -> bool:
        """检查对话框是否可见"""
        return self.is_visible(dialog_locator)

    def confirm_dialog(self, confirm_locator: str):
        """确认对话框"""
        self.click(confirm_locator)
