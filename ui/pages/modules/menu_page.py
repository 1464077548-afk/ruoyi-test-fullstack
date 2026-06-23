from ui.pages.base_page import BasePage
from typing import List


class MenuPage(BasePage):
    """菜单管理页面"""
    OPERATE_MESSAGE= 'common.operate_message'
    TABLE_LIST = 'common.table_list'

    # ========== 新增功能 ==========
    ADD_BUTTON = 'common.add_button'
    MENU_NAME_INPUT = 'menu.menu_name_input'
    MENU_PATH_INPUT = 'menu.menu_path_input'
    MENU_SORT_INPUT = 'menu.menu_sort_input'
    MENU_TYPE_SELECT = 'menu.menu_type'
    SAVE_BUTTON = 'menu.save_button'
    MENU_SEARCH_INPUT = 'menu.search_input'
    MENU_SEARCH_BUTTON = 'menu.search_button'
    
    EDIT_MENU_NAME_INPUT = 'menu.edit_menu_name_input'
    CONFIRM_DELETE_BUTTON = 'menu.confirm_delete_button'



    def goto_menu_management(self):
        """导航到菜单管理页面"""
        self.goto("/system/menu")
        self.wait_for_load_state()
    
    def click_add_menu(self):
        """点击新增菜单"""
        self.click(self.ADD_BUTTON)
        self.wait_for_load_state()
    
    def fill_menu_form(self, menu_name: str, menu_path: str, menu_sort: int, menu_type: str):
        """填写菜单表单"""
        self.fill(self.MENU_NAME_INPUT, menu_name)
        self.fill(self.MENU_PATH_INPUT, menu_path)
        self.fill(self.MENU_SORT_INPUT, str(menu_sort))
        # 使用 MENU_TYPE_SELECT 定位器，并传递 menu_type 参数来替换占位符
        option = self.get_locator(self.MENU_TYPE_SELECT, menu_type=menu_type)
        option.click()

    def click_save_menu(self):
        """点击保存菜单"""
        self.click(self.SAVE_BUTTON)
        self.wait_for_load_state()
    
    def click_cancel_menu(self):
        """点击取消"""
        self.click('menu.cancel_button')
        self.wait_for_load_state()
    
    def get_menu_tree(self) -> List[str]:
        """获取菜单树"""
        try:
            # 方法1: 使用 menu_tree 定位器
            locator = self.get_locator('menu.menu_tree')
            elements = locator.all()
            menus = [element.text_content().strip() for element in elements]
            if menus:
                print(f"通过 menu_tree 定位器获取到菜单: {menus}")
                return menus
            
            # 方法2: 尝试通过侧边栏获取菜单
            print("menu_tree 定位器未找到菜单，尝试通过侧边栏获取")
            sidebar_menu = self.page.locator('.el-menu-item')
            elements = sidebar_menu.all()
            menus = [element.text_content().strip() for element in elements]
            if menus:
                print(f"通过侧边栏获取到菜单: {menus}")
                return menus
            
            # 方法3: 尝试通过其他常见的菜单选择器
            print("侧边栏未找到菜单，尝试通过其他选择器获取")
            other_menu = self.page.locator('.menu-item')
            elements = other_menu.all()
            menus = [element.text_content().strip() for element in elements]
            if menus:
                print(f"通过其他选择器获取到菜单: {menus}")
                return menus
            
            # 方法4: 尝试通过文本内容查找
            print("其他选择器未找到菜单，尝试通过文本内容查找")
            menu_items = self.page.get_by_text("用户管理").all()
            if menu_items:
                print("找到用户管理菜单")
                return ["用户管理"]
            
            print("未找到任何菜单")
            return []
        except Exception as e:
            print(f"获取菜单树失败: {e}")
            return []
    def search_menu(self, menu_name: str):
        """搜索菜单"""
        self.fill(self.MENU_SEARCH_INPUT, menu_name)
        self.click(self.MENU_SEARCH_BUTTON)
        self.wait_for_load_state()
    
    def click_edit_menu(self, menu_name: str):
        """点击编辑菜单"""
        self.search_menu(menu_name)
        self.get_locator(self.TABLE_LIST).locator(f"tr:has-text('{menu_name}')").locator("button").filter(has_text="修改").click()
    
    def click_delete_menu(self, menu_name: str):
        """点击删除菜单"""
        self.search_menu(menu_name)
        self.get_locator(self.TABLE_LIST).locator(f"tr:has-text('{menu_name}')").locator("button").filter(has_text="删除").click()
    
    def confirm_delete(self):
        """确认删除"""
        self.click(self.CONFIRM_DELETE_BUTTON)
        self.wait_for_load_state()

    def create_menu(self, menu_data: dict):
        """创建菜单"""
        self.click_add_menu()
        self.fill_menu_form(menu_data['menuName'], menu_data['path'], menu_data['orderNum'], menu_data['type'])
        self.click_save_menu()
        message = self.get_text(self.OPERATE_MESSAGE)
        self.wait_for_locator(self.OPERATE_MESSAGE,state='detached')
        self.logger.info(f"创建菜单数据: {menu_data}")
        self.logger.info(f"🔥创建菜单消息: {message}")
        return message
    
    def edit_menu(self, menu_name: str, new_menu_name: str):
        """编辑菜单"""
        self.click_edit_menu(menu_name)
         # 填写编辑后的菜单信息
        self.fill(self.EDIT_MENU_NAME_INPUT, new_menu_name)
        self.click_save_menu()

        message = self.get_text(self.OPERATE_MESSAGE)
        self.wait_for_locator(self.OPERATE_MESSAGE,state='detached')
        self.logger.info(f"编辑菜单数据: {menu_name} 为 {new_menu_name}")
        self.logger.info(f"🔥编辑菜单消息: {message}")
        print(f"🔥编辑菜单消息: {message}", flush=True)
        return message
    
    def delete_menu(self, menu_name: str):
        """删除菜单"""
        self.click_delete_menu(menu_name)
        # 确认删除
        self.click(self.CONFIRM_DELETE_BUTTON)

        message = self.get_text(self.OPERATE_MESSAGE)
        # 等待消息从dom中移除
        self.wait_for_locator(self.OPERATE_MESSAGE, state='detached')
        print(f"🔥操作消息: {message}", flush=True)
        self.logger.info(f"🔥删除菜单: {menu_name},🔥操作消息: {message}")
        return message