"""L2: 监控模块接口测试"""
import pytest
from api.clients.monitor_client import MonitorClient


class TestMonitorModule:
    """监控模块测试类"""
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p0
    def test_system_monitoring_flow(self, monitor_client):
        """P0-系统监控完整流程"""
        # 1. 获取服务器信息
        server_response = monitor_client.get_server_info()
        assert server_response.get("code") == 200
        assert isinstance(server_response.get("data"), dict)
        
        # 2. 获取缓存信息（不清理缓存，避免影响并行测试）
        cache_response = monitor_client.get_cache_info()
        assert cache_response.get("code") == 200
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p1
    def test_monitoring_data_consistency(self, monitor_client):
        """P1-监控数据一致性测试"""
        # 1. 获取服务器信息，验证数据结构一致性
        for _ in range(2):
            server_response = monitor_client.get_server_info()
            assert server_response.get("code") == 200
            assert isinstance(server_response.get("data"), dict)
            assert "cpu" in server_response.get("data", {})
            assert "mem" in server_response.get("data", {})
    
   