from ui.pages.modules.home_page import HomePage
from ui.biz.common_biz import CommonBiz
from config.settings import Settings
from playwright.sync_api import expect

class HomeBiz(CommonBiz):
    """首页业务逻辑""" 
    def __init__(self, page):
        super().__init__(page)
        self.home_page = HomePage(page)
    def verify_menu_visibility(self):
        """验证菜单可见性"""
        return self.home_page.is_menu_visible()
