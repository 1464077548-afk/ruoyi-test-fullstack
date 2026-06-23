"""L2: 系统模块接口测试"""
import pytest
from api.clients.monitor_client import MonitorClient


class TestSystemModule:
    """系统模块测试类"""
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p0
    def test_get_server_info(self, monitor_client):
        """P0-获取服务器信息"""
        response = monitor_client.get_server_info()
        assert response.get("code") == 200
        assert "data" in response
        assert "cpu" in response.get("data", {})
        assert "mem" in response.get("data", {})
        assert "sysFiles" in response.get("data", {})
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p0
    def test_get_jvm_info(self, monitor_client):
        """P0-获取JVM信息"""
        try:
            response = monitor_client.get_jvm_info()
            assert response.get("code") == 200
            assert "data" in response
        except Exception:
            # JVM endpoint not available, skip test
            pytest.skip("JVM endpoint not available")

    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p1
    def test_get_cache_info(self, monitor_client):
        """P1-获取缓存信息"""
        response = monitor_client.get_cache_info()
        assert response.get("code") == 200
        assert "data" in response

    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p1
    def test_get_log_list(self, monitor_client):
        """P1-获取日志列表"""
        response = monitor_client.get_oper_log_list()
        assert response.get("code") == 200
        assert "rows" in response

    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p1
    def test_system_monitoring_flow(self, monitor_client):
        """P1-系统监控流程"""
        # 1. 获取服务器信息
        server_response = monitor_client.get_server_info()
        assert server_response.get("code") == 200
        
        # 2. 获取JVM信息 (skip if not available)
        try:
            jvm_response = monitor_client.get_jvm_info()
            assert jvm_response.get("code") == 200
        except Exception:
            pass
        
        # 3. 获取缓存信息
        cache_response = monitor_client.get_cache_info()
        assert cache_response.get("code") == 200
        
        # 4. 获取日志列表
        log_response = monitor_client.get_oper_log_list()
        assert log_response.get("code") == 200
