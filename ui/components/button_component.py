from ui.pages.base_page import BasePage


class ButtonComponent(BasePage):
    """按钮组件"""

    def __init__(self, page, locator=None):
        """初始化"""
        # 检查 page 是否有 page 属性（如 LoginPage 对象）
        if hasattr(page, 'page'):
            super().__init__(page.page)
        else:
            super().__init__(page)
        self.locator = locator

    def click(self, locator_key=None):
        """点击按钮"""
        if locator_key:
            super().click(locator_key)
        elif self.locator:
            self.page.locator(self.locator).click()

    def is_visible(self, locator_key=None) -> bool:
        """检查按钮是否可见"""
        if locator_key:
            return super().is_visible(locator_key)
        elif self.locator:
            return self.page.locator(self.locator).is_visible()
        return False

    def is_enabled(self, locator_key=None) -> bool:
        """检查按钮是否可用"""
        if locator_key:
            return super().is_enabled(locator_key)
        elif self.locator:
            return self.page.locator(self.locator).is_enabled()
        return False

    def get_text(self, locator_key=None) -> str:
        """获取按钮文本"""
        if locator_key:
            return super().get_text(locator_key)
        elif self.locator:
            return self.page.locator(self.locator).text_content().strip()
        return ""

    def hover(self, locator_key=None):
        """悬停按钮"""
        if locator_key:
            locator = self.get_locator(locator_key)
        elif self.locator:
            locator = self.page.locator(self.locator)
        else:
            return
        locator.hover()

    def get_icon(self, locator_key=None):
        """获取按钮图标"""
        if locator_key:
            locator = self.get_locator(locator_key)
        elif self.locator:
            locator = self.page.locator(self.locator)
        else:
            return None
        icon = locator.locator('i').first
        return icon if icon.is_visible() else None
