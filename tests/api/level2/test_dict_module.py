"""L2: 字典模块接口测试"""
import pytest
from api.clients.dict_client import DictClient
from common.utils.data_factory import DataFactory


class TestDictModule:
    """字典模块测试类"""
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p0
    def test_dict_type_crud_flow(self, dict_client):
        """P0-字典类型完整CRUD流程"""
        # 1. 创建字典类型
        dict_type_data = {
            "dictName": "测试字典类型",
            "dictType": f"test_dict_{DataFactory.random_string(6).lower()}",
            "status": "0",
            "remark": "测试字典类型"
        }
        create_response = dict_client.create_dict_type(dict_type_data)
        assert create_response.get("code") == 200
        
        # 2. 查询字典类型列表获取dictId
        dict_type_list = dict_client.get_dict_type_list(dictType=dict_type_data.get("dictType"))
        assert dict_type_list.get("code") == 200
        assert len(dict_type_list.get("rows", [])) > 0
        dict_id = dict_type_list.get("rows")[0].get("dictId")
        assert dict_id
        
        try:
            # 3. 获取字典类型详情
            dict_type_detail = dict_client.get_dict_type(dict_id)
            assert dict_type_detail.get("code") == 200
            assert dict_type_detail.get("data", {}).get("dictType") == dict_type_data["dictType"]
            
            # 4. 更新字典类型
            updated_data = {
                "dictId": dict_id,
                "dictName": f"{dict_type_data['dictName']}_updated",
                "dictType": dict_type_data["dictType"],
                "status": "1",
                "remark": "更新后的测试字典类型"
            }
            update_response = dict_client.update_dict_type(updated_data)
            assert update_response.get("code") == 200
            
            # 5. 验证更新成功
            updated_detail = dict_client.get_dict_type(dict_id)
            assert updated_detail.get("code") == 200
            assert updated_detail.get("data", {}).get("dictName") == updated_data["dictName"]
            assert updated_detail.get("data", {}).get("status") == "1"
            
            # 6. 刷新字典缓存
            refresh_response = dict_client.refresh_dict_cache()
            assert refresh_response.get("code") == 200
            
        finally:
            # 7. 删除字典类型
            delete_response = dict_client.delete_dict_type(dict_id)
            assert delete_response.get("code") == 200
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p0
    def test_dict_data_crud_flow(self, dict_client):
        """P0-字典数据完整CRUD流程"""
        # 1. 先创建一个字典类型
        dict_type_data = {
            "dictName": "测试字典类型",
            "dictType": f"test_dict_{DataFactory.random_string(6).lower()}",
            "status": "0",
            "remark": "测试字典类型"
        }
        create_type_response = dict_client.create_dict_type(dict_type_data)
        assert create_type_response.get("code") == 200
        
        # 2. 查询字典类型列表获取dictId
        dict_type_list = dict_client.get_dict_type_list(dictType=dict_type_data.get("dictType"))
        assert dict_type_list.get("code") == 200
        assert len(dict_type_list.get("rows", [])) > 0
        dict_id = dict_type_list.get("rows")[0].get("dictId")
        assert dict_id
        
        dict_code = None
        
        try:
            # 3. 创建字典数据
            dict_data = {
                "dictType": dict_type_data["dictType"],
                "dictLabel": "测试字典值",
                "dictValue": "test_value",
                "status": "0",
                "remark": "测试字典数据"
            }
            create_data_response = dict_client.create_dict_data(dict_data)
            assert create_data_response.get("code") == 200
            
            # 4. 查询字典数据列表获取dictCode
            dict_data_list = dict_client.get_dict_data_list(dictType=dict_type_data["dictType"])
            assert dict_data_list.get("code") == 200
            assert len(dict_data_list.get("rows", [])) > 0
            dict_code = dict_data_list.get("rows")[0].get("dictCode")
            assert dict_code
            
            # 5. 获取字典数据详情
            dict_data_detail = dict_client.get_dict_data(dict_code)
            assert dict_data_detail.get("code") == 200
            assert dict_data_detail.get("data", {}).get("dictValue") == "test_value"
            
            # 6. 更新字典数据
            updated_data = {
                "dictCode": dict_code,
                "dictType": dict_type_data["dictType"],
                "dictLabel": "更新后的测试字典值",
                "dictValue": "test_value_updated",
                "status": "1",
                "remark": "更新后的测试字典数据"
            }
            update_data_response = dict_client.update_dict_data(updated_data)
            assert update_data_response.get("code") == 200
            
            # 7. 验证更新成功
            updated_detail = dict_client.get_dict_data(dict_code)
            assert updated_detail.get("code") == 200
            assert updated_detail.get("data", {}).get("dictLabel") == updated_data["dictLabel"]
            assert updated_detail.get("data", {}).get("dictValue") == "test_value_updated"
            
            # 8. 根据字典类型获取字典数据
            dict_by_type = dict_client.get_dicts_by_type(dict_type_data["dictType"])
            assert dict_by_type.get("code") == 200
            assert isinstance(dict_by_type.get("data"), list)
            
        finally:
            # 9. 删除字典数据
            if dict_code:
                delete_data_response = dict_client.delete_dict_data(dict_code)
                assert delete_data_response.get("code") == 200
            
            # 10. 删除字典类型
            delete_type_response = dict_client.delete_dict_type(dict_id)
            assert delete_type_response.get("code") == 200
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p1
    def test_dict_type_search_combinations(self, dict_client):
        """P1-字典类型搜索组合条件"""
        # 测试各种搜索组合
        search_cases = [
            {'dictName': '状态'},
            {'dictType': 'sys'},
            {'status': '0'},
            {'dictName': '状态', 'status': '0'}
        ]
        
        for params in search_cases:
            result = dict_client.get_dict_type_list(**params)
            assert result.get("code") == 200
            assert "total" in result
            assert "rows" in result