# 测试数据清理工具使用说明

## 概述

本工具提供了一套完整的测试数据清理方案，包括：

- **自动清理**: 测试会话前后自动清理测试数据
- **命令行工具**: 独立的清理脚本，支持多种清理模式
- **灵活配置**: 可自定义清理规则和范围
- **安全操作**: 支持试运行模式，避免误删数据

## 快速开始

### 1. 查看测试数据

```bash
# 查看有多少测试数据（不会删除）
python tools/data_cleanup.py --dry-run
```

### 2. 清理测试数据

```bash
# 清理所有测试数据
python tools/data_cleanup.py

# 跳过确认，直接清理
python tools/data_cleanup.py -y
```

### 3. 清理指定表

```bash
# 只清理用户和角色表
python tools/data_cleanup.py --tables sys_user,sys_role
```

## 命令行工具

### 完整参数列表

```bash
python tools/data_cleanup.py --help
```

| 参数 | 说明 |
|------|------|
| `--dry-run` | 试运行，只统计不删除 |
| `--tables TABLES` | 指定要清理的表，逗号分隔 |
| `--list-tables` | 列出所有可清理的表 |
| `--verbose`, `-v` | 显示详细日志 |
| `--confirm`, `-y` | 跳过确认，直接执行 |

### 使用示例

#### 示例1：查看可清理的表

```bash
python tools/data_cleanup.py --list-tables
```

输出：
```
可清理的表:
----------------------------------------
  - sys_user: 测试用户（以test_或batch_开头）
  - sys_role: 测试角色
  - sys_dept: 测试部门
  ...
```

#### 示例2：试运行查看数据量

```bash
python tools/data_cleanup.py --dry-run
```

#### 示例3：清理并跳过确认

```bash
python tools/data_cleanup.py --confirm
```

## Fixture 使用

### 自动清理（推荐）

默认情况下，测试会话会自动清理测试数据：

```python
# 无需额外代码，自动执行
pytest tests/
```

### 手动清理 Fixtures

```python
def test_something(dry_run_cleanup, cleanup_tables):
    # 查看当前测试数据
    stats = dry_run_cleanup()
    print(f"当前有 {stats['total_records']} 条测试数据")
    
    # 执行测试...
    
    # 清理指定表
    cleanup_tables(['sys_user', 'sys_role'])
```

## 配置说明

配置文件：`config/cleanup_config.py`

### 主要配置项

```python
# 是否在测试会话结束时自动清理
AUTO_CLEANUP_ON_SESSION_END = True

# 是否在每个测试函数结束后清理（影响性能）
AUTO_CLEANUP_ON_FUNCTION_END = False

# 会话开始前需要清理的表
PRE_CLEANUP_TABLES = ['sys_user', 'sys_role']
```

### 清理规则配置

在 `common/utils/db_helper.py` 中的 `CLEANUP_CONFIG` 定义了各表的清理规则：

```python
CLEANUP_CONFIG = {
    'sys_user': {
        'pattern': "user_name LIKE 'test_%' OR user_name LIKE 'batch_%'",
        'description': '测试用户'
    },
    # ... 更多表
}
```

## 清理范围

默认会清理以下表的测试数据：

| 表名 | 说明 |
|------|------|
| `sys_user` | 测试用户 |
| `sys_role` | 测试角色 |
| `sys_dept` | 测试部门 |
| `sys_menu` | 测试菜单 |
| `sys_dict_type` | 测试字典类型 |
| `sys_dict_data` | 测试字典数据 |
| `sys_config` | 测试配置 |
| `sys_job` | 测试定时任务 |
| `sys_job_log` | 测试任务日志 |
| `sys_oper_log` | 测试操作日志 |
| `sys_login_info` | 测试登录日志 |

## 编程接口

### DBHelper 类

```python
from common.utils.db_helper import DBHelper

db = DBHelper()

# 清理测试数据
results = db.cleanup_test_data(dry_run=False)
print(f"清理了 {results['total_records']} 条记录")

# 清理指定表
results = db.cleanup_test_data(tables=['sys_user'])

# 试运行
results = db.cleanup_test_data(dry_run=True)

# 根据ID清理
deleted = db.cleanup_by_ids('sys_user', 'user_id', [1, 2, 3])

db.close()
```

## 注意事项

1. **测试数据命名规范**: 确保测试数据按规范命名（test_ 开头等），避免误删
2. **生产环境谨慎使用**: 在生产环境执行前务必使用 `--dry-run` 确认
3. **外键约束**: 工具已考虑表清理顺序，避免外键错误
4. **备份重要数据**: 清理前建议备份重要数据

## 常见问题

### Q: 如何添加新的表到清理范围？

A: 在 `common/utils/db_helper.py` 的 `CLEANUP_CONFIG` 中添加配置。

### Q: 如何只在特定测试中禁用自动清理？

A: 修改 `config/cleanup_config.py` 中的 `AUTO_CLEANUP_ON_SESSION_END = False`。

### Q: 清理操作安全吗？

A: 安全。工具只清理符合规则的测试数据，且支持试运行模式。

## 高级用法

### 自定义清理脚本

```python
from common.utils.db_helper import DBHelper

def custom_cleanup():
    db = DBHelper()
    
    # 自定义清理逻辑
    db.execute_update(
        "DELETE FROM sys_user WHERE create_time < %s",
        ('2024-01-01',)
    )
    
    db.close()
```
