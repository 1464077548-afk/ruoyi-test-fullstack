"""L1: 监控接口单接口测试"""
import pytest
from api.clients.monitor_client import MonitorClient


class TestMonitorApi:
    """监控API测试类"""
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_server_info(self, monitor_client):
        """P0-获取服务器信息"""
        response = monitor_client.get_server_info()
        assert response.get("code") == 200
        assert isinstance(response.get("data"), dict)
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_get_cache_info(self, monitor_client):
        """P1-获取缓存信息"""
        response = monitor_client.get_cache_info()
        assert response.get("code") == 200
        assert isinstance(response.get("data"), dict)