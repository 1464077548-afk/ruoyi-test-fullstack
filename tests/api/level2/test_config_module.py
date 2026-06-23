"""L2: 配置模块接口测试"""
import pytest
from api.clients.config_client import ConfigClient
from common.utils.data_factory import DataFactory


class TestConfigModule:
    """配置模块测试类"""
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p0
    def test_config_crud_flow(self, config_client, test_config_data):
        """P0-配置完整CRUD流程"""
        # 1. 创建配置
        create_response = config_client.create_config(test_config_data)
        assert create_response.get("code") == 200
        
        # 2. 查询配置列表获取configId
        config_list = config_client.get_config_list(configKey=test_config_data.get("configKey"))
        assert config_list.get("code") == 200
        assert len(config_list.get("rows", [])) > 0
        config_id = config_list.get("rows")[0].get("configId")
        assert config_id
        
        try:
            # 3. 获取配置详情
            config_detail = config_client.get_config(config_id)
            assert config_detail.get("code") == 200
            assert config_detail.get("data", {}).get("configKey") == test_config_data["configKey"]
            
            # 4. 根据配置键获取配置值
            config_by_key = config_client.get_config_by_key(test_config_data["configKey"])
            assert config_by_key.get("code") == 200
            assert config_by_key.get("msg") == test_config_data["configValue"]
            
            # 5. 更新配置
            updated_data = {
                "configId": config_id,
                "configName": f"{test_config_data['configName']}_updated",
                "configKey": test_config_data["configKey"],
                "configValue": "updated_test_value",
                "configType": "N",
                "remark": "更新后的测试配置"
            }
            update_response = config_client.update_config(updated_data)
            assert update_response.get("code") == 200
            
            # 6. 验证更新成功
            updated_detail = config_client.get_config(config_id)
            assert updated_detail.get("code") == 200
            assert updated_detail.get("data", {}).get("configName") == updated_data["configName"]
            assert updated_detail.get("data", {}).get("configValue") == "updated_test_value"
            
            # 7. 刷新配置缓存
            refresh_response = config_client.refresh_config_cache()
            assert refresh_response.get("code") == 200
            
            # 8. 再次根据配置键获取配置值，验证缓存已刷新
            config_by_key_after_refresh = config_client.get_config_by_key(test_config_data["configKey"])
            assert config_by_key_after_refresh.get("code") == 200
            assert config_by_key_after_refresh.get("msg") == "updated_test_value"
            
        finally:
            # 9. 验证配置已创建和更新成功
            # 注意：系统可能将测试配置标记为内置参数，不允许删除
            pass
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p1
    def test_config_search_combinations(self, config_client):
        """P1-配置搜索组合条件"""
        # 测试各种搜索组合
        search_cases = [
            {'configName': '系统'},
            {'configKey': 'sys'},
            {'configType': 'Y'},
            {'configName': '系统', 'configType': 'Y'}
        ]
        
        for params in search_cases:
            result = config_client.get_config_list(**params)
            assert result.get("code") == 200
            assert "total" in result
            assert "rows" in result
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p1
    def test_config_duplicate_key(self, config_client, test_config_data):
        """P1-配置键重复测试"""
        # 1. 创建一个配置
        create_response = config_client.create_config(test_config_data)
        assert create_response.get("code") == 200
        
        # 2. 尝试创建相同键的配置
        duplicate_response = config_client.create_config(test_config_data)
        assert duplicate_response.get("code") == 500
        assert "已存在" in duplicate_response.get("msg", "")
        
        # 3. 清理
        config_list = config_client.get_config_list(configKey=test_config_data["configKey"])
        if config_list.get("code") == 200 and len(config_list.get("rows", [])) > 0:
            config_id = config_list.get("rows")[0].get("configId")
            config_client.delete_config(config_id)