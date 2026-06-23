from ui.pages.modules.role_page import RolePage
from ui.biz.common_biz import CommonBiz
from playwright.sync_api import expect
import logging
class RoleBiz:
    def __init__(self, page):
        self.page = page
        self.role = RolePage(page)
        self.common = CommonBiz(page)
        self.logger = logging.getLogger(__name__)

    def add_role(self, test_role_data: dict):
        print(f"📋 开始创建角色: {test_role_data.get('roleName')}")
        self.role.click_add_role()
        self.role.fill_role_name(test_role_data['roleName'])
        self.role.fill_role_key(test_role_data['roleKey'])
        self.role.fill_role_sort(test_role_data['roleSort'])
        
        # 菜单分配
        if 'menuNames' in test_role_data:
            menu_names = test_role_data['menuNames']
            print(f"📋 准备分配菜单: {menu_names}")
            self.role.fill_menu_names(menu_names)
        else:
            print("⚠️ 未提供菜单列表")
        
        self.role.click_save_role()
        message = self.common.get_operate_message()
        self.logger.info(f"🔥创建角色: {test_role_data},🔥操作消息: {message}")
        if "成功" not in message:
            self.role.close_all_dialogs()
        return message



    def assign_data_permissions(self, role_name, option_text):
        self.common.common_search(self.role, role_name)
        
        self.role.click_more_button(role_name)
        # 点击数据权限
        self.role.click_data_permission_button()
        # 点击数据权限选项
        self.role.click_data_permission_option(option_text)
        # 确认操作
        self.role.click_save_role()
   
        message = self.common.get_operate_message()
        if "成功" not in message:
            #关闭新增角色的弹窗
            self.role.close_all_dialogs()
        return message

    def switch_tab(self, tab_name: str):
        """切换到指定tab页"""
        self.role.switch_tab(tab_name)
        self.logger.info(f"✅切换到 {tab_name} tab页")
        
    def close_tab(self):
        """关闭当前tab页"""
        self.role.close_tab()
        self.logger.info(f"✅关闭当前 tab页")
    
    def delete_role(self, role_name: str):
        """删除角色"""
        self.logger.info(f"❎开始删除角色: {role_name}")
        result = self.common.common_search(self.role, role_name)
        if not result:
            raise Exception(f"未找到角色: {role_name}")
        self.role.click_delete_role(role_name)
        self.common.confirm_dialog()
        message = self.common.get_operate_message()
        if "成功" not in message:
            #关闭新增角色的弹窗
            self.role.close_all_dialogs()
        else:
            self.logger.info(f"✅删除角色成功: {role_name}")
        return message

    def get_role_list(self):
        """获取角色列表"""
        role_list = self.role.get_role_list()
        return role_list
    def edit_role(self, role_name: str, new_role_name: str):
        """编辑角色"""
        self.logger.info(f"🔥开始编辑角色: {role_name} 为 {new_role_name}")
        self.role.click_edit_role(role_name)
        # 填写编辑后的角色信息
        self.role.fill_edit_role_form(new_role_name)
        self.role.click_save_role()
        message = self.common.get_operate_message()
        self.logger.info(f"✅编辑角色消息: {message}")
        if "成功" not in message:
            #关闭新增角色的弹窗
            self.role.close_all_dialogs()
        return message
    def search_role_by_name(self, role_name: str):
        """按角色名搜索角色"""
        self.role.fill_search_input(role_name)
        self.role.click_search_button()
        self.page.wait_for_timeout(500)  # 等待搜索结果加载
        role_info = self.get_role_list_from_table(role_name)

        return role_info

    def toggle_role_status(self, role_name: str):
        """切换角色状态"""
        try:
            # 搜索
            self.role.fill_search_input(role_name)
            self.role.click_search_button()
            self.page.wait_for_timeout(500)
            
            # 先查找所有行，找到角色名列完全匹配的那一行
            rows = self.role.get_locator(self.role.TABLE_LIST).all()
            target_row = None
            
            for row in rows:
                try:
                    role_name_cell = row.locator("td:nth-child(3)")
                    if role_name_cell.is_visible():
                        if role_name_cell.text_content().strip() == role_name:
                            target_row = row
                            break
                except:
                    continue
            
            if not target_row:
                raise Exception(f"未找到角色: {role_name}")
            
            # 点击状态切换按钮
            status_locator = '[role="switch"]'
            status_button = target_row.locator(status_locator).first
            status_button.click()
            # 确认操作
            self.common.click(self.role.SYS_PROMOPT_CONFIRM)
            # 获取操作消息
            message = self.common.get_operate_message()
            if "成功" not in message:
                #关闭新增角色的弹窗
                self.role.close_all_dialogs()
            return message
        except Exception as e:
            self.logger.error(f"状态切换失败: {e}")
            return "状态切换失败"

     
    def assign_user(self, role_name: str, user_name: str):
        """给角色分配用户"""
        print(f"给角色 {role_name} 分配用户 {user_name}")
        # 找到包含指定角色名的行，然后点击分配用户按钮
        self.search_role_by_name(role_name)
        
        # 先查找所有行，找到角色名列完全匹配的那一行
        rows = self.role.get_locator(self.role.TABLE_LIST).all()
        target_row = None
        
        for row in rows:
            try:
                role_name_cell = row.locator("td:nth-child(3)")
                if role_name_cell.is_visible():
                    if role_name_cell.text_content().strip() == role_name:
                        target_row = row
                        break
            except:
                continue
        
        if not target_row:
            raise Exception(f"未找到角色: {role_name}")
        
        # 点击更多按钮
        more_button = target_row.locator("button").filter(has_text="更多").first
        more_button.click()
        
        # 等待下拉菜单出现
        self.page.wait_for_timeout(300)
        
        # 直接在页面中查找分配用户按钮
        # 由于是下拉菜单，使用text定位
        data_permission_button = self.page.get_by_text("分配用户")
        data_permission_button.click()
        
        # 等待对话框打开
        self.page.wait_for_timeout(500)
        
        #点击添加用户按钮
        add_user_button = self.page.get_by_role("button", name="添加用户")
        add_user_button.click()
        
        # 等待选择用户对话框
        self.page.wait_for_timeout(500)
        
        #选择用户
        chose_user_dialog = self.page.get_by_role("dialog", name="选择用户")
        chose_user_dialog.get_by_placeholder("请输入用户名").fill(user_name)
        chose_user_dialog.get_by_role("button", name="搜索").click()
        
        # 等待搜索结果
        self.page.wait_for_timeout(500)
        
        #勾选用户
        table = chose_user_dialog.locator("table tr")
        row_locator = table.filter(has_text=f"{user_name}")
        checkbox = row_locator.locator(".el-checkbox__input").first
        checkbox.click()
        self.logger.info(f"✅成功勾选用户: {user_name}")
        
        #确认操作
        chose_user_dialog.get_by_role("button", name="确 定").click()
        
        # 等待对话框关闭
        self.page.wait_for_timeout(500)
        
        message = self.common.get_operate_message()
        
        # 验证分配是否成功
        if "成功" not in message:
            print(f"⚠️ 分配用户可能失败: {message}")
            self.role.close_all_dialogs()
        
        return message

    def search_role_by_key(self, role_key: str):
        """按角色键搜索角色"""
        self.role.fill_search_rolekey_input(role_key)
        self.role.click_search_button()
        # 等待搜索结果加载
        self.role.wait_for_load_state()
        self.role.wait_for_timeout(500)
        role_info = self.get_role_list_from_table(role_key)

        return role_info
    def get_role_list_from_table(self, keyword: str):
        """从表格中获取角色列表（同时匹配角色名和角色键）"""
        role_info = {
            "roleName": "",
            "roleKey": "",
            "roleSort": "",
            "status": ""
        }
        
        try:
            # 获取表格body
            table_body = self.role.get_locator(self.role.TABLE_LIST)
            # 获取所有行
            rows = table_body.locator("tr").all()
            print(f"找到 {len(rows)} 行数据")
            
            # 遍历每行，找到角色名或角色键完全匹配的那一行
            for row in rows:
                try:
                    role_name_cell = row.locator("td:nth-child(3)")
                    role_key_cell = row.locator("td:nth-child(4)")
                    
                    if role_name_cell.is_visible() and role_key_cell.is_visible():
                        role_name = role_name_cell.text_content().strip()
                        role_key = role_key_cell.text_content().strip()
                        
                        print(f"检查行: roleName={role_name}, roleKey={role_key}")
                        
                        # 匹配角色名或角色键
                        if role_name == keyword or role_key == keyword:
                            print(f"✅ 角色 {keyword} 在UI表格中找到")
                            role_info = {
                                "roleName": role_name,
                                "roleKey": role_key,
                                "roleSort": row.locator("td:nth-child(5)").text_content().strip(),
                                "status": row.get_by_role("switch").first.get_attribute("aria-checked")
                            }
                            break
                except Exception as e:
                    print(f"处理行时出错: {e}")
                    continue
            
            if not role_info["roleName"]:
                print(f"❌ 角色 {keyword} 未在UI表格中找到")
        
        except Exception as e:
            print(f"获取表格数据失败: {e}")
        
        self.logger.info(f"🔥搜索角色: {keyword},🔥角色信息: {role_info}")
        return role_info
