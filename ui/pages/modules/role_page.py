from ui.pages.modules.base_module_page import BaseModulePage
from typing import List





class RolePage(BaseModulePage):
    """角色管理页面"""
    #=============公共元素=============
    MORE_BUTTON = 'common.more_button'
    TABLE_LIST = 'common.table_list'
    SAVE_BUTTON = 'common.save_button'
    SWITCH_TAB = 'common.switch_tab'
    CLOSE_TAB = 'common.close_tab'



    #=============搜索=============
    SEARCH_INPUT = 'role.search_input'
    SEARCH_ROLEKEY_INPUT = 'role.search_roleKey'
    SEARCH_BUTTON = 'role.search_button'

    ADD_ROLE_BUTTON = 'role.add_button'
    DELETE_ROLE_BUTTON = 'role.delete_button'
    SAVE_BUTTON = 'role.save_button'



    #=============新增角色=============
    ADD_ROLE_DIALOG = 'role.add_dialog'
    ADD_ROLE_NAME_INPUT = 'role.roleName'
    ADD_ROLE_KEY_INPUT = 'role.roleKey'
    ADD_ROLE_SORT_INPUT = 'role.roleSort'
    # SAVE_BUTTON = 'role.save_button'
    CANCEL_BUTTON = 'role.cancel_button'
    ADD_ROLE_CANCEL_BUTTON ='role.add_role_cancel_button'
    CLOSE_BUTTON = 'role.close_button'

    CONFIRM_DELETE = 'role.confirm_delete'
    #=============分配权限=============
    ASSIGN_PERMISSIONS_BUTTON = 'role.assign_permissions_button'
    CHOSE_PERMISSIONS_BUTTON = 'role.chose_permissions_button'
    #=============编辑角色=============
    EDIT_ROLE_NAME_INPUT = 'role.edit_roleName'

    #=============操作消息=============
    OPERATE_MESSAGE = 'common.operate_message'
    SYS_PROMOPT_CONFIRM = 'common.sys_prompt_confirm'
    SYS_PROMOPT_CANCEL = 'user.sys_prompt_cancel'
    
    def goto_role_management(self):
        """导航到角色管理页面"""
        self.goto("/system/role")
    
    def click_add_role(self):
        """点击新增角色"""
        self.click(self.ADD_ROLE_BUTTON)
        self.wait_for_load_state()
    def fill_role_name(self, role_name: str):
        """填写角色名称"""
        self.fill(self.ADD_ROLE_NAME_INPUT, role_name)
    def fill_role_key(self, role_key: str):
        """填写角色键值"""
        self.fill(self.ADD_ROLE_KEY_INPUT, role_key)
    def fill_role_sort(self, role_sort: int):
        """填写角色排序"""
        self.fill(self.ADD_ROLE_SORT_INPUT, str(role_sort))
    def switch_tab(self, tab_name: str):
        """切换tab页"""
        # self.get_locator(self.SWITCH_TAB, tab_name=tab_name).click()
        self.click(self.SWITCH_TAB, tab_name=tab_name)

    def close_tab(self):
        """关闭当前tab页"""
        self.click(self.CLOSE_TAB)
    def click_cancel_role_dialog(self):
        """点击新增角色弹窗取消按钮"""
        try:   
            self.click(self.ADD_ROLE_CANCEL_BUTTON)
            self.logger.info("✅ 点击「取消」按钮成功关闭添加角色弹窗")
        except Exception as e:
            print(f"点击取消角色弹窗失败: {e}")
            # 使用CSS选择器直接定位关闭按钮
            try:
                self.click(self.CLOSE_BUTTON)
                print("✅ 点击关闭按钮成功关闭添加角色弹窗")
            except Exception as e2:
                print(f"点击关闭按钮失败: {e2}")
                # 尝试按ESC键关闭弹窗
                self.page.keyboard.press("Escape")
                print("✅ 通过Escape键关闭添加角色弹窗")

    def close_all_dialogs(self):
        """关闭所有弹窗"""
        self.page.keyboard.press("Escape")
        print("✅ 通过Escape键关闭所有弹窗")

    def fill_menu_names(self, menu_names: List[str]):
        """填写菜单名称 - 展开菜单树并选择指定子菜单"""
        # 等待菜单树加载
        self.page.wait_for_timeout(1500)
        
        # 先展开菜单树
        self._expand_menu_tree_full()
        
        # 先取消所有勾选（确保干净状态）
        self._clear_all_menu_checkboxes()
        
        # 选择指定的菜单
        for menu_name in menu_names:
            success = self._select_menu_with_retry(menu_name)
            
            if success:
                print(f"✅成功选择菜单: {menu_name}")
            else:
                print(f"❌未能选择菜单: {menu_name}")
    
    def _select_menu_with_retry(self, menu_name: str) -> bool:
        """选择菜单，带有重试机制"""
        attempts = [
            lambda: self._select_menu_by_checkbox_label(menu_name),
            lambda: self._select_menu_directly(menu_name),
            lambda: self._select_menu_by_tree_text(menu_name)
        ]
        
        for attempt in attempts:
            try:
                if attempt():
                    return True
            except Exception as e:
                print(f"尝试选择菜单 {menu_name} 失败: {e}")
        
        # 如果前几种方法都失败，尝试更直接的方法
        try:
            return self._select_menu_fallback(menu_name)
        except Exception as e:
            print(f"fallback选择菜单 {menu_name} 失败: {e}")
            return False
    
    def _select_menu_fallback(self, menu_name: str) -> bool:
        """备选菜单选择方法"""
        # 尝试查找包含菜单名称的树节点
        tree_items = self.page.locator(".el-tree-node")
        for i in range(tree_items.count()):
            try:
                item = tree_items.nth(i)
                if item.is_visible():
                    label = item.locator(".el-tree-node__label")
                    if label.count() > 0:
                        label_text = label.first.text_content().strip()
                        if label_text == menu_name:
                            checkbox = item.locator(".el-checkbox__input")
                            if checkbox.count() > 0:
                                checkbox.first.click()
                                self.page.wait_for_timeout(200)
                                return True
            except Exception:
                continue
        return False
    
    def _expand_menu_tree_full(self):
        """完全展开菜单树"""
        try:
            # 尝试点击展开/折叠按钮
            expand_button = self.page.get_by_text("展开/折叠")
            if expand_button.count() > 0 and expand_button.first.is_visible():
                expand_button.first.click()
                self.page.wait_for_timeout(1500)
                print("✅通过展开/折叠按钮展开菜单树")
                return
            
            # 如果没有展开按钮，尝试点击所有展开箭头
            expand_icons = self.page.locator(".el-tree-node__expand-icon")
            for i in range(expand_icons.count()):
                try:
                    icon = expand_icons.nth(i)
                    if icon.is_visible() and icon.is_enabled():
                        icon.click()
                        self.page.wait_for_timeout(200)
                except Exception:
                    continue
            print("✅通过点击展开箭头展开菜单树")
        except Exception as e:
            print(f"展开菜单树失败: {e}")
    
    def _clear_all_menu_checkboxes(self):
        """清除所有已勾选的菜单复选框"""
        try:
            # 找到所有已勾选的复选框
            checked_checkboxes = self.page.locator(".el-checkbox__input.is-checked")
            for i in range(checked_checkboxes.count()):
                try:
                    checkbox = checked_checkboxes.nth(i)
                    if checkbox.is_visible():
                        checkbox.click()
                        self.page.wait_for_timeout(100)
                except Exception:
                    continue
            print("✅已清除所有已勾选的菜单")
        except Exception as e:
            print(f"清除菜单勾选失败: {e}")
    
    def _expand_menu_tree(self):
        """展开菜单树"""
        try:
            expand_button = self.page.get_by_text("展开/折叠")
            if expand_button.count() > 0 and expand_button.first.is_visible():
                expand_button.first.click()
                self.page.wait_for_timeout(1000)
                print("✅通过展开/折叠按钮展开菜单树")
                return
        except Exception as e:
            print(f"尝试展开/折叠按钮失败: {e}")
    
    def _select_menu_directly(self, menu_name: str) -> bool:
        """直接选择菜单，不展开父菜单"""
        try:
            # 直接查找包含菜单名的元素
            elements = self.page.locator(f".el-tree-node__label:has-text('{menu_name}')")
            count = elements.count()
            print(f"_select_menu_directly: 找到 {count} 个匹配 '{menu_name}' 的标签")
            
            if count > 0:
                element = elements.first
                # 先尝试滚动到元素位置
                element.scroll_into_view_if_needed()
                self.page.wait_for_timeout(300)
                
                if element.is_visible():
                    # 找到父节点的复选框（不包含父菜单的复选框）
                    checkbox = element.locator("..").locator(".el-checkbox__input")
                    if checkbox.count() > 0:
                        checkbox.first.scroll_into_view_if_needed()
                        checkbox.first.click()
                        print(f"_select_menu_directly: 成功点击 '{menu_name}' 的复选框")
                        return True
                    else:
                        print(f"_select_menu_directly: 未找到 '{menu_name}' 的复选框")
                else:
                    print(f"_select_menu_directly: '{menu_name}' 元素不可见")
            return False
        except Exception as e:
            print(f"_select_menu_directly: 异常 - {e}")
            return False
    
    def _select_menu_by_checkbox_label(self, menu_name: str) -> bool:
        """通过标签选择菜单"""
        try:
            checkbox_label = self.page.locator(".el-checkbox__label").filter(has_text=menu_name)
            count = checkbox_label.count()
            print(f"_select_menu_by_checkbox_label: 找到 {count} 个匹配 '{menu_name}' 的标签")
            
            if count > 0:
                checkbox_label.first.wait_for(state="visible", timeout=5000)
                checkbox_label.first.scroll_into_view_if_needed()
                # 点击复选框（不是标签）
                checkbox = checkbox_label.first.locator("..").locator(".el-checkbox__input")
                if checkbox.count() > 0:
                    checkbox.first.click()
                    print(f"_select_menu_by_checkbox_label: 成功点击 '{menu_name}' 的复选框")
                    return True
                else:
                    print(f"_select_menu_by_checkbox_label: 未找到 '{menu_name}' 的复选框")
            return False
        except Exception as e:
            print(f"_select_menu_by_checkbox_label: 异常 - {e}")
            return False
    
    def _select_menu_by_tree_text(self, menu_name: str) -> bool:
        """通过树文本选择菜单"""
        try:
            menu_element = self.page.locator(".el-tree").get_by_text(menu_name)
            count = menu_element.count()
            print(f"_select_menu_by_tree_text: 找到 {count} 个匹配 '{menu_name}' 的树节点")
            
            if count > 0:
                # 先滚动到元素位置
                menu_element.first.scroll_into_view_if_needed()
                self.page.wait_for_timeout(300)
                
                # 尝试点击元素使其可见（可能需要展开父节点）
                try:
                    menu_element.first.click()
                    self.page.wait_for_timeout(300)
                except Exception:
                    pass
                
                # 再次检查是否可见
                if menu_element.first.is_visible():
                    # 尝试直接点击文本旁边的复选框
                    checkbox = menu_element.first.locator("..").locator(".el-checkbox__input")
                    if checkbox.count() > 0:
                        checkbox.first.scroll_into_view_if_needed()
                        checkbox.first.click()
                        print(f"_select_menu_by_tree_text: 成功点击 '{menu_name}' 的复选框")
                        return True
                    else:
                        print(f"_select_menu_by_tree_text: 未找到 '{menu_name}' 的复选框")
                else:
                    print(f"_select_menu_by_tree_text: '{menu_name}' 元素仍不可见")
            return False
        except Exception as e:
            print(f"_select_menu_by_tree_text: 异常 - {e}")
            return False
            

    def fill_role_form(self, role_data: dict):
        """填写角色表单"""
        print(f"填写角色表单: {role_data}")
        self.fill(self.ADD_ROLE_NAME_INPUT, role_data['roleName'])
        self.fill(self.ADD_ROLE_KEY_INPUT, role_data['roleKey'])
        self.fill(self.ADD_ROLE_SORT_INPUT, str(role_data['roleSort']))
        if 'menuNames' in role_data:
            self.fill_menu_names(role_data['menuNames'])
    
    def click_save_role(self):
        """点击保存角色"""
        self.click(self.SAVE_BUTTON)
        
    def create_role(self, role_data: dict):
        """创建角色"""
        self.click_add_role()
        self.fill_role_form(role_data)
        
        self.click_save_role()
        # 等待操作完成
        self.is_visible(self.OPERATE_MESSAGE)
        message = self.get_text(self.OPERATE_MESSAGE)
        #等待消息从dom中移除
        self.wait_for_locator(self.OPERATE_MESSAGE, state='detached')
        print(f"🔥操作消息: {message}", flush=True)
        self.logger.info(f"🔥创建角色: {role_data},🔥操作消息: {message}")
        return message
  
    def assign_permissions(self, role_name, option_text):
        """
        分配角色权限

        Returns:
            str: 操作结果信息
        """
        # 搜索角色
        self.search_role_by_name(role_name)
        
        # 等待表格加载完成
        self.wait_for_load_state()
        
        # 找到包含指定角色名的行
        rows = self.get_locator(self.TABLE_LIST).filter(has_text=role_name)
        # 点击该行的更多按钮
        # 直接在该行中查找更多按钮
        more_button = rows.locator("button").filter(has_text="更多")
        more_button.click()
        
        # 直接在页面中查找数据权限按钮
        # 由于是下拉菜单，使用text定位
        data_permission_button = self.page.get_by_text("数据权限")
        data_permission_button.click()
        
        # 等待权限分配弹窗
        self.wait_for_load_state()
        
        # 点击选择权限按钮
        self.click(self.CHOSE_PERMISSIONS_BUTTON)
        
        # 选择全部数据权限
        # 找到包含指定文本的选项
        permission_option = self.page.get_by_text(option_text)
        permission_option.click()
        
        # 点击确认按钮
        self.click(self.SAVE_BUTTON)

        # 等待操作完成
        self.wait_for_locator(self.OPERATE_MESSAGE)
        message = self.get_text(self.OPERATE_MESSAGE)
        # 等待消息从dom中移除
        self.wait_for_locator(self.OPERATE_MESSAGE, state='detached')
        print(f"🔥操作消息: {message}", flush=True)
        self.logger.info(f"🔥分配角色权限: {role_name},🔥操作消息: {message}")
        return message

    def fill_search_input(self, keyword: str):
        """填写搜索输入框"""
        self.fill(self.SEARCH_INPUT, keyword)
    def click_search_button(self):
        """点击搜索按钮"""
        self.click(self.SEARCH_BUTTON)

    def click_cancel_role(self):
        """点击取消"""
        self.click(self.CANCEL_BUTTON)

    def search_role_by_name(self, keyword: str):
        """搜索角色（精确匹配）"""
        self.wait_for_load_state()
        
        search_input = self.get_locator(self.SEARCH_INPUT)
        search_input.clear()
        search_input.fill(keyword)
        
        self.wait_for_timeout(500)
        self.page.keyboard.press("Enter")
        
        self.wait_for_load_state()
        self.wait_for_timeout(2000)
    def fill_search_rolekey_input(self, keyword: str):
        """填写角色键搜索输入框"""
        self.fill(self.SEARCH_ROLEKEY_INPUT, keyword)
    
    def search_role_by_key(self, keyword: str):
        self.fill(self.SEARCH_ROLEKEY_INPUT, keyword)
        return self.search_role(keyword)
    def close_add_role_dialog(self):
        """关闭新增角色弹窗"""
        self.click(self.ADD_ROLE_CANCEL_BUTTON)
    def search_role(self, keyword: str):
        """搜索角色"""
        self.search(keyword, self.SEARCH_INPUT, self.SEARCH_BUTTON)
        
        # 等待搜索结果加载
        self.wait_for_load_state()
        self.wait_for_timeout(500)
        
        # 查找完全匹配的行
        rows = self.get_locator(self.TABLE_LIST).locator("tr").all()
        target_row = None
        
        for row in rows:
            try:
                role_name_cell = row.locator("td:nth-child(3)")
                if role_name_cell.is_visible():
                    cell_text = role_name_cell.text_content().strip()
                    if cell_text == keyword:
                        target_row = row
                        break
            except Exception:
                continue
        
        if target_row is None:
            # 如果没有完全匹配，返回空信息
            return {
                "roleName": "",
                "roleKey": "",
                "roleSort": "",
                "status": ""
            }
        
        role_info = {
            "roleName": target_row.locator("td:nth-child(3)").text_content().strip(),
            "roleKey": target_row.locator("td:nth-child(4)").text_content().strip(),
            "roleSort": target_row.locator("td:nth-child(5)").text_content().strip(),
            "status": target_row.get_by_role("switch").get_attribute("aria-checked") if target_row.get_by_role("switch").count() > 0 else ""
        }
        self.logger.info(f"🔥搜索角色: {keyword},🔥角色信息: {role_info}")
        return role_info
    
    def get_role_list(self) -> List[str]:
        """获取角色列表"""
        locator = self.get_locator(self.TABLE_LIST).locator("td:nth-child(3)")
        elements = locator.all()
        return [element.text_content().strip() for element in elements]

    def click_delete_role(self, role_name: str):
        """点击删除角色"""
        self.get_locator(self.TABLE_LIST).filter(has_text=role_name).locator("button").filter(has_text="删除").click()

    def click_edit_role(self, role_name: str):
        """点击编辑角色"""
        self.search_role_by_name(role_name)
        self.get_locator(self.TABLE_LIST).filter(has_text=role_name).locator("button").filter(has_text="修改").click()
    def fill_edit_role_form(self, role_name: str):
        """填写编辑角色表单"""
        self.fill(self.EDIT_ROLE_NAME_INPUT, role_name)
    def click_more_button(self, role_name: str):
        """点击更多按钮"""
        row = self.get_locator(self.TABLE_LIST).filter(has_text=role_name)
        more_button = row.locator("button").filter(has_text="更多")
        more_button.click()
        return more_button
    def click_data_permission_button(self):
        """点击数据权限按钮"""
        data_permission_button = self.page.get_by_text("数据权限")
        data_permission_button.click()
        return data_permission_button
    def click_data_permission_option(self, option_text: str):
        """点击数据权限选项"""
        dialog = self.page.get_by_role("dialog", name="分配数据权限")
        dialog.get_by_placeholder("请选择").click()
    
        option_item_locator = self.page.get_by_text(option_text)
        option_item_locator.click()
        return option_item_locator
   
    def edit_role(self, role_name: str,new_role_name: str):
        """编辑角色"""
        print(f"🔥开始编辑角色: {role_name} 为 {new_role_name}")
        self.click_edit_role(role_name)
        self.wait_for_load_state()
        # 填写编辑后的角色信息
        self.fill(self.EDIT_ROLE_NAME_INPUT, new_role_name)
        self.click_save_role()
        self.is_visible(self.OPERATE_MESSAGE)
        message = self.get_text(self.OPERATE_MESSAGE)
        print(f"✅编辑角色消息: {message}")
        #等待dialog从dom移除
        self.wait_for_locator(self.OPERATE_MESSAGE, state="detached")
        return message
    def toggle_role_status(self, role_name: str):
        """切换角色状态"""
        return self.toggle_status(role_name, '[role="switch"]')
    def assign_user(self, role_name: str, user_name: str):
        """分配用户到角色"""
        # 找到包含指定角色名的行，然后点击分配用户按钮
        self.search_role_by_name(role_name)
        # self.take_screenshot(path="debug.png")
        # self.page.pause()  # 打开 Playwright Inspector
        row = self.get_locator(self.TABLE_LIST).filter(has_text=role_name)
        more_button = row.locator("button").filter(has_text="更多")
        more_button.click()
        
        # 直接在页面中查找数据权限按钮
        # 由于是下拉菜单，使用text定位
        data_permission_button = self.page.get_by_text("分配用户")
        data_permission_button.click()
        #点击添加用户按钮
        add_user_button = self.page.get_by_text("添加用户")
        add_user_button.click()
        #输入用户名
        pass
  
    def delete_role(self, role_name: str):
        """删除角色"""
        print(f"❎开始删除角色: {role_name}")
        return self.delete(role_name, "button:has-text('删除')")
    def _locate_role_operation_button(self, role_name: str, button_text: str):
        """定位角色操作按钮"""
        # 搜索角色
        self.search_role_by_name(role_name)
        # 等待表格加载完成
        self.wait_for_load_state()
        # 找到包含指定角色名的行
        rows = self.get_locator(self.TABLE_LIST).filter(has_text=role_name)
        more_button = rows.locator("button").filter(has_text=f"{button_text}")
        more_button.click()
        self.wait_for_load_state()
        return more_button

    # def assign_menu_to_role(self, role_name: str, menu_names: List[str]):
    #     """分配菜单到角色"""
    #     # 搜索角色
    #     self._locate_role_operation_button(role_name, "修改")
    #     #菜单权限分配
    #     self.click(self.ASSIGN_PERMISSIONS_BUTTON)
    #     self.wait_for_load_state()
    #     # 选择所有菜单
    #     for menu_name in menu_names:
    #         menu_checkbox = self.page.get_by_text(menu_name)
    #         menu_checkbox.check()
        
    #     # 点击确认按钮
    #     self.click(self.SAVE_BUTTON)

    #     # 等待操作完成
    #     self.wait_for_locator(self.OPERATE_MESSAGE)
    #     message = self.get_text(self.OPERATE_MESSAGE)
    #     # 等待消息从dom中移除
    #     self.wait_for_locator(self.OPERATE_MESSAGE, state='detached')
    #     print(f"🔥操作消息: {message}", flush=True)
    #     self.logger.info(f"🔥分配菜单到角色: {role_name},🔥操作消息: {message}")
    #     return message
        
