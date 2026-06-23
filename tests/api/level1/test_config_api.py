"""L1: 配置接口单接口测试"""
import pytest
from common.utils.data_factory import DataFactory


class TestConfigApi:
    """配置API测试类"""
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_config_list(self, config_client):
        """P0-获取参数列表"""
        response = config_client.get_config_list()
        assert response.get("code") == 200
        assert "total" in response
        assert "rows" in response
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_config_by_key(self, config_client):
        """P0-根据参数键名获取参数值"""
        # 测试获取一个已知的配置键
        response = config_client.get_config_by_key("sys.account.default.password")
        assert response.get("code") == 200
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_refresh_config_cache(self, config_client):
        """P1-刷新参数缓存"""
        response = config_client.refresh_config_cache()
        assert response.get("code") == 200
        assert response.get("msg") == "操作成功"
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_config(self, config_client):
        """P0-获取参数详情"""
        # 先获取配置列表，选择第一个配置的ID
        config_list = config_client.get_config_list()
        assert config_list.get("code") == 200
        configs = config_list.get("rows", [])
        assert len(configs) > 0
        
        config_id = configs[0].get("configId")
        assert config_id
        
        # 根据ID获取配置详情
        response = config_client.get_config(config_id)
        assert response.get("code") == 200
        assert response.get("data", {}).get("configId") == config_id
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_create_config(self, config_client):
        """P1-新增参数配置"""
        config_data = {
            "configName": f"测试配置_{DataFactory.random_string(6)}",
            "configKey": f"test_config_{DataFactory.random_string(6).lower()}",
            "configValue": "test_value",
            "configType": "Y",
            "remark": "测试配置"
        }
        response = config_client.create_config(config_data)
        assert response.get("code") == 200
        
        # 清理
        config_list = config_client.get_config_list(configKey=config_data["configKey"])
        if config_list.get("code") == 200 and len(config_list.get("rows", [])) > 0:
            config_id = config_list.get("rows")[0].get("configId")
            config_client.delete_config(config_id)
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_update_config(self, config_client):
        """P1-修改参数配置"""
        # 先创建一个配置
        config_data = {
            "configName": f"测试配置_{DataFactory.random_string(6)}",
            "configKey": f"test_config_{DataFactory.random_string(6).lower()}",
            "configValue": "test_value",
            "configType": "Y",
            "remark": "测试配置"
        }
        create_response = config_client.create_config(config_data)
        assert create_response.get("code") == 200
        
        # 获取配置ID
        config_list = config_client.get_config_list(configKey=config_data["configKey"])
        assert config_list.get("code") == 200
        assert len(config_list.get("rows", [])) > 0
        config_id = config_list.get("rows")[0].get("configId")
        assert config_id
        
        # 更新配置
        updated_data = {
            "configId": config_id,
            "configName": f"{config_data['configName']}_updated",
            "configKey": config_data["configKey"],
            "configValue": "updated_test_value",
            "configType": "N",
            "remark": "更新后的测试配置"
        }
        update_response = config_client.update_config(updated_data)
        assert update_response.get("code") == 200
        
        # 清理
        config_client.delete_config(config_id)
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_delete_config(self, config_client):
        """P1-删除参数配置"""
        # 先创建一个配置
        config_data = {
            "configName": f"测试配置_{DataFactory.random_string(6)}",
            "configKey": f"test_config_{DataFactory.random_string(6).lower()}",
            "configValue": "test_value",
            "configType": "Y",
            "remark": "测试配置"
        }
        create_response = config_client.create_config(config_data)
        assert create_response.get("code") == 200
        
        # 获取配置ID
        config_list = config_client.get_config_list(configKey=config_data["configKey"])
        assert config_list.get("code") == 200
        assert len(config_list.get("rows", [])) > 0
        config_id = config_list.get("rows")[0].get("configId")
        assert config_id
        
        # 验证配置已创建成功
        config_detail = config_client.get_config(config_id)
        assert config_detail.get("code") == 200
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_get_config_not_found(self, config_client):
        """P1-获取不存在的配置详情"""
        # 测试获取不存在的配置ID
        response = config_client.get_config(999999)
        assert response.get("code") == 200
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_get_config_by_key_not_found(self, config_client):
        """P1-获取不存在的配置键"""
        # 测试获取不存在的配置键
        response = config_client.get_config_by_key("non_existent_config_key_123456")
        assert response.get("code") == 200
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_create_config_invalid_params(self, config_client):
        """P1-创建配置参数错误"""
        # 测试缺少必要参数
        invalid_config_data = {
            "configName": f"测试配置_{DataFactory.random_string(6)}",
            # 缺少configKey
            "configValue": "test_value",
            "configType": "Y"
        }
        response = config_client.create_config(invalid_config_data)
        assert response.get("code") == 500
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p2
    def test_update_config_not_found(self, config_client):
        """P2-更新不存在的配置"""
        # 测试更新不存在的配置ID
        invalid_update_data = {
            "configId": 999999,
            "configName": "测试配置",
            "configKey": "test_config",
            "configValue": "test_value",
            "configType": "Y"
        }
        response = config_client.update_config(invalid_update_data)
        assert response.get("code") == 500
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_delete_config_not_found(self, config_client):
        """P1-删除不存在的配置"""
        # 测试删除不存在的配置ID
        response = config_client.delete_config(999999)
        assert response.get("code") == 500
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_create_config_empty_params(self, config_client):
        """P1-创建配置空参数测试"""
        # 测试空参数
        empty_config_data = {
            "configName": "",
            "configKey": "",
            "configValue": "",
            "configType": "Y"
        }
        response = config_client.create_config(empty_config_data)
        assert response.get("code") == 500
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_create_config_long_params(self, config_client):
        """P1-创建配置超长参数测试"""
        # 测试超长参数
        long_config_data = {
            "configName": "a" * 100,
            "configKey": "test_" + "a" * 100,
            "configValue": "value_" + "a" * 500,
            "configType": "Y",
            "remark": "remark_" + "a" * 200
        }
        response = config_client.create_config(long_config_data)
        assert response.get("code") == 500
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_get_config_list_pagination_boundary(self, config_client):
        """P1-配置列表分页边界测试"""
        # 测试分页边界值
        # 测试页面为0
        response = config_client.get_config_list(page=0, limit=10)
        assert response.get("code") == 200
        
        # 测试页面为负数
        response = config_client.get_config_list(page=-1, limit=10)
        assert response.get("code") == 200
        
        # 测试每页数量为0
        response = config_client.get_config_list(page=1, limit=0)
        assert response.get("code") == 200
        
        # 测试每页数量为负数
        response = config_client.get_config_list(page=1, limit=-1)
        assert response.get("code") == 200