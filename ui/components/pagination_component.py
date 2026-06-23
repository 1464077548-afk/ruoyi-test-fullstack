from ui.pages.base_page import BasePage


class PaginationComponent(BasePage):
    """分页组件"""

    def go_to_page(self, page_number: int, page_input_locator: str, confirm_button_locator: str):
        """跳转到指定页面"""
        self.fill(page_input_locator, str(page_number))
        self.click(confirm_button_locator)

    def go_to_next_page(self, next_page_locator: str):
        """跳转到下一页"""
        self.click(next_page_locator)

    def go_to_previous_page(self, previous_page_locator: str):
        """跳转到上一页"""
        self.click(previous_page_locator)

    def go_to_first_page(self, first_page_locator: str):
        """跳转到第一页"""
        self.click(first_page_locator)

    def go_to_last_page(self, last_page_locator: str):
        """跳转到最后一页"""
        self.click(last_page_locator)

    def get_current_page(self, current_page_locator: str) -> int:
        """获取当前页码"""
        current_page_text = self.get_text(current_page_locator)
        return int(current_page_text)
