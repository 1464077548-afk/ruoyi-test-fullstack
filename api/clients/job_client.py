from typing import Dict, Any
from api.clients.base_client import BaseClient


class JobClient(BaseClient):
    """定时任务API客户端"""
    
    def get_job_list(self, page: int = 1, limit: int = 10, **kwargs) -> Dict[str, Any]:
        """获取定时任务列表"""
        endpoint = "/job/schedule/list"
        params = {
            "pageNum": page,
            "pageSize": limit,
            **kwargs
        }
        return self.get(endpoint, params)
    
    def get_job_by_id(self, job_id: int) -> Dict[str, Any]:
        """根据ID获取定时任务"""
        endpoint = f"/job/schedule/{job_id}"
        return self.get(endpoint)
    
    def create_job(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """创建定时任务"""
        endpoint = "/job/schedule"
        return self.post(endpoint, data)
    
    def update_job(self, job_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """更新定时任务"""
        endpoint = "/job/schedule"
        data["jobId"] = job_id
        return self.put(endpoint, data)
    
    def delete_job(self, job_ids: list) -> Dict[str, Any]:
        """删除定时任务"""
        endpoint = "/job/schedule"
        return self.delete(endpoint, data={"ids": job_ids})
    
    def change_job_status(self, job_id: int, status: str) -> Dict[str, Any]:
        """改变定时任务状态"""
        endpoint = f"/job/schedule/changeStatus/{job_id}/{status}"
        return self.put(endpoint)
    
    def run_job_now(self, job_id: int) -> Dict[str, Any]:
        """立即执行定时任务"""
        endpoint = f"/job/schedule/run/{job_id}"
        return self.put(endpoint)
