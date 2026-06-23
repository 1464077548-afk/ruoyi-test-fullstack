from ui.pages.base_page import BasePage


class TableComponent(BasePage):
    """表格组件"""

    def __init__(self, page):
        """初始化"""
        super().__init__(page)
        self.table_selector = ".el-table"

    def is_visible(self, timeout: int = None) -> bool:
        """判断表格是否可见"""
        wait_timeout = timeout or self.timeout
        try:
            return self.page.locator(self.table_selector).is_visible(timeout=wait_timeout)
        except Exception:
            try:
                return self.page.locator(self.table_selector).first.is_visible(timeout=wait_timeout)
            except Exception:
                return False


    def get_row_count(self):
        """获取表格行数"""
        rows = self.page.locator(self.table_selector).locator('tbody tr')
        return rows.count()

    def get_headers(self):
        """获取表格表头"""
        try:          
            headers = []
            
            # 等待表格加载
            self.page.wait_for_selector(self.table_selector, timeout=10000)
            
            # 尝试多种方式定位表头
            header_elements = None
            attempts = [
                lambda: self.page.locator(self.table_selector).locator('thead th'),
                lambda: self.page.locator('.el-table thead tr th'),
                lambda: self.page.locator('table thead th'),
                lambda: self.page.locator('.el-table__header th')
            ]
            
            for attempt in attempts:
                try:
                    elements = attempt()
                    if elements.count() > 0:
                        header_elements = elements
                        break
                except Exception:
                    continue
            
            if header_elements is None:
                print("❌未能定位到表头元素")
                return []
                
            count = header_elements.count()
            print(f"找到 {count} 个表头元素")
                    
            for j in range(count):
                try:
                    header_text = header_elements.nth(j).text_content().strip()
                    print(f"表头 {j+1}: {header_text}")
                    if header_text:
                        headers.append(header_text)
                except Exception as e:
                    print(f"获取第 {j+1} 个表头失败: {e}")
            
            print(f"🔥获取到的表头为：{headers}")
            return headers
        except Exception as e:
            print(f"获取表头时出错：{e}")
            import traceback
            traceback.print_exc()
            return []

    def get_row(self, row_index):
        """获取指定行数据"""
        try:
            # 等待一段时间让表格完全渲染
            self.page.wait_for_timeout(2000)
            
            # 直接尝试获取表格行
            try:
                # 使用 .el-table__row 定位
                rows = self.page.locator('.el-table__row')
                row_count = rows.count()
                print(f"找到 {row_count} 行数据")
                
                if row_count > row_index:
                    row = rows.nth(row_index)
                    # 获取所有单元格
                    cells = row.locator('td')
                    cell_count = cells.count()
                    row_data = []
                    
                    for i in range(cell_count):
                        try:
                            cell = cells.nth(i)
                            cell_text = cell.text_content().strip()
                            row_data.append(cell_text)
                        except Exception as e:
                            print(f"获取单元格 {i} 数据失败: {e}")
                            row_data.append("")
                    
                    if row_data:
                        print(f"成功获取第 {row_index} 行数据: {row_data}")
                        return row_data
            except Exception as e:
                print(f"尝试使用 .el-table__row 定位失败: {e}")
            
            # 尝试使用 tbody tr 定位
            try:
                rows = self.page.locator('tbody tr')
                row_count = rows.count()
                print(f"找到 {row_count} 行数据")
                
                if row_count > row_index:
                    row = rows.nth(row_index)
                    # 获取所有单元格
                    cells = row.locator('td')
                    cell_count = cells.count()
                    row_data = []
                    
                    for i in range(cell_count):
                        try:
                            cell = cells.nth(i)
                            cell_text = cell.text_content().strip()
                            row_data.append(cell_text)
                        except Exception as e:
                            print(f"获取单元格 {i} 数据失败: {e}")
                            row_data.append("")
                    
                    if row_data:
                        print(f"成功获取第 {row_index} 行数据: {row_data}")
                        return row_data
            except Exception as e:
                print(f"尝试使用 tbody tr 定位失败: {e}")
            
            # 如果所有尝试都失败，返回空列表
            return []
        except Exception as e:
            print(f"获取行数据时出错：{e}")
            # 如果出现异常，返回空列表
            return []

    def get_current_page(self):
        """获取当前页码"""
        try:
            # 等待分页控件出现
            self.page.wait_for_selector('.el-pagination', timeout=30000)
            # 尝试使用指定的分页控件选择器
            current_page_locator = self.page.locator('.el-pagination__active-page')
            current_page_locator.wait_for(timeout=10000)
            current_page = current_page_locator.text_content()
            if current_page:
                return int(current_page)
            # 如果没有找到，返回默认值 1
            return 1
        except Exception as e:
            print(f"获取当前页码时出错：{e}")
            # 如果出现异常，返回默认值 1
            return 1

    def has_next_page(self):
        """是否有下一页"""
        try:
            # 等待分页控件出现
            self.page.wait_for_selector('.el-pagination', timeout=30000)
            # 尝试使用指定的分页控件选择器
            next_button = self.page.locator('.el-pagination__btn--next')
            next_button.wait_for(timeout=10000)
            return not next_button.is_disabled()
        except Exception as e:
            print(f"检查是否有下一页时出错：{e}")
            # 如果出现异常，返回 False
            return False

    def go_to_page(self, page_num):
        """跳转到指定页码"""
        try:
            # 等待分页控件出现
            self.page.wait_for_selector('.el-pagination', timeout=30000)
            # 尝试使用指定的分页控件选择器
            page_input = self.page.locator('.el-pagination__editor')
            page_input.wait_for(timeout=10000)
            page_input.fill(str(page_num))
            page_input.press('Enter')
            # 等待页面加载完成
            self.page.wait_for_load_state('networkidle', timeout=30000)
        except Exception as e:
            print(f"跳转到指定页码时出错：{e}")

    def change_page_size(self, size):
        """更改每页条数"""
        try:
            # 等待分页控件出现
            self.page.wait_for_selector('.el-pagination', timeout=30000)
            # 尝试使用指定的分页控件选择器
            size_selector = self.page.locator('.el-pagination__sizes .el-select')
            size_selector.wait_for(timeout=10000)
            size_selector.click()
            # 等待下拉选项出现
            option = self.page.locator(f'.el-select-dropdown__item:has-text("{size}")')
            option.wait_for(timeout=10000)
            option.click()
            # 等待页面加载完成
            self.page.wait_for_load_state('networkidle', timeout=30000)
        except Exception as e:
            print(f"更改每页条数时出错：{e}")

    def select_row(self, row_index):
        """选择指定行"""
        try:
            # 等待表格加载完成
            try:
                self.page.wait_for_load_state('networkidle', timeout=10000)
            except Exception as e:
                print(f"网络空闲等待超时: {e}")
            
            # 等待表格元素出现
            try:
                self.page.wait_for_selector('.el-table', timeout=10000)
            except Exception as e:
                print(f"表格元素未找到: {e}")
            
            # 等待一段时间让表格完全渲染
            self.page.wait_for_timeout(2000)
            
            # 尝试使用 .el-table__row 定位
            try:
                rows = self.page.locator('.el-table__row')
                row_count = rows.count()
                print(f"找到 {row_count} 行数据")
                
                if row_count > row_index:
                    row = rows.nth(row_index)
                    # 尝试点击复选框容器
                    try:
                        checkbox_container = row.locator('.el-table-column--selection .el-checkbox__input')
                        if checkbox_container.count() > 0:
                            checkbox_container.click()
                            print(f"成功选择第 {row_index} 行")
                            return
                    except Exception as e:
                        print(f"尝试点击复选框容器失败: {e}")
                    
                    # 尝试点击行本身
                    try:
                        row.click()
                        print(f"通过点击行本身选择第 {row_index} 行")
                        return
                    except Exception as e:
                        print(f"尝试点击行本身失败: {e}")
            except Exception as e:
                print(f"尝试使用 .el-table__row 定位失败: {e}")
            
            # 尝试使用 tbody tr 定位
            try:
                rows = self.page.locator('tbody tr')
                row_count = rows.count()
                print(f"找到 {row_count} 行数据")
                
                if row_count > row_index:
                    row = rows.nth(row_index)
                    # 尝试点击复选框容器
                    try:
                        checkbox_container = row.locator('.el-table-column--selection .el-checkbox__input')
                        if checkbox_container.count() > 0:
                            checkbox_container.click()
                            print(f"成功选择第 {row_index} 行")
                            return
                    except Exception as e:
                        print(f"尝试点击复选框容器失败: {e}")
                    
                    # 尝试点击行本身
                    try:
                        row.click()
                        print(f"通过点击行本身选择第 {row_index} 行")
                        return
                    except Exception as e:
                        print(f"尝试点击行本身失败: {e}")
            except Exception as e:
                print(f"尝试使用 tbody tr 定位失败: {e}")
        except Exception as e:
            print(f"选择行时出错：{e}")

    def is_row_selected(self, row_index):
        """检查行是否被选中"""
        try:
            # 等待表格加载完成
            try:
                self.page.wait_for_load_state('networkidle', timeout=10000)
            except Exception as e:
                print(f"网络空闲等待超时: {e}")
            
            # 等待表格元素出现
            try:
                self.page.wait_for_selector('.el-table', timeout=10000)
            except Exception as e:
                print(f"表格元素未找到: {e}")
            
            # 等待一段时间让表格完全渲染
            self.page.wait_for_timeout(1000)
            
            # 尝试使用 .el-table__row 定位
            try:
                rows = self.page.locator('.el-table__row')
                row_count = rows.count()
                print(f"找到 {row_count} 行数据")
                
                if row_count > row_index:
                    row = rows.nth(row_index)
                    # 尝试检查复选框容器的选中状态
                    try:
                        checkbox_container = row.locator('.el-table-column--selection .el-checkbox__input')
                        if checkbox_container.count() > 0:
                            # 尝试获取元素的 class 属性
                            checkbox_class = checkbox_container.evaluate("el => el.className")
                            is_checked = 'is-checked' in checkbox_class
                            print(f"第 {row_index} 行选中状态: {is_checked}")
                            return is_checked
                    except Exception as e:
                        print(f"尝试检查复选框容器失败: {e}")
            except Exception as e:
                print(f"尝试使用 .el-table__row 定位失败: {e}")
            
            # 尝试使用 tbody tr 定位
            try:
                rows = self.page.locator('tbody tr')
                row_count = rows.count()
                print(f"找到 {row_count} 行数据")
                
                if row_count > row_index:
                    row = rows.nth(row_index)
                    # 尝试检查复选框容器的选中状态
                    try:
                        checkbox_container = row.locator('.el-table-column--selection .el-checkbox__input')
                        if checkbox_container.count() > 0:
                            # 尝试获取元素的 class 属性
                            checkbox_class = checkbox_container.evaluate("el => el.className")
                            is_checked = 'is-checked' in checkbox_class
                            print(f"第 {row_index} 行选中状态: {is_checked}")
                            return is_checked
                    except Exception as e:
                        print(f"尝试检查复选框容器失败: {e}")
            except Exception as e:
                print(f"尝试使用 tbody tr 定位失败: {e}")
            
            # 尝试检查行本身是否有选中类
            try:
                rows = self.page.locator('.el-table__row')
                if rows.count() > row_index:
                    row = rows.nth(row_index)
                    # 尝试获取行元素的 class 属性
                    row_class = row.evaluate("el => el.className")
                    is_checked = 'current-row' in row_class or 'selected' in row_class
                    print(f"第 {row_index} 行选中状态 (行类): {is_checked}")
                    return is_checked
            except Exception as e:
                print(f"尝试检查行类失败: {e}")
            
            # 如果所有尝试都失败，返回 False
            return False
        except Exception as e:
            print(f"检查行是否被选中时出错：{e}")
            # 如果出现异常，返回 False
            return False

    def click_row_action(self, row_index, action_name):
        """点击行操作按钮"""
        try:  
            # 等待一段时间让表格完全渲染
            self.page.wait_for_timeout(2000)
            
            # 尝试使用 .el-table定位
            try:
                print(f"table_selector: {self.table_selector}")
                rows = self.table_selector.locator('.el-table__body tbody tr')
                row_count = rows.count()  
                print(f"找到 {row_count} 行数据")
                
                if row_count > row_index:
                    row = rows.nth(row_index)
                    print(f"第 {row_index} 行元素: {row}")
                    button = row.locator(f'button:has-text("{action_name}")')
                    button.click()
                    print(f"成功点击第 {row_index} 行的 {action_name} 按钮")
            except Exception as e:
                print(f"尝试使用 .el-table 定位失败: {e}")     
                # 尝试使用 tbody tr 定位
                try:
                    # 定位所有包含指定文本的按钮
                    buttons = self.page.locator(f'button:has-text("{action_name}"), a:has-text("{action_name}"), .el-dropdown-menu__item:has-text("{action_name}")')
                    button_count = buttons.count()
                    print(f"找到 {button_count} 个包含 {action_name} 的按钮")
                    
                    if button_count > 0:
                        for i in range(button_count):
                            try:
                                button = buttons.nth(i)
                                if not button.is_disabled():
                                    button.click()
                                    # 等待对话框出现，增加重试机制
                                    for attempt in range(3):
                                        try:
                                            self.page.wait_for_selector('.el-dialog', timeout=5000)
                                            print(f"成功点击 {action_name} 按钮，对话框已出现")
                                            return
                                        except Exception as e:
                                            print(f"尝试 {attempt+1} 等待对话框失败: {e}")
                                            self.page.wait_for_timeout(1000)
                                    return
                            except Exception as e:
                                print(f"尝试点击按钮 {i} 失败: {e}")
                                continue
                except Exception as e:
                    print(f"尝试使用通用定位器失败: {e}")
        except Exception as e:
            print(f"点击行操作按钮时出错：{e}")
