"""L1: 部门接口单接口测试"""
import pytest
from api.clients.dept_client import DeptClient
from common.utils.data_factory import DataFactory


class TestDeptApi:
    """部门API测试类"""
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_dept_list(self, dept_client):
        """P0-获取部门列表"""
        response = dept_client.get_dept_list()
        assert response.get("code") == 200
        assert isinstance(response.get("data"), list)
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_dept_list_exclude_child(self, dept_client):
        """P0-获取部门列表（排除节点）"""
        # 先获取部门列表，选择第一个部门的ID
        dept_list = dept_client.get_dept_list()
        assert dept_list.get("code") == 200
        depts = dept_list.get("data", [])
        assert len(depts) > 0
        
        dept_id = depts[0].get("deptId")
        assert dept_id
        
        # 获取排除该节点的部门列表
        response = dept_client.get_dept_list_exclude_child(dept_id)
        assert response.get("code") == 200
        assert isinstance(response.get("data"), list)
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_dept(self, dept_client):
        """P0-获取部门详情"""
        # 先获取部门列表，选择第一个部门的ID
        dept_list = dept_client.get_dept_list()
        assert dept_list.get("code") == 200
        depts = dept_list.get("data", [])
        assert len(depts) > 0
        
        dept_id = depts[0].get("deptId")
        assert dept_id
        
        # 根据ID获取部门详情
        response = dept_client.get_dept(dept_id)
        assert response.get("code") == 200
        assert response.get("data", {}).get("deptId") == dept_id