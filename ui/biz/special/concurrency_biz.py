"""并发业务场景测试:并发登录、多标签、同账号多端"""
from ui.pages.modules.login_page import LoginPage
from ui.biz.normal.login_biz import LoginBiz
from config.settings import settings
class ConcurrencyBiz:
    def __init__(self, browser):
        self.browser = browser
        self.base_url = settings.base_url

    # ==================== 并发：多用户同时登录 ====================
    def multi_user_concurrent_login(self, user_pwd_list):
        """多账号并发登录系统"""
        context_pages = []
        for username, pwd in user_pwd_list:
            ctx = self.browser.new_context()
            page = ctx.new_page()
            page.goto(self.base_url)
            user_login_biz = LoginBiz(page)
            user_login_biz.login(username, pwd)
            context_pages.append((ctx, page))
        return context_pages

    # ==================== 并发：多标签页操作同一数据 ====================
    def multi_tab_operate_same_data(self, main_page, menu, search_key):
        """多标签同时操作同一条数据"""
        new_tab = main_page.context.new_page()
        new_tab.goto(f"{self.base_url}{menu}")
        # 等待页面加载
        main_page.wait_for_load_state("domcontentloaded")
        new_tab.wait_for_load_state("domcontentloaded")
        # 主标签搜索
        try:
            # 尝试使用更精确的定位
            search_input = main_page.locator("input[placeholder*='账号']")
            if search_input.count() == 0:
                search_input = main_page.locator("input[placeholder*='名称']")
            # 如果找到多个匹配，选择第一个
            if search_input.count() > 1:
                search_input = search_input.first
            search_input.fill(search_key)
            # 点击查询按钮
            search_button = main_page.locator("//span[text()='查询']")
            if search_button.count() == 0:
                search_button = main_page.locator("//button[contains(text(),'查询')]")
            if search_button.count() > 1:
                search_button = search_button.first
            search_button.click()
        except Exception as e:
            print(f"主标签搜索失败: {e}")
        # 新标签搜索
        try:
            # 尝试使用更精确的定位
            search_input = new_tab.locator("input[placeholder*='账号']")
            if search_input.count() == 0:
                search_input = new_tab.locator("input[placeholder*='名称']")
            if search_input.count() > 1:
                search_input = search_input.first
            search_input.fill(search_key)
            # 点击查询按钮
            search_button = new_tab.locator("//span[text()='查询']")
            if search_button.count() == 0:
                search_button = new_tab.locator("//button[contains(text(),'查询')]")
            if search_button.count() > 1:
                search_button = search_button.first
            search_button.click()
        except Exception as e:
            print(f"新标签搜索失败: {e}")
        return new_tab

    # ==================== 并发：同账号多端登录 ====================
    def same_user_multi_login(self, username, pwd, count=2):
        """同一账号多个客户端同时登录"""
        ctx_pages = []
        for _ in range(count):
            ctx = self.browser.new_context()
            page = ctx.new_page()
            page.goto(self.base_url)
            login_biz = LoginBiz(page)
            login_biz.login(username, pwd)
            ctx_pages.append((ctx, page))
        return ctx_pages