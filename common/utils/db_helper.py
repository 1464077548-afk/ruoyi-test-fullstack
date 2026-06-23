import pymysql
import logging
import os
from typing import List, Dict, Any, Optional
from config.settings import settings

# PostgreSQL 驱动作为可选导入
try:
    import psycopg2
except ImportError:
    psycopg2 = None

logger = logging.getLogger(__name__)


class DBHelper:
    """数据库辅助类"""
    
    @staticmethod
    def _get_worker_id():
        """获取当前工作器ID（用于并行执行时区分不同工作器）"""
        return os.environ.get('PYTEST_XDIST_WORKER', 'gw0')
    
    # 清理配置 - 定义哪些表需要清理以及清理规则
    CLEANUP_CONFIG = {
        'sys_user': {
            'pattern': "user_name LIKE 'test_%' OR user_name LIKE 'batch_%' OR user_name LIKE 'new_%' OR user_name LIKE 'edit_%' OR user_name LIKE 'gw_%'",
            'description': '测试用户（以test_、batch_或gw_开头）'
        },
        'sys_role': {
            'pattern': "role_name LIKE '测试角色%' OR role_key LIKE 'test_%' OR role_name LIKE 'gw_%' OR role_key LIKE 'gw_%'",
            'description': '测试角色'
        },
        'sys_dept': {
            'pattern': "dept_name LIKE '测试部门%' OR dept_name LIKE 'new_测试部门%' OR dept_name LIKE '子部门_测试部门%' OR dept_name LIKE '测试子部门_%'",
            'description': '测试部门'
        },
        'sys_menu': {
            'pattern': "menu_name LIKE '测试菜单%'",
            'description': '测试菜单'
        },
        'sys_dict_type': {
            'pattern': "dict_name LIKE '测试字典%' OR dict_type LIKE 'test_%'",
            'description': '测试字典类型'
        },
        'sys_dict_data': {
            'pattern': "dict_label LIKE '测试标签%' OR dict_value LIKE 'test_%'",
            'description': '测试字典数据'
        },
        'sys_config': {
            'pattern': "config_name LIKE '测试配置%' OR config_key LIKE 'test_%'",
            'description': '测试配置'
        },
        'sys_job': {
            'pattern': "job_name LIKE '测试任务%' OR job_name LIKE 'test_job%'",
            'description': '测试定时任务'
        },
        'sys_job_log': {
            'pattern': "job_name LIKE '测试任务%'",
            'description': '测试任务日志'
        },
        'sys_oper_log': {
            'pattern': "oper_name LIKE 'test_%' OR oper_name LIKE 'batch_%'",
            'description': '测试操作日志'
        },
        'sys_login_info': {
            'pattern': "user_name LIKE 'test_%' OR user_name LIKE 'batch_%'",
            'description': '测试登录日志'
        }
    }
    
    def __init__(self, db_type='mysql', environment=None):
        self.db_type = db_type
        self.environment = environment
        self.connection = None
        self.in_transaction = False
    
    def connect(self):
        """连接数据库"""
        if self.db_type == 'mysql':
            self.connection = pymysql.connect(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USERNAME,
                password=settings.DB_PASSWORD,
                database=settings.DB_NAME,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        elif self.db_type == 'postgres':
            self.connection = psycopg2.connect(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USERNAME,
                password=settings.DB_PASSWORD,
                dbname=settings.DB_NAME
            )
        return self.connection
    
    def _ensure_connection(self):
        """确保数据库连接"""
        if not self.connection:
            self.connect()
    
    def execute_query(self, query, params=None) -> List[Dict]:
        """执行查询"""
        self._ensure_connection()
        
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
            if not self.in_transaction:
                self.connection.commit()
        return result
    
    def execute_update(self, query, params=None) -> int:
        """执行更新操作"""
        self._ensure_connection()
        
        with self.connection.cursor() as cursor:
            affected_rows = cursor.execute(query, params)
            if not self.in_transaction:
                self.connection.commit()
        return affected_rows
    
    def execute_batch(self, query, params_list) -> int:
        """批量执行更新操作"""
        self._ensure_connection()
        
        with self.connection.cursor() as cursor:
            affected_rows = 0
            for params in params_list:
                affected_rows += cursor.execute(query, params)
            if not self.in_transaction:
                self.connection.commit()
        return affected_rows
    
    def start_transaction(self):
        """开始事务"""
        self._ensure_connection()
        self.in_transaction = True
    
    def commit_transaction(self):
        """提交事务"""
        if self.in_transaction and self.connection:
            self.connection.commit()
            self.in_transaction = False
    
    def rollback_transaction(self):
        """回滚事务"""
        if self.in_transaction and self.connection:
            self.connection.rollback()
            self.in_transaction = False
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            try:
                if self.in_transaction:
                    self.rollback_transaction()
                self.connection.close()
            except Exception as e:
                logger.warning(f"关闭数据库连接时出错: {e}")
            finally:
                self.connection = None
    
    def table_exists(self, table_name: str) -> bool:
        """检查表是否存在"""
        self._ensure_connection()
        
        if self.db_type == 'mysql':
            query = "SHOW TABLES LIKE %s"
        else:
            query = "SELECT tablename FROM pg_tables WHERE tablename = %s"
        
        result = self.execute_query(query, (table_name,))
        return len(result) > 0
    
    def count_records(self, table_name: str, condition: str = None, params: tuple = None) -> int:
        """统计记录数"""
        self._ensure_connection()
        
        query = f"SELECT COUNT(*) as count FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        
        result = self.execute_query(query, params)
        return result[0]['count'] if result else 0
    
    def cleanup_test_data(self, tables: Optional[List[str]] = None, dry_run: bool = False, worker_id: Optional[str] = None) -> Dict[str, Any]:
        """
        清理测试数据（并行执行安全）
        
        Args:
            tables: 指定要清理的表列表，为None则清理所有配置的表
            dry_run: 是否为试运行（只统计不删除）
            worker_id: 工作器ID，只清理该工作器创建的数据；为None则清理所有测试数据
            
        Returns:
            清理结果统计
        """
        self._ensure_connection()
        
        # 获取当前工作器ID
        current_worker = worker_id if worker_id else self._get_worker_id()
        logger.info(f"当前工作器ID: {current_worker}")
        
        cleanup_results = {
            'total_tables': 0,
            'cleaned_tables': 0,
            'total_records': 0,
            'dry_run': dry_run,
            'details': [],
            'worker_id': current_worker
        }
        
        tables_to_clean = tables if tables else list(self.CLEANUP_CONFIG.keys())
        
        for table_name in tables_to_clean:
            if table_name not in self.CLEANUP_CONFIG:
                logger.debug(f"表 {table_name} 不在清理配置中，跳过")
                continue
            
            if not self.table_exists(table_name):
                logger.debug(f"表 {table_name} 不存在，跳过")
                continue
            
            config = self.CLEANUP_CONFIG[table_name]
            pattern = config['pattern']
            description = config['description']
            
            # 如果指定了工作器ID，只清理该工作器的数据
            if current_worker:
                worker_pattern = f"user_name LIKE '{current_worker}_%'" if table_name == 'sys_user' else \
                               f"(role_name LIKE '{current_worker}_%' OR role_key LIKE '{current_worker}_%')" if table_name == 'sys_role' else \
                               f"dept_name LIKE '{current_worker}_%'" if table_name == 'sys_dept' else None
                
                if worker_pattern:
                    pattern = worker_pattern
                    logger.debug(f"工作器 {current_worker} 的清理模式: {pattern}")
            
            try:
                # 统计记录数
                count = self.count_records(table_name, pattern)
                cleanup_results['total_tables'] += 1
                
                if count > 0:
                    cleanup_results['details'].append({
                        'table': table_name,
                        'description': description,
                        'count': count
                    })
                    cleanup_results['total_records'] += count
                    
                    if not dry_run:
                        # 执行删除
                        delete_query = f"DELETE FROM {table_name} WHERE {pattern}"
                        deleted = self.execute_update(delete_query)
                        logger.info(f"已从 {table_name} 删除 {deleted} 条测试数据")
                        cleanup_results['cleaned_tables'] += 1
                else:
                    logger.debug(f"{table_name} 没有需要清理的测试数据")
                    
            except Exception as e:
                logger.warning(f"清理表 {table_name} 时出错: {e}")
                cleanup_results['details'].append({
                    'table': table_name,
                    'description': description,
                    'error': str(e)
                })
        
        return cleanup_results
    
    def cleanup_by_ids(self, table_name: str, id_column: str, ids: List[int]) -> int:
        """
        根据ID列表清理数据
        
        Args:
            table_name: 表名
            id_column: ID列名
            ids: ID列表
            
        Returns:
            删除的记录数
        """
        if not ids:
            return 0
        
        self._ensure_connection()
        
        placeholders = ','.join(['%s'] * len(ids))
        query = f"DELETE FROM {table_name} WHERE {id_column} IN ({placeholders})"
        
        return self.execute_update(query, tuple(ids))
    
    def truncate_tables(self, tables: List[str], cascade: bool = False) -> Dict[str, int]:
        """
        清空表（慎用！）
        
        Args:
            tables: 表名列表
            cascade: 是否级联删除
            
        Returns:
            各表清空的记录数
        """
        results = {}
        
        for table_name in tables:
            if not self.table_exists(table_name):
                logger.warning(f"表 {table_name} 不存在")
                continue
            
            try:
                count = self.count_records(table_name)
                
                if self.db_type == 'mysql':
                    query = f"TRUNCATE TABLE {table_name}"
                else:
                    query = f"TRUNCATE TABLE {table_name}"
                    if cascade:
                        query += " CASCADE"
                
                self.execute_update(query)
                results[table_name] = count
                logger.warning(f"已清空表 {table_name}，删除 {count} 条记录")
                
            except Exception as e:
                logger.error(f"清空表 {table_name} 时出错: {e}")
                results[table_name] = -1
        
        return results
    
    def __enter__(self):
        """进入上下文管理器"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器"""
        self.close()


# 全局数据库辅助实例
db_helper = DBHelper()