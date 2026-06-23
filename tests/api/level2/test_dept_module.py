"""L2: 部门模块接口测试"""
import pytest
from api.clients.dept_client import DeptClient
from common.utils.data_factory import DataFactory


class TestDeptModule:
    """部门模块测试类"""
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p0
    def test_dept_crud_flow(self, dept_client):
        """P0-部门完整CRUD流程"""
        # 1. 获取根部门列表
        dept_list = dept_client.get_dept_list()
        assert dept_list.get("code") == 200
        depts = dept_list.get("data", [])
        assert len(depts) > 0
        
        # 2. 选择第一个部门作为父部门
        parent_dept = depts[0]
        parent_dept_id = parent_dept.get("deptId")
        assert parent_dept_id
        
        # 3. 创建子部门
        dept_data = {
            "deptName": f"测试部门_{DataFactory.random_string(6)}",
            "parentId": parent_dept_id,
            "orderNum": 100,
            "status": "0",
            "leader": "测试负责人",
            "phone": "13800138000",
            "email": "test@example.com",
            "remark": "测试部门"
        }
        create_response = dept_client.create_dept(dept_data)
        assert create_response.get("code") == 200
        
        # 4. 获取部门列表，找到创建的部门
        dept_list_after_create = dept_client.get_dept_list()
        assert dept_list_after_create.get("code") == 200
        created_dept = None
        for dept in dept_list_after_create.get("data", []):
            if dept.get("deptName") == dept_data["deptName"]:
                created_dept = dept
                break
        assert created_dept is not None
        dept_id = created_dept.get("deptId")
        assert dept_id
        
        try:
            # 5. 获取部门详情
            dept_detail = dept_client.get_dept(dept_id)
            assert dept_detail.get("code") == 200
            assert dept_detail.get("data", {}).get("deptName") == dept_data["deptName"]
            
            # 6. 更新部门信息
            updated_data = {
                "deptId": dept_id,
                "deptName": f"{dept_data['deptName']}_updated",
                "parentId": parent_dept_id,
                "orderNum": 200,
                "status": "1",
                "leader": "更新后的测试负责人",
                "phone": "13900139000",
                "email": "updated_test@example.com",
                "remark": "更新后的测试部门"
            }
            update_response = dept_client.update_dept(updated_data)
            assert update_response.get("code") == 200
            
            # 7. 验证更新成功
            updated_detail = dept_client.get_dept(dept_id)
            assert updated_detail.get("code") == 200
            assert updated_detail.get("data", {}).get("deptName") == updated_data["deptName"]
            assert updated_detail.get("data", {}).get("status") == "1"
            
            # 8. 获取排除该部门的部门列表
            exclude_response = dept_client.get_dept_list_exclude_child(dept_id)
            assert exclude_response.get("code") == 200
            assert isinstance(exclude_response.get("data"), list)
            
        finally:
            # 9. 删除部门
            delete_response = dept_client.delete_dept(dept_id)
            assert delete_response.get("code") == 200
            
            # 10. 验证部门已被删除
            dept_list_after_delete = dept_client.get_dept_list()
            assert dept_list_after_delete.get("code") == 200
            found = False
            for dept in dept_list_after_delete.get("data", []):
                if dept.get("deptId") == dept_id:
                    found = True
                    break
            assert not found
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p1
    def test_dept_hierarchy(self, dept_client):
        """P1-部门层次结构测试"""
        # 1. 获取部门列表
        dept_list = dept_client.get_dept_list()
        assert dept_list.get("code") == 200
        depts = dept_list.get("data", [])
        assert len(depts) > 0
        
        # 2. 验证部门层次结构
        def check_dept_hierarchy(depts, parent_id=None):
            for dept in depts:
                assert "deptId" in dept
                assert "deptName" in dept
                assert "parentId" in dept
                if parent_id is not None:
                    assert dept.get("parentId") == parent_id
                if "children" in dept and dept["children"]:
                    check_dept_hierarchy(dept["children"], dept.get("deptId"))
        
        check_dept_hierarchy(depts)
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p1
    def test_dept_exclude_child(self, dept_client):
        """P1-部门排除子节点测试"""
        # 1. 获取部门列表
        dept_list = dept_client.get_dept_list()
        assert dept_list.get("code") == 200
        depts = dept_list.get("data", [])
        assert len(depts) > 0
        
        # 2. 选择一个有子部门的部门
        target_dept = None
        for dept in depts:
            if "children" in dept and dept["children"]:
                target_dept = dept
                break
        
        if target_dept:
            dept_id = target_dept.get("deptId")
            assert dept_id
            
            # 3. 获取排除该部门的部门列表
            exclude_response = dept_client.get_dept_list_exclude_child(dept_id)
            assert exclude_response.get("code") == 200
            assert isinstance(exclude_response.get("data"), list)
            
            # 4. 验证返回的列表中不包含该部门
            for dept in exclude_response.get("data", []):
                assert dept.get("deptId") != dept_id