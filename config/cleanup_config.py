"""
测试数据清理配置
"""

# 测试数据标识前缀
TEST_DATA_PREFIXES = {
    'user': ['test_', 'new_', 'edit_'],
    'batch_user': 'batch_',
    'role': ['测试角色','test_'],
    'role_key': 'test_',
    'dept': ['测试部门', 'new_测试部门', '子部门_测试部门'],
    'menu': '测试菜单',
    'dict': ['测试字典','test_'],
    'config': '测试配置',
    'job': ['测试任务','test_job']
}

# 清理模式
CLEANUP_MODES = {
    'safe': '只清理按规则匹配的测试数据（推荐）',
    'aggressive': '清理所有测试数据（包括可能的边界情况）',
    'custom': '使用自定义规则清理'
}

# 是否在测试会话结束时自动清理
AUTO_CLEANUP_ON_SESSION_END = True

# 是否在每个测试函数结束后清理（可能影响性能）
AUTO_CLEANUP_ON_FUNCTION_END = False

# 需要在会话开始前清理的表
PRE_CLEANUP_TABLES = [
    'sys_user',
    'sys_role'
]

# 表清理顺序（考虑外键依赖）
CLEANUP_ORDER = [
    'sys_user_role',
    'sys_user_post',
    'sys_user',
    'sys_role_dept',
    'sys_role_menu',
    'sys_role',
    'sys_dict_data',
    'sys_dict_type',
    'sys_config',
    'sys_job_log',
    'sys_job',
    'sys_oper_log',
    'sys_login_info',
    'sys_menu',
    'sys_dept'
]
