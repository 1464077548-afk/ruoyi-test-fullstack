from ui.pages.base_page import BasePage


class InputComponent(BasePage):
    """输入框组件"""

    def fill_input(self, locator_key: str, value: str):
        """填写输入框"""
        self.fill(locator_key, value)

    def get_input_value(self, locator_key: str) -> str:
        """获取输入框值"""
        return self.get_value(locator_key)

    def clear_input(self, locator_key: str):
        """清空输入框"""
        locator = self.get_locator(locator_key)
        locator.clear()

    def get_placeholder(self, locator_key: str) -> str:
        """获取输入框占位符"""
        locator = self.get_locator(locator_key)
        return locator.get_attribute("placeholder")
