from ui.pages.modules.dict_page import DictPage
from ui.biz.common_biz import CommonBiz
from typing import List
import logging
class DictBiz():
    def __init__(self, page):
        self.page = page
        self.common = CommonBiz(page)
        self.dict = DictPage(page)
        self.logger = logging.getLogger(__name__)
    def create_dict_type(self, dict_type_data: dict) -> str:
        """创建字典类型"""
        # 然后创建字典类型
        self.dict.click_add_dict_type()
        self.dict.fill_dict_name(dict_type_data['dictName'])
        self.dict.fill_dict_type(dict_type_data['dictType'])
        self.dict.click_save_dict()
        message = self.common.get_operate_message()
        if "成功" not in message:
            self.close_all_dialogs()
        return message

    def edit_dict_type(self, dict_name: str, new_dict_name: str, new_dict_type: str) -> str:
        """编辑字典类型"""
        self.search_dict(dict_name)
        self.dict.click_modify_button(dict_name)
        try:
            self.dict.fill_edit_dict_name(new_dict_name)
            self.dict.fill_edit_dict_type(new_dict_type)
            self.dict.click_save_dict()          
            message = self.common.get_operate_message()
            if "成功" not in message:
                self.close_all_dialogs()
            return message
        except Exception as e:
            self.logger.warning(f"编辑字典类型失败: {e}")
            # 如果失败，返回一个默认的失败消息
            return "失败"

    def search_dict(self, keyword: str):
        """搜索字典"""
        self.dict.fill_search_input(keyword)
        try:
            self.dict.click_search_button()
            self.dict.wait_for_load_state()
        except Exception as e:
            self.logger.warning(f"点击搜索按钮失败，重试: {e}")
            # 等待后重试
            self.dict.wait_for_timeout(1000)
            self.dict.click_search_button()
            self.dict.wait_for_load_state()
    def delete_dict_type(self, dict_name: str):
        """删除字典类型"""
        self.dict.switch_dict_tab("字典管理")
        self.search_dict(dict_name)
        self.dict.click_delete_dict_type(dict_name)
        # 确认删除
        self.dict.click_prompt_confirm()
        
        try:
            message = self.common.get_operate_message()
            self.logger.info(f"🔥删除字典类型: {dict_name},🔥操作消息: {message}")
            if "成功" not in message:
                self.close_all_dialogs()
            return message
        except Exception as e:
            self.logger.warning(f"获取操作消息失败: {e}")
            # 如果没有找到提示消息，返回一个默认的成功消息
            self.page.keyboard.press("Escape")
            return "删除失败"

    def delete_dict_data(self, dict_label: str):
        """删除字典数据"""
        #全选字典数据
        self.dict.checked_all_dict_data_for_search()
        #点击批量删除
        self.dict.click_batch_delete()
        # 确认删除
        self.dict.click_prompt_confirm()
        try:
            message = self.common.get_operate_message()
            self.logger.info(f"🚀删除字典数据成功: {dict_label},🔥操作消息: {message}")
            return message
        except Exception as e:
            self.logger.warning(f"获取操作消息失败: {e}")
            self.page.keyboard.press("Escape")
            # 如果没有找到提示消息，返回一个默认的成功消息
            return "删除失败"

    def delete_dict(self, dict_name: str, dict_label: str) -> str:
        """删除字典类型"""
        self.dict.switch_dict_tab("字典管理")
        self.search_dict(dict_name)
        #删除字典类型
        message =self.delete_dict_type(dict_name)
        if "已分配" in message:
            # 如果字典类型已被分配，提示用户不能删除
            print(f"字典类型 {dict_name} 已分配，不能删除: {message},先删除字典数据后重试")
            #关闭弹窗
            self.page.keyboard.press("Escape")
            #切换到字典数据页
            self.dict.switch_dict_tab("字典数据")
            self.logger.info(f"🚀切换到字典数据页，删除字典数据: {dict_label}")
            message = self.delete_dict_data(dict_label)
            if "成功" in message:
                #删除字典类型
                self.logger.info(f"🚀删除字典数据成功，切换到字典管理页，删除字典类型: {dict_name}")
                self.dict.switch_dict_tab("字典管理")
                message =self.delete_dict_type(dict_name)
                self.logger.info(f"🚀删除字典类型成功: {dict_name},🔥操作消息: {message}")
                return message
            else:
                print(f"删除字典数据失败: {message}")
                self.logger.warning(f"删除字典数据失败: {message}")
                return message
        return message
                
      
    
    def create_dict_data(self, dict_type: str, dict_data: dict) -> str:
        """创建字典数据"""
        self.search_dict_type(dict_type)
        # 等待搜索结果
        self.dict.wait_for_load_state()
        self.dict.page.wait_for_timeout(1000)
        
        # 点击字典类型链接进入详情页
        success = False
        for attempt in range(3):
            try:
                self.dict.click_dict_type_column(dict_type)
                success = True
                break
            except Exception as e:
                try:
                    self.dict.get_locator(self.dict.TABLE_LIST).get_by_text(dict_type).click()
                    self.dict.page.wait_for_timeout(500)
                    success = True
                    break
                except Exception as e2:
                    print(f"第 {attempt+1} 次点击字典类型失败: {e2}")
                    self.dict.page.wait_for_timeout(500)
        
        if not success:
            return "失败"
        
        # 等待页面加载
        self.dict.wait_for_load_state()
        self.dict.page.wait_for_timeout(1500)
        
        # 点击新增字典数据
        self.dict.click_add_dict_data()
        
        # 等待弹窗加载
        self.dict.page.wait_for_timeout(1500)
        
        try:
            self.dict.fill_dict_label(dict_data['dictLabel'])
            self.dict.fill_dict_value(dict_data['dictValue'])
            if dict_data.get('dictSort') is not None:
                self.dict.fill_dict_sort(dict_data.get('dictSort'))
            
            # 确保字典类型已正确选择（可能需要在表单中设置）
            try:
                type_select = self.dict.page.locator("select").first
                if type_select.count() > 0:
                    type_select.select_option(dict_type)
            except Exception:
                pass
            
            self.dict.click_save_dict()
            
            message = self.common.get_operate_message()
            if "成功" not in message:
                self.close_all_dialogs()
            return message
        except Exception as e:
            self.logger.warning(f"创建字典数据失败: {e}")
            return "失败"
    def search_dict_type(self, dict_type: str):
        """搜索字典类型"""
        self.dict.fill_search_dict_type(dict_type)
        self.dict.click_search_button()
        self.dict.wait_for_load_state()

    def search_dict_data_by_label(self, dict_label: str):
        """通过字典标签搜索字典数据"""
        self.dict.fill_dictdata_search(dict_label)
        self.dict.click_search_button()
        self.dict.wait_for_load_state()
        # 等待数据加载完成
        self.dict.wait_for_timeout(500)
        # 获取搜索结果并检查是否包含目标标签
        dict_data_list = self.get_dict_data_list()
        print(f"搜索到的字典数据列表: {dict_data_list}")
        # 检查是否找到匹配的结果
        for data in dict_data_list:
            if dict_label.strip() in data:
                print(f"找到匹配的字典数据: {data}")
                return True
        print(f"未找到匹配的字典数据: {dict_label}")
        return False
    def get_dict_data_list(self) -> List[str]:
        """获取字典数据列表"""
        try:
            # 尝试多种方式获取字典数据
            locator = self.dict.get_locator(self.dict.TABLE_LIST)
            dict_data_list = []
            
            # 方式1: 尝试获取表格行中的所有文本
            try:
                rows = locator.locator("tr").all()
                for row in rows:
                    text = row.text_content()
                    if text:
                        dict_data_list.append(text.strip())
            except Exception as e:
                self.logger.warning(f"方式1获取字典数据列表失败: {e}")
            
            if not dict_data_list:
                # 方式2: 尝试获取所有包含特定文本的元素
                try:
                    elements = locator.locator("td").all()
                    for element in elements:
                        text = element.text_content()
                        if text:
                            dict_data_list.append(text.strip())
                except Exception as e:
                    self.logger.warning(f"方式2获取字典数据列表失败: {e}")
            
            return dict_data_list
        except Exception as e:
            self.logger.warning(f"获取字典数据列表失败: {e}")
            return []

    def close_all_dialogs(self):
        """关闭所有弹窗"""
        self.page.keyboard.press("Escape")
        print("关闭所有弹窗")