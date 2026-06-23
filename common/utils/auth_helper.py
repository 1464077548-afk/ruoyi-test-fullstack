from config.settings import settings
from common.utils.db_helper import db_helper


class AuthHelper:
    """认证辅助工具类 - 处理账户锁定等问题"""
    
    @staticmethod
    def unlock_user(username: str = None):
        """
        解锁指定用户账户
        
        在若依框架中，用户登录失败次数记录在 sys_user 表的 login_failed_num 字段
        锁定状态通过该字段判断，通常超过5次会被锁定
        
        :param username: 用户名，默认为配置文件中的测试用户
        """
        target_username = username or settings.USERNAME
        
        try:
            with DBHelper() as db:
                # 重置登录失败次数为0（解锁账户）
                update_query = """
                    UPDATE sys_user 
                    SET login_failed_num = 0, lock_time = NULL 
                    WHERE user_name = %s
                """
                affected_rows = db.execute_update(update_query, (target_username,))
                
                if affected_rows > 0:
                    print(f"✅ 用户 {target_username} 已解锁")
                else:
                    print(f"ℹ️ 用户 {target_username} 不存在或无需解锁")
                    
        except Exception as e:
            print(f"⚠️ 解锁用户失败: {e}")
    
    @staticmethod
    def get_user_login_failed_count(username: str = None) -> int:
        """
        获取用户登录失败次数
        
        :param username: 用户名，默认为配置文件中的测试用户
        :return: 登录失败次数
        """
        target_username = username or settings.USERNAME
        
        try:
            with DBHelper() as db:
                query = "SELECT login_failed_num FROM sys_user WHERE user_name = %s"
                result = db.execute_query(query, (target_username,))
                
                if result:
                    return result[0].get('login_failed_num', 0)
                return -1
                
        except Exception as e:
            print(f"⚠️ 查询登录失败次数失败: {e}")
            return -1

    @staticmethod
    def ensure_user_unlocked(username: str = None):
        """
        确保用户账户未被锁定
        
        在测试前调用此方法，确保测试账户可用
        
        :param username: 用户名，默认为配置文件中的测试用户
        """
        target_username = username or settings.USERNAME
        failed_count = AuthHelper.get_user_login_failed_count(target_username)
        
        if failed_count >= 5:
            AuthHelper.unlock_user(target_username)
        elif failed_count == -1:
            print(f"⚠️ 无法验证用户 {target_username} 的锁定状态")


# 为了兼容性，导入 DBHelper
from common.utils.db_helper import DBHelper
