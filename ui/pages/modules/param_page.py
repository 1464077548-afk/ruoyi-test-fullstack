from ui.pages.base_page import BasePage


class ParamPage(BasePage):
    """参数管理页面"""

    def add_param(self, param_name: str, param_key: str, param_value: str):
        """添加参数"""
        # 点击添加按钮
        self.click('param.add_button')
        
        # 填写参数信息
        self.fill('param.param_name', param_name)
        self.fill('param.param_key', param_key)
        self.fill('param.param_value', param_value)
        
        # 保存
        self.click('param.save_button')
        self.wait_for_load_state()

    def edit_param(self, param_name: str, param_key: str, param_value: str):
        """编辑参数"""
        # 点击编辑按钮
        self.click('param.edit_button')
        
        # 修改参数信息
        self.fill('param.param_name', param_name)
        self.fill('param.param_key', param_key)
        self.fill('param.param_value', param_value)
        
        # 保存
        self.click('param.save_button')
        self.wait_for_load_state()

    def delete_param(self):
        """删除参数"""
        # 点击删除按钮
        self.click('param.delete_button')
        
        # 确认删除
        self.click('param.confirm_delete')
        self.wait_for_load_state()

    def search_param(self, param_key: str):
        """搜索参数"""
        # 输入搜索关键词
        self.fill('param.search_input', param_key)
        
        # 点击搜索按钮
        self.click('param.search_button')
        self.wait_for_load_state()
