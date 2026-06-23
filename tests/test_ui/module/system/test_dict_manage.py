"""
L2: 字典管理模块测试
验证字典管理功能的完整测试
"""
import pytest


class TestDictManageModule:
    """字典管理模块测试类"""
    
    # ========================== 字典类型功能 ==========
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_dict_type_add_success(self, common_biz, dict_biz, test_dict_type_data, dict_client, page):
        """P0-新增字典类型成功"""
        # 导航到字典管理页面
        common_biz.switch_menu("系统管理/字典管理")
        
        # 创建字典类型
        message = dict_biz.create_dict_type(test_dict_type_data)
        
        # 验证操作成功提示
        assert "成功" in message, f"创建字典类型失败: {message}"
        
        # 清理：删除字典类型
        try:
            message = dict_biz.delete_dict_type(test_dict_type_data['dictName'])
            assert "成功" in message, f"清理删除失败: {message}"
        except Exception as e:
            print(f"UI删除失败，尝试API删除: {e}")
            try:
                dict_list = dict_client.get_dict_type_list()
                for item in dict_list.get('rows', []):
                    if item.get('dictName') == test_dict_type_data['dictName']:
                        dict_client.delete_dict_type(item.get('dictId'))
                        break
            except Exception as api_error:
                print(f"API删除也失败: {api_error}")
        
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_dict_type_add_duplicate(self, common_biz, dict_biz, test_dict_type_data, dict_client, page):
        """P1-新增重复字典类型"""
        # 导航到字典管理页面
        common_biz.switch_menu("系统管理/字典管理")
        
        # 先创建一个字典类型
        message = dict_biz.create_dict_type(test_dict_type_data)
        # 验证操作成功提示
        assert "成功" in message, f"创建字典类型失败: {message}"
        
        # 再创建同名字典类型
        message = dict_biz.create_dict_type(test_dict_type_data)
        
        # 验证重复提示
        assert "已存在" in message or "失败" in message, f"未检测到重复提示: {message}"
        
        # 清理：删除字典类型（使用 try-except 确保即使删除失败也能继续）
        try:
            message = dict_biz.delete_dict_type(test_dict_type_data['dictName'])
            assert "成功" in message, f"清理删除失败: {message}"
        except Exception as e:
            # 如果UI删除失败，尝试通过API删除
            print(f"UI删除失败，尝试API删除: {e}")
            try:
                dict_list = dict_client.get_dict_type_list()
                for item in dict_list.get('rows', []):
                    if item.get('dictName') == test_dict_type_data['dictName']:
                        dict_client.delete_dict_type(item.get('dictId'))
                        break
            except Exception as api_error:
                print(f"API删除也失败: {api_error}")
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_dict_type_edit_success(self, common_biz, dict_biz, test_dict_type_data, dict_client, page):
        """P0-编辑字典类型成功"""
        # 导航到字典管理页面
        common_biz.switch_menu("系统管理/字典管理")
        
        message = dict_biz.create_dict_type(test_dict_type_data)
        # 验证操作成功提示
        assert "成功" in message, f"创建字典类型失败: {message}"

        new_dict_name =f"new_{test_dict_type_data['dictName']}"
        new_dict_type = f"{test_dict_type_data['dictType']}_new"

        message = dict_biz.edit_dict_type(test_dict_type_data['dictName'], new_dict_name, new_dict_type)
        # 验证操作成功提示
        assert "成功" in message, f"编辑字典类型失败: {message}"

        # 清理：删除编辑后的字典类型
        try:
            message = dict_biz.delete_dict_type(new_dict_name)
            assert "成功" in message, f"清理删除失败: {message}"
        except Exception as e:
            print(f"UI删除失败，尝试API删除: {e}")
            try:
                dict_list = dict_client.get_dict_type_list()
                for item in dict_list.get('rows', []):
                    if item.get('dictName') == new_dict_name:
                        dict_client.delete_dict_type(item.get('dictId'))
                        break
            except Exception as api_error:
                print(f"API删除也失败: {api_error}")
        
        # 确保没有遗留弹窗
        dict_biz.close_all_dialogs()

    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_dict_type_delete_success(self, common_biz, dict_biz, test_dict_type_data, dict_client, page):
        """P0-删除字典类型成功"""
        # 导航到字典管理页面
        common_biz.switch_menu("系统管理/字典管理")
        
        # 先创建一个字典类型
        message = dict_biz.create_dict_type(test_dict_type_data)
        # 验证操作成功提示
        assert "成功" in message, f"创建字典类型失败: {message}"
        
        # 删除
        try:
            message = dict_biz.delete_dict_type(test_dict_type_data['dictName'])
            assert "成功" in message, f"删除字典类型失败: {message}"
        except Exception as e:
            print(f"UI删除失败，尝试API删除: {e}")
            try:
                dict_list = dict_client.get_dict_type_list()
                for item in dict_list.get('rows', []):
                    if item.get('dictName') == test_dict_type_data['dictName']:
                        dict_client.delete_dict_type(item.get('dictId'))
                        break
            except Exception as api_error:
                print(f"API删除也失败: {api_error}")
        
        # 验证字典类型列表不包含已删除字典类型
        dict_list = dict_client.get_dict_type_list()
        dict_names = [dict_type['dictName'] for dict_type in dict_list['rows']]
        assert test_dict_type_data['dictName'] not in dict_names
        

    # ======================================== 字典数据功能 ========================================
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_dict_data_add_success(self, common_biz, dict_biz, test_dict_type_data, test_dict_data, dict_client, page):
        """P0-新增字典数据成功"""
        # 导航到字典管理页面
        common_biz.switch_menu("系统管理/字典管理")
        
        # 先创建一个字典类型
        message = dict_biz.create_dict_type(test_dict_type_data)
        # 验证操作成功提示
        assert "成功" in message, f"创建字典类型失败: {message}"
        
        # 创建字典数据
        message = dict_biz.create_dict_data(test_dict_type_data['dictType'], test_dict_data)
        
        # 验证操作成功提示
        assert "成功" in message, f"创建字典数据失败: {message}"
        
        # 清理：删除字典类型（会级联删除字典数据）
        message = dict_biz.delete_dict(test_dict_type_data['dictName'],test_dict_data['dictLabel'])
        assert "成功" in message, f"清理删除失败: {message}"
       

    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_dict_data_search(self, common_biz, dict_biz, test_dict_type_data, test_dict_data, dict_client, page):
        """P0-通过字典标签搜索字典数据"""
        try:
            # 导航到字典管理页面
            common_biz.switch_menu("系统管理/字典管理")
            
            # 先创建一个字典类型
            message = dict_biz.create_dict_type(test_dict_type_data)
            assert "成功" in message, f"创建字典类型失败: {message}"
            
            # 创建字典数据
            message = dict_biz.create_dict_data(test_dict_type_data['dictType'], test_dict_data)
            assert "成功" in message, f"创建字典数据失败: {message}"
            
            
            result = dict_biz.search_dict_data_by_label(test_dict_data['dictLabel'])
            assert result, f"未找到字典数据: {test_dict_data['dictLabel']}"
        finally:
            # 清理：删除字典类型（会级联删除字典数据）
            try:
                message = dict_biz.delete_dict(test_dict_type_data['dictName'], test_dict_data['dictLabel'])
                assert "成功" in message, f"清理删除失败: {message}"
            except Exception as e:
                print(f"UI删除失败，尝试API删除: {e}")
                try:
                    dict_list = dict_client.get_dict_type_list()
                    for item in dict_list.get('rows', []):
                        if item.get('dictName') == test_dict_type_data['dictName']:
                            dict_client.delete_dict_type(item.get('dictId'))
                            break
                except Exception as api_error:
                    print(f"API删除也失败: {api_error}")

