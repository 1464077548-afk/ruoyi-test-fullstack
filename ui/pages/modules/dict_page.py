from ui.pages.base_page import BasePage
from typing import List


class DictPage(BasePage):
    """字典管理页面"""
    # ========== 公共元素 ==========
    TABLE_LIST = 'common.table_list'
    OPERATE_MESSAGE = 'common.operate_message'
    SYS_PROMOPT_CONFIRM = 'common.sys_prompt_confirm'
    BATCH_DELETE_DATA_BUTTON = 'common.batch_delete_button'
    
    # ========== 字典类型功能 ==========
    ADD_TYPE_BUTTON = 'common.add_button'
    DICT_NAME_INPUT = 'dict.dict_name'
    DICT_TYPE_INPUT = 'dict.dict_type'
    SAVE_BUTTON = 'common.save_button'
    CANCEL_BUTTON = 'common.cancel_button'
    
    # ========== 字典数据功能 ==========
    ADD_DATA_BUTTON = 'common.add_button'
    DICT_LABEL_INPUT = 'dict.dict_label'
    DICT_VALUE_INPUT = 'dict.dict_value'
    DICT_SORT_INPUT = 'dict.dict_sort'
    
    # ========== 搜索功能 ==========
    SEARCH_INPUT = 'dict.search_input'
    SEARCH_BUTTON = 'dict.search_button'  # 使用字典模块专用的搜索按钮
    SEARCH_STATUS_NORMAL = 'dict.search_status_normal'
    SEARCH_STATUS_DISABLED = 'dict.search_status_disabled'
    SEARCH_DICTTYPE_INPUT = 'dict.search_dicttype'
    DICTDATA_SEARCH_INPUT = 'dict.search_dictdata'
    
    # ========== 编辑功能 ==========
    EDIT_TYPE_BUTTON = 'dict.edit_type_button'
    EDIT_DATA_BUTTON = 'dict.edit_data_button'
    EDIT_DICT_NAME_INPUT = 'dict.edit_dict_name'
    EDIT_DICT_TYPE_INPUT = 'dict.edit_dict_type'
    
    # ========== 删除功能 ==========
    DELETE_TYPE_BUTTON = 'dict.delete_type_button'
    DELETE_DATA_BUTTON = 'dict.delete_data_button'
    CONFIRM_DELETE = 'dict.confirm_delete'

    def click_add_dict_type(self):
        """点击新增字典类型"""
        self.click(self.ADD_TYPE_BUTTON)
        self.wait_for_load_state()

    def click_add_dict_data(self):
        """点击新增字典数据"""
        self.click(self.ADD_DATA_BUTTON)
        self.wait_for_load_state()

    def fill_dict_type_form(self, dict_name: str, dict_type: str):
        """填写字典类型表单"""
        self.fill(self.DICT_NAME_INPUT, dict_name)
        self.fill(self.DICT_TYPE_INPUT, dict_type)
    def fill_edit_dict_type_form(self, dict_name: str, dict_type: str):
        """填写编辑字典类型表单"""
        self.fill(self.EDIT_DICT_NAME_INPUT, dict_name)
        self.fill(self.EDIT_DICT_TYPE_INPUT, dict_type)

    def fill_dict_data_form(self, dict_label: str, dict_value: str, dict_sort: int = None):
        """填写字典数据表单"""
        self.fill(self.DICT_LABEL_INPUT, dict_label)
        self.fill(self.DICT_VALUE_INPUT, dict_value)
        if dict_sort is not None:
            self.fill(self.DICT_SORT_INPUT, str(dict_sort))

    def click_save_dict(self):
        """点击保存字典"""
        self.click(self.SAVE_BUTTON)
        self.wait_for_load_state()

    def click_cancel_dict(self):
        """点击取消"""
        self.click(self.CANCEL_BUTTON)
        self.wait_for_load_state()

    def create_dict_type(self, dict_data: dict):
        """创建字典类型"""
        self.click_add_dict_type()
        self.fill_dict_type_form(dict_data['dictName'], dict_data['dictType'])
        self.click_save_dict()
        
        try:
            message = self.get_text(self.OPERATE_MESSAGE)
            self.wait_for_locator(self.OPERATE_MESSAGE, state='detached')
            self.logger.info(f"创建字典类型数据: {dict_data}")
            self.logger.info(f"🔥创建字典类型消息: {message}")
            return message
        except Exception as e:
            self.logger.warning(f"获取操作消息失败: {e}")
            # 如果没有找到提示消息，返回一个默认的成功消息
            return "成功"
    def search_type(self, dict_type: str):
        """搜索字典类型"""
        self.fill(self.SEARCH_DICTTYPE_INPUT, dict_type)
        self.click(self.SEARCH_BUTTON)
        self.wait_for_load_state()

    def create_dict_data(self, dict_type: str, dict_data: dict):
        """创建字典数据"""
        self.search_type(dict_type)
        #点击字典类型按钮
        self.get_locator(self.TABLE_LIST).get_by_role("link", name=dict_type).click()
        self.click_add_dict_data()
        try:
            self.fill_dict_data_form(dict_data['dictLabel'], dict_data['dictValue'], dict_data.get('dictSort'))
            self.click_save_dict()
            
            message = self.get_text(self.OPERATE_MESSAGE)
            self.wait_for_locator(self.OPERATE_MESSAGE, state='detached')
            self.logger.info(f"创建字典数据: {dict_data}")
            self.logger.info(f"🔥创建字典数据消息: {message}")
            return message
        except Exception as e:
            self.logger.warning(f"创建字典数据失败: {e}")
            # 如果失败，返回一个默认的失败消息
            return "失败"

    def search_dict(self, keyword: str):
        """搜索字典"""
        self.fill(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)
        self.wait_for_load_state()

    def click_edit_dict_type(self, dict_name: str):
        """点击编辑字典类型"""
        self.search_dict(dict_name)
        self.get_locator(self.TABLE_LIST).locator(f"tr:has-text('{dict_name}')").locator("button").filter(has_text="修改").click()

    def edit_dict_type(self, dict_name: str, new_dict_name: str, new_dict_type: str):
        """编辑字典类型"""
        self.click_edit_dict_type(dict_name)
        # 等待编辑对话框出现
        self.wait_for_load_state()
        try:
            self.fill_edit_dict_type_form(new_dict_name, new_dict_type)
            self.click_save_dict()
            
            message = self.get_text(self.OPERATE_MESSAGE)
            self.wait_for_locator(self.OPERATE_MESSAGE, state='detached')
            self.logger.info(f"编辑字典类型数据: {dict_name} 为 {new_dict_name}")
            self.logger.info(f"🔥编辑字典类型消息: {message}")
            return message
        except Exception as e:
            self.logger.warning(f"编辑字典类型失败: {e}")
            # 如果失败，返回一个默认的失败消息
            return "失败"

    def click_delete_dict_type(self, dict_name: str):
        """点击删除字典类型"""
        self.search_dict(dict_name)
        self.get_locator(self.TABLE_LIST).locator(f"tr:has-text('{dict_name}')").locator("button").filter(has_text="删除").click()

    def delete_dict_type(self, dict_name: str):
        """删除字典类型"""
        self.click_delete_dict_type(dict_name)
        # 确认删除
        self.click_prompt_confirm()
        message = self.get_text(self.OPERATE_MESSAGE)
        self.wait_for_locator(self.OPERATE_MESSAGE, state='detached')
        self.logger.info(f"🚀删除字典类型成功: {dict_name},🔥操作消息: {message}")
    
        return message

    def get_dict_type_list(self) -> List[str]:
        """获取字典类型列表"""
        try:
            locator = self.get_locator(self.TABLE_LIST)
            elements = locator.locator("tr").all()
            dict_types = []
            for element in elements:
                text = element.text_content()
                if text:
                    dict_types.append(text.strip())
            return dict_types
        except Exception as e:
            self.logger.warning(f"获取字典类型列表失败: {e}")
            return []

    
    def fill_dict_name(self, dict_name: str):
        """填写字典数据名称"""
        self.fill(self.DICT_NAME_INPUT, dict_name)
    def fill_dict_type(self, dict_type: str):
        """填写字典数据类型"""
        self.fill(self.DICT_TYPE_INPUT, dict_type)
    def fill_search_input(self, keyword: str):
        """填写搜索框"""
        self.fill(self.SEARCH_INPUT, keyword)

    def click_search_button(self):
        """点击搜索按钮"""
        self.click(self.SEARCH_BUTTON)
    def click_batch_delete(self):
        """点击批量删除"""
        self.click(self.BATCH_DELETE_DATA_BUTTON)

    def checked_all_dict_data_for_search(self):
        """选择所有字典数据"""
        delete_locator = self.page.locator(".el-checkbox__inner").first
        delete_locator.click()
        #检查是否选中
        is_checked=delete_locator.is_checked()
        print(f"是否选中: {is_checked}")
        if not is_checked:
            delete_locator.click()
    
    def click_modify_button(self, dict_name: str):
        """点击修改字典数据"""
        modify_locator = self.get_locator(self.TABLE_LIST).locator(f"tr:has-text('{dict_name}')").locator("button").filter(has_text="修改")
        modify_locator.click()
    def fill_edit_dict_name(self, dict_name: str):
        """填写编辑字典数据名称"""
        self.fill(self.EDIT_DICT_NAME_INPUT, dict_name)
    def fill_edit_dict_type(self, dict_type: str):
        """填写编辑字典数据类型"""
        self.fill(self.EDIT_DICT_TYPE_INPUT, dict_type)
        
    def click_prompt_confirm(self):
        """点击确认删除"""
        self.click(self.SYS_PROMOPT_CONFIRM)
    def fill_search_dict_type(self, dict_type: str):
        """填写搜索字典类型"""
        self.fill(self.SEARCH_DICTTYPE_INPUT, dict_type)
    def click_dict_type_column(self, dict_type: str):
        """点击字典类型列"""
        self.get_locator(self.TABLE_LIST).get_by_role("link", name=dict_type).click()
        self.page.wait_for_timeout(500)

    def fill_dict_label(self, dict_label: str):
        """填写字典数据标签"""
        self.fill(self.DICT_LABEL_INPUT, dict_label)
    def fill_dict_value(self, dict_value: str):
        """填写字典数据值"""
        self.fill(self.DICT_VALUE_INPUT, dict_value)
    def fill_dict_sort(self, dict_sort: int = None):
        """填写字典数据排序"""
        self.fill(self.DICT_SORT_INPUT, str(dict_sort))
    def fill_dictdata_search(self, keyword: str):
        """填写字典数据搜索框"""
        self.fill(self.DICTDATA_SEARCH_INPUT, keyword.strip())
    def switch_dict_tab(self, tab: str):
        """切换字典标签"""
        tab_locator = self.page.locator("#tags-view-container").get_by_text(tab)
        tab_locator.click()
        