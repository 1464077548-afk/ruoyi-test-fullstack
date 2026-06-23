"""L1: 字典接口单接口测试"""
import pytest
from api.clients.dict_client import DictClient
from common.utils.data_factory import DataFactory


class TestDictApi:
    """字典API测试类"""
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_dict_type_list(self, dict_client):
        """P0-获取字典类型列表"""
        response = dict_client.get_dict_type_list()
        assert response.get("code") == 200
        assert "total" in response
        assert "rows" in response
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_dict_type_options(self, dict_client):
        """P0-获取字典选择框列表"""
        response = dict_client.get_dict_type_options()
        assert response.get("code") == 200
        assert isinstance(response.get("data"), list)
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_dict_data_list(self, dict_client):
        """P0-获取字典数据列表"""
        response = dict_client.get_dict_data_list()
        assert response.get("code") == 200
        assert "total" in response
        assert "rows" in response
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_refresh_dict_cache(self, dict_client):
        """P1-刷新字典缓存"""
        response = dict_client.refresh_dict_cache()
        assert response.get("code") == 200
        assert response.get("msg") == "操作成功"
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_get_dicts_by_type(self, dict_client):
        """P1-根据字典类型获取字典数据"""
        response = dict_client.get_dicts_by_type("sys_normal_disable")
        assert response.get("code") == 200
        assert isinstance(response.get("data"), list)