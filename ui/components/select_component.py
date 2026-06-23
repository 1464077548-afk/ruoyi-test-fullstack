from ui.pages.base_page import BasePage
from playwright.sync_api import expect


class SelectComponent(BasePage):
    """选择器组件"""

    def open_select(self, select_locator: str):
        """打开选择器"""
        self.click(select_locator)

    def select_option(self, option_locator: str):
        """选择选项"""
        self.click(option_locator)

    def get_selected_value(self, select_locator: str) -> str:
        """获取选中值"""
        locator = self.get_locator(select_locator)
        return locator.input_value()

    def select_treeselect(self, locator_key: str, value: str):
        """选择treeselect - 修复元素被移除的问题"""
        try:
            # 定位下拉触发框
            trigger = self.get_locator(locator_key)
            trigger.click()
            self.page.wait_for_timeout(500)
            
            # 尝试查找并选择节点
            # 方法1: 直接查找包含目标文本的选项
            options = self.page.locator(".vue-treeselect__option")
            if options.count() > 0:
                target_option = options.filter(has_text=value).first
                if target_option.is_visible():
                    target_option.click()
                    self.logger.info(f"🔥选择treeselect节点: {value}")
                    return
            
            # 方法2: 尝试展开节点后选择
            try:
                arrows = self.page.locator(".vue-treeselect__option-arrow")
                if arrows.count() > 0:
                    # 使用nth(0)而不是遍历所有，避免元素被移除
                    first_arrow = arrows.nth(0)
                    if first_arrow.is_visible():
                        first_arrow.click()
                        self.page.wait_for_timeout(300)
                        
                        # 再次尝试查找目标选项
                        target_option = self.page.locator(".vue-treeselect__option").filter(has_text=value).first
                        if target_option.is_visible(timeout=2000):
                            target_option.click()
                            self.logger.info(f"🔥选择treeselect节点(展开后): {value}")
                            return
            except Exception as e:
                self.logger.debug(f"展开节点失败(可能已展开): {e}")
            
            # 方法3: 尝试直接输入方式
            try:
                input_element = self.page.locator(".vue-treeselect__input").first
                if input_element.is_visible():
                    input_element.fill(value)
                    self.page.wait_for_timeout(500)
                    # 按回车确认
                    self.page.keyboard.press("Enter")
                    self.logger.info(f"🔥输入treeselect值: {value}")
                    return
            except Exception as e:
                self.logger.debug(f"输入方式失败: {e}")
            
            self.logger.warning(f"未能选择treeselect节点: {value}")
            
        except Exception as e:
            self.logger.error(f"选择treeselect失败: {e}")
