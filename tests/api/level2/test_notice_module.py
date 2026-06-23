"""L2: 通知模块接口测试"""
import pytest
from api.clients.notice_client import NoticeClient
from common.utils.data_factory import DataFactory


class TestNoticeModule:
    """通知模块测试类"""
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p0
    def test_notice_crud_flow(self, notice_client):
        """P0-通知完整CRUD流程"""
        # 1. 创建通知
        notice_data = {
            "noticeTitle": f"测试公告_{DataFactory.random_string(6)}",
            "noticeType": "1",  # 1: 通知, 2: 公告
            "noticeContent": "测试公告内容",
            "status": "0",  # 0: 正常, 1: 关闭
            "remark": "测试公告"
        }
        create_response = notice_client.create_notice(notice_data)
        assert create_response.get("code") == 200
        
        # 2. 查询公告列表获取noticeId
        notice_list = notice_client.get_notice_list(noticeTitle=notice_data.get("noticeTitle"))
        assert notice_list.get("code") == 200
        assert len(notice_list.get("rows", [])) > 0
        notice_id = notice_list.get("rows")[0].get("noticeId")
        assert notice_id
        
        try:
            # 3. 获取公告详情
            notice_detail = notice_client.get_notice(notice_id)
            assert notice_detail.get("code") == 200
            assert notice_detail.get("data", {}).get("noticeTitle") == notice_data["noticeTitle"]
            assert notice_detail.get("data", {}).get("noticeType") == "1"
            assert notice_detail.get("data", {}).get("status") == "0"
            
            # 4. 更新公告
            updated_data = {
                "noticeId": notice_id,
                "noticeTitle": f"{notice_data['noticeTitle']}_updated",
                "noticeType": "2",  # 改为公告
                "noticeContent": "更新后的测试公告内容",
                "status": "1",  # 改为关闭
                "remark": "更新后的测试公告"
            }
            update_response = notice_client.update_notice(updated_data)
            assert update_response.get("code") == 200
            
            # 5. 验证更新成功
            updated_detail = notice_client.get_notice(notice_id)
            assert updated_detail.get("code") == 200
            assert updated_detail.get("data", {}).get("noticeTitle") == updated_data["noticeTitle"]
            assert updated_detail.get("data", {}).get("noticeType") == "2"
            assert updated_detail.get("data", {}).get("status") == "1"
            assert updated_detail.get("data", {}).get("noticeContent") == "更新后的测试公告内容"
            
        finally:
            # 6. 删除公告
            delete_response = notice_client.delete_notice(notice_id)
            assert delete_response.get("code") == 200
            
            # 7. 验证公告已被删除
            notice_list_after_delete = notice_client.get_notice_list(noticeTitle=notice_data["noticeTitle"])
            assert notice_list_after_delete.get("code") == 200
            assert notice_list_after_delete.get("total") == 0
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p1
    def test_notice_search_combinations(self, notice_client):
        """P1-公告搜索组合条件"""
        # 测试各种搜索组合
        search_cases = [
            {'noticeTitle': '测试'},
            {'noticeType': '1'},
            {'status': '0'},
            {'noticeType': '1', 'status': '0'}
        ]
        
        for params in search_cases:
            result = notice_client.get_notice_list(**params)
            assert result.get("code") == 200
            assert "total" in result
            assert "rows" in result
    
    @pytest.mark.api
    @pytest.mark.l2
    @pytest.mark.p1
    def test_notice_type_switch(self, notice_client):
        """P1-公告类型切换测试"""
        # 1. 创建通知类型的公告
        notice_data = {
            "noticeTitle": f"测试通知_{DataFactory.random_string(6)}",
            "noticeType": "1",  # 通知
            "noticeContent": "测试通知内容",
            "status": "0",
            "remark": "测试通知"
        }
        create_response = notice_client.create_notice(notice_data)
        assert create_response.get("code") == 200
        
        # 2. 查询公告列表获取noticeId
        notice_list = notice_client.get_notice_list(noticeTitle=notice_data.get("noticeTitle"))
        assert notice_list.get("code") == 200
        assert len(notice_list.get("rows", [])) > 0
        notice_id = notice_list.get("rows")[0].get("noticeId")
        assert notice_id
        
        try:
            # 3. 验证初始类型为通知
            notice_detail = notice_client.get_notice(notice_id)
            assert notice_detail.get("code") == 200
            assert notice_detail.get("data", {}).get("noticeType") == "1"
            
            # 4. 切换为公告类型
            update_data = {
                "noticeId": notice_id,
                "noticeTitle": notice_data["noticeTitle"],
                "noticeType": "2",  # 公告
                "noticeContent": notice_data["noticeContent"],
                "status": notice_data["status"],
                "remark": notice_data["remark"]
            }
            update_response = notice_client.update_notice(update_data)
            assert update_response.get("code") == 200
            
            # 5. 验证类型已切换
            updated_detail = notice_client.get_notice(notice_id)
            assert updated_detail.get("code") == 200
            assert updated_detail.get("data", {}).get("noticeType") == "2"
            
        finally:
            # 6. 清理
            notice_client.delete_notice(notice_id)