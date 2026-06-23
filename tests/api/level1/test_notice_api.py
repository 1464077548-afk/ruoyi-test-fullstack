"""L1: 通知接口单接口测试"""
import pytest
from api.clients.notice_client import NoticeClient
from common.utils.data_factory import DataFactory


class TestNoticeApi:
    """通知API测试类"""
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_notice_list(self, notice_client):
        """P0-获取公告列表"""
        response = notice_client.get_notice_list()
        assert response.get("code") == 200
        assert "total" in response
        assert "rows" in response
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_notice(self, notice_client):
        """P0-获取公告详情"""
        # 先获取公告列表，选择第一个公告的ID
        notice_list = notice_client.get_notice_list()
        assert notice_list.get("code") == 200
        notices = notice_list.get("rows", [])
        
        if len(notices) > 0:
            notice_id = notices[0].get("noticeId")
            assert notice_id
            
            # 根据ID获取公告详情
            response = notice_client.get_notice(notice_id)
            assert response.get("code") == 200
            assert response.get("data", {}).get("noticeId") == notice_id
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_create_notice(self, notice_client):
        """P1-新增公告"""
        notice_data = {
            "noticeTitle": f"测试公告_{DataFactory.random_string(6)}",
            "noticeType": "1",  # 1: 通知, 2: 公告
            "noticeContent": "测试公告内容",
            "status": "0",  # 0: 正常, 1: 关闭
            "remark": "测试公告"
        }
        response = notice_client.create_notice(notice_data)
        assert response.get("code") == 200
        
        # 清理
        notice_list = notice_client.get_notice_list(noticeTitle=notice_data["noticeTitle"])
        if notice_list.get("code") == 200 and len(notice_list.get("rows", [])) > 0:
            notice_id = notice_list.get("rows")[0].get("noticeId")
            notice_client.delete_notice(notice_id)
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_update_notice(self, notice_client):
        """P1-修改公告"""
        # 先创建一个公告
        notice_data = {
            "noticeTitle": f"测试公告_{DataFactory.random_string(6)}",
            "noticeType": "1",
            "noticeContent": "测试公告内容",
            "status": "0",
            "remark": "测试公告"
        }
        create_response = notice_client.create_notice(notice_data)
        assert create_response.get("code") == 200
        
        # 获取公告ID
        notice_list = notice_client.get_notice_list(noticeTitle=notice_data["noticeTitle"])
        assert notice_list.get("code") == 200
        assert len(notice_list.get("rows", [])) > 0
        notice_id = notice_list.get("rows")[0].get("noticeId")
        assert notice_id
        
        # 更新公告
        updated_data = {
            "noticeId": notice_id,
            "noticeTitle": f"{notice_data['noticeTitle']}_updated",
            "noticeType": "2",
            "noticeContent": "更新后的测试公告内容",
            "status": "1",
            "remark": "更新后的测试公告"
        }
        update_response = notice_client.update_notice(updated_data)
        assert update_response.get("code") == 200
        
        # 清理
        notice_client.delete_notice(notice_id)
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_delete_notice(self, notice_client):
        """P1-删除公告"""
        # 先创建一个公告
        notice_data = {
            "noticeTitle": f"测试公告_{DataFactory.random_string(6)}",
            "noticeType": "1",
            "noticeContent": "测试公告内容",
            "status": "0",
            "remark": "测试公告"
        }
        create_response = notice_client.create_notice(notice_data)
        assert create_response.get("code") == 200
        
        # 获取公告ID
        notice_list = notice_client.get_notice_list(noticeTitle=notice_data["noticeTitle"])
        assert notice_list.get("code") == 200
        assert len(notice_list.get("rows", [])) > 0
        notice_id = notice_list.get("rows")[0].get("noticeId")
        assert notice_id
        
        # 删除公告
        delete_response = notice_client.delete_notice(notice_id)
        assert delete_response.get("code") == 200
        
        # 验证公告已被删除
        notice_list_after_delete = notice_client.get_notice_list(noticeTitle=notice_data["noticeTitle"])
        assert notice_list_after_delete.get("code") == 200
        assert notice_list_after_delete.get("total") == 0
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_get_notice_not_found(self, notice_client):
        """P1-获取不存在的公告详情"""
        # 测试获取不存在的公告ID
        response = notice_client.get_notice(999999)
        assert response.get("code") == 200
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_create_notice_invalid_params(self, notice_client):
        """P1-创建公告参数错误"""
        # 测试缺少必要参数
        invalid_notice_data = {
            # 缺少noticeTitle
            "noticeType": "1",
            "noticeContent": "测试公告内容",
            "status": "0"
        }
        response = notice_client.create_notice(invalid_notice_data)
        assert response.get("code") == 500
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_update_notice_not_found(self, notice_client):
        """P1-更新不存在的公告"""
        # 测试更新不存在的公告ID
        invalid_update_data = {
            "noticeId": 999999,
            "noticeTitle": "测试公告",
            "noticeType": "1",
            "noticeContent": "测试公告内容",
            "status": "0"
        }
        response = notice_client.update_notice(invalid_update_data)
        assert response.get("code") == 500
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_delete_notice_not_found(self, notice_client):
        """P1-删除不存在的公告"""
        # 测试删除不存在的公告ID
        response = notice_client.delete_notice(999999)
        assert response.get("code") == 500
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_create_notice_empty_params(self, notice_client):
        """P1-创建公告空参数测试"""
        # 测试空参数
        empty_notice_data = {
            "noticeTitle": "",
            "noticeType": "1",
            "noticeContent": "",
            "status": "0"
        }
        response = notice_client.create_notice(empty_notice_data)
        assert response.get("code") == 500
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_create_notice_long_params(self, notice_client):
        """P1-创建公告超长参数测试"""
        # 测试超长参数
        long_notice_data = {
            "noticeTitle": "a" * 100,
            "noticeType": "1",
            "noticeContent": "content_" + "a" * 1000,
            "status": "0",
            "remark": "remark_" + "a" * 500
        }
        response = notice_client.create_notice(long_notice_data)
        assert response.get("code") == 500
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_get_notice_list_pagination_boundary(self, notice_client):
        """P1-公告列表分页边界测试"""
        # 测试分页边界值
        # 测试页面为0
        response = notice_client.get_notice_list(page=0, limit=10)
        assert response.get("code") == 200
        
        # 测试页面为负数
        response = notice_client.get_notice_list(page=-1, limit=10)
        assert response.get("code") == 200
        
        # 测试每页数量为0
        response = notice_client.get_notice_list(page=1, limit=0)
        assert response.get("code") == 200
        
        # 测试每页数量为负数
        response = notice_client.get_notice_list(page=1, limit=-1)
        assert response.get("code") == 200